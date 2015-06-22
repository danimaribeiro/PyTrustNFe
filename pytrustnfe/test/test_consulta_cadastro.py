#coding=utf-8
'''
Created on 22/06/2015

@author: danimar
'''
import unittest
from pytrustnfe.servicos.NfeConsultaCadastro import NfeConsultaCadastro
from pytrustnfe.xml.DynamicXml import DynamicXml


class Test(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        c = DynamicXml('ConsCad')
        c(xmlns="http://www.portalfiscal.inf.br/nfe", versao="2.00")
        c.infCons.xServ = 'CONS-CAD'
        c.infCons.UF = 'SC'
        c.infCons.CNPJ = '82951310000156'
        self.objeto_consulta = c

    def test_consulta_cadastro(self):
        try:
            dir_pfx = '/home/danimar/projetos/isotelha.pfx' #Hack
            
            com = NfeConsultaCadastro(dir_pfx, 'iso@#telha')
            xml, objeto = com.consultar_cadastro(self.objeto_consulta, 'SC')
            
            print xml
            print objeto
        except Exception as e:
            print(str(e))