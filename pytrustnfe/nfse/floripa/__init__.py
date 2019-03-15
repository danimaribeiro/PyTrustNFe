# -*- coding: utf-8 -*-
# © 2017 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import os
import hashlib
import base64
import requests
from pytrustnfe.xml import render_xml, sanitize_response
from pytrustnfe.certificado import extract_cert_and_key_from_pfx, save_cert_key
from pytrustnfe.nfse.assinatura import Assinatura

URLS = {
    'producao': {
        'processar_nota': 'https://nfps-e.pmf.sc.gov.br/api/v1/processamento/notas/processa',
        'cancelar_nota': 'https://nfps-e.pmf.sc.gov.br/api/v1/cancelamento/notas/cancela'
    },
    'homologacao': {
        'processar_nota': 'https://nfps-e-hml.pmf.sc.gov.br/api/v1/processamento/notas/processa',
        'cancelar_nota': 'https://nfps-e-hml.pmf.sc.gov.br/api/v1/cancelamento/notas/cancela'
    }
}


def _render(certificado, method, **kwargs):
    path = os.path.join(os.path.dirname(__file__), 'templates')
    xml_send = render_xml(path, '%s.xml' % method, False, **kwargs)

    cert, key = extract_cert_and_key_from_pfx(
        certificado.pfx, certificado.password)
    cert, key = save_cert_key(cert, key)
    signer = Assinatura(cert, key, certificado.password)
    xml_send = signer.assina_xml(xml_send, '')
    return xml_send


def _get_oauth_token(**kwargs):
    if kwargs['ambiente'] == 'producao':
        url = 'https://nfps-e.pmf.sc.gov.br/api/v1/autenticacao/oauth/token'
    else:
        url = 'https://nfps-e-hml.pmf.sc.gov.br/api/v1/autenticacao/oauth/token'

    m = hashlib.md5()
    secret = "%s:%s" % (kwargs["client_id"], kwargs["secret_id"])
    auth = base64.b64encode(secret.encode('utf-8'))
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Basic %s" % auth.decode('utf-8').replace('\n', '')
    }
    m.update(kwargs["password"].encode('utf-8'))
    password = m.hexdigest().upper()

    dados = "grant_type=password&username=%s&password=%s&client_id=%s&client_secret=%s" % (
        kwargs["username"], password, kwargs["client_id"], kwargs["secret_id"])
    r = requests.post(url, data=dados, headers=headers)
    if r.status_code == 200:
        return r.json()
    else:
        return r.json()


def _send(certificado, method, **kwargs):
    url = URLS[kwargs['ambiente']][method]
    xml_send = kwargs['xml']

    token = _get_oauth_token(**kwargs)
    if "access_token" not in token:
        raise Exception("%s - %s: %s" % (token["status"], token["error"],
                                         token["message"]))
    kwargs.update({"numero": 1, 'access_token': token["access_token"]})

    headers = {"Accept": "application/xml;charset=UTF-8",
               "Content-Type": "application/xml",
               "Authorization": "Bearer %s" % kwargs['access_token']}
    r = requests.post(url, headers=headers, data=xml_send)

    response, obj = sanitize_response(r.text.strip())
    return {
        'sent_xml': xml_send,
        'received_xml': response.encode('utf-8'),
        'object': obj,
        'status_code': r.status_code,
    }


def xml_processar_nota(certificado, **kwargs):
    return _render(certificado, 'processar_nota', **kwargs)


def processar_nota(certificado, **kwargs):
    if "xml" not in kwargs:
        kwargs['xml'] = xml_processar_nota(certificado, **kwargs)
    return _send(certificado, 'processar_nota', **kwargs)


def xml_cancelar_nota(certificado, **kwargs):
    return _render(certificado, 'cancelar_nota', **kwargs)


def cancelar_nota(certificado, **kwargs):
    if "xml" not in kwargs:
        kwargs['xml'] = xml_cancelar_nota(certificado, **kwargs)
    return _send(certificado, 'cancelar_nota', **kwargs)


def consultar_nota(certificado, **kwargs):
    if kwargs['ambiente'] == 'producao':
        url = "https://nfps-e.pmf.sc.gov.br/api/v1/consultas/notas/numero/%s" % (kwargs["numero"])
    else:
        url = "https://nfps-e-hml.pmf.sc.gov.br/api/v1/consultas/notas/numero/%s" % (kwargs["numero"])

    headers = {"Accept": "application/json",
               "Authorization": "Bearer %s" % kwargs['access_token']}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return r.text
    else:
        return r.text
