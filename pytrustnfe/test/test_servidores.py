# coding=utf-8
'''
Created on Jun 14, 2015

@author: danimar
'''
import unittest
from pytrustnfe.Servidores import localizar_url, localizar_qrcode

url_ba = 'https://nfe.sefaz.ba.gov.br/webservices/NFeAutorizacao4/NFeAutoriza\
cao4.asmx?wsdl'

url_sp = 'https://nfe.fazenda.sp.gov.br/ws/nfeautorizacao4.asmx?wsdl'

url_qrcode_homologacao_sp = 'https://homologacao.nfce.fazenda.sp.gov.br/NFCEConsultaPublica/Paginas/ConstultaQRCode.aspx'

url_sc = 'https://nfe.svrs.rs.gov.br/ws/NfeAutorizacao/NFeAutorizacao4.asmx?wsdl'

url_rs = 'https://nfe.sefazrs.rs.gov.br/ws/NfeAutorizacao/NFeAutorizacao4.asmx?wsdl'

url_cad_rs = 'https://cad.sefazrs.rs.gov.br/ws/cadconsultacadastro/cadconsultacadastro4.asmx?wsdl'

url_cad_sc = 'https://cad.svrs.rs.gov.br/ws/cadconsultacadastro/cadconsultacadastro2.asmx?wsdl'


class test_servidores(unittest.TestCase):

    def test_localizar_url(self):
        url = localizar_url('NfeAutorizacao', '29', ambiente=1)
        self.assertEqual(url, url_ba)
        url = localizar_url('NfeAutorizacao', '35', ambiente=1)
        self.assertEqual(url, url_sp)
        url = localizar_url('NfeAutorizacao', '42', ambiente=1)
        self.assertEqual(url, url_sc)
        url = localizar_url('NfeAutorizacao', '43', ambiente=1)
        self.assertEqual(url, url_rs)

        url = localizar_url('NfeConsultaCadastro', '43', ambiente=2)
        self.assertEqual(url, url_cad_rs)

        url = localizar_url('NfeConsultaCadastro', '42', ambiente=2)
        self.assertEqual(url, url_cad_sc)

    def test_localizar_qrcode(self):
        url = localizar_qrcode('35')
        self.assertEqual(url, url_qrcode_homologacao_sp)
