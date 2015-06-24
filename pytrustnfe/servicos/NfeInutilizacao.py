#coding=utf-8
'''
Created on 21/06/2015

@author: danimar
'''
from pytrustnfe.servicos.Comunicacao import Comunicacao
from pytrustnfe.xml import DynamicXml


class NfeInutilizacao(Comunicacao):
    
    def inutilizar(self, inutilizacao):
        xml = self._validar_xml(recibo)
        
        self.metodo = 'nfeinutilizacao2'
        self.tag_retorno = 'retInutNFe'
        self.web_service = 'ws/nfeinutilizacao/nfeinutilizacao2.asmx'
        self.url = 'nfe.sefazrs.rs.gov.br'
        
        return self._executar_consulta(xml)