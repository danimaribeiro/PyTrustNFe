#coding=utf-8
'''
Created on Jun 16, 2015

@author: danimar
'''
import mock
import unittest
import os.path
from pytrustnfe.servicos.Comunicacao import Comunicacao

XML_RETORNO = '<retEnviNFe><cStat>103</cStat>' \
                '<cUF>42</cUF></retEnviNFe>'

class test_comunicacao(unittest.TestCase):

    caminho = os.path.dirname(__file__)
    
    #Teste temporario
    def test_envio_without_mock(self):
        try:
            dir_pfx = '/home/danimar/Desktop/isotelha.pfx' #Hack
            
            com = Comunicacao(dir_pfx, 'iso@#telha')
            xml, objeto = com.envio_nfe()
            
            print xml
            print objeto
        except Exception as e:
            print(str(e))
        
    def test_envio_nfe(self):        
        dir_pfx = os.path.join(self.caminho, 'teste.pfx')
        
        with mock.patch('pytrustnfe.HttpClient.HTTPSConnection') as HttpsConnection:
            conn = HttpsConnection.return_value
            retorno = mock.MagicMock()            
            type(retorno).status = mock.PropertyMock(return_value='200')
            retorno.read.return_value = XML_RETORNO
                                        
            conn.getresponse.return_value = retorno            
        
            com = Comunicacao(dir_pfx, '123456')
            xml, objeto = com.envio_nfe()
            
            self.assertEqual(xml, XML_RETORNO, 'Envio de NF-e com problemas - xml de retorno inválido')
            self.assertEqual(objeto.cUF, 42, 'Envio de NF-e com problemas - objeto de retorno inválido')
            self.assertEqual(objeto.cStat, 103, 'Envio de NF-e com problemas - objeto de retorno inválido')
        
        
