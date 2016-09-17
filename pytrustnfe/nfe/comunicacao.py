# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from pytrustnfe.client import HttpClient
from pytrustnfe.certificado import save_cert_key, extract_cert_and_key_from_pfx

from ..xml import sanitize_response


def _soap_xml(body, cabecalho):
    xml = '<?xml version="1.0" encoding="utf-8"?>'
    xml += '<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"><soap:Header>'
    xml += '<nfeCabecMsg xmlns="http://www.portalfiscal.inf.br/nfe/wsdl/'+ cabecalho.soap_action +  '">'
    xml += '<cUF>' + cabecalho.estado + '</cUF><versaoDados>' + cabecalho.versao + '</versaoDados></nfeCabecMsg></soap:Header><soap:Body>'
    xml += '<nfeDadosMsg xmlns="http://www.portalfiscal.inf.br/nfe/wsdl/' + cabecalho.soap_action + '">'
    xml += body
    xml += '</nfeDadosMsg></soap:Body></soap:Envelope>'
    return xml.rstrip('\n')


def executar_consulta(certificado, url, cabecalho, xmlEnviar):
    cert, key = extract_cert_and_key_from_pfx(
        certificado.pfx, certificado.password)
    cert_path, key_path = save_cert_key(cert, key)
    client = HttpClient(url, cert_path, key_path)

    xml_enviar = _soap_xml(xmlEnviar, cabecalho)
    xml_retorno = client.post_soap(xml_enviar, cabecalho)
    return sanitize_response(xml_retorno)
