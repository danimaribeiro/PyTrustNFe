from ..Servidores import SIGLA_ESTADO
from pytrustnfe.xml import sanitize_response


def nfeInutilizacaoCE(session, xml_send, ambiente):
    soap = '<Envelope xmlns="http://www.w3.org/2003/05/soap-envelope"><Body>\
<nfeDadosMsg xmlns="http://www.portalfiscal.inf.br/nfe/wsdl/NFeInutilizacao4"\
>' + xml_send + '</nfeDadosMsg></Body></Envelope>'
    headers = {
        'SOAPAction': "",
        'Content-Type': 'application/soap+xml; charset="utf-8"'
    }
    if ambiente == 1:
        response = session.post(
            'https://nfe.sefaz.ce.gov.br/nfe4/services/NFeInutilizacao4',
            data=soap, headers=headers)
    else:
        response = session.post(
            'https://nfeh.sefaz.ce.gov.br/nfe4/services/NFeInutilizacao4',
            data=soap, headers=headers)
    response, obj = sanitize_response(response.text)
    return {
        'sent_xml': xml_send,
        'received_xml': response,
        'object': obj.Body.getchildren()[0]
    }


methods = {
    'NfeInutilizacaoCE': nfeInutilizacaoCE
}


def has_patch(cod_estado, metodo):
    uf = SIGLA_ESTADO[cod_estado]
    method = metodo+uf
    if method in methods:
        return methods[method]
    return None
