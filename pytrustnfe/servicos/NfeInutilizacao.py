#coding=utf-8
'''
Created on 21/06/2015

@author: danimar
'''
from pytrustnfe.servicos.Comunicacao import Comunicacao
from pytrustnfe.xml import DynamicXml


class NfeInutilizacao(Comunicacao):
    
    def inutilizar(self, inutilizacao):
        xml = None
        if isinstance(inutilizacao, DynamicXml):
            xml = inutilizacao.render()
        if isinstance(inutilizacao, basestring):
            xml = inutilizacao
        assert xml is not None, "Objeto inutilização deve ser do tipo DynamicXml ou string"
                
        
        return self._executar_consulta(xml)