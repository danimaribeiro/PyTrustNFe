# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import hashlib
import os
import requests
from lxml import etree
from .patch import has_patch
from .assinatura import Assinatura
from pytrustnfe.xml import render_xml, sanitize_response
from pytrustnfe.utils import gerar_chave, ChaveNFe
from pytrustnfe.Servidores import localizar_url
from pytrustnfe.urls import url_qrcode, url_qrcode_exibicao
from pytrustnfe.certificado import extract_cert_and_key_from_pfx, save_cert_key
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# Zeep
from requests import Session
from zeep import Client
from zeep.transports import Transport


def _generate_nfe_id(**kwargs):
    for item in kwargs["NFes"]:
        vals = {
            "cnpj": item["infNFe"]["emit"]["cnpj_cpf"],
            "estado": item["infNFe"]["ide"]["cUF"],
            "emissao": "%s%s"
            % (
                item["infNFe"]["ide"]["dhEmi"][2:4],
                item["infNFe"]["ide"]["dhEmi"][5:7],
            ),
            "modelo": item["infNFe"]["ide"]["mod"],
            "serie": item["infNFe"]["ide"]["serie"],
            "numero": item["infNFe"]["ide"]["nNF"],
            "tipo": item["infNFe"]["ide"]["tpEmis"],
            "codigo": item["infNFe"]["ide"]["cNF"],
        }
        chave_nfe = ChaveNFe(**vals)
        chave_nfe = gerar_chave(chave_nfe, "NFe")
        item["infNFe"]["Id"] = chave_nfe
        item["infNFe"]["ide"]["cDV"] = chave_nfe[len(chave_nfe) - 1 :]


def _render(certificado, method, sign, **kwargs):
    path = os.path.join(os.path.dirname(__file__), "templates")
    xmlElem_send = render_xml(path, "%s.xml" % method, True, **kwargs)

    modelo = xmlElem_send.find(".//{http://www.portalfiscal.inf.br/nfe}mod")
    modelo = modelo.text if modelo is not None else "55"

    if sign:
        signer = Assinatura(certificado.pfx, certificado.password)
        if method == "NfeInutilizacao":
            xml_send = signer.assina_xml(xmlElem_send, kwargs["obj"]["id"])
        if method == "NfeAutorizacao":
            xml_send = signer.assina_xml(
                xmlElem_send, kwargs["NFes"][0]["infNFe"]["Id"]
            )
        elif method == "RecepcaoEvento":
            xml_send = signer.assina_xml(xmlElem_send, kwargs["eventos"][0]["Id"])
        elif method == "RecepcaoEventoManifesto":
            xml_send = signer.assina_xml(
                xmlElem_send, kwargs["manifesto"]["identificador"]
            )

    else:
        xml_send = etree.tostring(xmlElem_send, encoding=str)
    return xml_send


