# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import os
from lxml import etree
from pytrustnfe import HttpClient
from pytrustnfe.xml import render_xml, sanitize_response


def _render(certificado, method, **kwargs):
    path = os.path.join(os.path.dirname(__file__), 'templates')
    xml_send = render_xml(path, '%s.xml' % method, True, **kwargs)
    return etree.tostring(xml_send)


def _send(certificado, method, **kwargs):
    base_url = ''
    if kwargs['ambiente'] == 'producao':
        base_url = 'https://nfe.etransparencia.com.br/rj.petropolis/webservice/aws_nfe.aspx'  # noqa
    else:
        base_url = 'https://nfehomologacao.etransparencia.com.br/rj.petropolis/webservice/aws_nfe.aspx'  # noqa
    xml_send = kwargs["xml"]
    path = os.path.join(os.path.dirname(__file__), 'templates')
    soap = render_xml(path, 'SoapRequest.xml', False, soap_body=xml_send.decode())
    client = HttpClient(base_url)
    response = client.post_soap(soap, 'NFeaction/AWS_NFE.%s' % method)
    response, obj = sanitize_response(response.encode('utf-8'))
    return {
        'sent_xml': xml_send.decode(),
        'received_xml': response.decode(),
        'object': obj
    }


def xml_processa_rps(certificado, **kwargs):
    return _render(certificado, 'PROCESSARPS', **kwargs)


def processa_rps(certificado, **kwargs):
    if "xml" not in kwargs:
        kwargs['xml'] = xml_processa_rps(certificado, **kwargs)
    return _send(certificado, 'PROCESSARPS', **kwargs)


def xml_consulta_protocolo(certificado, **kwargs):
    return _render(certificado, 'CONSULTAPROTOCOLO', **kwargs)


def consulta_protocolo(certificado, **kwargs):
    if "xml" not in kwargs:
        kwargs['xml'] = xml_consulta_protocolo(certificado, **kwargs)
    return _send(certificado, 'CONSULTAPROTOCOLO', **kwargs)


def xml_consulta_notas_protocolo(certificado, **kwargs):
    return _render(certificado, 'CONSULTANOTASPROTOCOLO', **kwargs)


def consulta_notas_protocolo(certificado, **kwargs):
    if "xml" not in kwargs:
        kwargs['xml'] = xml_consulta_notas_protocolo(certificado, **kwargs)
    return _send(certificado, 'CONSULTANOTASPROTOCOLO', **kwargs)


def xml_cancelar_nfse(certificado, **kwargs):
    return _render(certificado, 'CANCELANOTAELETRONICA', **kwargs)


def cancelar_nfse(certificado, **kwargs):
    if "xml" not in kwargs:
        kwargs['xml'] = xml_cancelar_nfse(certificado, **kwargs)
    return _send(certificado, 'CANCELANOTAELETRONICA', **kwargs)
