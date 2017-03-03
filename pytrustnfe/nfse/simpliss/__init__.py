# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# Endereços Simpliss Piracicaba
# Homologação: http://wshomologacao.simplissweb.com.br/nfseservice.svc
# Homologação site: http://homologacaonovo.simplissweb.com.br/Account/Login

# Prod:http://sistemas.pmp.sp.gov.br/semfi/simpliss/contrib/Account/Login
# Prod:http://sistemas.pmp.sp.gov.br/semfi/simpliss/ws_nfse/nfseservice.svc

import os
from lxml import etree
from pytrustnfe import HttpClient
from pytrustnfe.xml import render_xml, sanitize_response
from pytrustnfe.certificado import extract_cert_and_key_from_pfx, save_cert_key
from pytrustnfe.nfse.assinatura import Assinatura


def _render_xml(certificado, method, **kwargs):
    path = os.path.join(os.path.dirname(__file__), 'templates')
    xml_send = render_xml(path, '%s.xml' % method, False, **kwargs)

    cert, key = extract_cert_and_key_from_pfx(
        certificado.pfx, certificado.password)
    cert, key = save_cert_key(cert, key)

    pfx_path = certificado.save_pfx()
    signer = Assinatura(pfx_path, certificado.password)
    xml_send = signer.assina_xml(xml_send, '')

    return xml_send


def _validate(method, xml):
    path = os.path.join(os.path.dirname(__file__), 'templates')
    schema = os.path.join(path, '%s.xsd' % method)

    nfe = etree.fromstring(xml)
    esquema = etree.XMLSchema(etree.parse(schema))
    esquema.validate(nfe)
    erros = [x.message for x in esquema.error_log]
    return erros


def _send(method, **kwargs):
    if kwargs['ambiente'] == 'producao':
        base_url = 'http://sistemas.pmp.sp.gov.br/semfi/simpliss/ws_nfse/nfseservice.svc?WSDL'  # noqa
    else:
        base_url = 'http://wshomologacao.simplissweb.com.br/nfseservice.svc?WSDL'  # noqa

    xml_send = kwargs["xml"].replace('<?xml version="1.0"?>', '')
    path = os.path.join(os.path.dirname(__file__), 'templates')
    soap = render_xml(path, 'SoapRequest.xml', False, soap_body=xml_send)

    act = 'http://www.sistema.com.br/Sistema.Ws.Nfse/INfseService/%s' % method

    client = HttpClient(base_url)
    response = client.post_soap(soap, act)

    print response
    response, obj = sanitize_response(response)
    return {
        'sent_xml': xml_send,
        'received_xml': response,
        'object': obj
    }


def xml_recepcionar_lote_rps(certificado, **kwargs):
    return _render_xml(certificado, 'RecepcionarLoteRps', **kwargs)


def recepcionar_lote_rps(certificado, **kwargs):
    if "xml" not in kwargs:
        kwargs['xml'] = xml_recepcionar_lote_rps(certificado, **kwargs)
    return _send('RecepcionarLoteRps', **kwargs)


def xml_consultar_situacao_lote(certificado, **kwargs):
    return _render_xml(certificado, 'ConsultarSituacaoLoteRps', **kwargs)


def consultar_situacao_lote(certificado, **kwargs):
    if "xml" not in kwargs:
        kwargs['xml'] = xml_consultar_situacao_lote(certificado, **kwargs)
    return _send('ConsultarSituacaoLoteRps', **kwargs)


def consultar_nfse_por_rps(certificado, **kwargs):
    return _send('ConsultarNfsePorRps', **kwargs)


def consultar_lote_rps(certificado, **kwargs):
    return _send('ConsultarLoteRps', **kwargs)


def consultar_nfse(certificado, **kwargs):
    return _send('ConsultarNfse', **kwargs)


def cancelar_nfse(certificado, **kwargs):
    return _send('CancelarNfse', **kwargs)
