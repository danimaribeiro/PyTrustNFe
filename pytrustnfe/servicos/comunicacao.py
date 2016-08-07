# coding=utf-8
'''
Created on Jun 14, 2015

@author: danimar
'''

import suds.client
import suds_requests
import requests
from lxml import objectify
from uuid import uuid4
from pytrustnfe.HttpClient import HttpClient
from pytrustnfe.Certificado import converte_pfx_pem

from ..xml import sanitize_response

common_namespaces = {'soap': 'http://www.w3.org/2003/05/soap-envelope'}

soap_body_path = './soap:Envelope/soap:Body'
soap_fault_path = './soap:Envelope/soap:Body/soap:Fault'


class Comunicacao(object):
    url = ''
    web_service = ''
    metodo = ''
    tag_retorno = ''

    def __init__(self, cert, key):
        self.cert = cert
        self.key = key

    def _soap_xml(self, body):
        xml = '<?xml version="1.0" encoding="utf-8"?>'
        xml += '<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope"><soap12:Header>'
        xml += '<nfeCabecMsg xmlns="http://www.portalfiscal.inf.br/nfe/wsdl/NfeAutorizacao">'
        xml += '<cUF>43</cUF><versaoDados>3.10</versaoDados></nfeCabecMsg></soap12:Header><soap12:Body>'
        xml += '<nfeDadosMsg xmlns="http://www.portalfiscal.inf.br/nfe/wsdl/NfeAutorizacao">'
        xml += body
        xml += '</nfeDadosMsg></soap12:Body></soap12:Envelope>'
        return xml.rstrip('\n')

    def _preparar_temp_pem(self):
        cert_path = '/tmp/' + uuid4().hex
        key_path = '/tmp/' + uuid4().hex
        
        arq_temp = open(cert_path, 'w')
        arq_temp.write(self.cert)
        arq_temp.close()

        arq_temp = open(key_path, 'w')
        arq_temp.write(self.key)
        arq_temp.close()

        return cert_path, key_path

    def _validar_dados(self):
        assert self.url != '', "Url servidor não configurada"
        assert self.web_service != '', "Web service não especificado"
        assert self.metodo != '', "Método não configurado"
       

    def _validar_nfe(self, obj):
        if not isinstance(obj, dict):
            raise u"Objeto deve ser um dicionário de valores"

    def _executar_consulta(self, xmlEnviar):
        self._validar_dados()
        cert_path, key_path = self._preparar_temp_pem()

        client = HttpClient(self.url, cert_path, key_path)
        soap_xml = self._soap_xml(xmlEnviar)
        xml_retorno = client.post_xml(self.web_service, soap_xml)
        
        return sanitize_response(xml_retorno)
