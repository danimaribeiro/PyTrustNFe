# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

WS_NFE_AUTORIZACAO = 'NfeAutorizacao'
WS_NFE_RET_AUTORIZACAO = 'NfeRetAutorizacao'
WS_NFE_CANCELAMENTO = 'RecepcaoEventoCancelamento'
WS_NFE_INUTILIZACAO = 'NfeInutilizacao'
WS_NFE_CONSULTA = 'NfeConsultaProtocolo'
WS_NFE_SITUACAO = 'NfeStatusServico'
WS_NFE_CADASTRO = 'NfeConsultaCadastro'

WS_NFCE_AUTORIZACAO = 'NfeAutorizacao'
WS_NFCE_RET_AUTORIZACAO = 'NfeRetAutorizacao'
WS_NFCE_CANCELAMENTO = 'RecepcaoEventoCancelamento'
WS_NFCE_INUTILIZACAO = 'NfeInutilizacao'
WS_NFCE_CONSULTA = 'NfeConsultaProtocolo'
WS_NFCE_SITUACAO = 'NfeStatusServico'
WS_NFCE_CADASTRO = 'NfeConsultaCadastro'
WS_NFCE_RECEPCAO_EVENTO = 'RecepcaoEventoCarta'
WS_NFCE_QR_CODE = 'NfeQRCode'
WS_NFCE_RET_AUTORIZACAO = 'NFeRetAutorizacao',
WS_NFCE_CONSULTA_DESTINADAS = 'NfeConsultaDest',
WS_NFCE_DOWNLOAD = 'NfeDownloadNF',


WS_NFE_CADASTRO = 'NfeConsultaCadastro'
WS_DPEC_RECEPCAO = 'RecepcaoEventoEPEC'
WS_DPEC_CONSULTA = 8

WS_NFE_RECEPCAO_EVENTO = 'RecepcaoEventoCarta'
WS_NFE_DOWNLOAD = 'NfeDownloadNF'
WS_NFE_CONSULTA_DESTINADAS = 'NfeConsultaDest'
WS_DFE_DISTRIBUICAO = 12

NFE_AMBIENTE_PRODUCAO = 1
NFE_AMBIENTE_HOMOLOGACAO = 2
NFCE_AMBIENTE_PRODUCAO = 1
NFCE_AMBIENTE_HOMOLOGACAO = 2

NFE_MODELO = u'55'
NFCE_MODELO = u'65'

SIGLA_ESTADO = {
    '12': 'AC',
    '27': 'AL',
    '13': 'AM',
    '16': 'AP',
    '29': 'BA',
    '23': 'CE',
    '53': 'DF',
    '32': 'ES',
    '52': 'GO',
    '21': 'MA',
    '31': 'MG',
    '50': 'MS',
    '51': 'MT',
    '15': 'PA',
    '25': 'PB',
    '26': 'PE',
    '22': 'PI',
    '41': 'PR',
    '33': 'RJ',
    '24': 'RN',
    '11': 'RO',
    '14': 'RR',
    '43': 'RS',
    '42': 'SC',
    '28': 'SE',
    '35': 'SP',
    '17': 'TO',
}


def localizar_url(servico, estado, mod='55', ambiente=2):
    sigla = SIGLA_ESTADO[estado]
    ws = ESTADO_WS[sigla]
    if mod in ws:
        dominio = ws[mod][ambiente]['servidor']
        complemento = ws[mod][ambiente][servico]
    else:
        dominio = ws[ambiente]['servidor']
        complemento = ws[ambiente][servico]

    if sigla == 'RS' and servico == WS_NFE_CADASTRO:
        dominio = 'cad.sefazrs.rs.gov.br'
    if sigla in ('AC', 'RN', 'PB', 'SC') and \
       servico == WS_NFE_CADASTRO:
        dominio = 'cad.svrs.rs.gov.br'

    return "https://%s/%s" % (dominio, complemento)


def localizar_qrcode(estado, ambiente=2):
    sigla = SIGLA_ESTADO[estado]
    dominio = ESTADO_WS[sigla]['65'][ambiente]['servidor']
    complemento = ESTADO_WS[sigla]['65'][ambiente][WS_NFCE_QR_CODE]
    if 'https://' in complemento:
        return complemento
    return "https://%s/%s" % (dominio, complemento)


METODO_WS = {
    WS_NFE_AUTORIZACAO: {
        'webservice': 'NfeAutorizacao',
        'metodo': 'NfeAutorizacao',
    },
    WS_NFE_RET_AUTORIZACAO: {
        'webservice': 'NfeRetAutorizacao',
        'metodo': 'NfeRetAutorizacao',
    },
    WS_NFE_INUTILIZACAO: {
        'webservice': 'NfeInutilizacao2',
        'metodo': 'nfeInutilizacaoNF2',
    },
    WS_NFE_CONSULTA: {
        'webservice': 'NfeConsulta2',
        'metodo': 'nfeConsultaNF2',
    },
    WS_NFE_SITUACAO: {
        'webservice': 'NfeStatusServico2',
        'metodo': 'nfeStatusServicoNF2',
    },
    WS_NFE_CADASTRO: {
        'webservice': 'CadConsultaCadastro2',
        'metodo': 'consultaCadastro2',
    },
    WS_NFE_RECEPCAO_EVENTO: {
        'webservice': 'RecepcaoEvento',
        'metodo': 'nfeRecepcaoEvento',
    },
    WS_NFE_DOWNLOAD: {
        'webservice': 'NfeDownloadNF',
        'metodo': 'nfeDownloadNF',
    },
    WS_NFE_CONSULTA_DESTINADAS: {
        'webservice': 'NfeConsultaDest',
        'metodo': 'nfeConsultaNFDest',
    },
    WS_DFE_DISTRIBUICAO: {
        'webservice': 'NFeDistribuicaoDFe',
        'metodo': 'nfeDistDFeInteresse'
    }
}

