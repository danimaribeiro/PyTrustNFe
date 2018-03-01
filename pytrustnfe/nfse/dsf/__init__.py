# -*- encoding: utf-8 -*-
# © 2017 Fábio Luna, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import os
import requests
from pytrustnfe.xml import render_xml, sanitize_response
from pytrustnfe.certificado import extract_cert_and_key_from_pfx, save_cert_key
from pytrustnfe.nfse.assinatura import Assinatura


def _render(certificado, method, **kwargs):
    path = os.path.join(os.path.dirname(__file__), 'templates')
    if method == "testeEnviar":
        xml_send = render_xml(path, 'enviar.xml', True, **kwargs)
    else:
        xml_send = render_xml(path, '%s.xml' % method, False, **kwargs)

    cert, key = extract_cert_and_key_from_pfx(
        certificado.pfx, certificado.password)
    cert, key = save_cert_key(cert, key)
    signer = Assinatura(cert, key, certificado.password)
    xml_send = signer.assina_xml(xml_send, '')

    return xml_send


def _get_url(**kwargs):
    urls = {
        # Belém - PA
        '2715': 'http://www.issdigitalbel.com.br/WsNFe2/LoteRps.jws',
        # Sorocaba - SP
        '7145': 'http://issdigital.sorocaba.sp.gov.br/WsNFe2/LoteRps.jws',
        # Teresina - PI
        '1219': 'http://www.issdigitalthe.com.br/WsNFe2/LoteRps.jws',
        # Campinas - SP
        '6291': 'http://issdigital.campinas.sp.gov.br/WsNFe2/LoteRps.jws?wsdl',
        # Uberlandia - MG
        '5403': 'http://udigital.uberlandia.mg.gov.br/WsNFe2/LoteRps.jws',
        # São Luis - MA
        '0921': 'https://stm.semfaz.saoluis.ma.gov.br/WsNFe2/LoteRps?wsdl',
        # Campo Grande - MS
        '9051': 'http://issdigital.pmcg.ms.gov.br/WsNFe2/LoteRps.jws?wsdl',
    }
    return urls[kwargs['siafi_code']]


def _send(certificado, method, **kwargs):
    url = _get_url(**kwargs)

    xml_send = '<?xml version="1.0" encoding="utf-8"?>' +\
        kwargs['xml'].decode('utf-8')

    response = False
    soap = '<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/">'\
        '<Body>'\
        '<enviarSincrono xmlns="http://issdigital.pmcg.ms.gov.br/WsNFe2/LoteRps.jws">'\
        '<mensagemXml><![CDATA[' + xml_send + ']]></mensagemXml>'\
        '</enviarSincrono>'\
        '</Body>'\
        '</Envelope>'

    headers = {
        "Content-Type": 'text/xml; charset="utf-8"',
        "SOAPAction": "",
    }
    http_response = requests.post(url, data=soap, headers=headers)
    response, obj = sanitize_response(http_response.text.encode('utf-8'))

    return {
        'status_code': http_response.status_code,
        'sent_xml': xml_send,
        'received_xml': response,
        'object': obj
    }


def xml_enviar(certificado, **kwargs):
    return _render(certificado, 'enviar', **kwargs)


def enviar(certificado, **kwargs):
    if "xml" not in kwargs:
        kwargs['xml'] = xml_enviar(certificado, **kwargs)
    return _send(certificado, 'enviar', **kwargs)


def xml_teste_enviar(certificado, **kwargs):
    return _render(certificado, 'testeEnviar', **kwargs)


def teste_enviar(certificado, **kwargs):
    if "xml" not in kwargs:
        kwargs['xml'] = xml_teste_enviar(certificado, **kwargs)
    return _send(certificado, 'testeEnviar', **kwargs)


def cancelar(certificado, ** kwargs):
    return _send(certificado, 'cancelar', **kwargs)


def consulta_lote(**kwargs):
    return _send(False, 'consultarLote', **kwargs)


def xml_consultar_nfse_rps(certificado, **kwargs):
    return _render(certificado, 'consultarNFSeRps', **kwargs)


def consultar_nfse_rps(certificado, **kwargs):
    if "xml" not in kwargs:
        kwargs['xml'] = xml_consultar_nfse_rps(certificado, **kwargs)
    return _send(certificado, 'consultarNFSeRps', **kwargs)
