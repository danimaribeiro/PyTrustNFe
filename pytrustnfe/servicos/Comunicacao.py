#coding=utf-8
'''
Created on Jun 14, 2015

@author: danimar
'''

from lxml import objectify
from uuid import uuid4
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import tostring
from pytrustnfe.HttpClient import HttpClient
from pytrustnfe.Certificado import converte_pfx_pem

from xml.dom.minidom import parseString

from pytrustnfe.Strings import CONSULTA_CADASTRO_COMPLETA

common_namespaces = { 'soap': 'http://www.w3.org/2003/05/soap-envelope' }

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
        return '<?xml version="1.0" encoding="utf-8"?>'\
        '<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope">'\
        '<soap:Header>'\
        '<nfeCabecMsg xmlns="http://www.portalfiscal.inf.br/nfe/wsdl/' + self.metodo + '">'\
        '<cUF>42</cUF><versaoDados>2.00</versaoDados>'\
        '</nfeCabecMsg>'\
        '</soap:Header>'\
        '<soap:Body>'\
        '<nfeDadosMsg xmlns="http://www.portalfiscal.inf.br/nfe/wsdl/' + self.metodo + '">'\
        + body + '</nfeDadosMsg>'\
        '</soap:Body>'\
        '</soap:Envelope>'
    
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
    
    def _executar_consulta(self, xmlEnviar):
        self._validar_dados()
        chave, certificado = self._preparar_temp_pem()
        
        client = HttpClient(self.url, chave, certificado)
        soap_xml = self._soap_xml(xmlEnviar)
        xml_retorno = client.post_xml(self.web_service, soap_xml)

        
        dom = parseString(xml_retorno)
        nodes = dom.getElementsByTagNameNS(common_namespaces['soap'],'Fault')
        if len(nodes) > 0:            
            return nodes[0].toxml(), None
        
        nodes = dom.getElementsByTagName(self.tag_retorno)       
        if len(nodes) > 0:
            obj = objectify.fromstring(nodes[0].toxml())
            return nodes[0].toxml(), obj
        
       
        
        
        