def gerar_qrcode(id_csc: int, csc: str, xml_send: str, cert = False) -> str:
    xml = etree.fromstring(xml_send)
    signature = xml.find(
        ".//{http://www.w3.org/2000/09/xmldsig#}Signature")
    id = xml.find(
        ".//{http://www.portalfiscal.inf.br/nfe}infNFe").get('Id')
    if id is None:
        raise Exception("XML Invalido - Sem o ID")

    chave = id.replace('NFe', '')
    emit_uf = chave[:2]

    tp_amb = xml.find(".//{http://www.portalfiscal.inf.br/nfe}tpAmb")
    if tp_amb is None:
        raise Exception("XML Invalido - Sem o tipo de ambiente")

    dh_emi = xml.find(".//{http://www.portalfiscal.inf.br/nfe}dhEmi")
    if dh_emi is None:
        raise Exception("XML Invalido - Sem data de Emissao")
    dh_emi = dh_emi.text.split("-")[2].split("T")[0]

    tp_emis = xml.find(".//{http://www.portalfiscal.inf.br/nfe}tpEmis")
    if tp_emis is None:
        raise Exception("XML Invalido - Sem tipo de emissao")

    v_nf = xml.find(".//{http://www.portalfiscal.inf.br/nfe}vNF")
    if v_nf is None:
        raise Exception("XML Invalido - Sem o valor da NFe")

    url_qrcode_str = url_qrcode(
        estado=emit_uf,
        ambiente=tp_amb.text)
    url_qrcode_exibicao_str = url_qrcode_exibicao(
        estado=emit_uf,
        ambiente=tp_amb.text)

    if tp_emis != 1:
        if signature is None:
            if cert is not False:
                signer = Assinatura(certificado.pfx, certificado.password)
                xml_send = signer.assina_xml(xmlElem_send, id)
            else:
                raise Exception("XML Invalido - Sem assinatura e não "
                                "foi enviado o certificado nos parametros")
        digest_value = xml.find(
            ".//{http://www.w3.org/2000/09/xmldsig#}DigestValue")
        c_hash_qr_code = \
            "{ch_acesso}|{versao}|{tp_amb}|{dh_emi}|" \
            "{v_nf}|{dig_val}|{id_csc}|{csc}".format(
                ch_acesso=chave,
                versao=2,
                tp_amb=tp_amb.text,
                dh_emi=dh_emi,
                v_nf=float(v_nf.text),
                dig_val=digest_value.text,
                id_csc=int(id_csc),
                csc=csc
            )
        c_hash_qr_code = hashlib.sha1(c_hash_qr_code.encode()). \
            hexdigest()
        qr_code_url = 'p={ch_acesso}|{versao}|{tp_amb}|{dh_emi}|" \
                                "{v_nf}|{dig_val}|{id_csc}|{hash}'.format(
            ch_acesso=chave,
            versao=2,
            tp_amb=tp_amb.text,
            dh_emi=dh_emi,
            v_nf=float(v_nf.text),
            dig_val=digest_value.text,
            id_csc=int(id_csc),
            hash=c_hash_qr_code
        )
        qrcode = url_qrcode_str + qr_code_url
        url_consulta = url_qrcode_exibicao_str

        qrCode = xml.find(
            './/{http://www.portalfiscal.inf.br/nfe}qrCode').text = \
            qrcode
        urlChave = xml.find(
            './/{http://www.portalfiscal.inf.br/nfe}urlChave').text = \
            url_consulta
    else:
        c_hash_qr_code = \
        "{ch_acesso}|{versao}|{tp_amb}|{id_csc}|{csc}".format(
            ch_acesso=chave,
            versao=2,
            tp_amb=tp_amb.text,
            id_csc=int(id_csc),
            csc=csc
        )
        c_hash_qr_code = hashlib.sha1(c_hash_qr_code.encode()).hexdigest()

        qr_code_url = "p={ch_acesso}|{versao}|{tp_amb}|{id_csc}|" \
                      "{hash}".\
            format(
                ch_acesso=chave,
                versao=2,
                tp_amb=tp_amb.text,
                id_csc=int(id_csc),
                hash=c_hash_qr_code
            )
        qrcode = url_qrcode_str + qr_code_url
        url_consulta = url_qrcode_exibicao_str
        qrCode = xml.find(
            './/{http://www.portalfiscal.inf.br/nfe}qrCode').text = \
            qrcode
        urlChave = xml.find(
            './/{http://www.portalfiscal.inf.br/nfe}urlChave').text = \
            url_consulta
    return etree.tostring(xml)

def _get_session(certificado):
    cert, key = extract_cert_and_key_from_pfx(certificado.pfx, certificado.password)
    cert, key = save_cert_key(cert, key)

    session = Session()
    session.cert = (cert, key)
    session.verify = False
    return session


def _get_client(base_url, transport):
    client = Client(base_url, transport=transport)
    port = next(iter(client.wsdl.port_types))
    first_operation = [
        x
        for x in iter(client.wsdl.port_types[port].operations)
        if "zip" not in x.lower()
    ][0]
    return first_operation, client


def _send(certificado, method, **kwargs):
    xml_send = kwargs["xml"]
    base_url = localizar_url(
        method, kwargs["estado"], kwargs["modelo"], kwargs["ambiente"]
    )
    session = _get_session(certificado)
    patch = has_patch(kwargs["estado"], method)
    if patch:
        return patch(session, xml_send, kwargs["ambiente"])
    transport = Transport(session=session)
    first_op, client = _get_client(base_url, transport)
    return _send_zeep(first_op, client, xml_send)


def _send_zeep(first_operation, client, xml_send):
    parser = etree.XMLParser(strip_cdata=False)
    xml = etree.fromstring(xml_send, parser=parser)

    namespaceNFe = xml.find(".//{http://www.portalfiscal.inf.br/nfe}NFe")
    if namespaceNFe is not None:
        namespaceNFe.set("xmlns", "http://www.portalfiscal.inf.br/nfe")

    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    with client.settings(raw_response=True):
        response = client.service[first_operation](xml)
        response, obj = sanitize_response(response.text)
        return {
            "sent_xml": xml_send,
            "received_xml": response,
            "object": obj.Body.getchildren()[0],
        }


def xml_autorizar_nfe(certificado, **kwargs):
    _generate_nfe_id(**kwargs)
    return _render(certificado, "NfeAutorizacao", True, **kwargs)


def autorizar_nfe(certificado, **kwargs):  # Assinar
    if "xml" not in kwargs:
        kwargs["xml"] = xml_autorizar_nfe(certificado, **kwargs)
    return _send(certificado, "NfeAutorizacao", **kwargs)


def xml_retorno_autorizar_nfe(certificado, **kwargs):
    return _render(certificado, "NfeRetAutorizacao", False, **kwargs)


def retorno_autorizar_nfe(certificado, **kwargs):
    if "xml" not in kwargs:
        kwargs["xml"] = xml_retorno_autorizar_nfe(certificado, **kwargs)
    return _send(certificado, "NfeRetAutorizacao", **kwargs)


