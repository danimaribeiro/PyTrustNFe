# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import os.path
import unittest
from pytrustnfe.certificado import Certificado
from pytrustnfe.nfse.simpliss import consultar_situacao_lote
from pytrustnfe.nfse.simpliss import consultar_nfse_por_rps
from pytrustnfe.nfse.simpliss import consultar_lote
from pytrustnfe.nfse.simpliss import consultar_nfse
from pytrustnfe.nfse.simpliss import cancelar_nfse


class test_nfse_simpliss(unittest.TestCase):

    caminho = os.path.dirname(__file__)

    def test_consulta_situacao_lote(self):
        pfx_source = open('/home/danimar/Downloads/2016.pfx', 'r').read()
        pfx = Certificado(pfx_source, '1234')

        dados = {'cnpj_prestador': '12345678910234', 'inscricao_prestador': '123', 'protocolo': '123'}
        response = consultar_situacao_lote(
            pfx, consulta=dados, ambiente='homologacao')
        print response

    def test_consultar_nfse_rps(self):
        pfx_source = open('/home/danimar/Downloads/2016.pfx', 'r').read()
        pfx = Certificado(pfx_source, '1234')

        dados = {'cnpj_prestador': '01234567896589', 'inscricao_prestador': '123',
                 'tipo_rps': '1', 'serie_rps': 'AZ', 'numero_rps': 123}
        consultar_nfse_por_rps(
            pfx, consulta=dados, ambiente='homologacao')

    def test_consultar_lote(self):
        pfx_source = open('/home/danimar/Downloads/2016.pfx', 'r').read()
        pfx = Certificado(pfx_source, '1234')

        dados = {'cnpj_prestador': '01234567896589', 'protocolo': '545455451'}
        consultar_lote(
            pfx, consulta=dados, ambiente='homologacao')


    def test_consultar_nfse(self):
        pfx_source = open('/home/danimar/Downloads/2016.pfx', 'r').read()
        pfx = Certificado(pfx_source, '1234')

        dados = {'cnpj_prestador': '01234567896589', 'numero_nfse': '545455451'}
        consultar_nfse(
            pfx, consulta=dados, ambiente='homologacao')

    def test_cancelar_nfse(self):
        pfx_source = open('/home/danimar/Downloads/2016.pfx', 'r').read()
        pfx = Certificado(pfx_source, '1234')

        dados = {'cnpj_prestador': '01234567896589', 'numero_nfse': '545455451',
                 'inscricao_prestador': 454564, 'codigo_municipio': 1234567,
                 'codigo_cancelamento': '1'}
        cancelar_nfse(
            pfx, cancelar=dados, ambiente='homologacao')
