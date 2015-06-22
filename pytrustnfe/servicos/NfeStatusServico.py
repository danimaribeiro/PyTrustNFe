#coding=utf-8
'''
Created on 21/06/2015

@author: danimar
'''
from pytrustnfe.servicos.Comunicacao import Comunicacao
from pytrustnfe.xml import DynamicXml


class NfeStatusServico(Comunicacao):
    
    def status(self, consulta):
        xml = None
        if isinstance(consulta, DynamicXml):
            xml = consulta.render()
        if isinstance(consulta, basestring):
            xml = consulta
        assert xml is not None, "Objeto consulta deve ser do tipo DynamicXml ou string"
                
        
        return self._executar_consulta(xml)