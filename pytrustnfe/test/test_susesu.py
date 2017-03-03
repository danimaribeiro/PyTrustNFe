# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import os.path
import unittest
from pytrustnfe.nfse.susesu import enviar_nota_retorna_url


class test_nfse_susesu(unittest.TestCase):

    caminho = os.path.dirname(__file__)

    def test_enviar_nota_url_nota(self):
        dados = {
            'cnpj_prestador': '21118045000135',
            'codigo_prefeitura': 3150,
            'senha_nfd': 'fiscalb',
            'prestador':  {},
            'tomador': {}
        }
        response = enviar_nota_retorna_url(ambiente='homologacao', nfse=dados)
        self.assertEqual(response['received_xml'],
                         '0-Numero da nota fiscal invalido.')
