# PyTrustNFe
Biblioteca Python que tem por objetivo enviar NFe, NFCe e NFSe no Brasil

[![Coverage Status](https://coveralls.io/repos/danimaribeiro/PyTrustNFe/badge.svg?branch=master3)](https://coveralls.io/r/danimaribeiro/PyTrustNFe?branch=master3)
[![Code Health](https://landscape.io/github/danimaribeiro/PyTrustNFe/master3/landscape.svg?style=flat)](https://landscape.io/github/danimaribeiro/PyTrustNFe/master3)
[![Build Status](https://travis-ci.org/danimaribeiro/PyTrustNFe.svg?branch=master3)](https://travis-ci.org/danimaribeiro/PyTrustNFe)
[![PyPI version](https://badge.fury.io/py/PyTrustNFe3.svg)](https://badge.fury.io/py/PyTrustNFe3)

Dependências:
* PyXmlSec
* lxml
* signxml
* suds-jurko
* suds-jurko-requests
* reportlab
* Jinja2


NFSe - Cidades atendidas
--------------
* **Paulistana** - São Paulo/SP
* **Nota Carioca** - Rio de Janeiro/RJ
* **Imperial** - Petrópolis/RH
* [Susesu](cidades/susesu.md) - 3 cidades atendidas
* [Simpliss](cidades/simpliss.md) - 18 cidade atendidas
* [GINFES](cidaes/ginfes.md) - 79 cidades atendidas
* [DSF](cidades/dsf.md) - 7 cidades atendidas

Roadmap
--------------
Teste unitários

Implementar novos provedores de NFSe
* [Betha](cidades/betha.md) - 81 cidades atendidas  WIP
* [WebISS](cidades/webiss.md) - 51 cidades atendidas
* [ISSIntel](cidades/issintel.md) - 32 cidades atendidas
* [ISSNET](cidades/issnet.md) - 32 cidades atendidas
* [Saatri](cidades/saatri.md) - 31 cidades atendidas


Exemplos de uso da NFe
---------------

Consulta Cadastro por CNPJ:

```python
from pytrustnfe.nfe import consulta_cadastro
from pytrustnfe.certificado import Certificado

certificado = open("/path/certificado.pfx", "r").read()
certificado = Certificado(certificado, 'senha_pfx')
obj = {'cnpj': '12345678901234', 'estado': '42'}
resposta = consulta_cadastro(certificado, obj=obj, ambiente=1, estado='42')
```


Exemplo de uso da NFSe Paulistana
---------------------------------

Envio de RPS por lote

```python
certificado = open('/path/certificado.pfx', 'r').read()
certificado = Certificado(certificado, '123456')
# Necessário criar um dicionário com os dados, validação dos dados deve
# ser feita pela aplicação que está utilizando a lib
rps = [
    {
        'assinatura': '123',
        'serie': '1',
        'numero': '1',
        'data_emissao': '2016-08-29',
        'codigo_atividade': '07498',
        'valor_servico': '2.00',
        'valor_deducao': '3.00',
        'prestador': {
            'inscricao_municipal': '123456'
        },
        'tomador': {
            'tipo_cpfcnpj': '1',
            'cpf_cnpj': '12345678923256',
            'inscricao_municipal': '123456',
            'razao_social': 'Trustcode',
            'tipo_logradouro': '1',
            'logradouro': 'Vinicius de Moraes, 42',
            'numero': '42',
            'bairro': 'Corrego',
            'cidade': '4205407',  # Código da cidade, de acordo com o IBGE
            'uf': 'SC',
            'cep': '88037240',
        },
        'codigo_atividade': '07498',
        'aliquota_atividade': '5.00',
        'descricao': 'Venda de servico'
    }
]
nfse = {
    'cpf_cnpj': '12345678901234',
    'data_inicio': '2016-08-29',
    'data_fim': '2016-08-29',
    'total_servicos': '2.00',
    'total_deducoes': '3.00',
    'lista_rps': rps
}

retorno = envio_lote_rps(certificado, nfse=nfse)
# retorno é um dicionário { 'received_xml':'', 'sent_xml':'', 'object': object() }
print retorno['received_xml']
print retorno['sent_xml']

# retorno['object'] é um objeto python criado apartir do xml de resposta
print retorno['object'].Cabecalho.Sucesso
print retorno['object'].ChaveNFeRPS.ChaveNFe.NumeroNFe
print retorno['object'].ChaveNFeRPS.ChaveRPS.NumeroRPS
```


Cancelamento de NFSe:

```python
from pytrustnfe.certificado import Certificado
from pytrustnfe.nfse.paulistana import cancelamento_nfe

certificado = open('/path/certificado.pfx', 'r').read()
certificado = Certificado(certificado, '123456')
cancelamento = {
    'cnpj_remetente': '123',
    'assinatura': 'assinatura',
    'numero_nfse': '456',
    'inscricao_municipal': '654',
    'codigo_verificacao': '789',
}

retorno = cancelamento_nfe(certificado, cancelamento=cancelamento)

# retorno é um dicionário { 'received_xml':'', 'sent_xml':'', 'object': object() }
print retorno['received_xml']
print retorno['sent_xml']

# retorno['object'] é um objeto python criado apartir do xml de resposta
print retorno['object'].Cabecalho.Sucesso

if not retorno['object'].Cabecalho.Sucesso: # Cancelamento com erro
    print retorno['object'].Erro.Codigo
    print retorno['object'].Erro.Descricao
```
