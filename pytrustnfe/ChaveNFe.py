# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


class ChaveNFe(object):

    def __init__(self, **kwargs):
        self.cnpj = kwargs.pop('cnpj', '')
        self.estado = kwargs.pop('estado', '')
        self.emissao = kwargs.pop('emissao', '')
        self.modelo = kwargs.pop('modelo', '')
        self.serie = kwargs.pop('serie', '')
        self.numero = kwargs.pop('numero', '')
        self.tipo = kwargs.pop('tipo', '')
        self.codigo = kwargs.pop('codigo', '')

    def validar(self):
        assert self.cnpj != '', 'CNPJ necessário para criar chave NF-e'
        assert self.estado != '', 'Estado necessário para criar chave NF-e'
        assert self.emissao != '', 'Emissão necessário para criar chave NF-e'
        assert self.modelo != '', 'Modelo necessário para criar chave NF-e'
        assert self.serie != '', 'Série necessária para criar chave NF-e'
        assert self.numero != '', 'Número necessário para criar chave NF-e'
        assert self.tipo != '', 'Tipo necessário para criar chave NF-e'
        assert self.codigo != '', 'Código necessário para criar chave NF-e'
