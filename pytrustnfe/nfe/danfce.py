# -*- coding: utf-8 -*-
# © 2017 Johny Chen Jy, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import re
from textwrap import wrap
from io import BytesIO

from reportlab.lib import utils
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm, mm
from reportlab.graphics.barcode import qr
from reportlab.graphics import renderPDF
from reportlab.graphics.shapes import Drawing
from reportlab.platypus import Table, TableStyle, Paragraph, Image
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle


def format_cnpj_cpf(value):
    if len(value) < 12:  # CPF
        cValue = '%s.%s.%s-%s' % (value[:-8], value[-8:-5],
                                  value[-5:-2], value[-2:])
    else:
        cValue = '%s.%s.%s/%s-%s' % (value[:-12], value[-12:-9],
                                     value[-9:-6], value[-6:-2], value[-2:])
    return cValue


def getdateUTC(cDateUTC):
    cDt = cDateUTC[0:10].split('-')
    cDt.reverse()
    return '/'.join(cDt), cDateUTC[11:16]


def format_number(cNumber, precision=0, group_sep='.', decimal_sep=','):
    if cNumber:
        number = float(cNumber)
        return ("{:,." + str(precision) + "f}").format(number).\
            replace(",", "X").replace(".", ",").replace("X", ".")
    return ""


def tagtext(oNode=None, cTag=None):
    try:
        xpath = ".//{http://www.portalfiscal.inf.br/nfe}%s" % (cTag)
        cText = oNode.find(xpath).text
    except:
        cText = ''
    return cText


def get_image(path, width=1 * cm):
    img = utils.ImageReader(path)
    iw, ih = img.getSize()
    aspect = ih / float(iw)
    return Image(path, width=width, height=(width * aspect))


def format_telefone(telefone):
    telefone = re.sub('[^0-9]', '', telefone)
    if len(telefone) == 10:
        telefone = '(%s) %s-%s' % (telefone[0:2],
                                   telefone[2:6],
                                   telefone[6:])
    elif len(telefone) == 11:
        telefone = '(%s) %s-%s' % (telefone[0:2],
                                   telefone[2:7],
                                   telefone[7:])
    return telefone


