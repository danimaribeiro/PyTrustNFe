# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


import os
import hashlib
from lxml import etree
from .comunicacao import executar_consulta
from .assinatura import Assinatura
from pytrustnfe.xml import render_xml
from pytrustnfe.utils import CabecalhoSoap
from pytrustnfe.utils import gerar_chave, ChaveNFe
from pytrustnfe.Servidores import localizar_url, localizar_qrcode


def _build_header(method, **kwargs):
    action = {
        'NfeAutorizacao': ('NfeAutorizacao', '3.10'),
        'NfeRetAutorizacao': ('NfeRetAutorizacao', '3.10'),
        'NfeConsultaCadastro': ('CadConsultaCadastro2', '2.00'),
        'RecepcaoEventoCancelamento': ('RecepcaoEvento', '1.00'),
        'RecepcaoEventoCarta': ('RecepcaoEvento', '1.00'),
    }
    vals = {'estado': kwargs['estado'],
            'soap_action': action[method][0],
            'versao': action[method][1]}
    return CabecalhoSoap(**vals)


def _generate_nfe_id(**kwargs):
    for item in kwargs['NFes']:
        vals = {
            'cnpj': item['infNFe']['emit']['cnpj_cpf'],
            'estado': item['infNFe']['ide']['cUF'],
            'emissao': '%s%s' % (item['infNFe']['ide']['dhEmi'][2:4],
                                 item['infNFe']['ide']['dhEmi'][5:7]),
            'modelo': item['infNFe']['ide']['mod'],
            'serie': item['infNFe']['ide']['serie'],
            'numero': item['infNFe']['ide']['nNF'],
            'tipo': item['infNFe']['ide']['tpEmis'],
            'codigo': item['infNFe']['ide']['cNF'],
        }
        chave_nfe = ChaveNFe(**vals)
        chave_nfe = gerar_chave(chave_nfe, 'NFe')
        item['infNFe']['Id'] = chave_nfe
        item['infNFe']['ide']['cDV'] = chave_nfe[len(chave_nfe) - 1:]


def _add_required_node(elemTree):
    ns = elemTree.nsmap
    if None in ns:
        ns['ns'] = ns[None]
        ns.pop(None)

    prods = elemTree.findall('ns:NFe/ns:infNFe/ns:det/ns:prod', namespaces=ns)
    for prod in prods:
        cEan = etree.Element('cEAN')
        cEANTrib = etree.Element('cEANTrib')
        prod.insert(1, cEan)
        vProd = prod.find('ns:vProd', namespaces=ns)
        prod.insert(prod.index(vProd) + 1, cEANTrib)
    return elemTree


def _add_qrCode(xml, **kwargs):
    xml = etree.fromstring(xml)
    inf_nfe = kwargs['NFes'][0]['infNFe']
    nfe = xml.find(".//{http://www.portalfiscal.inf.br/nfe}NFe")
    infnfesupl = etree.Element('infNFeSupl')
    qrcode = etree.Element('qrCode')
    chave_nfe = inf_nfe['Id'][3:]
    dh_emissao = inf_nfe['ide']['dhEmi'].encode('hex')
    versao = '100'
    ambiente = kwargs['ambiente']
    valor_total = inf_nfe['total']['vNF']
    dest_cpf = 'Inexistente'
    dest = nfe.find(".//{http://www.portalfiscal.inf.br/nfe}dest")
    if dest:
        dest_parent = dest.getparent()
        dest_parent.remove(dest)
    if inf_nfe.get('dest', False):
        if inf_nfe['dest'].get('CPF', False):
            dest_cpf = inf_nfe['dest']['CPF']
            dest = etree.Element('dest')
            cpf = etree.Element('CPF')
            cpf.text = dest_cpf
            dest.append(cpf)
            dest_parent.append(dest)
    icms_total = inf_nfe['total']['vICMS']
    dig_val = xml.find(
        ".//{http://www.w3.org/2000/09/xmldsig#}DigestValue")\
        .text.encode('hex')
    cid_token = kwargs['NFes'][0]['infNFe']['codigo_seguranca']['cid_token']
    csc = kwargs['NFes'][0]['infNFe']['codigo_seguranca']['csc']

    c_hash_QR_code = "chNFe={0}&nVersao={1}&tpAmb={2}&cDest={3}&dhEmi={4}&vNF\
={5}&vICMS={6}&digVal={7}&cIdToken={8}{9}".\
        format(chave_nfe, versao, ambiente, dest_cpf, dh_emissao,
               valor_total, icms_total, dig_val, cid_token, csc)
    c_hash_QR_code = hashlib.sha1(c_hash_QR_code).hexdigest()

    QR_code_url = "?chNFe={0}&nVersao={1}&tpAmb={2}&{3}dhEmi={4}&vNF={5}&vICMS\
={6}&digVal={7}&cIdToken={8}&cHashQRCode={9}".\
        format(chave_nfe, versao, ambiente,
               'cDest={}&'.format(dest_cpf) if dest_cpf != 'Inexistente'
               else '', dh_emissao, valor_total, icms_total, dig_val,
               cid_token, c_hash_QR_code)
    qr_code_server = localizar_qrcode(kwargs['estado'], ambiente)
    qrcode_text = qr_code_server + QR_code_url
    qrcode.text = etree.CDATA(qrcode_text)
    infnfesupl.append(qrcode)
    nfe.insert(1, infnfesupl)
    return etree.tostring(xml)


