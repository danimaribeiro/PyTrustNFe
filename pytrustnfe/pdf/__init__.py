# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from super_table import PdfTable, PdfCell
from pytrustnfe import xml

inch = 28.34


class Danfe(object):

    objeto = None

    def __init__(self, objetoNFe):
        self.objeto = sanitize_response(objetoNFe)[1]
        self.NFe = self.objeto.getchildren()[2]
        self.infNFe = self.NFe.getchildren()[0]
        self.ide = self.infNFe.getchildren()[0]
        self.emitente = self.infNFe.getchildren()[1]
        self.destinatario = self.infNFe.getchildren()[2]

    def nfe(self):
        danfe = PdfTable(columns=12)
        pass


    def gerar(self):
        pass
