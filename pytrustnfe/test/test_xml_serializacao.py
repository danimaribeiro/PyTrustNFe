# coding=utf-8

import unittest
from lxml.etree import Element, ElementTree
from pytrustnfe.xml.DynamicXml import DynamicXml

XML_TESTE = '<enviNFe versao="3.10">'\
    '<idLote>1</idLote>'\
    '<indSinc>1</indSinc>'\
    '<NFe>'\
    '<infNFe versao="3.10" Id="NFe456465465465465654652123564878">'\
    '<ide>'\
    '<cUF>32</cUF>'\
    '<cNF>0001</cNF>'\
    '<natOp>Venda de mercadorias</natOp>'\
    '</ide>'\
    '</infNFe>'\
    '</NFe>'\
    '</enviNFe>'

XML_LIST = '<cobr>'\
    '<dup item="1">'\
    '<nDup>1</nDup>'\
    '<dVenc>21-06-2015</dVenc>'\
    '<vDup>123.00</vDup>'\
    '</dup>'\
    '<dup item="2">'\
    '<nDup>2</nDup>'\
    '<dVenc>21-07-2015</dVenc>'\
    '<vDup>123.00</vDup>'\
    '</dup>'\
    '</cobr>'


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

        xml = t.render()
        self.assertEqual(xml, XML_TESTE, "Geração de xml com problemas")

    def test_list_serializacao(self):
        t = DynamicXml("cobr")
        t.dup[0](item="1")
        t.dup[0].nDup = '1'
        t.dup[0].dVenc = '21-06-2015'
        t.dup[0].vDup = '123.00'
        t.dup[1](item="2")
        t.dup[1].nDup = '2'
        t.dup[1].dVenc = '21-07-2015'
        t.dup[1].vDup = '123.00'

        xml = t.render()
        self.assertEqual(xml, XML_LIST,
                         "Xml com lista de valores sendo gerado incorretamnte")
