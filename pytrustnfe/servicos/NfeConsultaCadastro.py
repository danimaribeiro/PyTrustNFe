#coding=utf-8
'''
Created on 21/06/2015

@author: danimar
'''
from pytrustnfe.servicos.Comunicacao import Comunicacao
from pytrustnfe.xml.DynamicXml import DynamicXml


class NfeConsultaCadastro(Comunicacao):
    
    def __init__(self, certificado, senha):
        super(NfeConsultaCadastro, self).__init__(certificado, senha)
        self.metodo = 'CadConsultaCadastro2'
        self.tag_retorno = 'retConsCad'
        
    
    def consultar_cadastro(self, cadastro, estado):
        xml = self._validar_xml(cadastro)
        
        self.web_service = '/ws/cadconsultacadastro/cadconsultacadastro2.asmx'
        self.url = 'cad.svrs.rs.gov.br'
        
        return self._executar_consulta(xml)