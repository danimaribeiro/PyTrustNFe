# -*- coding: utf-8-*-
# © 2016 Alessandro Fernandes Martini
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import unittest
# from lxml import etree
from pytrustnfe.nfe import _add_qrCode


class TestAddQRCode(unittest.TestCase):
    def setUp(self):
        self.xml_sem_qrcode = open('pytrustnfe/test/xml_sem_qrcode.xml', 'r')
        self.xml_com_qrcode = open('pytrustnfe/test/xml_com_qrcode.xml', 'r')
        dhEmi = '2016-11-09T16:03:25-00:00'
        chave_nfe = u'NFe35161121332917000163650010000000011448875034'
        ambiente = 2
        valor_total = '324.00'
        icms_total = '61.56'
        cid_token = '000001'
        csc = '123456789'
        estado = '35'
        total = {'vNF': valor_total, 'vICMS': icms_total}
        infnfe = {'ide': {'dhEmi': dhEmi}, 'Id': chave_nfe, 'total': total,
                  'codigo_seguranca': {'cid_token': cid_token, 'csc': csc}}
        infnfe = {'infNFe': infnfe}
        self.kwargs = {}
        self.kwargs['ambiente'] = ambiente
        self.kwargs['estado'] = estado
        self.kwargs['NFes'] = [infnfe]

    def test_add_qrCode(self):
        xml_init = self.xml_sem_qrcode.read()
        xml_end = _add_qrCode(xml_init, **self.kwargs)
        self.assertEqual(xml_end, self.xml_com_qrcode.read())
