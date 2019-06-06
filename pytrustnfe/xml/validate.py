# -*- coding: utf-8 -*-
# © 2016 Alessandro Fernandes Martini <alessandrofmartini@gmail.com>, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import os

from lxml import etree


class ValidarXml:
    PATH = os.path.dirname(os.path.abspath(__file__))

    def valida_nfe(self, xml):
        xsd = 'enviNFe_v4.00.xsd'
        erros = self.valida_esquema(xml, xsd)
        if len(erros) > 0:
            return {'ErrosEsquemas': "\n".join(erros)}
        else:
            return False

    def valida_distribuicao(self, xml):
        xsd = 'distDFeInt_v1.01.xsd'
        erros = self.valida_esquema(xml, xsd)
        if len(erros) >0:
            return {'ErrosEsquemas': "\n".join(erros)}
        else:
            return False

    def valida_esquema(self, xml, xsd_name):
        xsd = os.path.join(self.PATH, 'schemas/', xsd_name)
        xml_etree = etree.fromstring(xml)
        esquema = etree.XMLSchema(etree.parse(xsd))
        esquema.validate(xml_etree)
        erros = [x.message for x in esquema.error_log]
        return erros