SVRS = {
    NFE_AMBIENTE_PRODUCAO: {
        'servidor': 'nfe.svrs.rs.gov.br',
        WS_NFE_RECEPCAO_EVENTO: 'ws/recepcaoevento/recepcaoevento.asmx',
        WS_NFE_CANCELAMENTO: 'ws/recepcaoevento/recepcaoevento.asmx',
        WS_NFE_AUTORIZACAO: 'ws/NfeAutorizacao/NfeAutorizacao.asmx',
        WS_NFE_RET_AUTORIZACAO: 'ws/NfeRetAutorizacao/NfeRetAutorizacao.asmx',
        WS_NFE_CADASTRO: 'ws/CadConsultaCadastro/CadConsultaCadastro2.asmx',
        WS_NFE_INUTILIZACAO: 'ws/nfeinutilizacao/nfeinutilizacao2.asmx',
        WS_NFE_CONSULTA: 'ws/NfeConsulta/NfeConsulta2.asmx',
        WS_NFE_SITUACAO: 'ws/NfeStatusServico/NfeStatusServico2.asmx',
    },
    NFE_AMBIENTE_HOMOLOGACAO: {
        'servidor': 'nfe-homologacao.svrs.rs.gov.br',
        WS_NFE_RECEPCAO_EVENTO: 'ws/recepcaoevento/recepcaoevento.asmx',
        WS_NFE_CANCELAMENTO: 'ws/recepcaoevento/recepcaoevento.asmx',
        WS_NFE_AUTORIZACAO: 'ws/NfeAutorizacao/NfeAutorizacao.asmx',
        WS_NFE_RET_AUTORIZACAO: 'ws/NfeRetAutorizacao/NfeRetAutorizacao.asmx',
        WS_NFE_CADASTRO: 'ws/CadConsultaCadastro/CadConsultaCadastro2.asmx',
        WS_NFE_INUTILIZACAO: 'ws/nfeinutilizacao/nfeinutilizacao2.asmx',
        WS_NFE_CONSULTA: 'ws/NfeConsulta/NfeConsulta2.asmx',
        WS_NFE_SITUACAO: 'ws/NfeStatusServico/NfeStatusServico2.asmx',
    }
}

SVAN = {
    NFE_AMBIENTE_PRODUCAO: {
        'servidor': 'www.sefazvirtual.fazenda.gov.br',
        WS_NFE_RECEPCAO_EVENTO: 'RecepcaoEvento/RecepcaoEvento.asmx',
        WS_NFE_AUTORIZACAO: 'NfeAutorizacao/NfeAutorizacao.asmx',
        WS_NFE_RET_AUTORIZACAO: 'NfeRetAutorizacao/NfeRetAutorizacao.asmx',
        WS_NFE_INUTILIZACAO: 'NfeInutilizacao2/NfeInutilizacao2.asmx',
        WS_NFE_CONSULTA: 'NfeConsulta2/NfeConsulta2.asmx',
        WS_NFE_SITUACAO: 'NfeStatusServico2/NfeStatusServico2.asmx',
        WS_NFE_DOWNLOAD: 'NfeDownloadNF/NfeDownloadNF.asmx',
    },
    NFE_AMBIENTE_HOMOLOGACAO: {
        'servidor': 'hom.sefazvirtual.fazenda.gov.br',
        WS_NFE_RECEPCAO_EVENTO: 'RecepcaoEvento/RecepcaoEvento.asmx',
        WS_NFE_AUTORIZACAO: 'NfeAutorizacao/NfeAutorizacao.asmx',
        WS_NFE_RET_AUTORIZACAO: 'NfeRetAutorizacao/NfeRetAutorizacao.asmx',
        WS_NFE_INUTILIZACAO: 'NfeInutilizacao2/NfeInutilizacao2.asmx',
        WS_NFE_CONSULTA: 'NfeConsulta2/NfeConsulta2.asmx',
        WS_NFE_SITUACAO: 'NfeStatusServico2/NfeStatusServico2.asmx',
        WS_NFE_DOWNLOAD: 'NfeDownloadNF/NfeDownloadNF.asmx',
    }
}

SCAN = {
    NFE_AMBIENTE_PRODUCAO: {
        'servidor': 'www.scan.fazenda.gov.br',
        WS_NFE_RECEPCAO_EVENTO: 'RecepcaoEvento/RecepcaoEvento.asmx',
        WS_NFE_AUTORIZACAO: 'NfeAutorizacao/NfeAutorizacao.asmx',
        WS_NFE_RET_AUTORIZACAO: 'NfeRetAutorizacao/NfeRetAutorizacao.asmx',
        WS_NFE_INUTILIZACAO: 'NfeInutilizacao2/NfeInutilizacao2.asmx',
        WS_NFE_CONSULTA: 'NfeConsulta2/NfeConsulta2.asmx',
        WS_NFE_SITUACAO: 'NfeStatusServico2/NfeStatusServico2.asmx'
    },
    NFE_AMBIENTE_HOMOLOGACAO: {
        'servidor': 'hom.nfe.fazenda.gov.br',
        WS_NFE_RECEPCAO_EVENTO: 'RecepcaoEvento/RecepcaoEvento.asmx',
        WS_NFE_AUTORIZACAO: 'NfeAutorizacao/NfeAutorizacao.asmx',
        WS_NFE_RET_AUTORIZACAO: 'NfeRetAutorizacao/NfeRetAutorizacao.asmx',
        WS_NFE_INUTILIZACAO: 'NfeInutilizacao2/NfeInutilizacao2.asmx',
        WS_NFE_CONSULTA: 'NfeConsulta2/NfeConsulta2.asmx',
        WS_NFE_SITUACAO: 'NfeStatusServico2/NfeStatusServico2.asmx'
    }
}

