#coding=utf-8
'''
Created on 21/06/2015

@author: danimar
'''
from pytrustnfe.servicos.Comunicacao import Comunicacao
from pytrustnfe.xml import DynamicXml


class NfeDistribuicaoDFe(Comunicacao):
    
    def distribuicao(self, dfe):
        xml = None
        if isinstance(dfe, DynamicXml):
            xml = dfe.render()
        if isinstance(dfe, basestring):
            xml = dfe
        assert xml is not None, "Objeto recibo deve ser do tipo DynamicXml ou string"
                
        
        return self._executar_consulta(xml)