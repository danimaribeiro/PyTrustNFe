# coding=utf-8
'''
Created on Jun 14, 2015

@author: danimar
'''

from lxml import objectify
from uuid import uuid4
from pytrustnfe.xml.DynamicXml import DynamicXml
from pytrustnfe.HttpClient import HttpClient
from pytrustnfe.Certificado import converte_pfx_pem

from xml.dom.minidom import parseString

common_namespaces = {'soap': 'http://www.w3.org/2003/05/soap-envelope'}

soap_body_path = './soap:Envelope/soap:Body'
soap_fault_path = './soap:Envelope/soap:Body/soap:Fault'


class Comunicacao(object):
    url = ''
    web_service = ''
    metodo = ''
    tag_retorno = ''

    def __init__(self, certificado, senha):
        self.certificado = certificado
        self.senha = senha

    def _soap_xml(self, body):
        xml = '''<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope">
<soap:Header>
<nfeCabecMsg xmlns="http://www.portalfiscal.inf.br/nfe/wsdl/'''
        xml += self.metodo
        xml += '''"><cUF>42</cUF><versaoDados>2.00</versaoDados>
</nfeCabecMsg>
</soap:Header>
<soap:Body>
<nfeDadosMsg xmlns="http://www.portalfiscal.inf.br/nfe/wsdl/'''
        xml += self.metodo + '">' + body
        xml += '</nfeDadosMsg></soap:Body></soap:Envelope>'

    def _preparar_temp_pem(self):
        chave_temp = '/tmp/' + uuid4().hex
        certificado_temp = '/tmp/' + uuid4().hex

        chave, certificado = converte_pfx_pem(self.certificado, self.senha)
        arq_temp = open(chave_temp, 'w')
        arq_temp.write(chave)
        arq_temp.close()

        arq_temp = open(certificado_temp, 'w')
        arq_temp.write(certificado)
        arq_temp.close()

        return chave_temp, certificado_temp

    def _validar_dados(self):
        assert self.url != '', "Url servidor não configurada"
        assert self.web_service != '', "Web service não especificado"
        assert self.certificado != '', "Certificado não configurado"
        assert self.senha != '', "Senha não configurada"
        assert self.metodo != '', "Método não configurado"
        assert self.tag_retorno != '', "Tag de retorno não configurado"

    def _validar_xml(self, obj):
        xml = None
        if isinstance(obj, DynamicXml):
            xml = obj.render()
        if isinstance(obj, basestring):
            xml = obj
        assert xml is not None, "Objeto deve ser do tipo DynamicXml ou string"
        return xml

    def _executar_consulta(self, xmlEnviar):
        self._validar_dados()
        chave, certificado = self._preparar_temp_pem()

        client = HttpClient(self.url, chave, certificado)
        soap_xml = self._soap_xml(xmlEnviar)
        xml_retorno = client.post_xml(self.web_service, soap_xml)

        dom = parseString(xml_retorno)
        nodes = dom.getElementsByTagNameNS(common_namespaces['soap'], 'Fault')
        if len(nodes) > 0:
            return nodes[0].toxml(), None

        nodes = dom.getElementsByTagName(self.tag_retorno)
        if len(nodes) > 0:
            obj = objectify.fromstring(nodes[0].toxml())
            return nodes[0].toxml(), obj

        return xml_retorno, objectify.fromstring(xml_retorno)
