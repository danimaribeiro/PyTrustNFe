# coding=utf-8

import os.path
import unittest
from pytrustnfe.xml import render_xml, sanitize_response
from tests.const import LOTE_RPS, NFSE


def _get_nfse():
    nfse = NFSE
    nfse['lista_rps'] = LOTE_RPS
    return nfse


class test_nfse_paulistana_para_lote(unittest.TestCase):
    xml_path = os.path.join(os.path.dirname(__file__), 'XMLs')
    template_path = 'pytrustnfe/nfse/paulistana/templates'
    BATCH_SIZE = len(LOTE_RPS)

    def test_envio_nfse(self):
        nfse = _get_nfse()

        xml_send = render_xml(self.template_path, 'EnvioLoteRPS.xml', False, nfse=nfse)
        expected_xml = open(os.path.join(self.xml_path, 'xml_send_rps_batch_to_paulistana.xml'), 'r').read()

        _, obj = sanitize_response(xml_send)

        self.assertEqual(obj.Cabecalho.QtdRPS, self.BATCH_SIZE)
        # f = open(os.path.join(self.xml_path, 'xml_send_rps_batch_to_paulistana.xml'), 'w')
        # f.write(xml_send)
        # f.close()
        self.assertEqual(xml_send, expected_xml)
