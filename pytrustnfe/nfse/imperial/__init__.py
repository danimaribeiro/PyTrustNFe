# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import os
import requests
from lxml import etree
from requests import Session
from zeep import Client
from zeep.transports import Transport
from pytrustnfe.xml import render_xml, sanitize_response


def _render(certificado, method, **kwargs):
    path = os.path.join(os.path.dirname(__file__), 'templates')
    xml_send = render_xml(path, '%s.xml' % method, True, **kwargs)
    return etree.tostring(xml_send)


def _send(certificado, method, **kwargs):
    base_url = ''
    if kwargs['ambiente'] == 'producao':
        base_url = 'https://petropolis.sigiss.com.br/petropolis/ws/sigiss_ws.php'  # noqa
    else:
        raise Exception('Não existe ambiente de homologação!')

    xml_send = kwargs["xml"].decode('utf-8')
    headers = {
        'SOAPAction': "urn:sigiss_ws#%s" % method,
        'Content-Type': 'text/xml; charset="utf-8"'
    }

    r = requests.post(base_url, data=xml_send, headers=headers)
    response, obj = sanitize_response(r.text.strip())

    return {
        'sent_xml': xml_send,
        'received_xml': response,
        'object': obj.Body
    }


def xml_gerar_nota(certificado, **kwargs):
    return _render(certificado, 'GerarNota', **kwargs)


def gerar_nota(certificado, **kwargs):
    if "xml" not in kwargs:
        kwargs['xml'] = xml_gerar_nota(certificado, **kwargs)
    return _send(certificado, 'GerarNota', **kwargs)


def xml_cancelar_nota(certificado, **kwargs):
    return _render(certificado, 'CancelarNota', **kwargs)


def cancelar_nota(certificado, **kwargs):
    if "xml" not in kwargs:
        kwargs['xml'] = xml_cancelar_nota(certificado, **kwargs)
    return _send(certificado, 'CancelarNota', **kwargs)