SVC_AN = {
    NFE_AMBIENTE_PRODUCAO: {
        'servidor': 'www.svc.fazenda.gov.br',
        WS_NFE_RECEPCAO_EVENTO: 'RecepcaoEvento/RecepcaoEvento.asmx',
        WS_NFE_AUTORIZACAO: 'NfeAutorizacao/NfeAutorizacao.asmx',
        WS_NFE_RET_AUTORIZACAO: 'NfeRetAutorizacao/NfeRetAutorizacao.asmx',
        WS_NFE_CONSULTA: 'NfeConsulta2/NfeConsulta2.asmx',
        WS_NFE_SITUACAO: 'NfeStatusServico2/NfeStatusServico2.asmx'
    },
    NFE_AMBIENTE_HOMOLOGACAO: {
        'servidor': 'hom.nfe.fazenda.gov.br',
        WS_NFE_RECEPCAO_EVENTO: 'RecepcaoEvento/RecepcaoEvento.asmx',
        WS_NFE_AUTORIZACAO: 'NfeAutorizacao/NfeAutorizacao.asmx',
        WS_NFE_RET_AUTORIZACAO: 'NfeRetAutorizacao/NfeRetAutorizacao.asmx',
        WS_NFE_CONSULTA: 'NfeConsulta2/NfeConsulta2.asmx',
        WS_NFE_SITUACAO: 'NfeStatusServico2/NfeStatusServico2.asmx'
    }
}

SVC_RS = {
    NFE_AMBIENTE_PRODUCAO: {
        'servidor': 'nfe.sefazvirtual.rs.gov.br',
        WS_NFE_RECEPCAO_EVENTO: 'ws/recepcaoevento/recepcaoevento.asmx',
        WS_NFE_AUTORIZACAO: 'ws/NfeAutorizacao/NfeAutorizacao.asmx',
        WS_NFE_RET_AUTORIZACAO: 'ws/NfeRetAutorizacao/NfeRetAutorizacao.asmx',
        WS_NFE_CONSULTA: 'ws/NfeConsulta/NfeConsulta2.asmx',
        WS_NFE_SITUACAO: 'ws/NfeStatusServico/NfeStatusServico2.asmx',
    },
    NFE_AMBIENTE_HOMOLOGACAO: {
        'servidor': 'homologacao.nfe.sefazvirtual.rs.gov.br',
        WS_NFE_RECEPCAO_EVENTO: 'ws/recepcaoevento/recepcaoevento.asmx',
        WS_NFE_AUTORIZACAO: 'ws/NfeAutorizacao/NfeAutorizacao.asmx',
        WS_NFE_RET_AUTORIZACAO: 'ws/NfeRetAutorizacao/NfeRetAutorizacao.asmx',
        WS_NFE_CONSULTA: 'ws/NfeConsulta/NfeConsulta2.asmx',
        WS_NFE_SITUACAO: 'ws/NfeStatusServico/NfeStatusServico2.asmx',
    }
}

DPEC = {
    NFE_AMBIENTE_PRODUCAO: {
        'servidor': 'www.nfe.fazenda.gov.br',
        WS_DPEC_CONSULTA: 'SCERecepcaoRFB/SCERecepcaoRFB.asmx',
        WS_DPEC_RECEPCAO: 'SCEConsultaRFB/SCEConsultaRFB.asmx'
    },
    NFE_AMBIENTE_HOMOLOGACAO: {
        'servidor': 'hom.nfe.fazenda.gov.br',
        WS_DPEC_CONSULTA: 'SCERecepcaoRFB/SCERecepcaoRFB.asmx',
        WS_DPEC_RECEPCAO: 'SCEConsultaRFB/SCEConsultaRFB.asmx'
    }
}

AN = {
    NFE_AMBIENTE_PRODUCAO: {
        'servidor': 'www.nfe.fazenda.gov.br',
        WS_NFE_RECEPCAO_EVENTO: 'RecepcaoEvento/RecepcaoEvento.asmx',
        WS_NFE_CONSULTA_DESTINADAS: 'NFeConsultaDest/NFeConsultaDest.asmx',
        WS_NFE_DOWNLOAD: 'NfeDownloadNF/NfeDownloadNF.asmx',
        WS_DFE_DISTRIBUICAO: 'NFeDistribuicaoDFe/NFeDistribuicaoDFe.asmx',
    },
    NFE_AMBIENTE_HOMOLOGACAO: {
        'servidor': 'hom.nfe.fazenda.gov.br',
        WS_NFE_RECEPCAO_EVENTO: 'RecepcaoEvento/RecepcaoEvento.asmx',
        WS_NFE_CONSULTA_DESTINADAS: 'NFeConsultaDest/NFeConsultaDest.asmx',
        WS_NFE_DOWNLOAD: 'NfeDownloadNF/NfeDownloadNF.asmx',
        WS_DFE_DISTRIBUICAO: 'NFeDistribuicaoDFe/NFeDistribuicaoDFe.asmx',
    },
}

