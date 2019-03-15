AC = '12'
AL = '27'
AM = '13'
AP = '16'
BA = '29'
CE = '23'
DF = '53'
ES = '32'
GO = '52'
MA = '21'
MG = '31'
MS = '50'
MT = '51'
PA = '15'
PB = '25'
PE = '26'
PI = '22'
PR = '41'
RJ = '33'
RN = '24'
RO = '11'
RR = '14'
RS = '43'
SC = '42'
SE = '28'
SP = '35'
TO = '17'

PRODUCAO = '1'
HOMOLOGACAO = '2'

URLS = {
    PRODUCAO: {
        AC: 'http://www.sefaznet.ac.gov.br/nfce/qrcode?',
        AL: 'http://nfce.sefaz.al.gov.br/QRCode/consultarNFCe.jsp?',
        AM: 'http://sistemas.sefaz.am.gov.br/nfceweb/consultarNFCe.jsp?',
        AP: 'https://www.sefaz.ap.gov.br/nfce/nfcep.php?',
        BA: 'http://nfe.sefaz.ba.gov.br/servicos/nfce/qrcode.aspx?',
        DF: 'http://www.fazenda.df.gov.br/nfce/qrcode?',
        GO: 'http://nfe.sefaz.go.gov.br/nfeweb/sites/nfce/danfeNFCe?',
        MA: 'http://nfce.sefaz.ma.gov.br/portal/consultarNFCe.jsp?',
        MS: 'http://www.dfe.ms.gov.br/nfce/qrcode?',
        MT: 'http://www.sefaz.mt.gov.br/nfce/consultanfce?',
        PA: 'https://appnfc.sefa.pa.gov.br/portal/view/consultas/nfce/nfceForm.seam?',  # noqa
        PB: 'http://www.receita.pb.gov.br/nfce?',
        PE: 'http://nfce.sefaz.pe.gov.br/nfce/consulta?',
        PI: 'http://www.sefaz.pi.gov.br/nfce/qrcode?',
        PR: 'http://www.fazenda.pr.gov.br/nfce/consulta?',
        RJ: 'http://www4.fazenda.rj.gov.br/consultaNFCe/QRCode?',
        RN: 'http://nfce.set.rn.gov.br/consultarNFCe.aspx?',
        RO: 'http://www.nfce.sefin.ro.gov.br/consultanfce/consulta.jsp?',
        RR: 'https://www.sefaz.rr.gov.br/nfce/servlet/qrcode?',
        RS: 'https://www.sefaz.rs.gov.br/NFCE/NFCE-COM.aspx?',
        SE: 'http://www.nfce.se.gov.br/nfce/qrcode?',
        SP: 'https://www.nfce.fazenda.sp.gov.br/qrcode?',
        TO: 'http://www.sefaz.to.gov.br/nfce/qrcode?',
    },
    HOMOLOGACAO: {
        AC: 'http://www.hml.sefaznet.ac.gov.br/nfce/qrcode?',
        AL: 'http://nfce.sefaz.al.gov.br/QRCode/consultarNFCe.jsp?',
        AM: 'http://homnfce.sefaz.am.gov.br/nfceweb/consultarNFCe.jsp?',
        AP: 'https://www.sefaz.ap.gov.br/nfcehml/nfce.php?',
        BA: 'http://hnfe.sefaz.ba.gov.br/servicos/nfce/qrcode.aspx?',
        DF: 'http://www.fazenda.df.gov.br/nfce/qrcode?',
        GO: 'http://homolog.sefaz.go.gov.br/nfeweb/sites/nfce/danfeNFCe?',
        MA: 'http://homologacao.sefaz.ma.gov.br/portal/consultarNFCe.jsp?',
        MS: 'http://www.dfe.ms.gov.br/nfce/qrcode?',
        MT: 'http://homologacao.sefaz.mt.gov.br/nfce/consultanfce?',
        PA: 'https://appnfc.sefa.pa.gov.br/portal-homologacao/view/consultas/nfce/nfceForm.seam?',  # noqa
        PB: 'http://www.receita.pb.gov.br/nfcehom?',
        PE: 'http://nfcehomolog.sefaz.pe.gov.br/nfce/consulta?',
        PI: 'http://www.sefaz.pi.gov.br/nfce/qrcode?',
        PR: 'http://www.fazenda.pr.gov.br/nfce/consulta?',
        RJ: 'http://www4.fazenda.rj.gov.br/consultaNFCe/QRCode?',
        RN: 'http://hom.nfce.set.rn.gov.br/consultarNFCe.aspx?',
        RO: 'http://200.174.88.103:8080/nfce/servlet/qrcode?',
        RR: 'https://www.sefaz.rr.gov.br/nfce/servlet/qrcode?',
        RS: 'https://www.sefaz.rs.gov.br/NFCE/NFCE-COM.aspx?',
        SE: 'http://www.hom.nfe.se.gov.br/nfce/qrcode?',
        SP: 'https://www.homologacao.nfce.fazenda.sp.gov.br/qrcode?',
        TO: 'http://homologacao.sefaz.to.gov.br/nfce/qrcode?',
    }
}

