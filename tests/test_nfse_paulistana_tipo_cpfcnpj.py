# coding=utf-8

import os.path
import unittest
from pytrustnfe.xml import render_xml, sanitize_response
from tests.const import DEFAULT_RPS, NFSE

template_path = 'pytrustnfe/nfse/paulistana/templates'


def _get_nfse(tipo_cpfcnpj):
    nfse = NFSE
    lista_rps = DEFAULT_RPS

    for rps in lista_rps:
        rps['tomador']['tipo_cpfcnpj'] = tipo_cpfcnpj
        rps['tomador']['cpf_cnpj'] = '12345678923256'

    nfse['lista_rps'] = lista_rps
    return nfse


def get_objects(nfse):
    xml_rps = render_xml(template_path, 'EnvioRPS.xml', False, nfse=nfse)
    _, obj_rps = sanitize_response(xml_rps)

    xml_lote_rps = render_xml(template_path, 'EnvioLoteRPS.xml', False, nfse=nfse)
    _, obj_lote_rps = sanitize_response(xml_lote_rps)

    return obj_rps, obj_lote_rps


class test_nfse_paulistana_tipo_cpfcnpj(unittest.TestCase):

    def test_tipo_cpfcnpj_1(self):
        nfse = _get_nfse(tipo_cpfcnpj=1)

        obj_rps, obj_lote_rps = get_objects(nfse)

        self.assertTrue(hasattr(obj_rps.RPS, 'CPFCNPJTomador'))
        self.assertTrue(hasattr(obj_rps.RPS.CPFCNPJTomador, 'CPF'))
        self.assertTrue(hasattr(obj_lote_rps.RPS, 'CPFCNPJTomador'))
        self.assertTrue(hasattr(obj_lote_rps.RPS.CPFCNPJTomador, 'CPF'))

    def test_tipo_cpfcnpj_2(self):
        nfse = _get_nfse(tipo_cpfcnpj=2)

        obj_rps, obj_lote_rps = get_objects(nfse)

        self.assertTrue(hasattr(obj_rps.RPS, 'CPFCNPJTomador'))
        self.assertTrue(hasattr(obj_rps.RPS.CPFCNPJTomador, 'CNPJ'))
        self.assertTrue(hasattr(obj_lote_rps.RPS, 'CPFCNPJTomador'))
        self.assertTrue(hasattr(obj_lote_rps.RPS.CPFCNPJTomador, 'CNPJ'))

    def test_tipo_cpfcnpj_3(self):
        nfse = _get_nfse(tipo_cpfcnpj=3)

        obj_rps, obj_lote_rps = get_objects(nfse)

        self.assertFalse(hasattr(obj_rps.RPS, 'CPFCNPJTomador'))
