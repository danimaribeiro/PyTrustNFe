# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import tempfile
from OpenSSL import crypto
import os

class Certificado(object):
    def __init__(self, pfx, password):
        self.pfx = pfx
        self.password = password

    def save_pfx(self):
        pfx_temp = tempfile.mkstemp()[1]
        arq_temp = open(pfx_temp, "wb")
        arq_temp.write(self.pfx)
        arq_temp.close()
        return pfx_temp


def extract_cert_and_key_from_pfx(pfx, password):
    pfx = crypto.load_pkcs12(pfx, password)
    # PEM formatted private key
    key = crypto.dump_privatekey(crypto.FILETYPE_PEM, pfx.get_privatekey())
    # PEM formatted certificate
    cert = crypto.dump_certificate(crypto.FILETYPE_PEM, pfx.get_certificate())
    return cert.decode(), key.decode()


def save_cert_key(cert, key):
    fd_cert, cert_temp = tempfile.mkstemp()
    fd_key, key_temp = tempfile.mkstemp()

    os.write(fd_cert, cert.encode())
    os.close(fd_cert)

    os.write(fd_key, key.encode())
    os.close(fd_key)

    return cert_temp, key_temp