URLS_EXIBICAO = {
    PRODUCAO: {
        AC: 'www.sefaznet.ac.gov.br/nfce/consulta',
        AL: 'www.sefaz.al.gov.br/nfce/consulta',
        AM: 'www.sefaz.am.gov.br/nfce/consulta',
        AP: 'www.sefaz.ap.gov.br/nfce/consulta',
        BA: 'http://www.sefaz.ba.gov.br/nfce/consulta',
        CE: 'www.sefaz.ce.gov.br/nfce/consulta',
        DF: 'www.fazenda.df.gov.br/nfce/consulta',
        ES: 'www.sefaz.es.gov.br/nfce/consulta',
        GO: 'www.sefaz.go.gov.br/nfce/consulta',
        MA: 'www.sefaz.ma.gov.br/nfce/consulta',
        MS: 'www.dfe.ms.gov.br/nfce/consulta',
        MT: 'www.sefaz.mt.gov.br/nfce/consulta',
        MG: 'www.fazenda.mg.gov.br/nfce/consulta',
        PA: 'www.sefa.pa.gov.br/nfce/consulta',
        PB: 'www.receita.pb.gov.br/nfce/consulta',
        PE: 'nfce.sefaz.pe.gov.br/nfce/consulta',
        PI: 'www.sefaz.pi.gov.br/nfce/consulta',
        PR: 'http://www.fazenda.pr.gov.br/nfce/consulta',
        RJ: 'www.fazenda.rj.gov.br/nfce/consulta',
        RN: 'www.set.rn.gov.br/nfce/consulta',
        RO: 'www.sefin.ro.gov.br/nfce/consulta',
        RR: 'www.sefaz.rr.gov.br/nfce/consulta',
        RS: 'www.sefaz.rs.gov.br/nfce/consulta',
        SE: 'http://www.nfce.se.gov.br/nfce/consulta',
        SP: 'https://www.nfce.fazenda.sp.gov.br/consulta',
        TO: 'www.sefaz.to.gov.br/nfce/consulta',
    },
    HOMOLOGACAO: {
        AC: 'www.sefaznet.ac.gov.br/nfce/consulta',
        AL: 'www.sefaz.al.gov.br/nfce/consulta',
        AM: 'www.sefaz.am.gov.br/nfce/consulta',
        AP: 'www.sefaz.ap.gov.br/nfce/consulta',
        BA: 'http://hinternet.sefaz.ba.gov.br/nfce/consulta',
        CE: 'www.sefaz.ce.gov.br/nfce/consulta',
        DF: 'www.fazenda.df.gov.br/nfce/consulta',
        ES: 'www.sefaz.es.gov.br/nfce/consulta',
        GO: 'www.sefaz.go.gov.br/nfce/consulta',
        MA: 'www.sefaz.ma.gov.br/nfce/consulta',
        MS: 'www.dfe.ms.gov.br/nfce/consulta',
        MT: 'www.sefaz.mt.gov.br/nfce/consulta',
        MG: 'www.fazenda.mg.gov.br/nfce/consulta',
        PA: 'www.sefa.pa.gov.br/nfce/consulta',
        PB: 'www.receita.pb.gov.br/nfcehom',
        PE: 'nfce.sefaz.pe.gov.br/nfce/consulta',
        PI: 'www.sefaz.pi.gov.br/nfce/consulta',
        PR: 'http://www.fazenda.pr.gov.br/nfce/consulta',
        RJ: 'www.fazenda.rj.gov.br/nfce/consulta',
        RN: 'www.set.rn.gov.br/nfce/consulta',
        RO: 'www.sefin.ro.gov.br/nfce/consulta',
        RR: 'www.sefaz.rr.gov.br/nfce/consulta',
        RS: 'www.sefaz.rs.gov.br/nfce/consulta',
        SE: 'http://www.hom.nfe.se.gov.br/nfce/consulta',
        SP: 'https://www.homologacao.nfce.fazenda.sp.gov.br/consulta',
        TO: 'www.sefaz.to.gov.br/nfce/consulta',
    }
}


def url_qrcode(estado, ambiente):
    return URLS[ambiente][estado]


def url_qrcode_exibicao(estado, ambiente):
    return URLS_EXIBICAO[ambiente][estado]
