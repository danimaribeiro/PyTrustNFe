# coding=utf-8
'''
Created on Jun 14, 2015

@author: danimar
'''

import xmlsec
import libxml2
import os.path
from signxml import xmldsig
from signxml import methods
from lxml import etree

NAMESPACE_SIG = 'http://www.w3.org/2000/09/xmldsig#'


def recursively_empty(e):
    if e.text:
        return False
    return all((recursively_empty(c) for c in e.iterchildren()))


def assinar(xml, cert, key, reference, pfx, senha):
    context = etree.iterwalk(xml)
    for action, elem in context:
        parent = elem.getparent()
        if recursively_empty(elem):
            parent.remove(elem)

    element = xml.find('{' + xml.nsmap[None] + '}NFe')
    not_signed = etree.tostring(element)
    not_signed = "<!DOCTYPE NFe [<!ATTLIST infNFe Id ID #IMPLIED>]>" + \
        not_signed

    signer = xmldsig(element, digest_algorithm=u'sha1')
    ns = {}
    ns[None] = signer.namespaces['ds']
    signer.namespaces = ns
    signed_root = signer.sign(
        key=str(key), cert=cert, reference_uri=reference,
        algorithm="rsa-sha1", method=methods.enveloped,
        c14n_algorithm='http://www.w3.org/TR/2001/REC-xml-c14n-20010315')

    xmldsig(signed_root, digest_algorithm=u'sha1').verify(x509_cert=cert)
    # signature = Assinatura(pfx, senha)
    # xmlsec = signature.assina_xml(not_signed, reference)
    # xmlsec = xmlsec.replace("""<!DOCTYPE NFe [
# <!ATTLIST infNFe Id ID #IMPLIED>
# ]>\n""", "")
    return etree.tostring(signed_root)
    # , xmlsec


class Assinatura(object):

    def __init__(self, arquivo, senha):
        self.arquivo = arquivo
        self.senha = senha

    def _checar_certificado(self):
        if not os.path.isfile(self.arquivo):
            raise Exception('Caminho do certificado não existe.')

    def _inicializar_cripto(self):
        libxml2.initParser()
        libxml2.substituteEntitiesDefault(1)

        xmlsec.init()
        xmlsec.cryptoAppInit(None)
        xmlsec.cryptoInit()

    def _finalizar_cripto(self):
        xmlsec.cryptoShutdown()
        xmlsec.cryptoAppShutdown()
        xmlsec.shutdown()

        libxml2.cleanupParser()

    def assina_xml(self, xml, reference):
        self._checar_certificado()
        self._inicializar_cripto()
        try:
            doc_xml = libxml2.parseMemory(xml.encode('utf-8'),
                                          len(xml.encode('utf-8')))
            import ipdb; ipdb.set_trace()
            signNode = xmlsec.TmplSignature(doc_xml,
                                            xmlsec.transformInclC14NId(),
                                            xmlsec.transformRsaSha1Id(), None)

            doc_xml.getRootElement().addChild(signNode)
            refNode = signNode.addReference(
                xmlsec.transformSha1Id(),
                None, reference, None)

            refNode.addTransform(xmlsec.transformEnvelopedId())
            refNode.addTransform(xmlsec.transformInclC14NId())
            keyInfoNode = signNode.ensureKeyInfo()
            keyInfoNode.addX509Data()

            dsig_ctx = xmlsec.DSigCtx()
            chave = xmlsec.cryptoAppKeyLoad(
                filename=str(self.arquivo),
                format=xmlsec.KeyDataFormatPkcs12,
                pwd=str(self.senha), pwdCallback=None, pwdCallbackCtx=None)

            dsig_ctx.signKey = chave
            dsig_ctx.sign(signNode)

            status = dsig_ctx.status
            dsig_ctx.destroy()

            if status != xmlsec.DSigStatusSucceeded:
                raise RuntimeError(
                    'Erro ao realizar a assinatura do arquivo; status: "' +
                    str(status) + '"')

            xpath = doc_xml.xpathNewContext()
            xpath.xpathRegisterNs('sig', NAMESPACE_SIG)
            certs = xpath.xpathEval('//sig:X509Data/sig:X509Certificate')
            for i in range(len(certs)-1):
                certs[i].unlinkNode()
                certs[i].freeNode()

            xml = doc_xml.serialize()
            return xml
        finally:
            doc_xml.freeDoc()
            self._finalizar_cripto()
