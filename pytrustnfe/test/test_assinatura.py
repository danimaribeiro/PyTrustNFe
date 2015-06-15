#coding=utf-8
'''
Created on Jun 14, 2015

@author: danimar
'''
import unittest
from pytrustnfe.servicos.assinatura import Assinatura

XML_ASSINAR = '<?xml version="1.0" encoding="UTF-8"?>' \
               '<Envelope xmlns="urn:envelope">'  \
               '   <Data Id="NFe43150602261542000143550010000000761792265342">' \
               '     Hello, World!' \
               '   </Data>' \
               '</Envelope>'

XML_ASSINADO = ''

class test_assinatura(unittest.TestCase):

    def test_assinar_xml(self):
        print 'oola'
        assinatura = Assinatura('/home/danimar/Desktop/INFOGER.pfx', '123456')
        
        self.assertRaises(RuntimeError, assinatura.assina_xml, XML_ASSINAR)


#if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
#    unittest.main()
    