UFAM = {
    NFE_AMBIENTE_PRODUCAO: {
        'servidor': 'nfe.sefaz.am.gov.br',
        WS_NFE_RECEPCAO_EVENTO: 'services2/services/RecepcaoEvento',
        WS_NFE_AUTORIZACAO: 'services2/services/NfeAutorizacao',
        WS_NFE_RET_AUTORIZACAO: 'services2/services/NfeRetAutorizacao',
        WS_NFE_INUTILIZACAO: 'services2/services/NfeInutilizacao2',
        WS_NFE_CONSULTA: 'services2/services/NfeConsulta2',
        WS_NFE_SITUACAO: 'services2/services/NfeStatusServico2',
        WS_NFE_CADASTRO: 'services2/services/cadconsultacadastro2',
    },
    NFE_AMBIENTE_HOMOLOGACAO: {
        'servidor': 'homnfe.sefaz.am.gov.br',
        WS_NFE_RECEPCAO_EVENTO: 'services2/services/RecepcaoEvento',
        WS_NFE_AUTORIZACAO: 'services2/services/NfeAutorizacao',
        WS_NFE_RET_AUTORIZACAO: 'services2/services/NfeRetAutorizacao',
        WS_NFE_INUTILIZACAO: 'services2/services/NfeInutilizacao2',
        WS_NFE_CONSULTA: 'services2/services/NfeConsulta2',
        WS_NFE_SITUACAO: 'services2/services/NfeStatusServico2',
        WS_NFE_CADASTRO: 'services2/services/cadconsultacadastro2',
    }
}

UFBA = {
    NFE_AMBIENTE_PRODUCAO: {
        'servidor': 'nfe.sefaz.ba.gov.br',
        WS_NFE_AUTORIZACAO: 'webservices/NfeAutorizacao/NfeAutorizacao.asmx',
        WS_NFE_RET_AUTORIZACAO:
            'webservices/NfeRetAutorizacao/NfeRetAutorizacao.asmx',
        WS_NFE_CONSULTA: 'webservices/NfeConsulta/NfeConsulta.asmx',
        WS_NFE_SITUACAO: 'webservices/NfeStatusServico/NfeStatusServico.asmx',
        WS_NFE_INUTILIZACAO: 'webservices/nfenw/nfeinutilizacao2.asmx',
        WS_NFE_CADASTRO: 'webservices/nfenw/CadConsultaCadastro2.asmx',
        WS_NFE_RECEPCAO_EVENTO: 'webservices/sre/recepcaoevento',
    },
    NFE_AMBIENTE_HOMOLOGACAO: {
        'servidor': 'hnfe.sefaz.ba.gov.br',
        WS_NFE_AUTORIZACAO: 'webservices/NfeAutorizacao/NfeAutorizacao.asmx',
        WS_NFE_RET_AUTORIZACAO:
            'webservices/NfeRetAutorizacao/NfeRetAutorizacao.asmx',
        WS_NFE_CONSULTA: 'webservices/NfeConsulta/NfeConsulta.asmx',
        WS_NFE_SITUACAO: 'webservices/NfeStatusServico/NfeStatusServico.asmx',
        WS_NFE_INUTILIZACAO: 'webservices/nfenw/nfeinutilizacao2.asmx',
        WS_NFE_CADASTRO: 'webservices/nfenw/CadConsultaCadastro2.asmx',
        WS_NFE_RECEPCAO_EVENTO: 'webservices/sre/recepcaoevento',
    }
}

UFCE = {
    NFE_AMBIENTE_PRODUCAO: {
        'servidor': 'nfe.sefaz.ce.gov.br',
        WS_NFE_AUTORIZACAO: 'nfe2/services/NfeRecepcao2',
        WS_NFE_RET_AUTORIZACAO: 'nfe2/services/NfeRetRecepcao2',
        WS_NFE_INUTILIZACAO: 'nfe2/services/NfeInutilizacao2',
        WS_NFE_CONSULTA: 'nfe2/services/NfeConsulta2',
        WS_NFE_SITUACAO: 'nfe2/services/NfeStatusServico2',
        WS_NFE_CADASTRO: 'nfe2/services/CadConsultaCadastro2',
        WS_NFE_RECEPCAO_EVENTO: 'nfe2/services/RecepcaoEvento',
    },
    NFE_AMBIENTE_HOMOLOGACAO: {
        'servidor': 'nfeh.sefaz.ce.gov.br',
        WS_NFE_AUTORIZACAO: 'nfe2/services/NfeRecepcao2',
        WS_NFE_RET_AUTORIZACAO: 'nfe2/services/NfeRetRecepcao2',
        WS_NFE_INUTILIZACAO: 'nfe2/services/NfeInutilizacao2',
        WS_NFE_CONSULTA: 'nfe2/services/NfeConsulta2',
        WS_NFE_SITUACAO: 'nfe2/services/NfeStatusServico2',
        WS_NFE_CADASTRO: 'nfe2/services/CadConsultaCadastro2',
        WS_NFE_RECEPCAO_EVENTO: 'nfe2/services/RecepcaoEvento',
    }
}


