

def nfeInutilizacaoCE(session, xml_send):
    soap = '<Envelope xmlns="http://www.w3.org/2003/05/soap-envelope"><Body>\
<nfeDadosMsg xmlns="http://www.portalfiscal.inf.br/nfe/wsdl/NFeInutilizacao4"\
>' + xml_send + '</nfeDadosMsg></Body></Envelope>'
    headers = {
        'SOAPAction': "",
        'Content-Type': 'application/soap+xml; charset="utf-8"'
    }
    response = session.post(
        'https://nfeh.sefaz.ce.gov.br/nfe4/services/NFeInutilizacao4',
        data=soap, headers=headers)
    return response
