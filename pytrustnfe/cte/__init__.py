import os
from lxml import etree
from pytrustnfe.nfe.assinatura import Assinatura
from pytrustnfe.xml import render_xml, sanitize_response
from pytrustnfe.cte.webservices import localizar_url
from pytrustnfe.certificado import extract_cert_and_key_from_pfx, save_cert_key

# Zeep
from requests import Session
from zeep import Client
from zeep.transports import Transport


def _render(certificado, method, sign, reference, **kwargs):
    path = os.path.join(os.path.dirname(__file__), 'templates')
    xmlElem_send = render_xml(path, '%s.xml' % method, True, **kwargs)

    if sign:
        signer = Assinatura(certificado.pfx, certificado.password)
        xml_send = signer.assina_xml(xmlElem_send, reference)
    else:
        xml_send = etree.tostring(xmlElem_send, encoding=str)
    return xml_send


def _send(certificado, method, **kwargs):
    xml_send = kwargs["xml"]
    base_url = localizar_url(method,  kwargs['estado'], kwargs['ambiente'])

    cert, key = extract_cert_and_key_from_pfx(
        certificado.pfx, certificado.password)
    cert, key = save_cert_key(cert, key)

    session = Session()
    session.cert = (cert, key)
    session.verify = False
    transport = Transport(session=session)

    parser = etree.XMLParser(strip_cdata=False)
    xml = etree.fromstring(xml_send, parser=parser)

    client = Client(base_url, transport=transport)

    port = next(iter(client.wsdl.port_types))
    first_operation = [x for x in iter(
        client.wsdl.port_types[port].operations) if "zip" not in x.lower()][0]

    namespaceNFe = xml.find(".//{http://www.portalfiscal.inf.br/nfe}NFe")
    if namespaceNFe is not None:
        namespaceNFe.set('xmlns', 'http://www.portalfiscal.inf.br/nfe')

    with client.settings(raw_response=True):
        response = client.service[first_operation](xml)
        response, obj = sanitize_response(response.text)
        return {
            'sent_xml': xml_send,
            'received_xml': response,
            'object': obj.Body.getchildren()[0]
        }


def cte_recepcao(certificado, gerar_xml, **kwargs):  # Assinar
    if gerar_xml:
        return _render(certificado, 'CteRecepcao', True, **kwargs)
    return _send(certificado, 'CteRecepcao', **kwargs)


def cte_retorno_recepcao(certificado, gerar_xml, **kwargs):  # Assinar
    if gerar_xml:
        return _render(certificado, 'CteRetRecepcao', True, **kwargs)
    return _send(certificado, 'CteRetRecepcao', **kwargs)


def cte_inutilizacao(certificado, gerar_xml, **kwargs):  # Assinar
    if gerar_xml:
        return _render(certificado, 'CteInutilizacao', True, **kwargs)
    return _send(certificado, 'CteInutilizacao', **kwargs)


def cte_consulta_protocolo(certificado, gerar_xml, **kwargs):  # Assinar
    if gerar_xml:
        return _render(certificado, 'CteConsultaProtocolo', True, **kwargs)
    return _send(certificado, 'CteConsultaProtocolo', **kwargs)


def cte_consulta_cadastro(certificado, gerar_xml, **kwargs):  # Assinar
    if gerar_xml:
        return _render(certificado, 'CteConsultaCadastro', True, **kwargs)
    return _send(certificado, 'CteConsultaCadastro', **kwargs)


def cte_recepcao_evento(certificado, gerar_xml, **kwargs):  # Assinar
    if gerar_xml:
        return _render(certificado, 'CteRecepcaoEvento', True, **kwargs)
    return _send(certificado, 'CteRecepcaoEvento', **kwargs)


def cte_recepcao_os(certificado, gerar_xml, **kwargs):  # Assinar
    if gerar_xml:
        return _render(certificado, 'CTeRecepcaoOS', True, **kwargs)
    return _send(certificado, 'CTeRecepcaoOS', **kwargs)


def cte_distribuicao_dfe(certificado, gerar_xml, **kwargs):  # Assinar
    if gerar_xml:
        return _render(certificado, 'CTeDistribuicaoDFe', True, **kwargs)
    return _send(certificado, 'CTeDistribuicaoDFe', **kwargs)
