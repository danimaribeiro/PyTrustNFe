# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import os.path
import unittest
from pytrustnfe.certificado import Certificado
from pytrustnfe.nfse.ginfes import consultar_situacao_lote


class test_nfse_ginfes(unittest.TestCase):

    caminho = os.path.dirname(__file__)

    @unittest.skip
    def test_consulta_situacao_lote(self):
        pfx_source = open('/home/danimar/Downloads/machado.pfx', 'r').read()
        pfx = Certificado(pfx_source, '123456789')

        dados = {'ambiente': 'homologacao'}
        retorno = consultar_situacao_lote(
            pfx, consulta=dados, ambiente='homologacao')

        self.assertNotEqual(retorno['received_xml'], '')
        self.assertEqual(retorno['object'].Cabecalho.Sucesso, True)