class danfce(object):

    def __init__(self, list_xml, logo=None, timezone=None):

        self.current_font_size = 7
        self.current_font_name = 'NimbusSanL-Regu'

        self.max_height = 840
        self.min_height = 1
        self.min_width = 5
        self.max_width = 200
        self.current_height = 840

        self.oPDF_IO = BytesIO()
        self.canvas = canvas.Canvas(self.oPDF_IO, pagesize=(7.2 * cm, 30 * cm))
        self.canvas.setTitle('DANFCE')
        self.canvas.setLineWidth(.5)
        self.canvas.setFont(self.current_font_name, self.current_font_size)

        self.list_xml = list_xml
        self.logo = logo

        self.nfce_generate()

    def ide_emit(self, oXML=None):

        elem_emit = oXML.find(".//{http://www.portalfiscal.inf.br/nfe}emit")

        # Razão Social emitente
        nomeEmpresa = tagtext(oNode=elem_emit, cTag='xFant')
        self.drawTitle(nomeEmpresa, 10)

        if self.logo:
            img = get_image(self.logo, width=10 * mm)
            img.drawOn(self.canvas, 5, 830)

        cEnd = tagtext(oNode=elem_emit, cTag="xNome") + '<br />'
        cEnd += "CNPJ: %s  " % (format_cnpj_cpf(
            tagtext(oNode=elem_emit, cTag='CNPJ')))
        cEnd += "IE: %s" % (tagtext(oNode=elem_emit, cTag="IE")) + '<br />'
        cEnd += tagtext(oNode=elem_emit, cTag='xLgr') + ', ' + tagtext(
            oNode=elem_emit, cTag='nro') + ' - '
        cEnd += tagtext(oNode=elem_emit, cTag='xBairro') + '<br />' + tagtext(
            oNode=elem_emit, cTag='xMun') + ' - '
        cEnd += tagtext(oNode=elem_emit, cTag='UF') + ' - ' + tagtext(
            oNode=elem_emit, cTag='CEP') + '<br />'
        cEnd += 'Fone: ' + format_telefone(tagtext(
            oNode=elem_emit, cTag='fone'))

        self._drawCenteredParagraph(cEnd)
        self.drawLine()

    def danfce_information(self):
        self.drawTitle(
            "DANFE NFC-e - Documento Auxiliar da Nota Fiscal de",
            7, 'NimbusSanL-Bold')

        self.drawTitle("Consumidor Eletrônica", 7, 'NimbusSanL-Bold')

        self.drawString(
            "NFC-e não permite aproveitamento de crédito de ICMS", True)
        self.drawLine()

    def produtos(self, oXML=None, el_det=None, oPaginator=None,
                 list_desc=None, list_cod_prod=None):

        rows = [['Cód', 'Descrição', 'Qtde', 'Un', 'Unit.', 'Total']]
        colWidths = (25, 90, 15, 15, 25, 25)
        rowHeights = [7]

        for id in range(oPaginator[0], oPaginator[1]):

            item = el_det[id]
            el_prod = item.find(".//{http://www.portalfiscal.inf.br/nfe}prod")

            cod = tagtext(oNode=el_prod, cTag='cProd')
            descricao = tagtext(oNode=el_prod, cTag='xProd')
            descricao = (descricao[:20] + '..') if len(descricao) > 20 else descricao
            Un = tagtext(oNode=el_prod, cTag='uCom')
            Un = (Un[:2]) if len(Un) > 2 else Un
            qtde = format_number(tagtext(oNode=el_prod, cTag='qCom'),
                                 precision=2)
            vl_unit = format_number(tagtext(oNode=el_prod, cTag='vUnCom'),
                                    precision=2)
            vl_total = format_number(
                tagtext(oNode=el_prod, cTag='vProd'), precision=2)

            new_row = [cod, descricao, qtde, Un, vl_unit, vl_total]

            rows.append(new_row)
            rowHeights.append(self.current_font_size + 2)

        self._draw_product_table(rows, colWidths, rowHeights)

    def _draw_product_table(self, rows, colWidths, rowHeights):
        table = Table(rows, colWidths, tuple(rowHeights))
        table.setStyle(TableStyle([
            ('FONTSIZE', (0, 0), (-1, -1), 7),
            ('FONT', (0, 1), (-1, -1), 'NimbusSanL-Regu'),
            ('FONT', (0, 0), (-1, 0), 'NimbusSanL-Bold'),
            ('ALIGN', (0, 0), (-1, 0), "LEFT"),
            ('ALIGN', (1, 0), (-1, 0), "LEFT"),
            ('ALIGN', (2, 0), (-1, 0), "CENTER"),
            ('ALIGN', (3, 0), (-1, 0), "CENTER"),
            ('ALIGN', (0, 1), (-1, -1), "LEFT"),
            ('ALIGN', (1, 1), (-1, -1), "LEFT"),
            ('ALIGN', (2, 1), (-1, -1), "CENTER"),
            ('ALIGN', (3, 1), (-1, -1), "CENTER"),
        ]))

        w, h = table.wrapOn(self.canvas, 200, 450)
        table.drawOn(self.canvas, 0, self.current_height - (h * 1.2))
        self.current_height -= (h * 1.1)

    def totais(self, oXML=None):
        # Impostos
        el_total = oXML.find(".//{http://www.portalfiscal.inf.br/nfe}total")

        total_tributo = format_number(
            tagtext(oNode=el_total, cTag='vTotTrib'), precision=2)
        valor_total = format_number(
            tagtext(oNode=el_total, cTag='vProd'), precision=2)
        desconto = format_number(
            tagtext(oNode=el_total, cTag='vDesc'), precision=2)
        valor_a_pagar = format_number(
            tagtext(oNode=el_total, cTag='vNF'), precision=2)
        el_pag = oXML.find(".//{http://www.portalfiscal.inf.br/nfe}pag")
        troco = tagtext(oNode=el_pag, cTag="vTroco")

        payment_method_list = {'01': 'Dinheiro',
                               '02': 'Cheque',
                               '03': 'Cartão de Crédito',
                               '04': 'Cartão de Débito',
                               "05": "Crédito Loja",
                               '10': 'Vale Alimentação',
                               '11': 'Vale Refeição',
                               '12': 'Vale Presente',
                               '13': 'Vale Combustível',
                               '14': 'Duplicata Mercantil',
                               '15': 'Boleto Bancario',
                               '90': 'Sem Pagamento',
                               '99': 'Outros'}
        quant_produtos = len(oXML.findall(
            ".//{http://www.portalfiscal.inf.br/nfe}det"))

        payment_methods = []
        for pagId, item in enumerate(el_pag):
            payment = []
            tipo_pagamento = tagtext(oNode=item, cTag="tPag")
            val = format_number(tagtext(oNode=item, cTag="vPag"), precision=2)

            method = payment_method_list.get(tipo_pagamento)

            payment.append(method)
            payment.append(val)
            payment_methods.append(payment)

        values = {
            'quantidade_itens': quant_produtos,
            'total_tributo': total_tributo,
            'valor_total': valor_total,
            'desconto': desconto,
            'valor_a_pagar': valor_a_pagar,
            'formas_de_pagamento': payment_methods,
            'troco': troco,
        }

        self.draw_totals_table(values)

        self.drawLine()

    def draw_totals_table(self, values):
        rowHeights = [7, 7, 7, 7, 7]
        data = [
                ['QTD.TOTAL DE ITENS', values['quantidade_itens']],
                ['VALOR TOTAL R$', values['valor_total']],
                ['DESCONTO R$', values['desconto']],
                ['VALOR A PAGAR R$', values['valor_a_pagar']],
                ['FORMA DE PAGAMENTO', 'VALOR PAGO R$'],
               ]

        for item in values['formas_de_pagamento']:
            data.append([item[0], item[1]])
            rowHeights.append(7)
        data.append(['TROCO', format_number(values['troco'], precision=2)])
        rowHeights.append(7)

        table2 = Table(data, colWidths=(150, 50), rowHeights=tuple(rowHeights))
        table2.setStyle(TableStyle([
            ('FONTSIZE', (0, 0), (-1, -1), 7),
            ('FONT', (0, 0), (1, -1), 'NimbusSanL-Regu'),
            ('FONT', (0, 4), (1, 4), 'NimbusSanL-Bold'),
            ('ALIGN', (1, 0), (1, -1), "RIGHT")
        ]))
        w, h = table2.wrapOn(self.canvas, 200, 450)
        table2.drawOn(self.canvas, 0, self.current_height - (h * 1.1))
        self.current_height -= h

    def inf_authentication(self, oXML=None):
        el_infNFe = oXML.find(".//{http://www.portalfiscal.inf.br/nfe}infNFe")
        # n nfce, serie e data de solicitacao
        el_ide = oXML.find(".//{http://www.portalfiscal.inf.br/nfe}ide")

        el_NFeSupl = oXML.find(
            ".//{http://www.portalfiscal.inf.br/nfe}infNFeSupl")

        el_dest = el_infNFe.find(".//{http://www.portalfiscal.inf.br/nfe}dest")
        # chave, n protocolo, data autorizacao
        el_prot_nfe = oXML.find(
            ".//{http://www.portalfiscal.inf.br/nfe}protNFe")

        el_infAdic = oXML.find(
            ".//{http://www.portalfiscal.inf.br/nfe}infAdic")

        url_chave = tagtext(oNode=el_NFeSupl, cTag='urlChave')
        access_key = tagtext(oNode=el_prot_nfe, cTag="chNFe")

        frase_chave_acesso = 'Consulte pela Chave de Acesso em:<br />\
%s<br />%s' % (url_chave, access_key)

        qrcode = tagtext(oNode=el_NFeSupl, cTag='qrCode')

        cnpj = tagtext(oNode=el_dest, cTag='CNPJ')
        cpf = tagtext(oNode=el_dest, cTag='CPF')
        if cnpj:
            cnpj_cpf = format_cnpj_cpf(cnpj)
            cnpj_cpf = "CONSUMIDOR CNPJ: %s" % (cnpj)
        elif cpf:
            cnpj_cpf = format_cnpj_cpf(cpf)
            cnpj_cpf = "CONSUMIDOR CPF: %s" % (cpf)
        else:
            cnpj_cpf = u"CONSUMIDOR NÃO IDENTIFICADO"

        nNFC = tagtext(oNode=el_ide, cTag="nNF")
        serie = tagtext(oNode=el_ide, cTag='serie')

        dataSolicitacao = getdateUTC(tagtext(oNode=el_ide, cTag="dhEmi"))
        dataSolicitacao = dataSolicitacao[0] + "  " + dataSolicitacao[1]

        numProtocolo = tagtext(oNode=el_prot_nfe, cTag="nProt")

        dataAutorizacao = getdateUTC(tagtext(oNode=el_prot_nfe,
                                             cTag='dhRecbto'))
        dataAutorizacao = dataAutorizacao[0] + "  " + dataAutorizacao[1]

        text = u"%s <br />%s <br />NFC-e nº%s  Série %s  %s<br />\
Protocolo de autorização: %s<br />Data de autorização %s<br />\
" % (frase_chave_acesso, cnpj_cpf, nNFC, serie, dataSolicitacao,
            numProtocolo, dataAutorizacao)

        self._drawCenteredParagraph(text)

        self.draw_qr_code(qrcode)

        infAdFisco = tagtext(oNode=el_infAdic, cTag='infAdFisco')
        self._drawCenteredParagraph(infAdFisco)

        infCpl = tagtext(oNode=el_infAdic, cTag='infCpl')
        self._drawCenteredParagraph(infCpl)

    def _drawCenteredParagraph(self, text):

        style = ParagraphStyle(
            name='Normal',
            fontName='NimbusSanL-Regu',
            fontSize=7,
            alignment=TA_CENTER,
            leading=7,
        )

        paragraph = Paragraph(text, style=style)
        w, h = paragraph.wrapOn(self.canvas, 180, 300)
        paragraph.drawOn(self.canvas, 10, self.current_height - h)
        self.current_height -= (h*1.1)

    def drawString(self, string, centered=False):
        if centered:
            self.canvas.drawCentredString(
                self.max_width / 2, self.current_height, string)
            self.current_height -= self.current_font_size
        else:
            self.canvas.drawString(self.min_width, self.current_height, string)
            self.current_height -= self.current_font_size

    def drawTitle(self, string, size, font='NimbusSanL-Regu'):
        self.canvas.setFont(font, size)
        self.canvas.drawCentredString(
            self.max_width / 2, self.current_height, string)
        self.current_height -= self.current_font_size
        self.canvas.setFont(self.current_font_name, self.current_font_size)

    def drawLine(self):
        self.canvas.line(self.min_width, self.current_height,
                         self.max_width, self.current_height)
        self.current_height -= self.current_font_size

    def draw_qr_code(self, string):
        qr_code = qr.QrCodeWidget(string)
        drawing = Drawing(23 * mm, 23 * mm)
        drawing.add(qr_code)
        renderPDF.draw(drawing, self.canvas, 20 * mm, self.current_height - 85)
        self.current_height -= 85

    def newpage(self):
        self.current_height = self.max_height
        self.Page += 1
        self.canvas.showPage()

    def nfce_generate(self):
        for oXML in self.list_xml:
            oXML_cobr = oXML.find(
                ".//{http://www.portalfiscal.inf.br/nfe}cobr")

            self.NrPages = 1
            self.Page = 1

            # Calculando total linhas usadas para descrições dos itens
            # Com bloco fatura, apenas 29 linhas para itens na primeira folha
            nNr_Lin_Pg_1 = 34 if oXML_cobr is None else 30
            # [ rec_ini , rec_fim , lines , limit_lines ]
            oPaginator = [[0, 0, 0, nNr_Lin_Pg_1]]
            el_det = oXML.findall(".//{http://www.portalfiscal.inf.br/nfe}det")
            if el_det is not None:
                list_desc = []
                list_cod_prod = []
                nPg = 0
                for nId, item in enumerate(el_det):
                    el_prod = item.find(
                        ".//{http://www.portalfiscal.inf.br/nfe}prod")
                    infAdProd = item.find(
                        ".//{http://www.portalfiscal.inf.br/nfe}infAdProd")

                    list_ = wrap(tagtext(oNode=el_prod, cTag='xProd'), 56)
                    if infAdProd is not None:
                        list_.extend(wrap(infAdProd.text, 56))
                    list_desc.append(list_)

                    list_cProd = wrap(tagtext(oNode=el_prod, cTag='cProd'), 14)
                    list_cod_prod.append(list_cProd)

                    # Nr linhas necessárias p/ descrição item
                    nLin_Itens = len(list_)

                    if (oPaginator[nPg][2] + nLin_Itens) >= oPaginator[nPg][3]:
                        oPaginator.append([0, 0, 0, 77])
                        nPg += 1
                        oPaginator[nPg][0] = nId
                        oPaginator[nPg][1] = nId + 1
                        oPaginator[nPg][2] = nLin_Itens
                    else:
                        # adiciona-se 1 pelo funcionamento de xrange
                        oPaginator[nPg][1] = nId + 1
                        oPaginator[nPg][2] += nLin_Itens

                self.NrPages = len(oPaginator)   # Calculando nr. páginas

            self.ide_emit(oXML=oXML)
            # self.destinatario(oXML=oXML)
            self.danfce_information()

            self.produtos(oXML=oXML, el_det=el_det, oPaginator=oPaginator[0],
                          list_desc=list_desc, list_cod_prod=list_cod_prod)

            self.drawLine()

            self.totais(oXML=oXML)

            self.inf_authentication(oXML=oXML)

            # Gera o restante das páginas do XML
            for oPag in oPaginator[1:]:
                if oPag:
                    self.newpage()
                    self.ide_emit(oXML=oXML)
                    # self.destinatario(oXML=oXML)
                    self.produtos(oXML=oXML, el_det=el_det, oPaginator=oPag,
                                  list_desc=list_desc,
                                  list_cod_prod=list_cod_prod)
                    self.totais(oXML=oXML)
                    self.inf_authentication(oXML=oXML)

            self.newpage()

        self.canvas.save()

    def writeto_pdf(self, fileObj):
        pdf_out = self.oPDF_IO.getvalue()
        self.oPDF_IO.close()
        fileObj.write(pdf_out)
