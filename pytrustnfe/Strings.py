# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


CONSULTA_CADASTRO_COMPLETA = '<?xml version="1.0" encoding="utf-8"?>'\
        '<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope">'\
        '<soap:Header>'\
        '<nfeCabecMsg xmlns="http://www.portalfiscal.inf.br/nfe/wsdl/CadConsultaCadastro2">'\
        '<cUF>35</cUF><versaoDados>2.00</versaoDados>'\
        '</nfeCabecMsg>'\
        '</soap:Header>'\
        '<soap:Body>'\
        '<nfeDadosMsg xmlns="http://www.portalfiscal.inf.br/nfe/wsdl/CadConsultaCadastro2">'\
        '<ConsCad xmlns="http://www.portalfiscal.inf.br/nfe" versao="2.00">'\
        '<infCons><xServ>CONS-CAD</xServ><UF>SP</UF><IE>606081249112</IE></infCons>'\
        '</ConsCad></nfeDadosMsg>'\
        '</soap:Body>'\
        '</soap:Envelope>'

RETORNO_CONSULTA = '<?xml version="1.0" encoding="utf-8"?>'\
        '<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">'\
        '<soap:Header><nfeCabecMsg xmlns="http://www.portalfiscal.inf.br/nfe/wsdl/CadConsultaCadastro2">'\
        '<cUF>35</cUF><versaoDados>2.00</versaoDados></nfeCabecMsg>'\
        '</soap:Header><soap:Body>'\
        '<consultaCadastro2Result xmlns="http://www.portalfiscal.inf.br/nfe/wsdl/CadConsultaCadastro2">'\
        '<retConsCad versao="2.00" xmlns="http://www.portalfiscal.inf.br/nfe">'\
        '<infCons><verAplic>SP_NFE_PL_008f</verAplic><cStat>111</cStat>'\
        '<xMotivo>Consulta cadastro com uma ocorrência</xMotivo><UF>SP</UF>'\
        '<IE>606081249112</IE><dhCons>2015-06-17T14:54:23-03:00</dhCons><cUF>35</cUF>'\
        '<infCad><IE>606081249112</IE><CNPJ>02198926000169</CNPJ><UF>SP</UF><cSit>1</cSit>'\
        '<indCredNFe>1</indCredNFe><indCredCTe>4</indCredCTe><xNome>C. R. TUNUSSI &amp; CIA. LTDA</xNome>'\
        '<xRegApur>NORMAL - REGIME PERIÓDICO DE APURAÇÃO</xRegApur><CNAE>2825900</CNAE>'\
        '<dIniAtiv>1997-11-17</dIniAtiv><dUltSit>1997-11-17</dUltSit><ender>'\
        '<xLgr>RUA JOSE NICOLAU LUX</xLgr><nro>432</nro>'\
        '<xBairro>CONJUNTO HABITACIONAL FRANCISCO DE CILLO (INOCOOP)</xBairro><cMun>3545803</cMun>'\
        '<xMun>SANTA BARBARA D''OESTE</xMun><CEP>13457162</CEP></ender></infCad></infCons>'\
        '</retConsCad></consultaCadastro2Result></soap:Body></soap:Envelope>'
