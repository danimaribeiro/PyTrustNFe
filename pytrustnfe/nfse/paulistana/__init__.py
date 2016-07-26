

def _send(method, data):
    pass
    # TODO Assinar xml e retornar objeto de resposta


def envio_rps(data=None):
    return _send('envio_rps', data)

def envio_lote_rps(data=None):
    return _send('envio_lote_rps', data)

def teste_envio_lote_rps(data=None):
    return _send('teste_envio_lote_rps', data)

def cancelamento_nfe(data=None):
    return _send('cancelamento_n_fe', data)

def consulta_nfe(data=None):
    return _send('consulta_n_fe', data)

def consulta_nfe_recebidas(data=None):
    return _send('consulta_n_fe_recebidas', data)

def consulta_nfe_emitidas(data=None):
    return _send('consulta_n_fe_emitidas', data)

def consulta_lote(data=None):
    return _send('consulta_lote', data)

def consulta_informacoes_lote(data=None):
    return _send('consulta_informacoes_lote', data)

def consulta_cnpj(data=None):
    return _send('consulta_cnpj', data)
    
