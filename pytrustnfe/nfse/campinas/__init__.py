# -*- encoding: utf-8 -*-
# © 2017 Fábio Luna, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import os
import suds
from lxml import etree
from pytrustnfe.xml import render_xml, sanitize_response
from pytrustnfe.nfse.assinatura import Assinatura
from pytrustnfe import HttpClient


def _render_xml(certificado, method, **kwargs):
    path = os.path.join(os.path.dirname(__file__), 'templates')
    xml_send = render_xml(path, '%s.xml' % method, True, **kwargs)
    xml_send = etree.tostring(xml_send)

    return xml_send


def _validate(method, xml):
    path = os.path.join(os.path.dirname(__file__), 'templates')
    schema = os.path.join(path, '%s.xsd' % method)

    nfe = etree.fromstring(xml)
    esquema = etree.XMLSchema(etree.parse(schema))
    esquema.validate(nfe)
    erros = [x.message for x in esquema.error_log]
    return erros


def _send(certificado, method, **kwargs):
    url = 'http://issdigital.campinas.sp.gov.br/WsNFe2/LoteRps.jws?wsdl'  # noqa

    path = os.path.join(os.path.dirname(__file__), 'templates')

    if method == "testeEnviar":
        xml_send = render_xml(path, 'testeEnviar', **kwargs)
    else:
        xml_send = render_xml(path, '%s.xml' % method, False)
    client = HttpClient(url)

    pfx_path = certificado.save_pfx()
    signer = Assinatura(pfx_path, certificado.password)
    xml_signed = signer.assina_xml(xml_send, '')

    try:
        response = getattr(client.service, method)(xml_signed)
        response, obj = sanitize_response(response)
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
    if kwargs['ambiente'] == 'producao':
        return _send(certificado, 'enviar', **kwargs)
    else:
        return _send(certificado, 'testeEnviar', **kwargs)


def cancelar(certificado, ** kwargs):
    return _send(certificado, 'cancelar', **kwargs)


def consulta_lote(certificado, **kwargs):
    return _send(certificado, 'ConsultarLote', **kwargs)


def consultar_lote_rps(certificado, **kwarg):
    return _send(certificado, 'consultarNFSeRps', **kwarg)
