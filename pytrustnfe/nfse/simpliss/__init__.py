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
    schema = os.path.join(path, '%s.xsd' % method)

    from lxml import etree
    nfe = etree.fromstring(xml_send)
    esquema = etree.XMLSchema(etree.parse(schema))
    esquema.validate(nfe)
    erros = [x.message for x in esquema.error_log]

#    if erros:
#        raise Exception('\n'.join(erros))
    base_url = 'http://sistemas.pmp.sp.gov.br/semfi/simpliss/ws_nfse/nfseservice.svc?wsdl'

    cert, key = extract_cert_and_key_from_pfx(
        certificado.pfx, certificado.password)
    cert, key = save_cert_key(cert, key)
    client = get_authenticated_client(base_url, cert, key)

    #pfx_path = certificado.save_pfx()
    #signer = Assinatura(pfx_path, certificado.password)
    #xml_send = signer.assina_xml(xml_send, '')

    try:
        response = getattr(client.service, method)(xml_send)
    except suds.WebFault, e:
        return {
            'sent_xml': xml_send,
            'received_xml': e.fault.faultstring,
            'object': None
        }
    print response
    response, obj = sanitize_response(response)
    return {
        'sent_xml': xml_send,
        'received_xml': response,
        'object': obj
    }


def recepcionar_lote_rps(certificado, **kwargs):
    return _send(certificado, 'RecepcionarLoteRps', **kwargs)


def consultar_situacao_lote(certificado, **kwargs):
    return _send(certificado, 'ConsultarSituacaoLoteRps', **kwargs)


def consultar_nfse_por_rps(certificado, **kwargs):
    return _send(certificado, 'ConsultarNfsePorRps', **kwargs)


def consultar_lote_rps(certificado, **kwargs):
    return _send(certificado, 'ConsultarLoteRps', **kwargs)


def consultar_nfse(certificado, **kwargs):
    return _send(certificado, 'ConsultarNfse', **kwargs)


def cancelar_nfse(certificado, **kwargs):
    return _send(certificado, 'CancelarNfse', **kwargs)
