# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


import os
from .comunicacao import executar_consulta
from .assinatura import Assinatura
from pytrustnfe.xml import render_xml
from pytrustnfe.utils import CabecalhoSoap
from pytrustnfe.utils import gerar_chave, ChaveNFe
from pytrustnfe.Servidores import localizar_url
import re


def _build_header(**kwargs):
    vals = {'estado': kwargs['estado'], 'soap_action': ''}
    return CabecalhoSoap(**vals)


def _generate_nfe_id(**kwargs):
    for item in kwargs['NFes']:
        vals = {
            'cnpj': item['infNFe']['emit']['cnpj_cpf'],
            'estado': item['infNFe']['ide']['cUF'],
            'emissao': '%s%s' % (item['infNFe']['ide']['dhEmi'][2:4],
                                 item['infNFe']['ide']['dhEmi'][5:7]),
            'modelo': item['infNFe']['ide']['mod'],
            'serie': item['infNFe']['ide']['serie'],
            'numero': item['infNFe']['ide']['nNF'],
            'tipo': item['infNFe']['ide']['tpEmis'],
            'codigo': item['infNFe']['ide']['cNF'],
        }
        chave = ChaveNFe(**vals)
        chave_nfe = gerar_chave(chave, 'NFe')
        item['infNFe']['Id'] = chave_nfe
        item['infNFe']['ide']['cDV'] = chave_nfe[len(chave_nfe) - 1:]


def _send(certificado, method, **kwargs):
    path = os.path.join(os.path.dirname(__file__), 'templates')

    xml = render_xml(path, '%s.xml' % method, **kwargs)
    xml = '<!DOCTYPE NFe [<!ATTLIST infNFe Id ID #IMPLIED>]>' + xml
    xml = xml.replace('\n', '')
    pfx_path = certificado.save_pfx()
    signer = Assinatura(pfx_path, certificado.password)
    xml_signed = signer.assina_xml_nota(xml, kwargs['NFes'][0]['infNFe']['Id'])

    xml_signed = xml_signed.replace(
        '\n<!DOCTYPE NFe [\n<!ATTLIST infNFe Id ID #IMPLIED>\n]>\n', '')
    print xml_signed
    xml_signed = xml_signed.replace('\n', '')

    url = localizar_url(0,  'RS')
    cabecalho = _build_header(**kwargs)
    response, obj = executar_consulta(certificado, url, cabecalho, xml_signed)
    return {
        'sent_xml': xml_signed,
        'received_xml': response,
        'object': obj
    }


def autorizar_nfe(certificado, **kwargs):  # Assinar
    _generate_nfe_id(**kwargs)
    return _send(certificado, 'NfeAutorizacao', **kwargs)


def retorno_autorizar_nfe(certificado, **kwargs):
    return _send(certificado, 'NfeRetAutorizacao', **kwargs)


def recepcao_evento_cancelamento(certificado, **kwargs):  # Assinar
    return _send(certificado, 'RecepcaoEventoCancelamento', **kwargs)


def inutilizar_nfe(certificado, **kwargs):  # Assinar
    return _send(certificado, 'NfeInutilizacao', **kwargs)


def consultar_protocolo_nfe(certificado, **kwargs):
    return _send(certificado, 'NfeConsultaProtocolo', **kwargs)


def nfe_status_servico(certificado, **kwargs):
    return _send(certificado, 'NfeStatusServico.', **kwargs)


def consulta_cadastro(certificado, **kwargs):
    return _send(certificado, 'NfeConsultaCadastro.', **kwargs)


def recepcao_evento_carta_correcao(certificado, **kwargs):  # Assinar
    return _send(certificado, 'RecepcaoEventoCarta.', **kwargs)


def recepcao_evento_manifesto(certificado, **kwargs):  # Assinar
    return _send(certificado, 'RecepcaoEventoManifesto', **kwargs)


def recepcao_evento_epec(certificado, **kwargs):  # Assinar
    return _send(certificado, 'RecepcaoEventoEPEC', **kwargs)


def consulta_nfe_destinada(certificado, **kwargs):
    return _send(certificado, 'NfeConsultaDest', **kwargs)


def download_nfe(certificado, **kwargs):
    return _send(certificado, 'NfeDownloadNF', **kwargs)
