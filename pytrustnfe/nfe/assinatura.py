# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import signxml
from lxml import etree
from pytrustnfe.certificado import extract_cert_and_key_from_pfx
from signxml import XMLSigner


class Assinatura(object):

    def __init__(self, arquivo, senha):
        self.arquivo = arquivo
        self.senha = senha

    def assina_xml(self, xml_element, reference):
        cert, key = extract_cert_and_key_from_pfx(self.arquivo, self.senha)

        for element in xml_element.iter("*"):
            if element.text is not None and not element.text.strip():
                element.text = None

        signer = XMLSigner(
            method=signxml.methods.enveloped, signature_algorithm="rsa-sha1",
            digest_algorithm='sha1',
            c14n_algorithm='http://www.w3.org/TR/2001/REC-xml-c14n-20010315')

        ns = {}
        ns[None] = signer.namespaces['ds']
        signer.namespaces = ns

        signed_root = signer.sign(
            xml_element, key=key, cert=cert,
            reference_uri=('#%s' % reference))
        element_signed = signed_root.find(".//*[@Id='%s']" % reference)
        signature = signed_root.find(
            ".//{http://www.w3.org/2000/09/xmldsig#}Signature")
        if element_signed and signature:
            parent = element_signed.getparent()
            parent.append(signature)
        return etree.tostring(signed_root)
