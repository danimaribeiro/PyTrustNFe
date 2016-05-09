# coding=utf-8
'''
Created on 21/06/2015

@author: danimar
'''
from pytrustnfe.servicos.comunicacao import Comunicacao

class NfeStatusServico(Comunicacao):

    def status(self, consulta):
        xml = self._validar_xml(recibo)

        self.metodo = 'NfeStatusServico2'
        self.tag_retorno = 'retConsStatServ'
        self.web_service = 'ws/NfeStatusServico/NfeStatusServico2.asmx'
        self.url = 'nfe.sefazrs.rs.gov.br'

        return self._executar_consulta(xml)
