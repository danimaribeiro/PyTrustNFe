#coding=utf-8
'''
Created on 21/06/2015

@author: danimar
'''
from pytrustnfe.servicos.Comunicacao import Comunicacao
from pytrustnfe.xml import DynamicXml


class NfeRetAutorizacao(Comunicacao):
    
    def consulta_autorizacao(self, recibo):
        xml = self._validar_xml(recibo)
        
        self.metodo = 'NFeRetAutorizacao'
        self.tag_retorno = 'retConsReciNFe'
        self.web_service = 'ws/NfeRetAutorizacao/NFeRetAutorizacao.asmx'
        self.url = 'nfe.sefazrs.rs.gov.br'
        
        return self._executar_consulta(xml)