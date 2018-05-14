# © 2018 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import os
from lxml import etree
from requests import Session
from zeep import Client
from zeep.transports import Transport

from pytrustnfe.certificado import extract_cert_and_key_from_pfx, save_cert_key
from pytrustnfe.xml import render_xml, sanitize_response
from pytrustnfe.nfse.bh.assinatura import Assinatura


def _render(certificado, method, **kwargs):
    path = os.path.join(os.path.dirname(__file__), 'templates')
    xml_send = render_xml(path, '%s.xml' % method, True, **kwargs)

    reference = ''
    if method == 'GerarNfse':
        reference = 'rps:%s' % kwargs['rps']['numero']
        ref_lote = 'lote%s' % kwargs['rps']['numero_lote']
    elif method == 'CancelarNfse':
        reference = 'Cancelamento_NF%s' % kwargs['cancelamento']['numero_nfse']

    signer = Assinatura(certificado.pfx, certificado.password)
    xml_send = signer.assina_xml(xml_send, reference)
    xml_send = signer.assina_xml(etree.fromstring(xml_send), ref_lote)
    return xml_send.encode('utf-8')


def _send(certificado, method, **kwargs):
    base_url = ''
    if kwargs['ambiente'] == 'producao':
        base_url = 'https://bhissdigital.pbh.gov.br/bhiss-ws/nfse?wsdl'
    else:
        base_url = 'https://bhisshomologa.pbh.gov.br/bhiss-ws/nfse?wsdl'

    xml_send = kwargs["xml"].decode('utf-8')
    xml_cabecalho = '<?xml version="1.0" encoding="UTF-8"?>\
    <cabecalho xmlns="http://www.abrasf.org.br/nfse.xsd" versao="1.00">\
    <versaoDados>1.00</versaoDados></cabecalho>'

    cert, key = extract_cert_and_key_from_pfx(
        certificado.pfx, certificado.password)
    cert, key = save_cert_key(cert, key)

    session = Session()
    session.cert = (cert, key)
    session.verify = False
    transport = Transport(session=session)

    client = Client(base_url, transport=transport)

    response = client.service[method](xml_cabecalho, xml_send)

    response, obj = sanitize_response(response.encode('utf-8'))
    return {
        'sent_xml': xml_send,
        'received_xml': response.decode('utf-8'),
        'object': obj
    }


def xml_gerar_nfse(certificado, **kwargs):
    return _render(certificado, 'GerarNfse', **kwargs)


def gerar_nfse(certificado, **kwargs):
    if "xml" not in kwargs:
        kwargs['xml'] = xml_gerar_nfse(certificado, **kwargs)
    return _send(certificado, 'GerarNfse', **kwargs)


def xml_cancelar_nfse(certificado, **kwargs):
    return _render(certificado, 'CancelarNfse', **kwargs)


def cancelar_nfse(certificado, **kwargs):
    if "xml" not in kwargs:
        kwargs['xml'] = xml_cancelar_nfse(certificado, **kwargs)
    return _send(certificado, 'CancelarNfse', **kwargs)
