#coding=utf-8
'''
Created on Jun 14, 2015

@author: danimar
'''
import unittest
import os, os.path
from pytrustnfe.servicos.Assinatura import Assinatura

XML_ASSINAR = '<?xml version="1.0" encoding="UTF-8"?>' \
               '<!DOCTYPE Envelope [ ' \
               '     <!ATTLIST Data Id ID #IMPLIED>' \
               ']>' \
               '<Envelope xmlns="urn:envelope">'  \
               '   <Data Id="NFe43150602261542000143550010000000761792265342">' \
               '     Hello, World!' \
               '   </Data>' \
               '</Envelope>'

XML_ERRADO = '<?xml version="1.0" encoding="UTF-8"?>' \
               '<Envelope xmlns="urn:envelope">'  \
               ' <Data Id="NFe43150602261542000143550010000000761792265342">' \
               '     Hello, World!' \
               '   </Data>' \
               '</Envelope>'

class test_assinatura(unittest.TestCase):
    
    caminho = os.path.dirname(__file__)

    def test_assinar_xml_arquivo_invalido(self):
        assinatura = Assinatura(os.path.join(self.caminho, 'teste_nao_existe.pfx'), '123456')
        self.assertRaises(Exception, assinatura.assina_xml, XML_ASSINAR)

    def test_assinar_xml_senha_invalida(self):        
        assinatura = Assinatura(os.path.join(self.caminho,'teste.pfx'), '123')
        self.assertRaises(Exception, assinatura.assina_xml, XML_ASSINAR)

    def test_assinar_xml_invalido(self):        
        assinatura = Assinatura(os.path.join(self.caminho,'teste.pfx'), '123456')
        self.assertRaises(RuntimeError, assinatura.assina_xml, XML_ERRADO)

    def test_assinar_xml_valido(self):        
        assinatura = Assinatura(os.path.join(self.caminho,'teste.pfx'), '123456')
        xml = assinatura.assina_xml(XML_ASSINAR)        
        xml_assinado = open(os.path.join(self.caminho, 'xml_assinado.xml'), 'r').read()    
        
        self.assertEqual(xml_assinado, xml, 'Xml assinado é inválido')

    