UFGO = {
    NFE_AMBIENTE_PRODUCAO: {
        'servidor': 'nfe.sefaz.go.gov.br',
        WS_NFE_RECEPCAO_EVENTO: 'nfe/services/v2/RecepcaoEvento',
        WS_NFE_AUTORIZACAO: 'nfe/services/v2/NfeAutorizacao',
        WS_NFE_RET_AUTORIZACAO: 'nfe/services/v2/NfeRetAutorizacao',
        WS_NFE_INUTILIZACAO: 'nfe/services/v2/NfeInutilizacao2',
        WS_NFE_CONSULTA: 'nfe/services/v2/NfeConsulta2',
        WS_NFE_SITUACAO: 'nfe/services/v2/NfeStatusServico2',
        WS_NFE_CADASTRO: 'nfe/services/v2/CadConsultaCadastro2',
    },
    NFE_AMBIENTE_HOMOLOGACAO: {
        'servidor': 'homolog.sefaz.go.gov.br',
        WS_NFE_RECEPCAO_EVENTO: 'nfe/services/v2/RecepcaoEvento',
        WS_NFE_AUTORIZACAO: 'nfe/services/v2/NfeAutorizacao',
        WS_NFE_RET_AUTORIZACAO: 'nfe/services/v2/NfeRetAutorizacao',
        WS_NFE_INUTILIZACAO: 'nfe/services/v2/NfeInutilizacao2',
        WS_NFE_CONSULTA: 'nfe/services/v2/NfeConsulta2',
        WS_NFE_SITUACAO: 'nfe/services/v2/NfeStatusServico2',
        WS_NFE_CADASTRO: 'nfe/services/v2/CadConsultaCadastro2',
    }
}


UFMT = {
    NFE_AMBIENTE_PRODUCAO: {
        'servidor': 'nfe.sefaz.mt.gov.br',
        WS_NFE_AUTORIZACAO: 'nfews/v2/services/NfeAutorizacao',
        WS_NFE_RET_AUTORIZACAO: 'nfews/v2/services/NfeRetAutorizacao',
        WS_NFE_INUTILIZACAO: 'nfews/v2/services/NfeInutilizacao2',
        WS_NFE_CONSULTA: 'nfews/v2/services/NfeConsulta2',
        WS_NFE_SITUACAO: 'nfews/v2/services/NfeStatusServico2',
        WS_NFE_CADASTRO: 'nfews/v2/services/CadConsultaCadastro2',
        WS_NFE_RECEPCAO_EVENTO: 'nfews/v2/services/RecepcaoEvento',
    },
    NFE_AMBIENTE_HOMOLOGACAO: {
        'servidor': 'homologacao.sefaz.mt.gov.br',
        WS_NFE_AUTORIZACAO: 'nfews/v2/services/NfeAutorizacao',
        WS_NFE_RET_AUTORIZACAO: 'nfews/v2/services/NfeRetAutorizacao',
        WS_NFE_INUTILIZACAO: 'nfews/v2/services/NfeInutilizacao2',
        WS_NFE_CONSULTA: 'nfews/v2/services/NfeConsulta2',
        WS_NFE_SITUACAO: 'nfews/v2/services/NfeStatusServico2',
        WS_NFE_CADASTRO: 'nfews/v2/services/CadConsultaCadastro2',
        WS_NFE_RECEPCAO_EVENTO: 'nfews/v2/services/RecepcaoEvento',
    }
}

UFMS = {
    NFE_AMBIENTE_PRODUCAO: {
        'servidor': 'nfe.fazenda.ms.gov.br',
        WS_NFE_RECEPCAO_EVENTO: 'producao/services2/RecepcaoEvento',
        WS_NFE_AUTORIZACAO: 'producao/services2/NfeAutorizacao',
        WS_NFE_RET_AUTORIZACAO: 'producao/services2/NfeRetAutorizacao',
        WS_NFE_CADASTRO: 'producao/services2/CadConsultaCadastro2',
        WS_NFE_INUTILIZACAO: 'producao/services2/NfeInutilizacao2',
        WS_NFE_CONSULTA: 'producao/services2/NfeConsulta2',
        WS_NFE_SITUACAO: 'producao/services2/NfeStatusServico2',
    },
    NFE_AMBIENTE_HOMOLOGACAO: {
        'servidor': 'homologacao.nfe.ms.gov.br',
        WS_NFE_RECEPCAO_EVENTO: 'homologacao/services2/RecepcaoEvento',
        WS_NFE_AUTORIZACAO: 'homologacao/services2/NfeAutorizacao',
        WS_NFE_RET_AUTORIZACAO: 'homologacao/services2/NfeRetAutorizacao',
        WS_NFE_CADASTRO: 'homologacao/services2/CadConsultaCadastro2',
        WS_NFE_INUTILIZACAO: 'homologacao/services2/NfeInutilizacao2',
        WS_NFE_CONSULTA: 'homologacao/services2/NfeConsulta2',
        WS_NFE_SITUACAO: 'homologacao/services2/NfeStatusServico2',
    }
}

