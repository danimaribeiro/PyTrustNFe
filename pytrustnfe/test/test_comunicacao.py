# coding=utf-8
'''
Created on Jun 16, 2015

@author: danimar
'''
import unittest
import os.path


XML_RETORNO = '<retEnviNFe><cStat>103</cStat>' \
                '<cUF>42</cUF></retEnviNFe>'


class test_comunicacao(unittest.TestCase):

    caminho = os.path.dirname(__file__)

    def test_envio_nfe(self):
        pass
