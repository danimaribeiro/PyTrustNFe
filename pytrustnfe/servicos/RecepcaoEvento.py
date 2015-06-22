#coding=utf-8
'''
Created on 21/06/2015

@author: danimar
'''
from pytrustnfe.servicos.Comunicacao import Comunicacao
from pytrustnfe.xml import DynamicXml


class RecepcaoEvento(Comunicacao):
    
    def registrar_evento(self, evento):
        xml = None
        if isinstance(evento, DynamicXml):
            xml = evento.render()
        if isinstance(evento, basestring):
            xml = evento
        assert xml is not None, "Objeto recibo deve ser do tipo DynamicXml ou string"
                
        
        return self._executar_consulta(xml)