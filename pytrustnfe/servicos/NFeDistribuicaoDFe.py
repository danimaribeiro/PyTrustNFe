#coding=utf-8
'''
Created on 21/06/2015

@author: danimar
'''
from pytrustnfe.servicos.Comunicacao import Comunicacao
from pytrustnfe.xml import DynamicXml


class NfeDistribuicaoDFe(Comunicacao):
    
    def distribuicao(self, dfe):
        xml = self._validar_xml(recibo)

        self.metodo = 'NFeDistribuicaoDFe'
        self.tag_retorno = 'retDistDFeInt'
        self.web_service = 'NFeDistribuicaoDFe/NFeDistribuicaoDFe.asmx'
        self.url = 'www1.nfe.fazenda.gov.br'

        return self._executar_consulta(xml)