import os
import suds

from lxml import etree

from pytrustnfe.client import get_authenticated_client
from pytrustnfe.certificado import extract_cert_and_key_from_pfx, save_cert_key
from pytrustnfe.xml import render_xml, sanitize_response

from .assinatura import Assinatura


def _render(certificado, method, **kwargs):
    path = os.path.join(os.path.dirname(__file__), "templates")
    xml_send = render_xml(path, f"{method}.xml", False, **kwargs)
    signer = Assinatura(certificado.pfx, certificado.password)
    xml_send = etree.fromstring(xml_send)
    xml_send = signer.assina_xml(xml_send)
    return xml_send


def _send(certificado, method, **kwargs):
    base_url = "https://nfse.goiania.go.gov.br/ws/nfse.asmx?wsdl"
    xml_send = kwargs["xml"]
    cert, key = extract_cert_and_key_from_pfx(certificado.pfx, certificado.password)
    cert, key = save_cert_key(cert, key)
    client = get_authenticated_client(base_url, cert, key)

    try:
        response = getattr(client.service, method)(xml_send)
    except suds.WebFault as e:
        return {
            "send_xml": str(xml_send),
            "received_xml": str(e.fault.faultstring),
            "object": None,
        }

    response, obj = sanitize_response(response)
    return {"send_xml": str(xml_send), "received_xml": str(response), "object": obj}


def xml_gerar_nfse(certificado, **kwargs):
    """ Retorna o XML montado para ser enviado para o Webservice """

    return _render(certificado, "GerarNfse", **kwargs)


def gerar_nfse(certificado, **kwargs):
    """" Gera uma NFSe de saída """

    if "xml" not in kwargs:
        kwargs["xml"] = xml_gerar_nfse
    return _send(certificado, "GerarNfse", **kwargs)


def consulta_nfse_por_rps(certificado, **kwargs):
    """ Consulta os dados de um NFSe já emitida """

    if "xml" not in kwargs:
        kwargs["xml"] = _render(certificado, "ConsultarNfseRps", **kwargs)
    return _send(certificado, "ConsultarNfseRps", **kwargs)
