# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import tempfile
from OpenSSL import crypto
from datetime import datetime


class Certificado(object):
    def __init__(self, pfx, password):
        self.pfx = pfx
        self.password = password
        pfx = crypto.load_pkcs12(pfx, password)

        cert = pfx.get_certificate()
        cert_date =  int(str(cert.get_notAfter(),'UTF-8').strip('Z'))
        sha1_fingerprint = cert.digest("sha1")
        now  = datetime.now()
        date = int(now.strftime("%Y%m%d%H%M%S"))
        '''
        Exceto certificado de testes
        '''
        if cert_date < date or str(sha1_fingerprint,'UTF-8') ==  "DE:08:15:1E:DA:12:B3:5F:76:BF:5D:4E:56:C1:14:12:8A:85:B6:47":
            print("WARNING: Certificado expirado")

    def save_pfx(self):
        pfx_temp = tempfile.mkstemp()[1]
        arq_temp = open(pfx_temp, "wb")
        arq_temp.write(self.pfx)
        arq_temp.close()
        return pfx_temp


def extract_cert_and_key_from_pfx(pfx, password):
    try:
        pfx = crypto.load_pkcs12(pfx, password)
    except:
        print("WARING: Falha ao ler certiticado. Verifique a senha")
    # PEM formatted private key
    key = crypto.dump_privatekey(crypto.FILETYPE_PEM, pfx.get_privatekey())
    # PEM formatted certificate
    cert = crypto.dump_certificate(crypto.FILETYPE_PEM, pfx.get_certificate())
    return cert.decode(), key.decode()


def save_cert_key(cert, key):
    cert_temp = tempfile.mkstemp()[1]
    key_temp = tempfile.mkstemp()[1]

    arq_temp = open(cert_temp, "w")
    arq_temp.write(cert)
    arq_temp.close()

    arq_temp = open(key_temp, "w")
    arq_temp.write(key)
    arq_temp.close()

    return cert_temp, key_temp