UFMG = {
    NFE_AMBIENTE_PRODUCAO: {
        'servidor': 'nfe.fazenda.mg.gov.br',
        WS_NFE_AUTORIZACAO: 'nfe2/services/NfeAutorizacao',
        WS_NFE_RET_AUTORIZACAO: 'nfe2/services/NfeRetAutorizacao',
        WS_NFE_INUTILIZACAO: 'nfe2/services/NfeInutilizacao2',
        WS_NFE_CONSULTA: 'nfe2/services/NfeConsulta2',
        WS_NFE_SITUACAO: 'nfe2/services/NfeStatus2',
        WS_NFE_CADASTRO: 'nfe2/services/cadconsultacadastro2',
        WS_NFE_RECEPCAO_EVENTO: 'nfe2/services/RecepcaoEvento',
    },
    NFE_AMBIENTE_HOMOLOGACAO: {
        'servidor': 'hnfe.fazenda.mg.gov.br',
        WS_NFE_AUTORIZACAO: 'nfe2/services/NfeAutorizacao',
        WS_NFE_RET_AUTORIZACAO: 'nfe2/services/NfeRetAutorizacao',
        WS_NFE_INUTILIZACAO: 'nfe2/services/NfeInutilizacao2',
        WS_NFE_CONSULTA: 'nfe2/services/NfeConsulta2',
        WS_NFE_SITUACAO: 'nfe2/services/NfeStatus2',
        WS_NFE_CADASTRO: 'nfe2/services/cadconsultacadastro2',
        WS_NFE_RECEPCAO_EVENTO: 'nfe2/services/RecepcaoEvento',
    }
}

UFPR = {
    NFE_AMBIENTE_PRODUCAO: {
        'servidor': 'nfe.fazenda.pr.gov.br',
        WS_NFE_AUTORIZACAO: 'nfe/NFeAutorizacao3',
        WS_NFE_RET_AUTORIZACAO: 'nfe/NFeRetAutorizacao3',
        WS_NFE_INUTILIZACAO: 'nfe/NFeInutilizacao3',
        WS_NFE_CONSULTA: 'nfe/NFeConsulta3',
        WS_NFE_SITUACAO: 'nfe/NFeStatusServico3',
        WS_NFE_CADASTRO: 'nfe/CadConsultaCadastro2',
        WS_NFE_RECEPCAO_EVENTO: 'nfe-evento/NFeRecepcaoEvento',
    },
    NFE_AMBIENTE_HOMOLOGACAO: {
        'servidor': 'homologacao.nfe.fazenda.pr.gov.br',
        WS_NFE_AUTORIZACAO: 'nfe/NFeAutorizacao3',
        WS_NFE_RET_AUTORIZACAO: 'nfe/NFeRetAutorizacao3',
        WS_NFE_INUTILIZACAO: 'nfe/NFeInutilizacao3',
        WS_NFE_CONSULTA: 'nfe/NFeConsulta3',
        WS_NFE_SITUACAO: 'nfe/NFeStatusServico3',
        WS_NFE_CADASTRO: 'nfe/CadConsultaCadastro2',
        WS_NFE_RECEPCAO_EVENTO: 'nfe-evento/NFeRecepcaoEvento',
    }
}

UFPE = {
    NFE_AMBIENTE_PRODUCAO: {
        'servidor': 'nfe.sefaz.pe.gov.br',
        WS_NFE_RECEPCAO_EVENTO: 'nfe-service/services/RecepcaoEvento',
        WS_NFE_CANCELAMENTO: 'nfe-service/services/RecepcaoEvento',
        WS_NFE_AUTORIZACAO: 'nfe-service/services/NfeAutorizacao',
        WS_NFE_RET_AUTORIZACAO: 'nfe-service/services/NfeRetAutorizacao',
        WS_NFE_INUTILIZACAO: 'nfe-service/services/NfeInutilizacao2',
        WS_NFE_CONSULTA: 'nfe-service/services/NfeConsulta2',
        WS_NFE_SITUACAO: 'nfe-service/services/NfeStatusServico2',
        WS_NFE_CADASTRO: 'nfe-service/services/CadConsultaCadastro2',
    },
    NFE_AMBIENTE_HOMOLOGACAO: {
        'servidor': 'nfehomolog.sefaz.pe.gov.br',
        WS_NFE_RECEPCAO_EVENTO: 'nfe-service/services/RecepcaoEvento',
        WS_NFE_CANCELAMENTO: 'nfe-service/services/RecepcaoEvento',
        WS_NFE_AUTORIZACAO: 'nfe-service/services/NfeAutorizacao',
        WS_NFE_RET_AUTORIZACAO: 'nfe-service/services/NfeRetAutorizacao',
        WS_NFE_INUTILIZACAO: 'nfe-service/services/NfeInutilizacao2',
        WS_NFE_CONSULTA: 'nfe-service/services/NfeConsulta2',
        WS_NFE_SITUACAO: 'nfe-service/services/NfeStatusServico2',
        WS_NFE_CADASTRO: 'nfe-service/services/CadConsultaCadastro2',
    }
}


