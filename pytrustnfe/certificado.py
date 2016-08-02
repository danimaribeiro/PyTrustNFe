# coding=utf-8
'''
Created on Jun 16, 2015

@author: danimar
'''
import os.path
from OpenSSL import crypto


class Certificado(object):
    def __init__(self, pfx, password):
        self.pfx = pfx
        self.password = password


def converte_pfx_pem(pfx_stream, senha):
    try:
        certificado = crypto.load_pkcs12(pfx_stream, senha)

        privada = crypto.dump_privatekey(crypto.FILETYPE_PEM,
                                         certificado.get_privatekey())
        certificado = crypto.dump_certificate(crypto.FILETYPE_PEM,
                                              certificado.get_certificate())
    except Exception as e:
        if len(e.message) == 1 and len(e.message[0]) == 3 and \
                e.message[0][2] == 'mac verify failure':
            raise Exception('Senha inválida')
        raise
    return certificado, privada
