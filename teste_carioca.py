# -*- coding: utf-8 -*-

import logging
from datetime import datetime
from pytrustnfe.nfe import consulta_cadastro
#import pytrustnfe.nfe 
from pytrustnfe.certificado import Certificado
from pytrustnfe.nfse.paulistana  import cancelamento_nfe
from pytrustnfe.nfse.paulistana  import envio_lote_rps
from pytrustnfe.nfse.carioca  import gerar_nfse


logger = logging.getLogger(__name__)
dbg = 0


#certificado_path = open(b'/data/certs/23834691000124.pfx', 'rb').read()
certificado_path = open(b'/data/certs/expirado.pfx', 'rb').read()
certificado = Certificado(certificado_path, 'audaz$321')

if dbg>1 :print('type(certificado)')
if dbg>1 :print(type(certificado))
if dbg>9 :print(certificado.pfx)
if dbg>1 :print(certificado.password)
# Necessário criar um dicionário com os dados, validação dos dados deve
# ser feita pela aplicação que está utilizando a lib

#retorno = envio_lote_rps(certificado, nfse=nfse)
#retorno = gerar_nfse(certificado, nfse=rps)

#xml  = { "rps" : {"rps" : { "numero" : "1" }}}
#retorno = gerar_nfse(certificado, nfse=xml)

rps = {
    'ambiente': '2',
    'rps': {
        'ambiente': '2',
        'numero': '1',
        'serie': 'ABC',
        'tipo_rps': '1',
        'data_emissao': '2010-01-01T21:00:00',
        'natureza_operacao': '1',
        'optante_simples': '1',
        'incentivador_cultural': '2',
        'status': '1',
        #'regime_tributacao': '',
        #'numero_substituido': '',
        '#serie_substituido': '',
        '#tipo_substituido': '',
        'valor_servico': '9.99',
        'valor_deducao': '0',
        'valor_pis': '0',
        'valor_cofins': '0',
        'valor_inss': '0',
        'valor_ir': '0',
        'valor_csll': '0',
        'iss_retido': '0',
        'valor_iss': '0',
        'valor_iss_retido': '0',
        'outras_retencoes': '0',
        'base_calculo': '9.99',
        'aliquota_issqn': '0.05',
        'valor_liquido_nfse': '9.99',
        'desconto_incondicionado': '',
        'desconto_condicionado': '',
        'codigo_servico': '0107',
        'cnae_servico': '',
        'codigo_tributacao_municipio': '010701',
        'codigo_municipio': '3304557',
        'descricao': 'Venda de servico',
        'prestador': {
            'cnpj': '123456789011213',
            'inscricao_municipal': '123456',
        },
        'tomador': {
            'tipo_cpfcnpj': '1',
            'cpf_cnpj': '12345678923256',
            'inscricao_municipal': '123456',
            'razao_social': 'Trustcode',
            'tipo_logradouro': '1',
            'logradouro': 'Vinicius de Moraes, 42',
            'numero': '42',
            'complemento': '',
            'bairro': 'Corrego',
            'cidade': '4205407',  # Código da cidade, de acordo com o IBGE
            'uf': 'SC',
            'cep': '88037240',
            'tomador.telefone': '',
            'tomador.email': ''
        },
    }
}


retorno = gerar_nfse(certificado, **rps)




# retorno é um dicionário { 'received_xml':'', 'sent_xml':'', 'object': object() }
if dbg>=9 :print(retorno['sent_xml'])
if dbg>=1 :print(retorno['received_xml'])

# retorno['object'] é um objeto python criado apartir do xml de resposta
if dbg>=9 :print(retorno['object'])
#print retorno['object'].Cabecalho.Sucesso
#print retorno['object'].ChaveNFeRPS.ChaveNFe.NumeroNFe
#print retorno['object'].ChaveNFeRPS.ChaveRPS.NumeroRPS