UFRS = {
    NFE_MODELO : {
        NFE_AMBIENTE_PRODUCAO: {
            'servidor': 'nfe.sefaz.rs.gov.br',
            WS_NFE_RECEPCAO_EVENTO: 'ws/recepcaoevento/recepcaoevento.asmx',
            WS_NFE_AUTORIZACAO: 'ws/NfeAutorizacao/NFeAutorizacao.asmx',
            WS_NFE_RET_AUTORIZACAO: 'ws/NfeRetAutorizacao/NFeRetAutorizacao.asmx',
            WS_NFE_CADASTRO: 'ws/cadconsultacadastro/cadconsultacadastro2.asmx',
            WS_NFE_CONSULTA_DESTINADAS: 'ws/nfeConsultaDest/nfeConsultaDest.asmx',
            WS_NFE_DOWNLOAD: 'ws/nfeDownloadNF/nfeDownloadNF.asmx',
            WS_NFE_INUTILIZACAO: 'ws/NfeInutilizacao/NfeInutilizacao2.asmx',
            WS_NFE_CONSULTA: 'ws/NfeConsulta/NfeConsulta2.asmx',
            WS_NFE_SITUACAO: 'ws/NfeStatusServico/NfeStatusServico2.asmx',
            WS_NFE_CANCELAMENTO: 'ws/recepcaoevento/recepcaoevento.asmx',
        },
        NFE_AMBIENTE_HOMOLOGACAO: {
            'servidor': 'nfe-homologacao.sefazrs.rs.gov.br',
            WS_NFE_RECEPCAO_EVENTO: 'ws/recepcaoevento/recepcaoevento.asmx',
            WS_NFE_AUTORIZACAO: 'ws/NfeAutorizacao/NFeAutorizacao.asmx',
            WS_NFE_RET_AUTORIZACAO: 'ws/NfeRetAutorizacao/NFeRetAutorizacao.asmx',
            WS_NFE_CADASTRO: 'ws/cadconsultacadastro/cadconsultacadastro2.asmx',
            WS_NFE_CONSULTA_DESTINADAS: 'ws/nfeConsultaDest/nfeConsultaDest.asmx',
            WS_NFE_DOWNLOAD: 'ws/nfeDownloadNF/nfeDownloadNF.asmx',
            WS_NFE_INUTILIZACAO: 'ws/NfeInutilizacao/NfeInutilizacao2.asmx',
            WS_NFE_CONSULTA: 'ws/NfeConsulta/NfeConsulta2.asmx',
            WS_NFE_SITUACAO: 'ws/NfeStatusServico/NfeStatusServico2.asmx',
            WS_NFE_CANCELAMENTO: 'ws/recepcaoevento/recepcaoevento.asmx',
        }
    },
    NFCE_MODELO: {
        NFE_AMBIENTE_PRODUCAO: {
            'servidor': 'nfce.sefaz.rs.gov.br',
            WS_NFCE_RECEPCAO_EVENTO: 'ws/recepcaoevento/recepcaoevento.asmx',
            WS_NFCE_AUTORIZACAO: 'ws/NfeAutorizacao/NFeAutorizacao.asmx',
            WS_NFCE_RET_AUTORIZACAO: 'ws/NfeRetAutorizacao/NFeRetAutorizacao.asmx',
            WS_NFCE_CADASTRO: 'ws/cadconsultacadastro/cadconsultacadastro2.asmx',
            WS_NFCE_CONSULTA_DESTINADAS: 'ws/nfeConsultaDest/nfeConsultaDest.asmx',
            WS_NFCE_DOWNLOAD: 'ws/nfeDownloadNF/nfeDownloadNF.asmx',
            WS_NFCE_INUTILIZACAO: 'ws/NfeInutilizacao/NfeInutilizacao2.asmx',
            WS_NFCE_CONSULTA: 'ws/NfeConsulta/NfeConsulta2.asmx',
            WS_NFCE_SITUACAO: 'ws/NfeStatusServico/NfeStatusServico2.asmx',
            WS_NFCE_CANCELAMENTO: 'ws/recepcaoevento/recepcaoevento.asmx',
            WS_NFCE_QR_CODE: 'https://www.sefaz.rs.gov.br/NFCE/NFCE-COM.aspx',
        },
        NFE_AMBIENTE_HOMOLOGACAO: {
            'servidor': 'nfce-homologacao.sefazrs.rs.gov.br',
            WS_NFCE_RECEPCAO_EVENTO: 'ws/recepcaoevento/recepcaoevento.asmx',
            WS_NFCE_AUTORIZACAO: 'ws/NfeAutorizacao/NFeAutorizacao.asmx',
            WS_NFCE_RET_AUTORIZACAO: 'ws/NfeRetAutorizacao/NFeRetAutorizacao.asmx',
            WS_NFCE_CADASTRO: 'ws/cadconsultacadastro/cadconsultacadastro2.asmx',
            WS_NFCE_CONSULTA_DESTINADAS: 'ws/nfeConsultaDest/nfeConsultaDest.asmx',
            WS_NFCE_DOWNLOAD: 'ws/nfeDownloadNF/nfeDownloadNF.asmx',
            WS_NFCE_INUTILIZACAO: 'ws/NfeInutilizacao/NfeInutilizacao2.asmx',
            WS_NFCE_CONSULTA: 'ws/NfeConsulta/NfeConsulta2.asmx',
            WS_NFCE_SITUACAO: 'ws/NfeStatusServico/NfeStatusServico2.asmx',
            WS_NFCE_CANCELAMENTO: 'ws/recepcaoevento/recepcaoevento.asmx',
            WS_NFCE_QR_CODE: 'https://www.sefaz.rs.gov.br/NFCE/NFCE-COM.aspx'
        }
    }
}

