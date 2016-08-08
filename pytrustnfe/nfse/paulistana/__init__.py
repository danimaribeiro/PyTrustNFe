# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import os
import logging
import suds
from uuid import uuid4
from lxml import etree
from pytrustnfe.xml import render_xml, valida_schema, sanitize_response
from pytrustnfe.client import get_authenticated_client
from pytrustnfe.certificado import extract_cert_and_key_from_pfx, save_cert_key


from signxml import XMLSigner
from signxml import methods


def sign_xml(xml, cert, key):
    parser = etree.XMLParser(remove_blank_text=True, remove_comments=True)
    elem = etree.fromstring(xml, parser=parser)

    root = etree.Element('root')
    rps = elem.find('RPS')

    signer = XMLSigner(
        digest_algorithm=u'sha1', signature_algorithm="rsa-sha1",
        method=methods.enveloped,
        c14n_algorithm='http://www.w3.org/TR/2001/REC-xml-c14n-20010315')
    ns = {}
    ns[None] = signer.namespaces['ds']
    signer.namespaces = ns
    signed_root = signer.sign(rps, key=str(key), cert=cert)

    root.append(
        signed_root.find('{http://www.w3.org/2000/09/xmldsig#}Signature'))
    elem.remove(rps)
    elem.append(signed_root)
    elem.append(root.find('{http://www.w3.org/2000/09/xmldsig#}Signature'))
    return etree.tostring(elem)


def _send(certificado, method, **kwargs):
    # A little hack to test
    path = os.path.join(os.path.dirname(__file__), 'templates')
    if method == 'TesteEnvioLoteRPS':
        xml = render_xml(path, 'EnvioLoteRPS.xml', **kwargs)
    else:
        xml = render_xml(path, '%s.xml' % method, **kwargs)
    base_url = 'https://nfe.prefeitura.sp.gov.br/ws/lotenfe.asmx?wsdl'

    cert, key = extract_cert_and_key_from_pfx(
        certificado.pfx, certificado.password)
    cert_path, key_path = save_cert_key(cert, key)
    client = get_authenticated_client(base_url, cert_path, key_path)

    xml_signed = sign_xml(xml, cert, key)

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
