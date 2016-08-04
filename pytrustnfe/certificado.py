# coding=utf-8
'''
Created on Jun 16, 2015

@author: danimar
'''
from uuid import uuid4
import os.path
from OpenSSL import crypto


class Certificado(object):
    def __init__(self, pfx, password):
        self.pfx = pfx
        self.password = password


def converte_pfx_pem(pfx_stream, senha):
    try:
        certificado = crypto.load_pkcs12(pfx_stream, senha)

        cert = crypto.dump_certificate(crypto.FILETYPE_PEM,
                                       certificado.get_certificate())
        key = crypto.dump_privatekey(crypto.FILETYPE_PEM,
                                     certificado.get_privatekey())
    except Exception as e:
        if len(e.message) == 1 and len(e.message[0]) == 3 and \
                e.message[0][2] == 'mac verify failure':
            raise Exception('Senha inválida')
        raise
    return cert, key


def save_cert_key(cert, key):
    cert_temp = '/tmp/' + uuid4().hex
    key_temp = '/tmp/' + uuid4().hex

    arq_temp = open(cert_temp, 'w')
    arq_temp.write(cert)
    arq_temp.close()

    arq_temp = open(key_temp, 'w')
    arq_temp.write(key)
    arq_temp.close()

    return cert_temp, key_temp
