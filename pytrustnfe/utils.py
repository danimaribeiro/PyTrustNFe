# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


import re
from datetime import date, datetime
import lxml.etree as ET


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


def date_tostring(data):
    assert isinstance(data, date), "Objeto date requerido"
    return data.strftime("%d-%m-%y")


def datetime_tostring(data):
    assert isinstance(data, datetime), "Objeto datetime requerido"
    return data.strftime("%d-%m-%y %H:%M:%S")


def gerar_chave(obj_chave, prefix=None):
    assert isinstance(obj_chave, ChaveNFe), "Objeto deve ser do tipo ChaveNFe"
    obj_chave.validar()
    chave_parcial = "%s%s%s%s%s%s%d%s" % (
        obj_chave.estado, obj_chave.emissao,
        obj_chave.cnpj, obj_chave.modelo,
        obj_chave.serie.zfill(3), str(obj_chave.numero).zfill(9),
        obj_chave.tipo, obj_chave.codigo)
    chave_parcial = re.sub('[^0-9]', '', chave_parcial)
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


def _find_node(xml, node):
    for item in xml.iterchildren("*"):
        if node in item.tag:
            return item
        else:
            item = _find_node(item, node)
            if item is not None:
                return item
    return None


def gerar_nfeproc(envio, recibo):
    NSMAP = {None: 'http://www.portalfiscal.inf.br/nfe'}
    root = ET.Element("nfeProc", versao="3.10", nsmap=NSMAP)
    parser = ET.XMLParser(encoding='utf-8')
    docEnvio = ET.fromstring(envio.encode('utf-8'), parser=parser)
    docRecibo = ET.fromstring(recibo.encode('utf-8'), parser=parser)

    nfe = _find_node(docEnvio, "NFe")
    protocolo = _find_node(docRecibo, "protNFe")
    if nfe is None or protocolo is None:
        return b''
    root.append(nfe)
    root.append(protocolo)
    return ET.tostring(root)


def gerar_nfeproc_cancel(nfe_proc, cancelamento):
    docEnvio = ET.fromstring(nfe_proc)
    docCancel = ET.fromstring(cancelamento)

    ev_cancelamento = _find_node(docCancel, "retEvento")
    if ev_cancelamento is None:
        return b''
    docEnvio.append(ev_cancelamento)
    return ET.tostring(docEnvio)
