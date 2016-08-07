# coding=utf-8
'''
Created on 21/06/2015

@author: danimar
'''
import os
from lxml import etree
from suds.sax.element import Element
from suds.sax.text import Raw
from suds.sax.parser import Parser
from pytrustnfe.servicos.comunicacao import Comunicacao
from pytrustnfe import utils
from pytrustnfe.xml import render_xml
from pytrustnfe.servicos.assinatura import assinar


class NfeAutorizacao(Comunicacao):

    def __init__(self, cert, key):
        Comunicacao.__init__(self, cert, key)

    def autorizar_nfe(self, nfe, id):        
        self.url = 'nfe-homologacao.sefazrs.rs.gov.br'
        self.web_service = '/ws/NfeAutorizacao/NFeAutorizacao.asmx'
        self.metodo = 'nfeAutorizacaoLote'
        
        self._validar_nfe(nfe)
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'xml')        
        xml = render_xml(path, 'nfeEnv.xml', **nfe)

        #xmlElem = etree.fromstring(xml) TODO Assinar
        #xml_signed = assinar(xmlElem, self.cert, self.key, '#%s' % id)
        print xml
        xml_response, obj = self._executar_consulta(xml)
        
        return {
            'sent_xml': xml,
            'received_xml': xml_response,
            'object': obj.Body.nfeAutorizacaoLoteResult
        }
