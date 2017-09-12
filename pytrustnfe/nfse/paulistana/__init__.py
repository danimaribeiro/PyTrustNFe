# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import os
import suds
from OpenSSL import crypto
from base64 import b64encode
from pytrustnfe.xml import render_xml, sanitize_response
from pytrustnfe.client import get_authenticated_client
from pytrustnfe.certificado import extract_cert_and_key_from_pfx, save_cert_key
from pytrustnfe.nfse.assinatura import Assinatura


def sign_tag(certificado, **kwargs):
    pkcs12 = crypto.load_pkcs12(certificado.pfx, certificado.password)
    key = pkcs12.get_privatekey()
    if 'nfse' in kwargs:
        for item in kwargs['nfse']['lista_rps']:
            signed = crypto.sign(key, item['assinatura'], 'SHA1')
            item['assinatura'] = b64encode(signed).decode()
    if 'cancelamento' in kwargs:
        signed = crypto.sign(key, kwargs['cancelamento']['assinatura'], 'SHA1')
        kwargs['cancelamento']['assinatura'] = b64encode(signed).decode()


def _send(certificado, method, **kwargs):
    # A little hack to test
    path = os.path.join(os.path.dirname(__file__), 'templates')
    if method == 'TesteEnvioLoteRPS' or method == 'EnvioLoteRPS' \
       or method == 'CancelamentoNFe':
        sign_tag(certificado, **kwargs)

    if method == 'TesteEnvioLoteRPS':
        xml_send = render_xml(path, 'EnvioLoteRPS.xml', False, **kwargs)
    else:
        xml_send = render_xml(path, '%s.xml' % method, False, **kwargs)
    base_url = 'https://nfe.prefeitura.sp.gov.br/ws/lotenfe.asmx?wsdl'

    cert, key = extract_cert_and_key_from_pfx(
        certificado.pfx, certificado.password)
    cert, key = save_cert_key(cert, key)
    client = get_authenticated_client(base_url, cert, key)

    signer = Assinatura(cert, key, certificado.password)
    xml_send = signer.assina_xml(xml_send, '')

    try:
        response = getattr(client.service, method)(1, xml_send)
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


def envio_rps(certificado, **kwargs):
    return _send(certificado, 'EnvioRPS', **kwargs)


# Testado pois usa o mesmo xml que o teste_envio_lote_rps
def envio_lote_rps(certificado, **kwargs):
    return _send(certificado, 'EnvioLoteRPS', **kwargs)


# Testado
def teste_envio_lote_rps(certificado, **kwargs):
    return _send(certificado, 'TesteEnvioLoteRPS', **kwargs)


def cancelamento_nfe(certificado, **kwargs):
    return _send(certificado, 'CancelamentoNFe', **kwargs)


# Testado
def consulta_nfe(certificado, **kwargs):
    return _send(certificado, 'ConsultaNFe', **kwargs)


# Testado
def consulta_nfe_recebidas(certificado, **kwargs):
    return _send(certificado, 'ConsultaNFeRecebidas', **kwargs)


# Testado
def consulta_nfe_emitidas(certificado, **kwargs):
    return _send(certificado, 'ConsultaNFeEmitidas', **kwargs)


# Testado
def consulta_lote(certificado, **kwargs):
    return _send(certificado, 'ConsultaLote', **kwargs)


# Testado
def consulta_informacoes_lote(certificado, **kwargs):
    return _send(certificado, 'ConsultaInformacoesLote', **kwargs)


# Testado
def consulta_cnpj(certificado, **kwargs):
    return _send(certificado, 'ConsultaCNPJ', **kwargs)
