# coding=utf-8
'''
Created on 01/07/2015

@author: danimar
'''
from pytrustnfe.xml.DynamicXml import DynamicXml
from reportlab.platypus.tables import Table
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus.doctemplate import SimpleDocTemplate
from reportlab.lib import colors

inch = 28.34


class Danfe(object):

    objeto = None

    def __init__(self, objetoNFe):
        assert isinstance(objetoNFe, DynamicXml),\
            'ObjetoNFe deve ser do tipo DynamicXml'
        self.objeto = objetoNFe

    def gerar(self):
        doc = SimpleDocTemplate(
            '/home/danimar/projetos/pdfs/danfe.pdf',
            pagesize=A4, leftMargin=0.5 * inch, rightMargin=0.5 * inch,
            topMargin=0.5 * inch, bottomMargin=0.5 * inch)

        elementos = []

        data = [
            ['Recebemos de verdesaine industria e comércio os produtos constantes na nota fiscal abaixo ', '',
             'NF-e\nNº 000.000.001\nSérie 001'],
            ['Data de recebimento',
             'Identificação e assinatura do recebedor',
             '']
        ]

        estilo = [('SPAN', (0, 0), (1, 0)),
                  ('SPAN', (2, 0), (2, 1)),
                  ('FONTSIZE', (0, 0), (1, 1), 8.0),
                  ('VALIGN', (0, 0), (1, 1), 'TOP'),
                  ('ALIGN', (2, 0), (2, 1), 'CENTER'),
                  ('GRID', (0, 0), (3, 1), 1, colors.black)]
        colunas = [4 * inch, 12 * inch, 4 * inch]
        table = Table(data, style=estilo, colWidths=colunas)

        elementos.append(table)

        doc.build(elementos)
