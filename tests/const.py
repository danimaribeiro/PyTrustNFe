LOTE_RPS = [
    {
        'assinatura': '123',
        'serie': '1',
        'numero': str(i),
        'data_emissao': '2016-08-29',
        'codigo_atividade': '07498',
        'total_servicos': '2.00',
        'total_deducoes': '3.00',
        'prestador': {
            'inscricao_municipal': '123456'
        },
        'tomador': {
            'tipo_cpfcnpj': 1,
            'cpf_cnpj': '12345678923256',
            'inscricao_municipal': '123456',
            'razao_social': 'Trustcode',
            'tipo_logradouro': '1',
            'complemento': 'aaa',
            'logradouro': 'Vinicius de Moraes, 42',
            'numero': '42',
            'bairro': 'Corrego',
            'cidade': 'Floripa',
            'uf': 'SC',
            'cep': '88037240',
            'email': 'user@user.com'
        },
        'codigo_atividade': '07498',
        'aliquota_atividade': '5.00',
        'descricao': 'Venda de servico'
    } for i in range(5)
]

DEFAULT_RPS = [
    {
        'assinatura': '123',
        'serie': '1',
        'numero': '1',
        'data_emissao': '2016-08-29',
        'codigo_atividade': '07498',
        'prestador': {
            'inscricao_municipal': '123456'
        },
        'tomador': {
            'tipo_cpfcnpj': 1,
            'cpf_cnpj': '12345678923256',
        },
    }
]

NFSE = {
    'cpf_cnpj': '12345678901234',
    'data_inicio': '2016-08-29',
    'data_fim': '2016-08-29',
    'lista_rps': []
}
