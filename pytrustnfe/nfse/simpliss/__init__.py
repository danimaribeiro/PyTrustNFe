# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import os
import suds
from pytrustnfe.xml import render_xml, sanitize_response
from pytrustnfe.client import get_authenticated_client
from pytrustnfe.certificado import extract_cert_and_key_from_pfx, save_cert_key
from pytrustnfe.nfse.assinatura import Assinatura


def _send(certificado, method, **kwargs):
    # A little hack to test
    path = os.path.join(os.path.dirname(__file__), 'templates')

    xml_send = render_xml(path, '%s.xml' % method, False, **kwargs)

    base_url = 'Achar URL'

    cert, key = extract_cert_and_key_from_pfx(
        certificado.pfx, certificado.password)
    cert, key = save_cert_key(cert, key)
    client = get_authenticated_client(base_url, cert, key)

    pfx_path = certificado.save_pfx()
    signer = Assinatura(pfx_path, certificado.password)
    xml_send = signer.assina_xml(xml_send, '')

    try:
        response = getattr(client.service, method)(1, xml_send)
    except suds.WebFault, e:
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


def envio_lote_rps(certificado, **kwargs):
    return _send(certificado, 'EnvioLoteRps', **kwargs)


def consultar_situacao_lote(certificado, **kwargs):
    return _send(certificado, 'ConsultarSituacaoLote', **kwargs)


def consultar_nfse_por_rps(certificado, **kwargs):
    return _send(certificado, 'ConsultarNFSePorRps', **kwargs)


def consultar_lote(certificado, **kwargs):
    return _send(certificado, 'ConsultarLote', **kwargs)


def consultar_nfse(certificado, **kwargs):
    return _send(certificado, 'ConsultarNFSe', **kwargs)


def cancelar_nfse(certificado, **kwargs):
    return _send(certificado, 'CancelarNFSe', **kwargs)
