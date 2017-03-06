# coding=utf-8

import tempfile
import os.path
import unittest
from lxml import etree
from pytrustnfe.nfe.danfe import danfe


class test_danfe(unittest.TestCase):

    caminho = os.path.dirname(__file__)

    def test_can_generate_danfe(self):
        path = os.path.join(os.path.dirname(__file__), 'XMLs')
        xml_string = open(os.path.join(path, 'NFe00000857.xml'), "r").read()
        # xml_string = open('/home/danimar/Downloads/NFe (5).xml', "r").read()

        xml_element = etree.fromstring(xml_string)

        oDanfe = danfe(list_xml=[xml_element])

        # Para testar localmente o Danfe
        # with open('/home/danimar/danfe.pdf', 'w') as oFile:
        with tempfile.TemporaryFile(mode='w') as oFile:
            oDanfe.writeto_pdf(oFile)
