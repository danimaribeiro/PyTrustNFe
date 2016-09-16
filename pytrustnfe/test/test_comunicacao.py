# coding=utf-8
'''
Created on Jun 16, 2015

@author: danimar
'''
import mock
import unittest
from unittest import skip
import os.path
from pytrustnfe.nfe.comunicacao import executar_consulta


XML_RETORNO = '<retEnviNFe><cStat>103</cStat>' \
                '<cUF>42</cUF></retEnviNFe>'


class test_comunicacao(unittest.TestCase):

    caminho = os.path.dirname(__file__)

    @skip('Por enquanto pulamos')
    def test_envio_nfe(self):
        dir_pfx = os.path.join(self.caminho, 'teste.pfx')

        with mock.patch('pytrustnfe.client.requests') as request:
            conn = request.return_value
            retorno = mock.MagicMock()
            type(retorno).status = mock.PropertyMock(return_value='200')
            retorno.read.return_value = XML_RETORNO

            conn.getresponse.return_value = retorno
            xml, objeto = executar_consulta(dir_pfx)

            self.assertEqual(
                xml, XML_RETORNO,
                'Envio de NF-e com problemas - xml de retorno inválido')
            self.assertEqual(
                objeto.cUF, 42,
                'Envio de NF-e com problemas - objeto de retorno inválido')
            self.assertEqual(
                objeto.cStat, 103,
                'Envio de NF-e com problemas - objeto de retorno inválido')
