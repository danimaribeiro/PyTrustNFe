# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import os
import unicodedata
from pytrustnfe.xml import render_xml
from pytrustnfe.client import get_client


def _render_xml(method, **kwargs):
    path = os.path.join(os.path.dirname(__file__), 'templates')
    xml_send = render_xml(path, '%s.xml' % method, False, **kwargs)
    return xml_send


def _send(method, **kwargs):
    if kwargs['ambiente'] == 'producao':
        base_url = 'http://www.susesu.com.br/wsnfd/serviconfd.asmx?WSDL'
    else:
        base_url = 'http://pira.comunix.net:5002/gestaopublica/wsnfd/ServicoNfd.asmx?WSDL'  # noqa

    client = get_client(base_url)
    try:
        xml_send = kwargs["xml"]
        result = getattr(client.service, method)(__inject={'msg': xml_send})
    except Exception as e:
        return {
            'sent_xml': xml_send,
            'received_xml': e.fault.faultstring,
        }
    result = str(result)
    result = unicodedata.normalize('NFKD', result).encode('ascii', 'ignore')
    return {
        'sent_xml': xml_send,
        'received_xml': result,
    }


def xml_enviar_nota(**kwargs):
    return _render_xml('EnviarNota', **kwargs)


def enviar_nota(**kwargs):
    if "xml" not in kwargs:
        kwargs['xml'] = xml_enviar_nota(**kwargs)
    return _send('EnviarNota', **kwargs)


def xml_enviar_nota_retorna_url(**kwargs):
    return _render_xml('EnviarNotaRetornaurlNota', **kwargs)


def enviar_nota_retorna_url(**kwargs):
    if "xml" not in kwargs:
        kwargs['xml'] = xml_enviar_nota_retorna_url(**kwargs)
    return _send('EnviarNotaRetornaurlNota', **kwargs)
