#coding=utf-8
'''
Created on 21/06/2015

@author: danimar
'''
from pytrustnfe.servicos.Comunicacao import Comunicacao
from pytrustnfe.xml import DynamicXml


class NfeRetAutorizacao(Comunicacao):
    
    def consulta_autorizacao(self, recibo):
        xml = None
        if isinstance(recibo, DynamicXml):
            xml = recibo.render()
        if isinstance(recibo, basestring):
            xml = recibo
        assert xml is not None, "Objeto recibo deve ser do tipo DynamicXml ou string"
                
        
        return self._executar_consulta(xml)