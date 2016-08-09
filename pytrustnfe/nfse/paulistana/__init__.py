# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import os
import logging
import suds
from OpenSSL import crypto
from base64 import b64encode, b64decode
from uuid import uuid4
from pytrustnfe.xml import render_xml, valida_schema, sanitize_response
from pytrustnfe.client import get_authenticated_client
from pytrustnfe.certificado import extract_cert_and_key_from_pfx, save_cert_key
from pytrustnfe.nfe.assinatura import Assinatura



def sign_tag(certificado, **kwargs):
    pkcs12 = crypto.load_pkcs12(certificado.pfx, certificado.password)
    key = pkcs12.get_privatekey()
    for item in kwargs['nfse']['lista_rps']:
        signed = crypto.sign(key, item['assinatura'], 'SHA1')
        item['assinatura'] = b64encode(signed)


def _send(certificado, method, **kwargs):
    # A little hack to test
    path = os.path.join(os.path.dirname(__file__), 'templates')
    if method == 'TesteEnvioLoteRPS' or method == 'EnvioLoteRPS':
        sign_tag(certificado, **kwargs)

    if method == 'TesteEnvioLoteRPS':
        xml = render_xml(path, 'EnvioLoteRPS.xml', **kwargs)
    else:
        xml = render_xml(path, '%s.xml' % method, **kwargs)
    base_url = 'https://nfe.prefeitura.sp.gov.br/ws/lotenfe.asmx?wsdl'

    cert, key = extract_cert_and_key_from_pfx(
        certificado.pfx, certificado.password)
    cert_path, key_path = save_cert_key(cert, key)
    client = get_authenticated_client(base_url, cert_path, key_path)

    pfx_path = certificado.save_pfx()
    signer = Assinatura(pfx_path, certificado.password)
    xml_signed = signer.assina_xml(xml, '')

    try:
        response = getattr(client.service, method)(1, xml_signed)
    except suds.WebFault, e:
        return {
            'sent_xml': xml_signed,
            'received_xml': e.fault.faultstring,
            'object': None
        }

    response, obj = sanitize_response(response)
    return {
        'sent_xml': xml_signed,
        'received_xml': response,
        'object': obj
    }


def envio_rps(certificado, **kwargs):
    return _send(certificado, 'EnvioRPS', **kwargs)


def envio_lote_rps(certificado, **kwargs):
    return _send(certificado, 'EnvioLoteRPS', **kwargs)


def teste_envio_lote_rps(certificado, **kwargs):
    return _send(certificado, 'TesteEnvioLoteRPS', **kwargs)


def cancelamento_nfe(certificado, **kwargs):
    return _send(certificado, 'CancelamentoNFe', **kwargs)


def consulta_nfe(certificado, **kwargs):
    return _send('ConsultaNFe', **kwargs)


def consulta_nfe_recebidas(certificado, **kwargs):
    return _send('ConsultaNFeRecebidas', **kwargs)


def consulta_nfe_emitidas(data=None):
    return _send('ConsultaNFeEmitidas', data)


def consulta_lote(data=None):
    return _send('ConsultaLote', data)


def consulta_informacoes_lote(data=None):
    return _send('ConsultaInformacoesLote', data)


def consulta_cnpj(data=None):
    return _send('ConsultaCNPJ', data)
