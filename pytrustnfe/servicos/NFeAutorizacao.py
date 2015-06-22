#coding=utf-8
'''
Created on 21/06/2015

@author: danimar
'''
from pytrustnfe.servicos.Comunicacao import Comunicacao
from pytrustnfe.xml import DynamicXml


class NfeAutorizacao(Comunicacao):
    
    def autorizar_nfe(self, nfe, sincrono=True):
        xml = None
        if isinstance(nfe, DynamicXml):
            xml = nfe.render()
        if isinstance(nfe, basestring):
            xml = nfe
        assert xml is not None, "Objeto nfe deve ser do tipo DynamicXml ou string"
                
        
        return self._executar_consulta(xml)