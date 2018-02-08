# coding=utf-8

import mock
import os.path
import unittest
from pytrustnfe.certificado import Certificado
from pytrustnfe.nfe import consulta_cadastro


class test_consulta_cadastro(unittest.TestCase):

    caminho = os.path.dirname(__file__)

    def test_conta_de_cadastro(self):
        pfx_source = open(os.path.join(self.caminho, 'teste.pfx'), 'rb').read()
        pfx = Certificado(pfx_source, '123456')

        obj = {'cnpj': '12345678901234', 'estado': '42'}
        consulta_cadastro(pfx, obj=obj, ambiente=1, estado='42')
