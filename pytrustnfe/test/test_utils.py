# coding=utf-8
'''
Created on Jun 16, 2015

@author: danimar
'''
import unittest
import datetime
from pytrustnfe.utils import date_tostring, datetime_tostring, \
    gerar_chave
from pytrustnfe.utils import ChaveNFe


class test_utils(unittest.TestCase):
    kwargs = {
        'cnpj': '33009911002506', 'estado': '52', 'emissao': '0604',
        'modelo': '55', 'serie': '012', 'numero': 780,
        'tipo': 0, 'codigo': '26730161'
    }

    def test_date_tostring(self):
        hoje = datetime.date.today()
        data = date_tostring(hoje)
        self.assertEqual(data, hoje.strftime("%d-%m-%y"),
                         "Não convertido corretamente")
        self.assertRaises(Exception, date_tostring, "Not a date")

    def test_datetime_tostring(self):
        hoje = datetime.datetime.now()
        data = datetime_tostring(hoje)
        self.assertEqual(data, hoje.strftime("%d-%m-%y %H:%M:%S"),
                         "Não convertido corretamente")
        self.assertRaises(Exception, datetime_tostring, "Not a date")

    def test_geracao_chave(self):
        chave = ChaveNFe(**self.kwargs)
        str_chave = gerar_chave(chave)
        chave_correta = '52060433009911002506550120000007800267301615'
        self.assertEqual(str_chave, chave_correta,
                         "Geração de chave nf-e incorreta")

        str_chave = gerar_chave(chave, prefix='NFe')
        chave_correta = 'NFe52060433009911002506550120000007800267301615'
        self.assertEqual(str_chave, chave_correta,
                         "Geração de chave nf-e com prefixo incorreta")

        self.assertRaises(Exception, gerar_chave, "Not a ChaveNFe object")
        self.assertRaises(Exception, gerar_chave, "Not a ChaveNFe object")

    def test_chave_nfe(self):
        chave = ChaveNFe(**self.kwargs)
        with self.assertRaises(AssertionError) as cm:
            chave.cnpj = ''
            chave.validar()
        chave.cnpj = '1234567891011'
        self.assertEqual('CNPJ necessário para criar chave NF-e',
                         cm.exception.message,
                         'Validação da chave nf-e incorreta')

        with self.assertRaises(AssertionError) as cm:
            chave.estado = ''
            chave.validar()
        chave.estado = '42'
        self.assertEqual('Estado necessário para criar chave NF-e',
                         cm.exception.message,
                         'Validação da chave nf-e incorreta')

        with self.assertRaises(AssertionError) as cm:
            chave.emissao = ''
            chave.validar()
        chave.emissao = '0'
        self.assertEqual('Emissão necessário para criar chave NF-e',
                         cm.exception.message,
                         'Validação da chave nf-e incorreta')

        with self.assertRaises(AssertionError) as cm:
            chave.modelo = ''
            chave.validar()
        chave.modelo = '55'
        self.assertEqual('Modelo necessário para criar chave NF-e',
                         cm.exception.message,
                         'Validação da chave nf-e incorreta')

        with self.assertRaises(AssertionError) as cm:
            chave.serie = ''
            chave.validar()
        chave.serie = '012'
        self.assertEqual('Série necessária para criar chave NF-e',
                         cm.exception.message,
                         'Validação da chave nf-e incorreta')

        with self.assertRaises(AssertionError) as cm:
            chave.numero = ''
            chave.validar()
        chave.numero = '000000780'
        self.assertEqual('Número necessário para criar chave NF-e',
                         cm.exception.message,
                         'Validação da chave nf-e incorreta')

        with self.assertRaises(AssertionError) as cm:
            chave.tipo = ''
            chave.validar()
        chave.tipo = '42'
        self.assertEqual('Tipo necessário para criar chave NF-e',
                         cm.exception.message,
                         'Validação da chave nf-e incorreta')

        with self.assertRaises(AssertionError) as cm:
            chave.codigo = ''
            chave.validar()
        self.assertEqual('Código necessário para criar chave NF-e',
                         cm.exception.message,
                         'Validação da chave nf-e incorreta')
