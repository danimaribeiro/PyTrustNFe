# coding=utf-8

import mock
import os.path
import unittest

import pytest
from lxml import etree

from pytrustnfe import xml
from pytrustnfe.certificado import Certificado
from pytrustnfe.nfse import paulistana
from pytrustnfe.nfse.paulistana import envio_lote_rps
from pytrustnfe.nfse.paulistana import cancelamento_nfe
from pytrustnfe.xml import sanitize_response


class test_nfse_paulistana(unittest.TestCase):

    caminho = os.path.dirname(__file__)
  
    def _get_rps(self):
        rps = [
            {
                "assinatura": "123",
                "serie": "1",
                "numero": "1",
                "data_emissao": "2016-08-29",
                "codigo_atividade": "07498",
                "total_servicos": "2.00",
                "total_deducoes": "3.00",
                "prestador": {"inscricao_municipal": "123456"},
                "tomador": {
                    "tipo_cpfcnpj": "1",
                    "cpf_cnpj": "12345678923256",
                    "inscricao_municipal": "123456",
                    "razao_social": "Trustcode",
                    "tipo_logradouro": "1",
                    "logradouro": "Vinicius de Moraes, 42",
                    "numero": "42",
                    "bairro": "Corrego",
                    "cidade": "Floripa",
                    "uf": "SC",
                    "cep": "88037240",
                },
                "codigo_atividade": "07498",
                "aliquota_atividade": "5.00",
                "descricao": "Venda de servico",
            }
        ]
        return rps

    def _get_rps_carga_tributaria(self):
        rps = [
            {
                "assinatura": "123",
                "serie": "1",
                "numero": "1",
                "data_emissao": "2016-08-29",
                "codigo_atividade": "07498",
                "total_servicos": "2.00",
                "total_deducoes": "3.00",
                "prestador": {"inscricao_municipal": "123456"},
                "tomador": {
                    "tipo_cpfcnpj": "1",
                    "cpf_cnpj": "12345678923256",
                    "inscricao_municipal": "123456",
                    "razao_social": "Trustcode",
                    "tipo_logradouro": "1",
                    "logradouro": "Vinicius de Moraes, 42",
                    "numero": "42",
                    "bairro": "Corrego",
                    "cidade": "Floripa",
                    "uf": "SC",
                    "cep": "88037240",
                },
                "codigo_atividade": "07498",
                "aliquota_atividade": "5.00",
                "descricao": "Venda de servico",
                "valor_carga_tributaria": "30.00",
                "fonte_carga_tributaria": "IBPT"

            }
        ]
        return rps

    def _get_nfse(self, rps):

        nfse = {
            "cpf_cnpj": "12345678901234",
            "data_inicio": "2016-08-29",
            "data_fim": "2016-08-29",
            "lista_rps": rps,
        }
        return nfse

    def test_envio_nfse(self):
        pfx_source = open(os.path.join(self.caminho, "teste.pfx"), "rb").read()
        pfx = Certificado(pfx_source, "123456")

        rps = self._get_rps()
        nfse = self._get_nfse(rps)
        path = os.path.join(os.path.dirname(__file__), "XMLs")
        xml_return = open(os.path.join(path, "paulistana_resultado.xml"), "r").read()

        with mock.patch(
            "pytrustnfe.nfse.paulistana.get_authenticated_client"
        ) as client:
            retorno = mock.MagicMock()
            client.return_value = retorno
            retorno.service.EnvioLoteRPS.return_value = xml_return

            retorno = envio_lote_rps(pfx, nfse=nfse)

            self.assertEqual(retorno["received_xml"], xml_return)
            self.assertEqual(retorno["object"].Cabecalho.Sucesso, True)
            self.assertEqual(retorno["object"].ChaveNFeRPS.ChaveNFe.NumeroNFe, 446)
            self.assertEqual(retorno["object"].ChaveNFeRPS.ChaveRPS.NumeroRPS, 6)

    def test_nfse_signature(self):
        pfx_source = open(os.path.join(self.caminho, "teste.pfx"), "rb").read()
        pfx = Certificado(pfx_source, "123456")

        rps = self._get_rps()
        nfse = self._get_nfse(rps)
        path = os.path.join(os.path.dirname(__file__), "XMLs")
        xml_sent = open(os.path.join(path, "paulistana_signature.xml"), "r").read()

        with mock.patch(
            "pytrustnfe.nfse.paulistana.get_authenticated_client"
        ) as client:
            retorno = mock.MagicMock()
            client.return_value = retorno
            retorno.service.EnvioLoteRPS.return_value = "<xml></xml>"

            retorno = envio_lote_rps(pfx, nfse=nfse)
            self.assertEqual(retorno["sent_xml"], xml_sent)

    def _get_cancelamento(self):
        return {
            "cnpj_remetente": "123",
            "assinatura": "assinatura",
            "numero_nfse": "456",
            "inscricao_municipal": "654",
            "codigo_verificacao": "789",
        }

    def test_cancelamento_nfse_ok(self):
        pfx_source = open(os.path.join(self.caminho, "teste.pfx"), "rb").read()
        pfx = Certificado(pfx_source, "123456")
        cancelamento = self._get_cancelamento()

        path = os.path.join(os.path.dirname(__file__), "XMLs")
        xml_return = open(os.path.join(path, "paulistana_canc_ok.xml"), "r").read()

        with mock.patch(
            "pytrustnfe.nfse.paulistana.get_authenticated_client"
        ) as client:
            retorno = mock.MagicMock()
            client.return_value = retorno
            retorno.service.CancelamentoNFe.return_value = xml_return

            retorno = cancelamento_nfe(pfx, cancelamento=cancelamento)

            self.assertEqual(retorno["received_xml"], xml_return)
            self.assertEqual(retorno["object"].Cabecalho.Sucesso, True)

    def test_cancelamento_nfse_com_erro(self):
        pfx_source = open(os.path.join(self.caminho, "teste.pfx"), "rb").read()
        pfx = Certificado(pfx_source, "123456")
        cancelamento = self._get_cancelamento()

        path = os.path.join(os.path.dirname(__file__), "XMLs")
        xml_return = open(os.path.join(path, "paulistana_canc_errado.xml"), "r").read()

        with mock.patch(
            "pytrustnfe.nfse.paulistana.get_authenticated_client"
        ) as client:
            retorno = mock.MagicMock()
            client.return_value = retorno
            retorno.service.CancelamentoNFe.return_value = xml_return

            retorno = cancelamento_nfe(pfx, cancelamento=cancelamento)

            self.assertEqual(retorno["received_xml"], xml_return)
            self.assertEqual(retorno["object"].Cabecalho.Sucesso, False)
            self.assertEqual(retorno["object"].Erro.ChaveNFe.NumeroNFe, 446)

    def test_nfse_com_carga_tributaria(self):

        rps = self._get_rps_carga_tributaria()
        nfse = self._get_nfse(rps)

        path = os.path.join(os.path.dirname(paulistana.__file__), 'templates')

        xml_send = xml.render_xml(path, 'EnvioLoteRPS.xml', False, nfse=nfse)

        _, xml_send_obj = sanitize_response(xml_send)

        self.assertEqual(xml_send_obj.RPS.ValorCargaTributaria, 30.00)
        self.assertEqual(xml_send_obj.RPS.FonteCargaTributaria, "IBPT")

    def test_nfse_sem_carga_tributaria(self):

        rps = self._get_rps()
        nfse = self._get_nfse(rps)

        path = os.path.join(os.path.dirname(paulistana.__file__), 'templates')

        xml_send = xml.render_xml(path, 'EnvioLoteRPS.xml', False, nfse=nfse)

        _, xml_send_obj = sanitize_response(xml_send)

        with pytest.raises(AttributeError) as error:
            xml_send_obj.RPS.ValorCargaTributaria
            self.assertEqual(error.match, "no such child: ValorCargaTributaria")

            xml_send_obj.RPS.FonteCargaTributaria
            self.assertEqual(error.match, "no such child: FonteCargaTributaria")

