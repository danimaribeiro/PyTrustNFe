import os
from pytrustnfe.xml import render_xml
from pytrustnfe.client import get_authenticated_client
from pytrustnfe.certificado import converte_pfx_pem


def _send(certificado, method, **kwargs):
    # A little hack to test
    path = os.path.join(os.path.dirname(__file__), 'templates')
    if method == 'teste_envio_lote_rps':
        xml = render_xml(path, 'envio_lote_rps.xml', **kwargs)
    else:
        xml = render_xml(path, '%s.xml' % method, **kwargs)

    base_url = 'https://nfe.prefeitura.sp.gov.br/ws/lotenfe.asmx'

    import ipdb; ipdb.set_trace()
    key, cert = converte_pfx_pem(certificado.pfx, certificado.password)
    client = get_authenticated_client(base_url, key, cert)

    response = client.teste_envio_lote_rps(xml)

    return response


def envio_rps(certificado, **kwargs):
    return _send(certificado, 'envio_rps', **kwargs)

def envio_lote_rps(certificado, **kwargs):
    return _send(certificado, 'envio_lote_rps', **kwargs)

def teste_envio_lote_rps(certificado, **kwargs):
    return _send(certificado, 'teste_envio_lote_rps', **kwargs)

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