UFSP = {
    NFE_MODELO: {
        NFE_AMBIENTE_PRODUCAO: {
            'servidor': 'nfe.fazenda.sp.gov.br',
            WS_NFE_AUTORIZACAO: 'ws/nfeautorizacao.asmx',
            WS_NFE_RET_AUTORIZACAO: 'ws/nferetautorizacao.asmx',
            WS_NFE_INUTILIZACAO: 'ws/nfeinutilizacao2.asmx',
            WS_NFE_CONSULTA: 'ws/nfeconsulta2.asmx',
            WS_NFE_SITUACAO: 'ws/nfestatusservico2.asmx',
            WS_NFE_CADASTRO: 'ws/cadconsultacadastro2.asmx',
            WS_NFE_RECEPCAO_EVENTO: 'ws/recepcaoevento.asmx',
            WS_NFE_CANCELAMENTO: 'ws/recepcaoevento.asmx',
        },
        NFE_AMBIENTE_HOMOLOGACAO: {
            'servidor': 'homologacao.nfe.fazenda.sp.gov.br',
            WS_NFE_AUTORIZACAO: 'ws/nfeautorizacao.asmx',
            WS_NFE_RET_AUTORIZACAO: 'ws/nferetautorizacao.asmx',
            WS_NFE_INUTILIZACAO: 'ws/nfeinutilizacao2.asmx',
            WS_NFE_CONSULTA: 'ws/nfeconsulta2.asmx',
            WS_NFE_SITUACAO: 'ws/nfestatusservico2.asmx',
            WS_NFE_CADASTRO: 'ws/cadconsultacadastro2.asmx',
            WS_NFE_RECEPCAO_EVENTO: 'ws/recepcaoevento.asmx',
            WS_NFE_CANCELAMENTO: 'ws/recepcaoevento.asmx',
        }
    },
    NFCE_MODELO: {
        NFCE_AMBIENTE_PRODUCAO: {
            'servidor': 'nfce.fazenda.sp.gov.br',
            WS_NFCE_AUTORIZACAO: 'ws/nfeautorizacao.asmx',
            WS_NFCE_RET_AUTORIZACAO: 'ws/nferetautorizacao.asmx',
            WS_NFCE_INUTILIZACAO: 'ws/nfeinutilizacao2.asmx',
            WS_NFCE_CONSULTA: 'ws/nfeconsulta2.asmx',
            WS_NFCE_SITUACAO: 'ws/nfestatusservico2.asmx',
            WS_NFCE_CADASTRO: 'ws/cadconsultacadastro2.asmx',
            WS_NFCE_RECEPCAO_EVENTO: 'ws/recepcaoevento.asmx',
            WS_NFCE_QR_CODE: '',
        },
        NFCE_AMBIENTE_HOMOLOGACAO: {
            'servidor': 'homologacao.nfce.fazenda.sp.gov.br',
            WS_NFCE_AUTORIZACAO: 'ws/nfeautorizacao.asmx',
            WS_NFCE_RET_AUTORIZACAO: 'ws/nferetautorizacao.asmx',
            WS_NFCE_INUTILIZACAO: 'ws/nfeinutilizacao2.asmx',
            WS_NFCE_CONSULTA: 'ws/nfeconsulta2.asmx',
            WS_NFCE_SITUACAO: 'ws/nfestatusservico2.asmx',
            WS_NFCE_CADASTRO: 'ws/cadconsultacadastro2.asmx',
            WS_NFCE_RECEPCAO_EVENTO: 'ws/recepcaoevento.asmx',
            WS_NFCE_QR_CODE: 'NFCEConsultaPublica/Paginas/ConstultaQRCode.aspx',
        }
    }
}


ESTADO_WS = {
    'AC': SVRS,
    'AL': SVRS,
    'AM': UFAM,
    'AP': SVRS,
    'BA': UFBA,
    'CE': UFCE,
    'DF': SVRS,
    'ES': SVRS,
    'GO': UFGO,
    'MA': SVAN,
    'MG': UFMG,
    'MS': UFMS,
    'MT': UFMT,
    'PA': SVAN,
    'PB': SVRS,
    'PE': UFPE,
    'PI': SVAN,
    'PR': UFPR,
    'RJ': SVRS,
    'RN': SVRS,
    'RO': SVRS,
    'RR': SVRS,
    'RS': UFRS,
    'SC': SVRS,
    'SE': SVRS,
    'SP': UFSP,
    'TO': SVRS,
}


#
# Informação obtida em
# http://www.nfe.fazenda.gov.br/portal/webServices.aspx
#  Última verificação: 15/08/2014 16:22
#
# Autorizadores em contingência:
# - UF que utilizam a SVC-AN - Sefaz Virtual de Contingência Ambiente Nacional:
#       AC, AL, AP, DF, ES, MG, PB, RJ, RN, RO, RR, RS, SC, SE, SP, TO
# - UF que utilizam a SVC-RS - Sefaz Virtual de Contingência Rio Grande do Sul:
#       AM, BA, CE, GO, MA, MS, MT, PA, PE, PI, PR
#

ESTADO_WS_CONTINGENCIA = {
    'AC': SVC_AN,
    'AL': SVC_AN,
    'AM': SVC_RS,
    'AP': SVC_AN,
    'BA': SVC_RS,
    'CE': SVC_RS,
    'DF': SVC_AN,
    'ES': SVC_AN,
    'GO': SVC_RS,
    'MA': SVC_RS,
    'MG': SVC_AN,
    'MS': SVC_RS,
    'MT': SVC_RS,
    'PA': SVC_RS,
    'PB': SVC_AN,
    'PE': SVC_RS,
    'PI': SVC_RS,
    'PR': SVC_RS,
    'RJ': SVC_AN,
    'RN': SVC_AN,
    'RO': SVC_AN,
    'RR': SVC_AN,
    'RS': SVC_AN,
    'SC': SVC_AN,
    'SE': SVC_AN,
    'SP': SVC_AN,
    'TO': SVC_AN,
}
