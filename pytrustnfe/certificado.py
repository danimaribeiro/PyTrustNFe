# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from uuid import uuid4
from OpenSSL import crypto


class Certificado(object):
    def __init__(self, pfx, password):
        self.pfx = pfx
        self.password = password

    def save_pfx(self):
        pfx_temp = '/tmp/' + uuid4().hex
        arq_temp = open(pfx_temp, 'w')
        arq_temp.write(self.pfx)
        arq_temp.close()
        return pfx_temp


def extract_cert_and_key_from_pfx(pfx, password):
    pfx = crypto.load_pkcs12(pfx, password)
    # PEM formatted private key
    key = crypto.dump_privatekey(crypto.FILETYPE_PEM,
                                 pfx.get_privatekey())
    # PEM formatted certificate
    cert = crypto.dump_certificate(crypto.FILETYPE_PEM,
                                   pfx.get_certificate())
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
