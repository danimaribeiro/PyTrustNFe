import os
import logging
import suds
from lxml import etree
from pytrustnfe.xml import render_xml, valida_schema
from pytrustnfe.client import get_authenticated_client
from pytrustnfe.certificado import converte_pfx_pem, save_cert_key


def _send(certificado, method, **kwargs):
    # A little hack to test
    path = os.path.join(os.path.dirname(__file__), 'templates')
    if method == 'teste_envio_lote_rps':
        xml = render_xml(path, 'envio_lote_rps.xml', **kwargs)
    else:
        xml = render_xml(path, '%s.xml' % method, **kwargs)

    base_url = 'https://nfe.prefeitura.sp.gov.br/ws/lotenfe.asmx?wsdl'

    cert, key = converte_pfx_pem(certificado.pfx, certificado.password)
    cert, key = save_cert_key(cert, key)eh
    client = get_authenticated_client(base_url, cert, key)

    try:
        response = getattr(client.service, method)(1, xml)
    except suds.WebFault, e:
        response = e.fault.faultstring
    return response


def envio_rps(certificado, **kwargs):
    return _send(certificado, 'envio_rps', **kwargs)

def envio_lote_rps(certificado, **kwargs):
    return _send(certificado, 'envio_lote_rps', **kwargs)

def teste_envio_lote_rps(certificado, **kwargs):
    return _send(certificado, 'TesteEnvioLoteRPS', **kwargs)

def cancelamento_nfe(certificado, **kwargs):
    return _send(certificado, 'cancelamento_n_fe', **kwargs)

def consulta_nfe(certificado, **kwargs):
    return _send('consulta_n_fe', **kwargs)

def consulta_nfe_recebidas(certificado, **kwargs):
    return _send('consulta_n_fe_recebidas', **kwargs)

def consulta_nfe_emitidas(data=None):
    return _send('consulta_n_fe_emitidas', data)

def consulta_lote(data=None):
    return _send('consulta_lote', data)

def consulta_informacoes_lote(data=None):
    return _send('consulta_informacoes_lote', data)

def consulta_cnpj(data=None):
    return _send('consulta_cnpj', data)
