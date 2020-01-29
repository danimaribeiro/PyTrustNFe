# coding=utf-8

import mock
import os.path
import unittest
from pytrustnfe.certificado import Certificado
from pytrustnfe.nfse.natal import recepcionar_lote_rps


class test_nfse_natal(unittest.TestCase):

    caminho = os.path.dirname(__file__)

    def _get_nfse(self):
        rps_list = [
            {
                "numero": "1",
                "serie": "UNICA",
                "tipo_rps": "1",
                "data_emissao": "2020-01-279",
                "natureza_operacao": "1",
                "regime_tributacao": "1",
                "optante_simples": "1",
                "incentivador_cultural": "2",
                "servico": {
                    "valor_servico": "1.00",
                    "iss_retido": "2",
                    "base_calculo": "0.00",
                    "codigo_servico": "01.07",
                    "cnae_servico": "6209100",
                    "descricao": "Sistema NFSe",
                    "codigo_municipio": "2408102",
                },
                "prestador": {
                    "cnpj": "23809070000190",
                    "inscricao_municipal": "2143992",
                    "razao_social": "SERVICOS DE TI",
                    "fantasia": "SERVICOS DE TI",
                    "endereco": "AV AMINTAS",
                    "numero": "3755",
                    "complemento": "SALA 32",
                    "bairro": "Lagoa Nova",
                    "codigo_municipio": "2408102",
                    "uf": "RN",
                    "cep": "59075810",
                    "telefone": "4132095554",
                    "email": "SUPORTE@EMAIL.COM.BR",
                },
                "tomador": {
                    "cpf_cnpj": "01812418000166",
                    "razao_social": "LEONIR",
                    "endereco": "RUA GROBEIRO",
                    "numero": "128",
                    "bairro": "Lagoa Nova",
                    "cidade": "3159506",
                    "uf": "BH",
                    "cep": "1231231313",
                    "email": "leonir@yahoo.com.br",
                    "orgao_gerador": {"codigo_municipio": "3159506"},
                },
            }
        ]
        nfse = {
            "numero_lote": "1",
            "cnpj_prestador": "23809070000190",
            "inscricao_municipal": "2143992",
            "lista_rps": rps_list,
        }
        return nfse

    def test_recepcionar_lote_rps(self):
        pfx_source = open(os.path.join(self.caminho, "teste.pfx"), "rb").read()
        pfx = Certificado(pfx_source, "123456")

        nfse = self._get_nfse()
        path = os.path.join(os.path.dirname(__file__), "XMLs")
        sent_xml = open(os.path.join(path, "natal_sent_xml.xml"), "r").read()

        retorno = recepcionar_lote_rps(pfx, nfse=nfse)
        self.assertEqual(retorno["sent_xml"], sent_xml)
