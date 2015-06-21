#coding=utf-8

import unittest
from lxml.etree import Element, ElementTree
from pytrustnfe.xml.DynamicXml import DynamicXml, gerar_xml


class test_xml_serializacao(unittest.TestCase):
    
    def test_serializacao(self):        
        t = DynamicXml("enviNFe")
        t(versao="3.10")
        t.idLote = "1"
        t.indSinc = "1"
        t.NFe.infNFe(versao="3.10", Id="NFe456465465465465654652123564878")
        t.NFe.infNFe.ide.cUF = "32"
        t.NFe.infNFe.ide.cNF = "0001"
        t.NFe.infNFe.ide.natOp = "Venda de mercadorias"
        
        print("Iniciando a geração do xml")
        print str(t)
        root = Element(str(t))
        gerar_xml(root, t)
        print(dir(t))
        
        tree = ElementTree(root)        
        tree.write("/home/danimar/Desktop/nfe.xml")
        
        