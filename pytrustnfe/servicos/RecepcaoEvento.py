#coding=utf-8
'''
Created on 21/06/2015

@author: danimar
'''
from pytrustnfe.servicos.Comunicacao import Comunicacao


class RecepcaoEvento(Comunicacao):

    def registrar_evento(self, evento):
        xml = self._validar_xml(recibo)

        self.metodo = 'RecepcaoEvento'
        self.tag_retorno = 'retEnvEvento'
        self.web_service = 'ws/recepcaoevento/recepcaoevento.asmx'
        self.url = 'nfe.sefazrs.rs.gov.br'

        return self._executar_consulta(xml)
