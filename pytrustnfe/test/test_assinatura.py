# coding=utf-8
'''
Created on Jun 14, 2015

@author: danimar
'''
import os
import os.path
import unittest
from lxml import etree
from pytrustnfe.nfe.assinatura import Assinatura


XML_ASSINAR = '<?xml version="1.0" encoding="UTF-8"?>' \
              '<Envelope xmlns="urn:envelope">'  \
              '   <Data Id="NFe43150602261542000143550010000000761792265342">'\
              '     Hello, World!' \
              '   </Data>' \
              '</Envelope>'


XML_ERRADO = '<?xml version="1.0" encoding="UTF-8"?>' \
             '<Envelope xmlns="urn:envelope">'  \
             ' <Data Id="NFe">' \
             '     Hello, World!' \
             '   </Data>' \
             '</Envelope>'


class test_assinatura(unittest.TestCase):

    caminho = os.path.dirname(__file__)

    def test_assinar_xml_senha_invalida(self):
        pfx = open(os.path.join(self.caminho, 'teste.pfx')).read()
        signer = Assinatura(pfx, '123')
        self.assertRaises(Exception, signer.assina_xml, signer,
                          etree.fromstring(XML_ASSINAR),
                          'NFe43150602261542000143550010000000761792265342')

    def test_assinar_xml_invalido(self):
        pfx = open(os.path.join(self.caminho, 'teste.pfx')).read()
        signer = Assinatura(pfx, '123456')
        self.assertRaises(Exception, signer.assina_xml, signer,
                          etree.fromstring(XML_ERRADO),
                          'NFe43150602261542000143550010000000761792265342')

    def test_assinar_xml_valido(self):
        pfx = open(os.path.join(self.caminho, 'teste.pfx')).read()
        signer = Assinatura(pfx, '123456')
        xml = signer.assina_xml(
            etree.fromstring(XML_ASSINAR),
            'NFe43150602261542000143550010000000761792265342')
        xml_assinado = open(os.path.join(self.caminho,
                                         'xml_valido_assinado.xml'),
                            'r').read()
        self.assertEqual(xml_assinado, xml, 'Xml assinado é inválido')
