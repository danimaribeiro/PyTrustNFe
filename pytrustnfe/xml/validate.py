# -*- coding: utf-8 -*-
# © 2016 Alessandro Fernandes Martini <alessandrofmartini@gmail.com>, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import os

from lxml import etree

PATH = os.path.dirname(os.path.abspath(__file__))


def valida_nfe(xml_nfe):
    xsd = 'schemas/enviNFe_v4.00.xsd'
    return valida_esquema(xml_nfe, xsd)


def valida_distribuicao(xml):
    xsd = 'distDFeInt_v1.01.xsd'
    return valida_esquema(xml, xsd)


def valida_esquema(xml, xsd_name):
    xsd = os.path.join(PATH, xsd_name)
    xml_etree = etree.fromstring(xml)
    esquema = etree.XMLSchema(etree.parse(xsd))
    esquema.validate(xml_etree)
    erros = [x.message for x in esquema.error_log]
    return "\n".join(erros)
