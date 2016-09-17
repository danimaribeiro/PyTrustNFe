# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


import os
from lxml import etree
from .comunicacao import executar_consulta
from .assinatura import Assinatura
from pytrustnfe.xml import render_xml
from pytrustnfe.utils import CabecalhoSoap
from pytrustnfe.utils import gerar_chave, ChaveNFe
from pytrustnfe.Servidores import localizar_url


def _build_header(method, **kwargs):
    action = {
        'NfeAutorizacao': ('NfeAutorizacao', '3.10'),
        'NfeRetAutorizacao': ('NfeRetAutorizacao', '3.10'),
        'NfeConsultaCadastro': ('CadConsultaCadastro2', '2.00'),
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
        prod.insert(9, cEANTrib)
    return elemTree


def _send(certificado, method, sign, **kwargs):
    path = os.path.join(os.path.dirname(__file__), 'templates')

    xmlElem_send = render_xml(path, '%s.xml' % method, True, **kwargs)
    if sign:
        # Caso for autorização temos que adicionar algumas tags tipo
        # cEan, cEANTrib porque o governo sempre complica e não segue padrão
        if method == 'NfeAutorizacao':
            xmlElem_send = _add_required_node(xmlElem_send)

        signer = Assinatura(certificado.pfx, certificado.password)
        xml_send = signer.assina_xml(
            xmlElem_send, kwargs['NFes'][0]['infNFe']['Id'])
    else:
        xml_send = etree.tostring(xmlElem_send)

    url = localizar_url(method,  kwargs['estado'], kwargs['ambiente'])
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
