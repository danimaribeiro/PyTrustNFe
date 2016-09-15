# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import signxml
from lxml import etree
from pytrustnfe.certificado import extract_cert_and_key_from_pfx
from signxml import XMLSigner
from StringIO import StringIO


class Assinatura(object):

    def __init__(self, arquivo, senha):
        self.arquivo = arquivo
        self.senha = senha

    def assina_xml(self, xml, reference):
        cert, key = extract_cert_and_key_from_pfx(self.arquivo, self.senha)

        parser = etree.XMLParser(remove_blank_text=True, remove_comments=True)
        root = etree.parse(StringIO(xml), parser=parser)
        for element in root.iter("*"):
            if element.text is not None and not element.text.strip():
                element.text = None

        signer = XMLSigner(
            method=signxml.methods.enveloped, signature_algorithm="rsa-sha1",
            digest_algorithm='sha1',
            c14n_algorithm='http://www.w3.org/TR/2001/REC-xml-c14n-20010315')

        signed_root = signer.sign(
            root, key=key, cert=cert, reference_only=True,
            reference_uri=('#%s' % reference))
        signed_root[2].append(signed_root[3])
        return etree.tostring(signed_root)
