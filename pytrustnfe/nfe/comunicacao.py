# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from pytrustnfe.client import HttpClient
from pytrustnfe.certificado import save_cert_key, extract_cert_and_key_from_pfx

from ..xml import sanitize_response


metodos = {
    'NfeAutorizacao': 'NFeAutorizacao4',
    'NfeRetAutorizacao': 'NFeRetAutorizacao4',
    'NfeConsultaCadastro': 'CadConsultaCadastro4',
    'NfeInutilizacao': 'NFeInutilizacao4',
    'RecepcaoEventoCancelamento': 'NFeRecepcaoEvento4',
    'RecepcaoEventoCarta': 'NFeRecepcaoEvento4',
    'NFeDistribuicaoDFe': 'NFeDistribuicaoDFe/nfeDistDFeInteresse',
    'RecepcaoEventoManifesto': 'RecepcaoEvento',
}
def _soap_xml(body, method):
    xml = '<?xml version="1.0" encoding="utf-8"?>'
    xml += '<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope">'
    xml += '<soap:Body>'
    xml += '<nfeDadosMsg xmlns="http://www.portalfiscal.inf.br/nfe/wsdl/' + metodos[method] + '">'
    xml += body
    xml += '</nfeDadosMsg></soap:Body></soap:Envelope>'
    return xml.rstrip('\n')

def _post_header(method):
    """Retorna um dicionário com os atributos para o cabeçalho da requisição HTTP"""
    if method != 'NFeDistribuicaoDFe':
        response = {
            'content-type': 'application/soap+xml; charset=utf-8;',
            'Accept': 'application/soap+xml; charset=utf-8;',
            #'SOAPAction': "",
            }
    else:
        response = {
            'Content-type': 'text/xml; charset=utf-8;',
            'SOAPAction': "http://www.portalfiscal.inf.br/nfe/wsdl/%s" % metodos[method],
            'Accept': 'application/soap+xml; charset=utf-8',
        }

    return response


def executar_consulta(certificado, url, method, xmlEnviar, send_raw=False):
    cert, key = extract_cert_and_key_from_pfx(
        certificado.pfx, certificado.password)
    cert_path, key_path = save_cert_key(cert, key)
    client = HttpClient(url, cert_path, key_path)

    xml_enviar = _soap_xml(xmlEnviar, method)

    if send_raw:
        xml = '<?xml version="1.0" encoding="utf-8"?>' + xmlEnviar.rstrip('\n')
        xml_enviar = xml
    xml_retorno = client.post_soap(xml_enviar, _post_header(method), send_raw)
    return sanitize_response(xml_retorno.encode())
