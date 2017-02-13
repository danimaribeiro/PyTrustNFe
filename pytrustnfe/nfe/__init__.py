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
from pytrustnfe.xml.validate import valida_nfe
from pytrustnfe.exceptions import NFeValidationException


def _build_header(method, **kwargs):
    action = {
        'NfeAutorizacao': ('NfeAutorizacao', '3.10'),
        'NfeRetAutorizacao': ('NfeRetAutorizacao', '3.10'),
        'NfeConsultaCadastro': ('CadConsultaCadastro2', '2.00'),
        'NfeInutilizacao': ('NfeInutilizacao2', '3.10'),
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
        element = prod.find('ns:cEAN', namespaces=ns)
        if element is None:
            cEan = etree.Element('cEAN')
            prod.insert(1, cEan)
        element = prod.find('ns:cEANTrib', namespaces=ns)
        if element is None:
            cEANTrib = etree.Element('cEANTrib')
            vProd = prod.find('ns:vProd', namespaces=ns)
            prod.insert(prod.index(vProd) + 1, cEANTrib)
    return elemTree


def _add_qrCode(xml, **kwargs):
    xml = etree.fromstring(xml)
    inf_nfe = kwargs['NFes'][0]['infNFe']
    nfe = xml.find(".//{http://www.portalfiscal.inf.br/nfe}NFe")
    infnfesupl = etree.Element('infNFeSupl')
    #cria o nó qrCode no xml
    qrcode = etree.Element('qrCode')
    #busca a chave da nfe
    chave_nfe = inf_nfe['Id'][3:]
    #versao do qrCode
    versao = '100'
    #tipo de ambiente
    ambiente = kwargs['ambiente']
    #doc identificação do cliente
    dest_cpf = None
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
    #data e hora de emissao da nfce
    dh_emissao = inf_nfe['ide']['dhEmi'].encode('hex')
    #valor total da nfce
    valor_total = inf_nfe['total']['vNF']
    #valor total do icms
    icms_total = inf_nfe['total']['vICMS']
    #digest value
    dig_val = xml.find(
        ".//{http://www.w3.org/2000/09/xmldsig#}DigestValue")\
        .text.encode('hex')
    #identificação do csc
    cid_token = kwargs['NFes'][0]['infNFe']['codigo_seguranca']['cid_token']
    #codigo de seguranca do contribuinte
    csc = kwargs['NFes'][0]['infNFe']['codigo_seguranca']['csc']
    
    #hash qrCode
    if dest_cpf == None:
    
        c_hash_QR_code = 'chNFe={}&nVersao={}&tpAmb={}&dhEmi={}&vNF={}&vICMS={}&digVal={}&cIdToken={}{}'\
            .format(chave_nfe, versao, ambiente, dh_emissao,\
                 valor_total,icms_total, dig_val, cid_token, csc)

    else:
        c_hash_QR_code = 'chNFe={}&nVersao={}&tpAmb={}&cDest={}&dhEmi={}&vNF={}&vICMS={}&digVal={}&cIdToken={}{}'\
            .format(chave_nfe, versao, ambiente, dest_cpf, dh_emissao,\
                 valor_total,icms_total, dig_val, cid_token, csc)

    c_hash_QR_code = hashlib.sha1(c_hash_QR_code).hexdigest()
    #url qrCode
    if dest_cpf == None:
        QR_code_url = "?chNFe={}&nVersao={}&tpAmb={}&dhEmi={}&vNF={}&vICMS={}&digVal={}&cIdToken={}&cHashQRCode={}"\
            .format(chave_nfe, versao, ambiente, dh_emissao, valor_total,\
               icms_total, dig_val, cid_token, c_hash_QR_code)
    else:
        QR_code_url = "?chNFe={}&nVersao={}&tpAmb={}&cDest={}&dhEmi={}&vNF={}&vICMS={}&digVal={}&cIdToken={}&cHashQRCode={}".\
            format(chave_nfe, versao, ambiente, dest_cpf, dh_emissao,\
               valor_total, icms_total, dig_val, cid_token, c_hash_QR_code)
               
    qr_code_server = localizar_qrcode(kwargs['estado'], ambiente)
    qrcode_text = qr_code_server + QR_code_url
    qrcode.text = etree.CDATA(qrcode_text)
    infnfesupl.append(qrcode)
    nfe.insert(1, infnfesupl)
    return etree.tostring(xml)

def _send(certificado, method, sign, mod='55', **kwargs):
    path = os.path.join(os.path.dirname(__file__), 'templates')
    xmlElem_send = render_xml(path, '%s.xml' % method, True, **kwargs)
    
    if sign:
        # Caso for autorização temos que adicionar algumas tags tipo
        # cEan, cEANTrib porque o governo sempre complica e não segue padrão
        if method == 'NfeAutorizacao':
            xmlElem_send = _add_required_node(xmlElem_send)

        signer = Assinatura(certificado.pfx, certificado.password)
        if method == 'NfeInutilizacao':
            xml_send = signer.assina_xml(xmlElem_send, kwargs['obj']['id'])
        if method == 'NfeAutorizacao':
            xml_send = signer.assina_xml(
                xmlElem_send, kwargs['NFes'][0]['infNFe']['Id'])
            if 'validate' in kwargs:
                erros = valida_nfe(xml_send)
                if erros:
                    raise NFeValidationException('Erro ao validar NFe',
                                                 erros=erros,
                                                 sent_xml=xml_send)
        elif method == 'RecepcaoEventoCancelamento':
            xml_send = signer.assina_xml(
                xmlElem_send, kwargs['eventos'][0]['Id'])

        if method == 'RecepcaoEventoCarta':
            xml_send = signer.assina_xml(
                xmlElem_send, kwargs['Id'])

        if mod == '65':
            xml_send = _add_qrCode(xml_send, **kwargs)

    else:
        xml_send = etree.tostring(xmlElem_send)

    url = localizar_url(method,  kwargs['estado'], mod,
                        kwargs['ambiente'])
    cabecalho = _build_header(method, **kwargs)

    response, obj = executar_consulta(certificado, url, cabecalho, xml_send)
    return {
        'sent_xml': xml_send,
        'received_xml': response,
        'object': obj
    }


def autorizar_nfe(certificado, mod='55', **kwargs):  # Assinar
    _generate_nfe_id(**kwargs)
    return _send(certificado, 'NfeAutorizacao', True, mod, **kwargs)

def retorno_autorizar_nfe(certificado, mod='55', **kwargs):
    return _send(certificado, 'NfeRetAutorizacao', False, mod, **kwargs)


def recepcao_evento_cancelamento(certificado, mod='55', **kwargs):  # Assinar
    return _send(certificado, 'RecepcaoEventoCancelamento', True, mod, **kwargs)

def inutilizar_nfe(certificado, mod='55', **kwargs):  # Assinar
    return _send(certificado, 'NfeInutilizacao', mod, True, **kwargs)

def consultar_protocolo_nfe(certificado, mod='55', **kwargs):
    return _send(certificado, 'NfeConsultaProtocolo', True, mod, **kwargs)

def nfe_status_servico(certificado, mod='55', **kwargs):
    return _send(certificado, 'NfeStatusServico', False, mod, **kwargs)

def consulta_cadastro(certificado, mod='55', **kwargs):
    return _send(certificado, 'NfeConsultaCadastro', False, mod, **kwargs)

def recepcao_evento_carta_correcao(certificado, mod='55', **kwargs):  # Assinar
    return _send(certificado, 'RecepcaoEventoCarta', True, mod, **kwargs)

def recepcao_evento_manifesto(certificado, mod='55', **kwargs):  # Assinar
    return _send(certificado, 'RecepcaoEventoManifesto', True, mod, **kwargs)

def recepcao_evento_epec(certificado, mod='55', **kwargs):  # Assinar
    return _send(certificado, 'RecepcaoEventoEPEC', True, mod, **kwargs)

def consulta_nfe_destinada(certificado, mod='55', **kwargs):
    return _send(certificado, 'NfeConsultaDest', False, mod, **kwargs)

def download_nfe(certificado, mod='55', **kwargs):
    return _send(certificado, 'NfeDownloadNF', False, mod, **kwargs)
