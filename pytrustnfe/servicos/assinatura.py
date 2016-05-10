# coding=utf-8
'''
Created on Jun 14, 2015

@author: danimar
'''

from signxml import xmldsig
from signxml import methods
from lxml import etree
from OpenSSL import crypto


def extract_cert_and_key_from_pfx(pfx, password):
    pfx = crypto.load_pkcs12(pfx, password)
    # PEM formatted private key
    key = crypto.dump_privatekey(crypto.FILETYPE_PEM,
                                 pfx.get_privatekey())
    # PEM formatted certificate
    cert = crypto.dump_certificate(crypto.FILETYPE_PEM,
                                   pfx.get_certificate())
    return cert, key


def recursively_empty(e):
    if e.text:
        return False
    return all((recursively_empty(c) for c in e.iterchildren()))


def assinar(xml, cert, key, reference):
    context = etree.iterwalk(xml)
    for action, elem in context:
        parent = elem.getparent()
        if recursively_empty(elem):
            parent.remove(elem)

    # element = xml.find('{' + xml.nsmap[None] + '}NFe')
    signer = xmldsig(xml, digest_algorithm=u'sha1')
    ns = {}
    ns[None] = signer.namespaces['ds']
    signer.namespaces = ns
    signed_root = signer.sign(
        key=str(key), cert=cert, reference_uri=reference,
        algorithm="rsa-sha1", method=methods.enveloped,
        c14n_algorithm='http://www.w3.org/TR/2001/REC-xml-c14n-20010315')

    xmldsig(signed_root, digest_algorithm=u'sha1').verify(x509_cert=cert)
    return etree.tostring(signed_root)
