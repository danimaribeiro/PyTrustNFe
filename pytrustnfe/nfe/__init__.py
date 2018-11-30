# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


import os
import requests
from lxml import etree
from .assinatura import Assinatura
from pytrustnfe.xml import render_xml, sanitize_response
from pytrustnfe.utils import gerar_chave, ChaveNFe
from pytrustnfe.Servidores import localizar_url
from pytrustnfe.certificado import extract_cert_and_key_from_pfx, save_cert_key
from requests.packages.urllib3.exceptions import InsecureRequestWarning


# Zeep
from requests import Session
from zeep import Client
from zeep.transports import Transport


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


def _render(certificado, method, sign, **kwargs):
    path = os.path.join(os.path.dirname(__file__), 'templates')
    xmlElem_send = render_xml(path, '%s.xml' % method, True, **kwargs)

    modelo = xmlElem_send.find(".//{http://www.portalfiscal.inf.br/nfe}mod")
    modelo = modelo.text if modelo is not None else '55'

    if sign:
        signer = Assinatura(certificado.pfx, certificado.password)
        if method == 'NfeInutilizacao':
            xml_send = signer.assina_xml(xmlElem_send, kwargs['obj']['id'])
        if method == 'NfeAutorizacao':
            xml_send = signer.assina_xml(
                xmlElem_send, kwargs['NFes'][0]['infNFe']['Id'])
        elif method == 'RecepcaoEvento':
            xml_send = signer.assina_xml(
                xmlElem_send, kwargs['eventos'][0]['Id'])
        elif method == 'RecepcaoEventoManifesto':
            xml_send = signer.assina_xml(
                xmlElem_send, kwargs['manifesto']['identificador'])

    else:
        xml_send = etree.tostring(xmlElem_send, encoding=str)
    return xml_send


def _send(certificado, method, **kwargs):
    xml_send = kwargs["xml"]
    base_url = localizar_url(
        method,  kwargs['estado'], kwargs['modelo'], kwargs['ambiente'])

    cert, key = extract_cert_and_key_from_pfx(
        certificado.pfx, certificado.password)
    cert, key = save_cert_key(cert, key)

    session = Session()
    session.cert = (cert, key)
    session.verify = False
    transport = Transport(session=session)

    parser = etree.XMLParser(strip_cdata=False)
    xml = etree.fromstring(xml_send, parser=parser)

    client = Client(base_url, transport=transport)

    port = next(iter(client.wsdl.port_types))
    first_operation = [x for x in iter(
        client.wsdl.port_types[port].operations) if "zip" not in x.lower()][0]

    namespaceNFe = xml.find(".//{http://www.portalfiscal.inf.br/nfe}NFe")
    if namespaceNFe is not None:
        namespaceNFe.set('xmlns', 'http://www.portalfiscal.inf.br/nfe')

    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    with client.settings(raw_response=True):
        response = client.service[first_operation](xml)
        response, obj = sanitize_response(response.text)
        return {
            'sent_xml': xml_send,
            'received_xml': response,
            'object': obj.Body.getchildren()[0]
        }


def xml_autorizar_nfe(certificado, **kwargs):
    _generate_nfe_id(**kwargs)
    return _render(certificado, 'NfeAutorizacao', True, **kwargs)


def autorizar_nfe(certificado, **kwargs):  # Assinar
    if "xml" not in kwargs:
        kwargs['xml'] = xml_autorizar_nfe(certificado, **kwargs)
    return _send(certificado, 'NfeAutorizacao', **kwargs)


def xml_retorno_autorizar_nfe(certificado, **kwargs):
    return _render(certificado, 'NfeRetAutorizacao', False, **kwargs)


def retorno_autorizar_nfe(certificado, **kwargs):
    if "xml" not in kwargs:
        kwargs['xml'] = xml_retorno_autorizar_nfe(certificado, **kwargs)
    return _send(certificado, 'NfeRetAutorizacao', **kwargs)


def xml_recepcao_evento_cancelamento(certificado, **kwargs):  # Assinar
    return _render(certificado, 'RecepcaoEvento', True, **kwargs)


def recepcao_evento_cancelamento(certificado, **kwargs):  # Assinar
    if "xml" not in kwargs:
        kwargs['xml'] = xml_recepcao_evento_cancelamento(certificado, **kwargs)
    return _send(certificado, 'RecepcaoEvento', **kwargs)


def xml_inutilizar_nfe(certificado, **kwargs):
    return _render(certificado, 'NfeInutilizacao', True, **kwargs)


