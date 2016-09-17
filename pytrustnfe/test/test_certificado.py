# coding=utf-8
'''
Created on Jun 14, 2015

@author: danimar
'''
import unittest
import os
import os.path
from pytrustnfe.certificado import Certificado
from pytrustnfe.certificado import save_cert_key
from pytrustnfe.certificado import extract_cert_and_key_from_pfx

CHAVE = '-----BEGIN PRIVATE KEY-----\n' \
    'MIICdQIBADANBgkqhkiG9w0BAQEFAASCAl8wggJbAgEAAoGBAJONRp6l1y2ojgv8\n' \
    'tP3AOLW0vjWQqiPseBLM7YAxbzz5R7LYlWHC0ZJ4uIvd4Cvc6AuoNJoeuhzFcwHx\n' \
    'PL0TcFuW+5up1ktUohwaJ+/zKrMODCKt0gvif302yqasMnwLh9mGZQIkLkHPOX8p\n' \
    'ZQDC4dlqwOyYDi0f+bRd5C7aWx3RAgMBAAECgYADqASP+dwTLZIXifOSNikxl4D/\n' \
    'Is6UhU+UZ6+a9Z6kDClSrTtGaOV4k7U/AgiEDb1STKDBEPHbtKjc63Vt2gV2teem\n' \
    'ohU0Giv+gD42uuwy2DM31OfYrpR46mzOK9JrpQc78b36ealL3AWJ1gyBbbcOWbAb\n' \
    'KmP742V7pcD07EEp4QJBAM/e7M8VdLgOyaQzH9KHekU6fJlI4vy1UwgRUwx3/1W6\n' \
    'zlBYo1qXfc7NSVG8ZaSrJwW4rPn393u31CpXv+oc/OMCQQC1txS6nxM9+p/641HX\n' \
    'CHXiWJRn0Wv7rT1FyF2dHO+OQOkCCnHCsGDMf3bacTNb7iyaPbXEDac8od5uF/3h\n' \
    'aUy7AkBDPGoAeYItXqseL2Mlp6iG5+oRcp/o+YWH4IKqT84JHslI98KutL1+vKvw\n'\
    'gi2mW63djeR1Xh1wqP85SvTKduHdAkAIJLlIF8Lr/yRWQQO06EsoJqIX+Pmm4L+j\n'\
    'NfSECvztWhlXHxK0D+V2pKu15GbR0t2q1+Micx4wiGyIcIjPJkHrAkAvlbXGFcGT\n'\
    'pk9bQ8nl7EYqlvVn1TejzTLfBhBYOse/xT/NI4Kwjkan9R+EJ1cOc9EE8gm1W3jv\n'\
    'fMw/Bh2wC5kj\n'\
    '-----END PRIVATE KEY-----\n'

CERTIFICADO = '-----BEGIN CERTIFICATE-----\n'\
    'MIICMTCCAZqgAwIBAgIQfYOsIEVuAJ1FwwcTrY0t1DANBgkqhkiG9w0BAQUFADBX\n'\
    'MVUwUwYDVQQDHkwAewA1ADkARgAxAEUANAA2ADEALQBEAEQARQA1AC0ANABEADIA\n'\
    'RgAtAEEAMAAxAEEALQA4ADMAMwAyADIAQQA5AEUAQgA4ADMAOAB9MB4XDTE1MDYx\n'\
    'NTA1NDc1N1oXDTE2MDYxNDExNDc1N1owVzFVMFMGA1UEAx5MAHsANQA5AEYAMQBF\n'\
    'ADQANgAxAC0ARABEAEUANQAtADQARAAyAEYALQBBADAAMQBBAC0AOAAzADMAMgAy\n'\
    'AEEAOQBFAEIAOAAzADgAfTCBnzANBgkqhkiG9w0BAQEFAAOBjQAwgYkCgYEAk41G\n'\
    'nqXXLaiOC/y0/cA4tbS+NZCqI+x4EsztgDFvPPlHstiVYcLRkni4i93gK9zoC6g0\n'\
    'mh66HMVzAfE8vRNwW5b7m6nWS1SiHBon7/Mqsw4MIq3SC+J/fTbKpqwyfAuH2YZl\n'\
    'AiQuQc85fyllAMLh2WrA7JgOLR/5tF3kLtpbHdECAwEAATANBgkqhkiG9w0BAQUF\n'\
    'AAOBgQArdh+RyT6VxKGsXk1zhHsgwXfToe6GpTF4W8PHI1+T0WIsNForDhvst6nm\n'\
    'QtgAhuZM9rxpOJuNKc+pM29EixpAiZZiRMCSWEItNyEVdUIi+YnKBcAHd88TwO86\n'\
    'd126MWQ2O8cu5W1VoDp7hYBYKOnLbYi11/StO+0rzK+oPYAvIw==\n'\
    '-----END CERTIFICATE-----\n'


class test_assinatura(unittest.TestCase):

    caminho = os.path.dirname(__file__)

    def test_preparar_pfx(self):
        dir_pfx = open(os.path.join(self.caminho, 'teste.pfx'), 'r').read()
        cert, key = extract_cert_and_key_from_pfx(dir_pfx, '123456')
        self.assertEqual(key, CHAVE, 'Chave gerada inválida')
        self.assertEqual(cert, CERTIFICADO, 'Certificado inválido')

    def test_save_pfx(self):
        pfx_source = open(os.path.join(self.caminho, 'teste.pfx'), 'r').read()
        pfx = Certificado(pfx_source, '123')
        path = pfx.save_pfx()
        saved = open(path, 'r').read()
        self.assertEqual(pfx_source, saved,
                         'Arquivo pfx salvo não bate com arquivo lido')

    def test_save_cert_and_key(self):
        dir_pfx = open(os.path.join(self.caminho, 'teste.pfx'), 'r').read()
        cert, key = extract_cert_and_key_from_pfx(dir_pfx, '123456')
        cert_path, key_path = save_cert_key(cert, key)
        cert_saved = open(cert_path, 'r').read()
        key_saved = open(key_path, 'r').read()
        self.assertEqual(
            cert, cert_saved, 'Certificado não corresponde ao original')
        self.assertEqual(key, key_saved, 'Chave não corresponde ao original')

    def test_pfx_nao_existe(self):
        self.assertRaises(Exception, extract_cert_and_key_from_pfx,
                          'file.pfx', '123456')

    def test_pfx_senha_invalida(self):
        dir_pfx = os.path.join(self.caminho, 'teste.pfx')
        self.assertRaises(Exception, extract_cert_and_key_from_pfx,
                          dir_pfx, '123')
