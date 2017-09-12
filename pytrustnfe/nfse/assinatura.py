# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from lxml import etree
import xmlsec
import os.path

consts = xmlsec.constants

NAMESPACE_SIG = 'http://www.w3.org/2000/09/xmldsig#'


class Assinatura(object):

    def __init__(self, cert_pem, private_key, password):
        self.cert_pem = cert_pem
        self.private_key = private_key
        self.password = password

    def _checar_certificado(self):
        if not os.path.isfile(self.private_key):
            raise Exception('Caminho do certificado não existe.')

    def assina_xml(self, xml, reference):
        self._checar_certificado()
        template = etree.fromstring(xml)

        key = xmlsec.Key.from_file(
            self.private_key, format=xmlsec.constants.KeyDataFormatPem,
            password=self.password)

        signature_node = xmlsec.template.create(
            template, c14n_method=consts.TransformInclC14N,
            sign_method=consts.TransformRsaSha1)
        template.append(signature_node)
        ref = xmlsec.template.add_reference(
            signature_node, consts.TransformSha1, uri='')

        xmlsec.template.add_transform(ref, consts.TransformEnveloped)
        xmlsec.template.add_transform(ref, consts.TransformInclC14N)

        ki = xmlsec.template.ensure_key_info(signature_node)
        xmlsec.template.add_x509_data(ki)

        ctx = xmlsec.SignatureContext()
        ctx.key = key

        ctx.key.load_cert_from_file(
            self.cert_pem, consts.KeyDataFormatPem)

        ctx.sign(signature_node)
        return etree.tostring(template, encoding=str)
