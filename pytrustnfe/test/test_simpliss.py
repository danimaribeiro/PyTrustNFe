# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import os.path
import unittest
from pytrustnfe.certificado import Certificado
from pytrustnfe.nfse.simpliss import recepcionar_lote_rps


class test_nfse_simpliss(unittest.TestCase):

    caminho = os.path.dirname(__file__)

    def test_recepcionar_lote(self):
        pfx_source = open('/home/danimar/Downloads/machado.pfx', 'r').read()
        pfx = Certificado(pfx_source, '123456789')

        dados = {'cnpj_prestador': '12345678910234',
                 'inscricao_prestador': '123',
                 'protocolo': '123'}
        response = recepcionar_lote_rps(
            pfx, consulta=dados, ambiente='homologacao')
        print response
