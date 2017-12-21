# -*- encoding: utf-8 -*-
# © 2017 Fábio Luna, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import os
import suds
from lxml import etree
from pytrustnfe.xml import render_xml, sanitize_response
from pytrustnfe.certificado import extract_cert_and_key_from_pfx, save_cert_key
from pytrustnfe.nfse.assinatura import Assinatura
from pytrustnfe.client import get_client


def _render(certificado, method, **kwargs):
    path = os.path.join(os.path.dirname(__file__), 'templates')
    if method == "testeEnviar":
        xml_send = render_xml(path, 'enviar.xml', True, **kwargs)
    else:
        xml_send = render_xml(path, '%s.xml' % method, False, **kwargs)

    if type(xml_send) != str:
        xml_send = etree.tostring(xml_send)

    return xml_send


def _send(certificado, method, **kwargs):
    url = 'http://issdigital.campinas.sp.gov.br/WsNFe2/LoteRps.jws?wsdl'  # noqa

    path = os.path.join(os.path.dirname(__file__), 'templates')

    xml_send = _render(path, method, **kwargs)
    client = get_client(url)

    if certificado:
        cert, key = extract_cert_and_key_from_pfx(
            certificado.pfx, certificado.password)
        cert, key = save_cert_key(cert, key)
        signer = Assinatura(cert, key, certificado.password)
        xml_send = signer.assina_xml(xml_send, '')

    try:
        response = getattr(client.service, method)(xml_send)
        response, obj = sanitize_response(response.encode())
    except suds.WebFault as e:
        return {
            'sent_xml': xml_send,
            'received_xml': e.fault.faultstring,
            'object': None
        }

    return {
        'sent_xml': xml_send,
        'received_xml': response,
        'object': obj
    }


def enviar(certificado, **kwargs):
    return _send(certificado, 'enviar', **kwargs)


def teste_enviar(certificado, **kwargs):
    return _send(certificado, 'testeEnviar', **kwargs)


def cancelar(certificado, ** kwargs):
    return _send(certificado, 'cancelar', **kwargs)


def consulta_lote(**kwargs):
    return _send(False, 'consultarLote', **kwargs)


def consultar_lote_rps(certificado, **kwarg):
    return _send(certificado, 'consultarNFSeRps', **kwarg)
