# coding=utf-8
'''
Created on Jun 16, 2015

@author: danimar
'''
import os.path
from OpenSSL import crypto


def converte_pfx_pem(caminho, senha):
    if not os.path.isfile(caminho):
        raise Exception('Certificado não existe')
    stream = open(caminho, 'rb').read()
    try:
        certificado = crypto.load_pkcs12(stream, senha)

        privada = crypto.dump_privatekey(crypto.FILETYPE_PEM,
                                         certificado.get_privatekey())
        certificado = crypto.dump_certificate(crypto.FILETYPE_PEM,
                                              certificado.get_certificate())
    except Exception as e:
        if len(e.message) == 1 and len(e.message[0]) == 3 and \
           e.message[0][2] == 'mac verify failure':
            raise Exception('Senha inválida')
        raise
    return privada, certificado
