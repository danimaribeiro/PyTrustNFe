# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import tempfile
from OpenSSL import crypto
#import datetime
from datetime import datetime

#temp
import ssl

class Certificado(object):
    def __init__(self, pfx, password):
        self.pfx = pfx
        self.password = password

        pfx = crypto.load_pkcs12(pfx, password).get_certificate()
        cert_date =  int(str(pfx.get_notAfter(),'UTF-8').strip('Z'))
        now  = datetime.now()
        date = int(now.strftime("%Y%m%d%H%M%S"))
        if cert_date < date:
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
        print("ERROR: Falha ao ler certiticado. Verifique a senha")
        exit()
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
