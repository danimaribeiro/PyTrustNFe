# coding=utf-8
'''
Created on 21/06/2015

@author: danimar
'''
from lxml import etree
from pytrustnfe.servicos.comunicacao import Comunicacao
from pytrustnfe import utils
from pytrustnfe.xml import render_xml
from pytrustnfe.servicos.assinatura import assinar


class NfeAutorizacao(Comunicacao):

    def __init__(self, cert, key, certificado, senha):
        Comunicacao.__init__(self, certificado, senha)
        self.cert = cert
        self.key = key

    def autorizar_nfe(self, nfe):
        self._validar_nfe(nfe)
        xml = render_xml('nfeEnv.xml', **nfe)

        self.metodo = 'NFeAutorizacao'
        self.tag_retorno = 'retEnviNFe'
        self.web_service = 'ws/NfeAutorizacao/NFeAutorizacao.asmx'
        self.url = 'nfe.sefazrs.rs.gov.br'

        return self._executar_consulta(xml)

    def autorizar_nfe_e_recibo(self, nfe, id):
        self._validar_nfe(nfe)
        xml = render_xml('nfeEnv.xml', **nfe)

        return assinar(xml, self.cert, self.key,
                       '#%s' % id,
                       self.certificado, self.senha)

        self.metodo = 'NFeAutorizacao'
        self.tag_retorno = 'retEnviNFe'
        self.web_service = 'ws/NfeAutorizacao/NFeAutorizacao.asmx'
        self.url = 'nfe.sefazrs.rs.gov.br'

        xml_recibo, recibo = self._executar_consulta(xml)

        consulta_recibo = utils.gerar_consulta_recibo(recibo)
        self._validar_nfe(nfe)

        self.metodo = 'NFeRetAutorizacao'
        self.tag_retorno = 'retConsReciNFe'
        self.web_service = 'ws/NfeRetAutorizacao/NFeRetAutorizacao.asmx'
        self.url = 'nfe.sefazrs.rs.gov.br'

        return self._executar_consulta(xml), consulta_recibo
