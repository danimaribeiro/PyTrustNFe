#coding=utf-8
'''
Created on 21/06/2015

@author: danimar
'''
from pytrustnfe.servicos.Comunicacao import Comunicacao
from pytrustnfe.xml import DynamicXml
from pytrustnfe import utils


class NfeAutorizacao(Comunicacao):
    
    def __init__(self, certificado, senha):
        Comunicacao.__init__(self, certificado, senha)
    
    def autorizar_nfe(self, nfe):
        xml = self._validar_xml(nfe)
                
        self.metodo = 'NFeAutorizacao'
        self.tag_retorno = 'retEnviNFe'
        self.web_service = 'ws/NfeAutorizacao/NFeAutorizacao.asmx'
        self.url = 'nfe.sefazrs.rs.gov.br'
        
        return self._executar_consulta(xml)
    
    def autorizar_nfe_e_recibo(self, nfe):
        xml = self._validar_xml(nfe)
                
        self.metodo = 'NFeAutorizacao'
        self.tag_retorno = 'retEnviNFe'
        self.web_service = 'ws/NfeAutorizacao/NFeAutorizacao.asmx'
        self.url = 'nfe.sefazrs.rs.gov.br'
        
        xml_recibo, recibo = self._executar_consulta(xml)
        
        consulta_recibo = utils.gerar_consulta_recibo(recibo)
        xml = self._validar_xml(nfe)
        
        self.metodo = 'NFeRetAutorizacao'
        self.tag_retorno = 'retConsReciNFe'
        self.web_service = 'ws/NfeRetAutorizacao/NFeRetAutorizacao.asmx'
        self.url = 'nfe.sefazrs.rs.gov.br'
        
        return self._executar_consulta(xml)
        
        
        