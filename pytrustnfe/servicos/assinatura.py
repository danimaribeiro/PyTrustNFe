'''
Created on Jun 14, 2015

@author: danimar
'''
import xmlsec, libxml2

NAMESPACE_SIG = 'http://www.w3.org/2000/09/xmldsig#'

class Assinatura(object):

    def __init__(self, arquivo, senha):
        self.arquivo = arquivo
        self.senha = senha
        
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
        
    
    def assina_xml(self, xml):
        self._inicializar_cripto()
        try:
            doc_xml = libxml2.parseMemory(xml.encode('utf-8'), len(xml.encode('utf-8')))
            
            signNode = xmlsec.TmplSignature(doc_xml, xmlsec.transformInclC14NId(),
                                        xmlsec.transformRsaSha1Id(), None)
            
            
            doc_xml.getRootElement().addChild(signNode)    
            refNode = signNode.addReference(xmlsec.transformSha1Id(),
                                            None, '#NFe43150602261542000143550010000000761792265342', None)
            
            refNode.addTransform(xmlsec.transformEnvelopedId())
            refNode.addTransform(xmlsec.transformInclC14NId())
            keyInfoNode = signNode.ensureKeyInfo()
            keyInfoNode.addX509Data()  
                   
            dsig_ctx = xmlsec.DSigCtx()   
            chave = xmlsec.cryptoAppKeyLoad(filename=str(self.arquivo), format=xmlsec.KeyDataFormatPkcs12, pwd=str(self.senha), pwdCallback=None, pwdCallbackCtx=None)
                
            dsig_ctx.signKey = chave
            dsig_ctx.sign(signNode)
            
            status = dsig_ctx.status
            dsig_ctx.destroy()

            if status != xmlsec.DSigStatusSucceeded:
                raise RuntimeError('Erro ao realizar a assinatura do arquivo; status: "' + str(status) + '"')

            xpath = doc_xml.xpathNewContext()
            xpath.xpathRegisterNs('sig', NAMESPACE_SIG)
            certificados = xpath.xpathEval('//sig:X509Data/sig:X509Certificate')
            for i in range(len(certificados)-1):
                certificados[i].unlinkNode()
                certificados[i].freeNode()

            xml = doc_xml.serialize()           
            open('/home/danimar/Desktop/assinado.xml', 'wb').write(xml)

            return xml
        finally:
            doc_xml.freeDoc()
            self._finalizar_cripto()
