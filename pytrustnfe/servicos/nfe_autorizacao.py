# coding=utf-8
'''
Created on 21/06/2015

@author: danimar
'''
from lxml import etree
from suds.sax.element import Element
from pytrustnfe.servicos.comunicacao import Comunicacao
from pytrustnfe import utils
from pytrustnfe.xml import render_xml
from pytrustnfe.servicos.assinatura import assinar


class NfeAutorizacao(Comunicacao):

    def __init__(self, cert, key):
        Comunicacao.__init__(self, cert, key)

    def autorizar_nfe(self, nfe, id):
        self._validar_nfe(nfe)
        xml = render_xml('nfeEnv.xml', **nfe)

        xml_signed = assinar(xml, self.cert, self.key, '#%s' % id)

        client = self._get_client(
            'https://nfe-homologacao.sefazrs.rs.gov.br/ws/NfeAutorizacao/NFeAutorizacao.asmx?wsdl')

        cabecalho = client.factory.create('nfeCabecMsg')
        cabecalho.cUF = '43'
        cabecalho.versaoDados = '3.10'
        client.set_options(soapheaders=cabecalho)

        resposta = client.service.nfeAutorizacaoLote(xml_signed)
        print client.last_sent()
        print client.last_received()

        consulta_recibo = utils.gerar_consulta_recibo(resposta)

        client = self._get_client(
            'https://nfe-homologacao.sefazrs.rs.gov.br/ws/NfeRetAutorizacao/NFeRetAutorizacao.asmx'
        )
        return client.service.nfeRetAutorizacao(consulta_recibo)