def inutilizar_nfe(certificado, **kwargs):
    if "xml" not in kwargs:
        kwargs['xml'] = xml_inutilizar_nfe(certificado, **kwargs)
    return _send(certificado, 'NfeInutilizacao', **kwargs)


def xml_consultar_protocolo_nfe(certificado, **kwargs):
    return _render(certificado, 'NfeConsultaProtocolo', False, **kwargs)


def consultar_protocolo_nfe(certificado, **kwargs):
    if "xml" not in kwargs:
        kwargs['xml'] = xml_consultar_protocolo_nfe(certificado, **kwargs)
    return _send(certificado, 'NfeConsultaProtocolo', **kwargs)


def xml_nfe_status_servico(certificado, **kwargs):
    return _render(certificado, 'NfeStatusServico', False, **kwargs)


def nfe_status_servico(certificado, **kwargs):
    if "xml" not in kwargs:
        kwargs['xml'] = xml_nfe_status_servico(certificado, **kwargs)
    return _send(certificado, 'NfeStatusServico', **kwargs)


def xml_consulta_cadastro(certificado, **kwargs):
    return _render(certificado, 'NfeConsultaCadastro', False, **kwargs)


def consulta_cadastro(certificado, **kwargs):
    if "xml" not in kwargs:
        kwargs['xml'] = xml_consulta_cadastro(certificado, **kwargs)
        kwargs['modelo'] = '55'
    return _send(certificado, 'NfeConsultaCadastro', **kwargs)


def xml_recepcao_evento_carta_correcao(certificado, **kwargs):  # Assinar
    return _render(certificado, 'RecepcaoEvento', True, **kwargs)


def recepcao_evento_carta_correcao(certificado, **kwargs):  # Assinar
    if "xml" not in kwargs:
        kwargs['xml'] = xml_recepcao_evento_carta_correcao(
            certificado, **kwargs)
    return _send(certificado, 'RecepcaoEvento', **kwargs)


def xml_recepcao_evento_manifesto(certificado, **kwargs):  # Assinar
    return _render(certificado, 'RecepcaoEvento', True, **kwargs)


def recepcao_evento_manifesto(certificado, **kwargs):  # Assinar
    if "xml" not in kwargs:
        kwargs['xml'] = xml_recepcao_evento_manifesto(certificado, **kwargs)
    return _send(certificado, 'RecepcaoEvento', **kwargs)


def xml_consulta_distribuicao_nfe(certificado, **kwargs):  # Assinar
    return _render(certificado, 'NFeDistribuicaoDFe', False, **kwargs)


def _send_v310(certificado, **kwargs):
    xml_send = kwargs["xml"]
    base_url = localizar_url(
        'NFeDistribuicaoDFe',  kwargs['estado'], kwargs['modelo'],
        kwargs['ambiente'])

    cert, key = extract_cert_and_key_from_pfx(
        certificado.pfx, certificado.password)
    cert, key = save_cert_key(cert, key)

    session = Session()
    session.cert = (cert, key)
    session.verify = False
    transport = Transport(session=session)

    xml = etree.fromstring(xml_send)
    xml_um = etree.fromstring('<nfeCabecMsg xmlns="http://www.portalfiscal.inf.br/nfe/wsdl/"><cUF>AN</cUF><versaoDados>1.00</versaoDados></nfeCabecMsg>')
    client = Client(base_url, transport=transport)

    port = next(iter(client.wsdl.port_types))
    first_operation = next(iter(client.wsdl.port_types[port].operations))
    with client.settings(raw_response=True):
        response = client.service[first_operation](nfeDadosMsg=xml, _soapheaders=[xml_um])
        response, obj = sanitize_response(response.text)
        return {
            'sent_xml': xml_send,
            'received_xml': response,
            'object': obj.Body.nfeDistDFeInteresseResponse.nfeDistDFeInteresseResult
        }


def consulta_distribuicao_nfe(certificado, **kwargs):
    if "xml" not in kwargs:
        kwargs['xml'] = xml_consulta_distribuicao_nfe(certificado, **kwargs)
    return _send_v310(certificado, **kwargs)


def xml_download_nfe(certificado, **kwargs):  # Assinar
    return _render(certificado, 'NFeDistribuicaoDFe', False, **kwargs)


def download_nfe(certificado, **kwargs):
    if "xml" not in kwargs:
        kwargs['xml'] = xml_download_nfe(certificado, **kwargs)
    return _send_v310(certificado, **kwargs)
