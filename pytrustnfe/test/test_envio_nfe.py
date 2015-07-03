# coding=utf-8

'''
Created on 01/07/2015

@author: danimar
'''
import unittest
from pytrustnfe.xml.DynamicXml import DynamicXml


class test_envio(unittest.TestCase):

    def test_envio_nfe(self):
        t = DynamicXml('enviNFe')
        t(versao="3.10")
        t.idLote = "1"
        t.indSinc = "1"
        t.NFe.infNFe(versao="3.10", Id="NFe123")
        t.NFe.infNFe.ide.cUF = '43'
        t.NFe.infNFe.ide.cNF = '12345678'
        t.NFe.infNFe.ide.natOp = u'Venda de produção'
        t.NFe.infNFe.ide.indPag = '1'
        t.NFe.infNFe.ide.mod = '55'
        t.NFe.infNFe.ide.serie = '49'
        t.NFe.infNFe.ide.nNF = '9'
        t.NFe.infNFe.ide.dhEmi = '2015-06-30T15:18:05-03:00'
        t.NFe.infNFe.ide.dhSaiEnt = '2015-06-30T15:18:05-03:00'
        t.NFe.infNFe.ide.tpNF = '1'
        t.NFe.infNFe.ide.idDest = '2'
        t.NFe.infNFe.ide.cMunFG = '4321667'
        t.NFe.infNFe.ide.tpImp = '1'
        t.NFe.infNFe.ide.tpEmis = '1'
        t.NFe.infNFe.ide.cDV = '3'
        t.NFe.infNFe.ide.tpAmb = '2'
        t.NFe.infNFe.ide.finNFe = '1'
        t.NFe.infNFe.ide.indFinal = '0'
        t.NFe.infNFe.ide.indPres = '0'
        t.NFe.infNFe.ide.procEmi = '0'
        t.NFe.infNFe.ide.verProc = 'Odoo Brasil 8.0'

        # Emitente
        t.NFe.infNFe.emit.CNPJ = '02261542000143'
        t.NFe.infNFe.emit.xNome = 'Trust-Code'
        t.NFe.infNFe.emit.xFant = 'Trust-Code'
        t.NFe.infNFe.emit.enderEmit.xLgr = 'Rua severiano rodrigues'
        t.NFe.infNFe.emit.enderEmit.nro = '1092'
        t.NFe.infNFe.emit.enderEmit.xBairro = 'Santa Rita'
        t.NFe.infNFe.emit.enderEmit.cMun = '4321667'
        t.NFe.infNFe.emit.enderEmit.xMun = 'Tres Cachoeiras'
        t.NFe.infNFe.emit.enderEmit.UF = 'RS'
        t.NFe.infNFe.emit.enderEmit.CEP = '95099190'
        t.NFe.infNFe.emit.enderEmit.cPais = '1058'
        t.NFe.infNFe.emit.enderEmit.xPais = 'Brasil'
        t.NFe.infNFe.emit.enderEmit.Fone = '15551238069'
        t.NFe.infNFe.emit.IE = '3220014803'
        t.NFe.infNFe.emit.CRT = '3'

        # Destinatario
        t.NFe.infNFe.dest.CNPJ = '77311846000177'
        t.NFe.infNFe.dest.xNome = 'Akretion'
        t.NFe.infNFe.dest.enderEmit.xLgr = 'Rua severiano rodrigues'
        t.NFe.infNFe.dest.enderEmit.nro = '47'
        t.NFe.infNFe.dest.enderEmit.xBairro = 'Santa Rita'
        t.NFe.infNFe.dest.enderEmit.cMun = '3304557'
        t.NFe.infNFe.dest.enderEmit.xMun = 'Rio de Janeiro'
        t.NFe.infNFe.dest.enderEmit.UF = 'RJ'
        t.NFe.infNFe.dest.enderEmit.CEP = '20081000'
        t.NFe.infNFe.dest.enderEmit.cPais = '1058'
        t.NFe.infNFe.dest.enderEmit.xPais = 'Brasil'
        t.NFe.infNFe.dest.enderEmit.Fone = '2125162954'
        t.NFe.infNFe.dest.indIEDest = '9'
        t.NFe.infNFe.dest.email = 'danimar@trustcode.com.br'

        t.NFe.infNFe.det[0](nItem="1")
        t.NFe.infNFe.det[0].prod.cProd = 'A6679'
        t.NFe.infNFe.det[0].prod.cEAN = '1234567890'
        t.NFe.infNFe.det[0].prod.xProd = 'iPod'
        t.NFe.infNFe.det[0].prod.NCM = '84716053'
        t.NFe.infNFe.det[0].prod.CFOP = '6101'
        t.NFe.infNFe.det[0].prod.uCom = 'UN'
        t.NFe.infNFe.det[0].prod.qCom = '1.0'
        t.NFe.infNFe.det[0].prod.vUnCom = '22.90'
        t.NFe.infNFe.det[0].prod.vProd = '22.90'
        t.NFe.infNFe.det[0].prod.cEANTrib = ''
        t.NFe.infNFe.det[0].prod.uTrib = 'UN'
        t.NFe.infNFe.det[0].prod.qTrib = '1.00'
        t.NFe.infNFe.det[0].prod.vUnTrib = '22.90'
        t.NFe.infNFe.det[0].prod.indTot = '1'

        t.NFe.infNFe.det[0].imposto.ICMS.ICMS00.orig = '0'
        t.NFe.infNFe.det[0].imposto.ICMS.ICMS00.CST = '00'
        t.NFe.infNFe.det[0].imposto.ICMS.ICMS00.modBC = '0'
        t.NFe.infNFe.det[0].imposto.ICMS.ICMS00.vBC = '22.90'
        t.NFe.infNFe.det[0].imposto.ICMS.ICMS00.pICMS = '18.00'
        t.NFe.infNFe.det[0].imposto.ICMS.ICMS00.vICMS = '4.12'

        print t.render(pretty_print=True)