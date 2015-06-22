#coding=utf-8
'''
Created on 21/06/2015

@author: danimar
'''
from pytrustnfe.servicos.Comunicacao import Comunicacao
from pytrustnfe.xml import DynamicXml


class NfeConsultaCadastro(Comunicacao):
    
    def consultar_cadastro(self, cadastro):
        xml = None
        if isinstance(cadastro, DynamicXml):
            xml = cadastro.render()
        if isinstance(cadastro, basestring):
            xml = cadastro
        assert xml is not None, "Objeto cadastro deve ser do tipo DynamicXml ou string"
                
        
        return self._executar_consulta(xml)