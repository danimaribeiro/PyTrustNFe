# -*- encoding: utf-8 -*-
# © 2017 Fábio Luna, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import os
import suds
from lxml import etree
from pytrustnfe.xml import render_xml, sanitize_response
from pytrustnfe.certificado import extract_cert_and_key_from_pfx, save_cert_key
from pytrustnfe.nfse.assinatura import Assinatura
from pytrustnfe.client import get_client


def _render(certificado, method, **kwargs):
    path = os.path.join(os.path.dirname(__file__), 'templates')
    if method == "testeEnviar":
        xml_send = render_xml(path, 'enviar.xml', True, **kwargs)
    else:
        xml_send = render_xml(path, '%s.xml' % method, False, **kwargs)

    if type(xml_send) != str:
        xml_send = etree.tostring(xml_send)
    return xml_send.decode()


def _get_url(**kwargs):

    try:
        cod_cidade = kwargs['nfse']['cidade']
    except (KeyError, TypeError):
        raise KeyError("Código de cidade inválido!")

    urls = {
        # Belém - PA
        '2715': 'http://www.issdigitalbel.com.br/WsNFe2/LoteRps.jws?wsdl',
        # Sorocaba - SP
        '7145': 'http://issdigital.sorocaba.sp.gov.br/WsNFe2/LoteRps.jws?wsdl',
        # Teresina - PI
        '1219': 'http://www.issdigitalthe.com.br/WsNFe2/LoteRps.jws?wsdl',
        # Campinas - SP
        '6291': 'http://issdigital.campinas.sp.gov.br/WsNFe2/LoteRps.jws?wsdl',
        # Uberlandia - MG
        '5403': 'http://udigital.uberlandia.mg.gov.br/WsNFe2/LoteRps.jws?wsdl',
        # São Luis - MA
        '0921':
        'http://sistemas.semfaz.saoluis.ma.gov.br/WsNFe2/LoteRps.jws?wsdl',
        # Campo Grande - MS
        '2729': 'http://issdigital.pmcg.ms.gov.br/WsNFe2/LoteRps.jws?wsdl',
    }

    try:
        return urls[str(cod_cidade)]
    except KeyError:
        raise KeyError("DSF não emite notas da cidade {}!".format(
            cod_cidade))


def _send(certificado, method, **kwargs):
    url = _get_url(**kwargs)

    path = os.path.join(os.path.dirname(__file__), 'templates')

    xml_send = _render(path, method, **kwargs)
    client = get_client(url)
    response = False

    if certificado:
        cert, key = extract_cert_and_key_from_pfx(
            certificado.pfx, certificado.password)
        cert, key = save_cert_key(cert, key)
        signer = Assinatura(cert, key, certificado.password)
        xml_send = signer.assina_xml(xml_send, '')

    try:
        response = getattr(client.service, method)(xml_send)
        response, obj = sanitize_response(response.encode())
    except suds.WebFault as e:
        return {
            'sent_xml': xml_send,
            'received_xml': e.fault.faultstring,
            'object': None
        }
    except Exception as e:
        if response:
            raise Exception(response)
        else:
            raise e

    return {
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
