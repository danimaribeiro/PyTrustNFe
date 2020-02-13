# © 2019 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import os
from OpenSSL import crypto
from base64 import b64encode

from requests import Session
from zeep import Client
from zeep.transports import Transport
from requests.packages.urllib3 import disable_warnings

from pytrustnfe.xml import render_xml, sanitize_response
from pytrustnfe.certificado import extract_cert_and_key_from_pfx, save_cert_key
from pytrustnfe.nfe.assinatura import Assinatura
from lxml import etree


def sign_rps(path, certificado, **kwargs):
    if "nfse" in kwargs:
        lote = ""
        for item in kwargs["nfse"]["lista_rps"]:
            data = {"rps": item}
            xml_rps = render_xml(path, "Rps.xml", True, **data)

            signer = Assinatura(certificado.pfx, certificado.password)
            lote += signer.assina_xml(
                xml_rps, f"rps:{item.get('numero')}{item.get('serie')}", getchildren=True
            )
        return lote
    return ""


def _render(certificado, method, **kwargs):
    path = os.path.join(os.path.dirname(__file__), "templates")
    parser = etree.XMLParser(
        remove_blank_text=True, remove_comments=True, strip_cdata=False
    )

    lote = ""
    referencia = ""
    if method == "RecepcionarLoteRps":
        referencia = "lote"
        lote = sign_rps(path, certificado, **kwargs)

    kwargs["lote"] = lote
    xml_send = render_xml(path, "%s.xml" % method, False, **kwargs)

    signer = Assinatura(certificado.pfx, certificado.password)

    xml_send = signer.assina_xml(etree.fromstring(
        xml_send, parser=parser), f"{referencia}", getchildren=True)
    return xml_send


def _send(certificado, method, **kwargs):
    base_url = ""
    if kwargs["ambiente"] == "producao":
        base_url = "https://wsnfsev1.natal.rn.gov.br:8444"
    else:
        base_url = "https://wsnfsev1homologacao.natal.rn.gov.br:8443/axis2/services/NfseWSServiceV1?wsdl"

    base_url = "https://wsnfsev1homologacao.natal.rn.gov.br:8443/axis2/services/NfseWSServiceV1?wsdl"
    cert, key = extract_cert_and_key_from_pfx(
        certificado.pfx, certificado.password)
    cert, key = save_cert_key(cert, key)

    disable_warnings()
    session = Session()
    session.cert = (cert, key)
    session.verify = False
    transport = Transport(session=session)

    client = Client(wsdl=base_url, transport=transport)
    xml_send = {}
    xml_send = {
        "nfseDadosMsg": kwargs["xml"],
        "nfseCabecMsg": """<?xml version="1.0"?>
        <cabecalho xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" versao="1" xmlns="http://www.abrasf.org.br/ABRASF/arquivos/nfse.xsd">
        <versaoDados>1</versaoDados>
        </cabecalho>""",
    }

    response = client.service[method](**xml_send)
    response, obj = sanitize_response(response)
    return {"sent_xml": xml_send, "received_xml": response, "object": obj}


def xml_recepcionar_lote_rps(certificado, **kwargs):
    return _render(certificado, "RecepcionarLoteRps", **kwargs)


def recepcionar_lote_rps(certificado, **kwargs):
    if "xml" not in kwargs:
        kwargs["xml"] = xml_recepcionar_lote_rps(certificado, **kwargs)
    return _send(certificado, "RecepcionarLoteRps", **kwargs)


def xml_consultar_lote_rps(certificado, **kwargs):
    return _render(certificado, "ConsultarLoteRps", **kwargs)


def consultar_lote_rps(certificado, **kwargs):
    if "xml" not in kwargs:
        kwargs["xml"] = xml_consultar_lote_rps(certificado, **kwargs)
    return _send(certificado, "ConsultarLoteRps", **kwargs)


def xml_cancelar_nfse(certificado, **kwargs):
    return _render(certificado, "cancelarNfse", **kwargs)


def cancelar_nfse(certificado, **kwargs):
    if "xml" not in kwargs:
        kwargs["xml"] = xml_cancelar_nfse(certificado, **kwargs)
    return _send(certificado, "cancelarNfse", **kwargs)
