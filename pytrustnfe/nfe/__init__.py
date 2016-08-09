# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


import os
from lxml import etree
from .comunicacao import Comunicacao
from .assinatura import sign_xml, Assinatura
from pytrustnfe import utils
from pytrustnfe.xml import render_xml


class NFe(Comunicacao):

    def __init__(self, cert, key):
        Comunicacao.__init__(self, cert, key)

    def consultar_cadastro(self, cadastro, estado):
        self.url = 'https://cad.sefazrs.rs.gov.br/ws/cadconsultacadastro/cadconsultacadastro2.asmx'
        self.metodo = 'NfeConsultaCadastro'
        
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'xml')
        xml = render_xml(path, 'consultar_cadastro.xml', **cadastro)
        
        xml_response, obj = self._executar_consulta(xml)
        
        return {
            'sent_xml': xml,
            'received_xml': xml_response,
            'object': obj.Body.nfeAutorizacaoLoteResult
        }


    def autorizar_nfe(self, nfe, nfe_id):        
        self.url = 'https://nfe-homologacao.sefazrs.rs.gov.br/ws/NfeAutorizacao/NFeAutorizacao.asmx'
        self.metodo = 'NfeAutorizacao/nfeAutorizacaoLote'

        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'xml')
        xml = render_xml(path, 'nfeEnv.xml', **nfe)
        
        xmlElem = etree.fromstring(xml)        
        xml_signed = sign_xml(xmlElem, self.cert, self.key, '#%s' % nfe_id)

        xml_response, obj = self._executar_consulta(xml_signed)
        
        return {
            'sent_xml': xml_signed,
            'received_xml': xml_response,
            'object': obj.Body.nfeAutorizacaoLoteResult
        }
