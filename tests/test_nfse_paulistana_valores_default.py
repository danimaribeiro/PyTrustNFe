# coding=utf-8

import os.path
import unittest
from pytrustnfe.xml import render_xml, sanitize_response
from tests.const import DEFAULT_RPS, NFSE

default_values = {
    'TipoRPS': 'RPS',
    'TributacaoRPS': 'T',
    'ValorCOFINS': 0.0,
    'ValorINSS': 0.0,
    'ValorIR': 0.0,
    'ValorPIS': 0.0,
    'ValorCSLL': 0.0,
    'ISSRetido': False
}
attrs = ['TipoRPS', 'TributacaoRPS', 'ValorPIS', 'ValorCOFINS', 'ValorINSS', 'ValorIR', 'ValorCSLL', 'ISSRetido']


def _get_nfse():
    nfse = NFSE
    nfse['lista_rps'] = DEFAULT_RPS
    return nfse


class test_nfse_paulistana_valores_default(unittest.TestCase):
    template_path = 'pytrustnfe/nfse/paulistana/templates'
    xml_path = os.path.join(os.path.dirname(__file__), 'XMLs')
    nfse = _get_nfse()

    def test_rps_sem_valores(self):

        xml_rps = render_xml(self.template_path, 'EnvioRPS.xml', False, nfse=self.nfse)

        _, obj = sanitize_response(xml_rps)

        for attr in attrs:
            self.assertEqual(getattr(obj.RPS, attr), default_values[attr])

    def test_lote_rps_sem_valores(self):
        xml_lote_rps = render_xml(self.template_path, 'EnvioLoteRPS.xml', False, nfse=self.nfse)

        _, obj = sanitize_response(xml_lote_rps)

        for attr in attrs:
            self.assertEqual(getattr(obj.RPS, attr), default_values[attr])
