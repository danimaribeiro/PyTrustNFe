# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


import os
from lxml import etree
from pytrustnfe.comunicacao import executar_consulta, Comunicacao
from .assinatura import sign_xml, Assinatura
from pytrustnfe import utils
from pytrustnfe.xml import render_xml
from pytrustnfe.utils import CabecalhoSoap


def _build_header(**kwargs):
    estado = kwargs['estado']
    return CabecalhoSoap({ 'estado': estado, 'soap_action': '' })


def _send(certificado, method, **kwargs):
    path = os.path.join(os.path.dirname(__file__), 'templates')
    
    xml = render_xml(path, '%s.xml' % method, **kwargs)

    pfx_path = certificado.save_pfx()
    signer = Assinatura(pfx_path, certificado.password)
    xml_signed = signer.assina_xml(xml, '')
    
    cabecalho = _build_header(**kwargs)
    
    return executar_consulta(certificado, cabecalho, xml_signed)
    


def autorizar_nfe(certificado, **kwargs): # Assinar
    _send(certificado, 'NfeAutorizacao', **kwargs)
    
def retorno_autorizar_nfe(certificado, **kwargs):
    _send(certificado, 'NfeRetAutorizacao', **kwargs)
    
def recepcao_evento_cancelamento(certificado, **kwargs):  # Assinar
    _send(certificado, 'RecepcaoEventoCancelamento', **kwargs)

def inutilizar_nfe(certificado, **kwargs): # Assinar
    _send(certificado, 'NfeInutilizacao', **kwargs)

def consultar_protocolo_nfe(certificado, **kwargs):
    _send(certificado, 'NfeConsultaProtocolo', **kwargs)
    
def nfe_status_servico(certificado, **kwargs):
    _send(certificado, 'NfeStatusServico.', **kwargs)
    
def consulta_cadastro(certificado, **kwargs):
    _send(certificado, 'NfeConsultaCadastro.', **kwargs)
    
def recepcao_evento_carta_correcao(certificado, **kwargs): # Assinar
    _send(certificado, 'RecepcaoEventoCarta.', **kwargs)
    
def recepcao_evento_manifesto(certificado, **kwargs): # Assinar
    _send(certificado, 'RecepcaoEventoManifesto', **kwargs)
    
def recepcao_evento_epec(certificado, **kwargs): # Assinar
    _send(certificado, 'RecepcaoEventoEPEC', **kwargs)
    
def consulta_nfe_destinada(certificado, **kwargs):
    _send(certificado, 'NfeConsultaDest', **kwargs)
    
def download_nfe(certificado, **kwargs):
    _send(certificado, 'NfeDownloadNF', **kwargs)
    

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
