# coding=utf-8
'''
Created on 22/06/2015

@author: danimar
'''
from datetime import date, datetime
from pytrustnfe.ChaveNFe import ChaveNFe


def date_tostring(data):
    assert isinstance(data, date), "Objeto date requerido"
    return data.strftime("%d-%m-%y")


def datetime_tostring(data):
    assert isinstance(data, datetime), "Objeto datetime requerido"
    return data.strftime("%d-%m-%y %H:%M:%S")


def gerar_consulta_recibo(recibo):
    c = DynamicXml('consReciNFe')
    c(xmlns="http://www.portalfiscal.inf.br/nfe", versao="2.00")
    c.tpAmb = recibo.tpAmb
    c.nRec = recibo.infRec.nRec
    return c


def gerar_chave(obj_chave, prefix=None):
    assert isinstance(obj_chave, ChaveNFe), "Objeto deve ser do tipo ChaveNFe"
    obj_chave.validar()

    chave_parcial = "%s%s%s%s%s%s%s%s" % (obj_chave.estado, obj_chave.emissao,
                                          obj_chave.cnpj, obj_chave.modelo,
                                          obj_chave.serie, obj_chave.numero,
                                          obj_chave.tipo, obj_chave.codigo)
    soma = 0
    contador = 2
    for c in reversed(chave_parcial):
        soma += int(c) * contador
        contador += 1
        if contador == 10:
            contador = 2
    dv = (11 - soma % 11) if (soma % 11 != 0 and soma % 11 != 1) else 0
    if prefix:
        return prefix + chave_parcial + str(dv)
    return chave_parcial + str(dv)


def descompacta_nfe_distribuicao(xml):
    pass