def xml_recepcao_evento_cancelamento(certificado, **kwargs):  # Assinar
    return _render(certificado, "RecepcaoEvento", True, **kwargs)


def recepcao_evento_cancelamento(certificado, **kwargs):  # Assinar
    if "xml" not in kwargs:
        kwargs["xml"] = xml_recepcao_evento_cancelamento(certificado, **kwargs)
    return _send(certificado, "RecepcaoEvento", **kwargs)


def xml_inutilizar_nfe(certificado, **kwargs):
    return _render(certificado, "NfeInutilizacao", True, **kwargs)


def inutilizar_nfe(certificado, **kwargs):
    if "xml" not in kwargs:
        kwargs["xml"] = xml_inutilizar_nfe(certificado, **kwargs)
    return _send(certificado, "NfeInutilizacao", **kwargs)


def xml_consultar_protocolo_nfe(certificado, **kwargs):
    return _render(certificado, "NfeConsultaProtocolo", False, **kwargs)


def consultar_protocolo_nfe(certificado, **kwargs):
    if "xml" not in kwargs:
        kwargs["xml"] = xml_consultar_protocolo_nfe(certificado, **kwargs)
    return _send(certificado, "NfeConsultaProtocolo", **kwargs)


def xml_nfe_status_servico(certificado, **kwargs):
    return _render(certificado, "NfeStatusServico", False, **kwargs)


def nfe_status_servico(certificado, **kwargs):
    if "xml" not in kwargs:
        kwargs["xml"] = xml_nfe_status_servico(certificado, **kwargs)
    return _send(certificado, "NfeStatusServico", **kwargs)


def xml_consulta_cadastro(certificado, **kwargs):
    return _render(certificado, "NfeConsultaCadastro", False, **kwargs)


def consulta_cadastro(certificado, **kwargs):
    if "xml" not in kwargs:
        kwargs["xml"] = xml_consulta_cadastro(certificado, **kwargs)
        kwargs["modelo"] = "55"
    return _send(certificado, "NfeConsultaCadastro", **kwargs)


def xml_recepcao_evento_carta_correcao(certificado, **kwargs):  # Assinar
    return _render(certificado, "RecepcaoEvento", True, **kwargs)


def recepcao_evento_carta_correcao(certificado, **kwargs):  # Assinar
    if "xml" not in kwargs:
        kwargs["xml"] = xml_recepcao_evento_carta_correcao(certificado, **kwargs)
    return _send(certificado, "RecepcaoEvento", **kwargs)


def xml_recepcao_evento_manifesto(certificado, **kwargs):  # Assinar
    return _render(certificado, "RecepcaoEvento", True, **kwargs)


def recepcao_evento_manifesto(certificado, **kwargs):  # Assinar
    if "xml" not in kwargs:
        kwargs["xml"] = xml_recepcao_evento_manifesto(certificado, **kwargs)
    return _send(certificado, "RecepcaoEvento", **kwargs)


def xml_consulta_distribuicao_nfe(certificado, **kwargs):  # Assinar
    return _render(certificado, "NFeDistribuicaoDFe", False, **kwargs)


def consulta_distribuicao_nfe(certificado, **kwargs):
    if "xml" not in kwargs:
        kwargs["xml"] = xml_consulta_distribuicao_nfe(certificado, **kwargs)
    return _send_v310(certificado, **kwargs)


def xml_download_nfe(certificado, **kwargs):  # Assinar
    return _render(certificado, "NFeDistribuicaoDFe", False, **kwargs)


def download_nfe(certificado, **kwargs):
    if "xml" not in kwargs:
        kwargs["xml"] = xml_download_nfe(certificado, **kwargs)
    return _send_v310(certificado, **kwargs)


def _send_v310(certificado, **kwargs):
    xml_send = kwargs["xml"]
    base_url = localizar_url(
        "NFeDistribuicaoDFe", kwargs["estado"], kwargs["modelo"], kwargs["ambiente"]
    )

    cert, key = extract_cert_and_key_from_pfx(certificado.pfx, certificado.password)
    cert, key = save_cert_key(cert, key)

    session = Session()
    session.cert = (cert, key)
    session.verify = False
    transport = Transport(session=session)

    xml = etree.fromstring(xml_send)
    xml_um = etree.fromstring(
        '<nfeCabecMsg xmlns="http://www.portalfiscal.inf.br/nfe/wsdl/"><cUF>AN</cUF><versaoDados>1.00</versaoDados></nfeCabecMsg>'
    )
    client = Client(base_url, transport=transport)

    port = next(iter(client.wsdl.port_types))
    first_operation = next(iter(client.wsdl.port_types[port].operations))
    with client.settings(raw_response=True):
        response = client.service[first_operation](
            nfeDadosMsg=xml, _soapheaders=[xml_um]
        )
        response, obj = sanitize_response(response.text)
        return {
            "sent_xml": xml_send,
            "received_xml": response,
            "object": obj.Body.nfeDistDFeInteresseResponse.nfeDistDFeInteresseResult,
        }
