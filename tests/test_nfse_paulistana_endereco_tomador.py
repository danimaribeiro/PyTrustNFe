# coding=utf-8

import unittest
from pytrustnfe.xml import render_xml, sanitize_response
from tests.const import NFSE, DEFAULT_RPS


attrs = ['TipoLogradouro', 'Logradouro', 'NumeroEndereco', 'ComplementoEndereco', 'Bairro', 'CEP']

template_path = 'pytrustnfe/nfse/paulistana/templates'


def _get_nfse(lista_rps):
    nfse = NFSE
    nfse['lista_rps'] = lista_rps
    return nfse


def get_objects(nfse):
    xml_rps = render_xml(template_path, 'EnvioRPS.xml', False, nfse=nfse)
    _, obj_rps = sanitize_response(xml_rps)

    xml_lote_rps = render_xml(template_path, 'EnvioLoteRPS.xml', False, nfse=nfse)
    _, obj_lote_rps = sanitize_response(xml_lote_rps)

    return obj_rps, obj_lote_rps


class test_nfse_paulistana_endereco_tomador(unittest.TestCase):

    def test_rps_sem_cidade(self):
        nfse = _get_nfse(DEFAULT_RPS)

        obj_rps, obj_lote_rps = get_objects(nfse)

        self.assertFalse(hasattr(obj_rps.RPS, 'EnderecoTomador'))
        self.assertFalse(hasattr(obj_lote_rps.RPS, 'EnderecoTomador'))

    def test_rps_sem_dados_endereco(self):
        lista_rps = DEFAULT_RPS

        for rps in lista_rps:
            rps['tomador']['cidade'] = 'Florianópolis'

        nfse = _get_nfse(lista_rps)

        obj_rps, obj_lote_rps = get_objects(nfse)

        self.assertTrue(hasattr(obj_rps.RPS, 'EnderecoTomador'))
        self.assertTrue(hasattr(obj_lote_rps.RPS, 'EnderecoTomador'))

        for attr in attrs:
            self.assertFalse(hasattr(obj_rps.RPS.EnderecoTomador, attr))
            self.assertFalse(hasattr(obj_lote_rps.RPS.EnderecoTomador, attr))