def _send(certificado, method, sign, **kwargs):
    path = os.path.join(os.path.dirname(__file__), 'templates')
    xmlElem_send = render_xml(path, '%s.xml' % method, True, **kwargs)
    modelo = xmlElem_send.find(".//{http://www.portalfiscal.inf.br/nfe}mod")
    modelo = modelo.text if modelo is not None else '55'
    if modelo == '65':
        pagamento = etree.Element('pag')
        tipo_pagamento = etree.Element('tPag')
        valor = etree.Element('vPag')
        valor_pago = kwargs['NFes'][0]['infNFe']['total']['vNF']
        metodo_pagamento = kwargs['NFes'][0]['infNFe']['pagamento']
        tipo_pagamento.text, valor.text = metodo_pagamento, valor_pago
        pagamento.append(tipo_pagamento)
        pagamento.append(valor)
        transp = xmlElem_send.find(
                ".//{http://www.portalfiscal.inf.br/nfe}transp")
        transp.addnext(pagamento)

    if sign:
        # Caso for autorização temos que adicionar algumas tags tipo
        # cEan, cEANTrib porque o governo sempre complica e não segue padrão
        if method == 'NfeAutorizacao':
            xmlElem_send = _add_required_node(xmlElem_send)

        signer = Assinatura(certificado.pfx, certificado.password)
        if method == 'NfeAutorizacao':
            xml_send = signer.assina_xml(
                xmlElem_send, kwargs['NFes'][0]['infNFe']['Id'])
        elif method == 'RecepcaoEventoCancelamento':
            xml_send = signer.assina_xml(
                xmlElem_send, kwargs['eventos'][0]['Id'])

        if method == 'RecepcaoEventoCarta':
            xml_send = signer.assina_xml(
                xmlElem_send, kwargs['Id'])

        if modelo == '65':
            xml_send = _add_qrCode(xml_send, **kwargs)

    else:
        xml_send = etree.tostring(xmlElem_send)

    url = localizar_url(method,  kwargs['estado'], modelo,
                        kwargs['ambiente'])
    cabecalho = _build_header(method, **kwargs)

    response, obj = executar_consulta(certificado, url, cabecalho, xml_send)
    return {
        'sent_xml': xml_send,
        'received_xml': response,
        'object': obj
    }


def autorizar_nfe(certificado, **kwargs):  # Assinar
    _generate_nfe_id(**kwargs)
    return _send(certificado, 'NfeAutorizacao', True, **kwargs)


def retorno_autorizar_nfe(certificado, **kwargs):
    return _send(certificado, 'NfeRetAutorizacao', False, **kwargs)


def recepcao_evento_cancelamento(certificado, **kwargs):  # Assinar
    return _send(certificado, 'RecepcaoEventoCancelamento', True, **kwargs)


def inutilizar_nfe(certificado, **kwargs):  # Assinar
    return _send(certificado, 'NfeInutilizacao', True, **kwargs)


def consultar_protocolo_nfe(certificado, **kwargs):
    return _send(certificado, 'NfeConsultaProtocolo', True, **kwargs)


def nfe_status_servico(certificado, **kwargs):
    return _send(certificado, 'NfeStatusServico', False, **kwargs)


def consulta_cadastro(certificado, **kwargs):
    return _send(certificado, 'NfeConsultaCadastro', False, **kwargs)


def recepcao_evento_carta_correcao(certificado, **kwargs):  # Assinar
    return _send(certificado, 'RecepcaoEventoCarta', True, **kwargs)


def recepcao_evento_manifesto(certificado, **kwargs):  # Assinar
    return _send(certificado, 'RecepcaoEventoManifesto', True, **kwargs)


def recepcao_evento_epec(certificado, **kwargs):  # Assinar
    return _send(certificado, 'RecepcaoEventoEPEC', True, **kwargs)


def consulta_nfe_destinada(certificado, **kwargs):
    return _send(certificado, 'NfeConsultaDest', False, **kwargs)


def download_nfe(certificado, **kwargs):
    return _send(certificado, 'NfeDownloadNF', False, **kwargs)
