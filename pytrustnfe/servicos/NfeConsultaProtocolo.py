#coding=utf-8
'''
Created on 21/06/2015

@author: danimar
'''
from pytrustnfe.servicos.Comunicacao import Comunicacao
from pytrustnfe.xml import DynamicXml


class NfeConsultaProtocolo(Comunicacao):
    
    def consultar_protocolo(self, recibo):
        xml = self._validar_xml(recibo)

        self.metodo = 'NfeConsulta2'
        self.tag_retorno = 'retConsSitNFe'
        self.web_service = 'ws/NfeConsulta/NfeConsulta2.asmx'
        self.url = 'nfe.sefazrs.rs.gov.br'

        return self._executar_consulta(xml)