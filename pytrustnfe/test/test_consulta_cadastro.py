# coding=utf-8
'''
Created on 22/06/2015

@author: danimar
'''
import unittest
from unittest import skip
from pytrustnfe.nfe import consulta_cadastro


class Test(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    @skip('Pulando')
    def test_consulta_cadastro(self):
        try:
            dir_pfx = 'teste.pfx'
            com = consulta_cadastro(dir_pfx, 'iso@#telha')
            xml, objeto = com.consultar_cadastro(self.objeto_consulta, 'SC')

            print xml
            print objeto
        except Exception as e:
            print(str(e))
