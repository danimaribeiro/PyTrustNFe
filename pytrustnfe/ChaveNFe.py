# coding=utf-8
'''
Created on 23/06/2015

@author: danimar
'''


class ChaveNFe(object):

    def __init__(self, valores):
        self.cnpj = ''
        self.estado = ''
        self.emissao = ''
        self.modelo = ''
        self.serie = ''
        self.numero = ''
        self.tipo = ''
        self.codigo = ''

    def validar(self):
        assert self.cnpj != '', 'CNPJ necessário para criar chave NF-e'
        assert self.estado != '', 'Estado necessário para criar chave NF-e'
        assert self.emissao != '', 'Emissão necessário para criar chave NF-e'
        assert self.modelo != '', 'Modelo necessário para criar chave NF-e'
        assert self.serie != '', 'Série necessária para criar chave NF-e'
        assert self.numero != '', 'Número necessário para criar chave NF-e'
        assert self.tipo != '', 'Tipo necessário para criar chave NF-e'
        assert self.codigo != '', 'Código necessário para criar chave NF-e'
