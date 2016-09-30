# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, BaseDocTemplate, Table, TableStyle
from reportlab.lib.pagesizes import A4
#  from reportlab.lib.units import mm

INCH = 28.34


class PdfTable(object):

    def __init__(self, columns=1, width=100):
        self.columns = columns
        self.width = width
        self.cells = []
        self.cell_width = self.width/float(self.columns)

    def add_cell(self, cell):
        cell.width = self.cell_width
        if cell.value.__class__ == PdfTable:
            cell.value.width = cell.width
            cell.value.cell_width = cell.width / float(cell.value.columns)

        if cell.colspan > 1:
            colspan_tot = sum([x.colspan for x in self.cells])
            colspan_tot += cell.colspan
            # if colspan_tot % self.columns != 0:
            #    raise Exception('Colspan incompatível')
        self.cells.append(cell)

    def render(self):
        colspan_tot = sum([x.colspan for x in self.cells])
        if colspan_tot % self.columns != 0:
            raise Exception('O número de celulas adicionadas é incompleto')

        style = []
        data = []
        linha = []
        colspan_tot = 0
        i = j = 0

        for cell in self.cells:
            colspan_tot += cell.colspan
            style += cell.style(j, i)
            j += 1

            if isinstance(cell.value, PdfTable):
                linha.append(cell.value.render())
            else:
                linha.append(cell.value)
                if cell.colspan > 1:
                    for xi in range(1, cell.colspan):
                        linha.append('')
                        style += cell.style(j, i, colspan=False)
                        j += 1

            if colspan_tot % self.columns == 0:
                data.append(linha)
                colspan_tot = 0
                linha = []
                j = 0
                i += 1

        t = Table(data, colWidths=[self.cell_width for
                                   k in range(self.columns)])
        t.setStyle(TableStyle(style))
        return t


class PdfCell(object):

    def __init__(self, value, colspan=1):
        self.width = 1
        self.value = value
        self.colspan = colspan
        self.background_color = colors.white
        self.text_color = colors.black
        self.font_size = 5
        self.bold = False
        self.border_width = 1
        self.border_color = colors.black

    def style(self, i, j, colspan=True):
        span = []
        if self.colspan > 1 and colspan:
            span = [('SPAN', (i, j), (i+self.colspan-1, j))]
        if not self.border_width == 0:
            span += [('INNERGRID', (i, j), (i, j), self.border_width,
                      self.border_color),
                     ('BOX', (i, j), (i, j), self.border_width,
                      self.border_color)]
        return span + [
            ('BACKGROUND', (i, j), (i, j), self.background_color),
            ('TEXTCOLOR', (i, j), (i, j), self.text_color),
            ('TOPPADDING', (i, j), (i, j), 3 if
                isinstance(self.value, str) else 0),
            ('LEFTPADDING', (i, j), (i, j), 5 if
                isinstance(self.value, str) else 0),
            ('RIGHTPADDING', (i, j), (i, j), 5 if
                isinstance(self.value, str) else 0),
            ('BOTTOMPADDING', (i, j), (i, j), 3 if
                isinstance(self.value, str) else 0),
            ('FONTSIZE', (i, j), (i, j), self.font_size),
        ]


if __name__ == '__main__':

    table = PdfTable(columns=30, width=(20 * INCH)*1.7)

    table2 = PdfTable(columns=12)

    table2.add_cell(PdfCell('RECEBEMOS DE ISOCOMPÓSITOS EIRELI ME OS PRODUTOS \
E/OU SERVIÇOS CONSTANTES DA NOTA FISCAL ELETRÔNICA INDICADA AO LADO',
                    colspan=12))
    table2.add_cell(PdfCell('Data de Recebimento', colspan=2))
    table2.add_cell(PdfCell('Assinatura', colspan=10))

    table.add_cell(PdfCell(table2, colspan=10))
    table.add_cell(PdfCell(table2, colspan=20))

    table = table.render()

    doc = SimpleDocTemplate("ola.pdf", pagesize=A4, leftMargin=0,
                            rightMargin=0, topMargin=0, bottomMargin=0)
    doc.build([table])
