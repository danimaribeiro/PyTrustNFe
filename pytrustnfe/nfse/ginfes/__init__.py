# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import os
import suds
from lxml import etree
from pytrustnfe.xml import render_xml, sanitize_response
from pytrustnfe.client import get_authenticated_client
from pytrustnfe.certificado import extract_cert_and_key_from_pfx, save_cert_key
from pytrustnfe.nfe.assinatura import Assinatura


def _render(certificado, method, **kwargs):
    path = os.path.join(os.path.dirname(__file__), 'templates')
    xml_send = render_xml(path, '%s.xml' % method, True, **kwargs)

    reference = ''
    if method == 'RecepcionarLoteRpsV3':
        reference = 'rps%s' % kwargs['nfse']['lista_rps'][0]['numero']

    signer = Assinatura(certificado.pfx, certificado.password)
    xml_send = signer.assina_xml(xml_send, reference)
    return xml_send


def _send(certificado, method, **kwargs):
    base_url = ''
    if kwargs['ambiente'] == 'producao':
        base_url = 'https://producao.ginfes.com.br/ServiceGinfesImpl?wsdl'
    else:
        base_url = 'https://homologacao.ginfes.com.br/ServiceGinfesImpl?wsdl'

    cert, key = extract_cert_and_key_from_pfx(
        certificado.pfx, certificado.password)
    cert, key = save_cert_key(cert, key)
    client = get_authenticated_client(base_url, cert, key)
    try:
        xml_send = kwargs['xml']
        header = '<ns2:cabecalho xmlns:ns2="http://www.ginfes.com.br/cabecalho_v03.xsd" versao="3"><versaoDados>3</versaoDados></ns2:cabecalho>' #noqa
        response = getattr(client.service, method)(header, xml_send)
    except suds.WebFault as e:
        return {
            'sent_xml': xml_send,
            'received_xml': e.fault.faultstring,
            'object': None
        }

    response, obj = sanitize_response(response)
    return {
        'sent_xml': xml_send,
        'received_xml': response,
        'object': obj
    }


def xml_recepcionar_lote_rps(certificado, **kwargs):
    return _render(certificado, 'RecepcionarLoteRpsV3', **kwargs)


def recepcionar_lote_rps(certificado, **kwargs):
    if "xml" not in kwargs:
        kwargs['xml'] = xml_recepcionar_lote_rps(certificado, **kwargs)
    return _send(certificado, 'RecepcionarLoteRpsV3', **kwargs)


def xml_consultar_situacao_lote(certificado, **kwargs):
    return _render(certificado, 'ConsultarSituacaoLoteRpsV3', **kwargs)


def consultar_situacao_lote(certificado, **kwargs):
    if "xml" not in kwargs:
        kwargs['xml'] = xml_consultar_situacao_lote(certificado, **kwargs)
    return _send(certificado, 'ConsultarSituacaoLoteRpsV3', **kwargs)


def consultar_nfse_por_rps(certificado, **kwargs):
    return _send(certificado, 'ConsultarNfsePorRpsV3', **kwargs)


def xml_consultar_lote_rps(certificado, **kwargs):
    return _render(certificado, 'ConsultarLoteRpsV3', **kwargs)


def consultar_lote_rps(certificado, **kwargs):
    if "xml" not in kwargs:
        kwargs['xml'] = xml_consultar_lote_rps(certificado, **kwargs)
    return _send(certificado, 'ConsultarLoteRpsV3', **kwargs)


def consultar_nfse(certificado, **kwargs):
    return _send(certificado, 'ConsultarNfseV3', **kwargs)


def xml_cancelar_nfse(certificado, **kwargs):
    return _render(certificado, 'CancelarNfseV3', **kwargs)


def cancelar_nfse(certificado, **kwargs):
    if "xml" not in kwargs:
        kwargs['xml'] = xml_cancelar_nfse(certificado, **kwargs)
    return _send(certificado, 'CancelarNfseV3', **kwargs)
