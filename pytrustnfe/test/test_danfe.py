'''
Created on 01/07/2015

@author: danimar
'''
import unittest
from pytrustnfe.pdf.Danfe import Danfe
from pytrustnfe.xml.DynamicXml import DynamicXml

class test_danfe(unittest.TestCase):

    def test_geracao_danfe(self):
        nfe = DynamicXml('ProtNFe')
        pdf = Danfe(nfe)
        pdf.gerar()
        
        

