import xml.dom.minidom
import os
import mock
from pytrustnfe.nfse.natal import recepcionar_lote_rps
from pytrustnfe.certificado import Certificado
from pytrustnfe.nfse.assinatura import Assinatura


rps_list = [
    {
        "numero": "E2143992638620191226",
        "serie": "UNICA",
        "tipo_rps": "1",
        "data_emissao": "2020-01-279",
        "natureza_operacao": "1",
        "regime_tributacao": "1",
        "optante_simples": "1",
        "incentivador_cultural": "2",
        "servico": {
            "valor_servico": "1.00",
            "iss_retido": "2",
            "base_calculo": "0.00",
            "codigo_servico": "01.07",
            "cnae_servico": "6209100",
            "descricao": "Sistema SGP|1.0000|220.00|220.00#",
            "codigo_municipio": "2408102",
        },
        "prestador": {
            "cnpj": "23809070000190",
            "inscricao_municipal": "2143992",
            "razao_social": "TSMX SERVICOS DE TI EIRELI",
            "fantasia": "TSMX",
            "endereco": "AV AMINTAS BARROS",
            "numero": "3700",
            "complemento": "SALA 1907 BLOCO A",
            "bairro": "Lagoa Nova",
            "codigo_municipio": "2408102",
            "uf": "RN",
            "cep": "59075810",
            "telefone": "4132095554",
            "email": "SUPORTE@CONTABILIZEI.COM.BR",
        },
        "tomador": {
            "cpf_cnpj": "01812418000166",
            "razao_social": "LEONIR NETO",
            "endereco": "RUA IRMÃO GROBEIRO",
            "numero": "14",
            "bairro": "CRUZEIRO",
            "cidade": "3159506",
            "uf": "MG",
            "cep": "35225000",
            "email": "leonirneto@uol.com.br",
            "orgao_gerador": {"codigo_municipio"},
        },
    }
]
nfse = {
    "numero_lote": "1",
    "cnpj_prestador": "23809070000190",
    "inscricao_municipal": "2143992",
    "lista_rps": rps_list,
}

caminho = os.path.dirname(__file__)
pfx_source = open(os.path.join(caminho, "tests/teste.pfx"), "rb").read()
pfx = Certificado(pfx_source, "123456")

retorno = recepcionar_lote_rps(pfx, nfse=nfse, ambiente="homologacao")

# dom = xml.dom.minidom.parseString(retorno['received_xml'])
# received_xml = dom.toprettyxml()
# print(received_xml)

dom = xml.dom.minidom.parseString(retorno.get("sent_xml"))
sent_xml = dom.toprettyxml()
print(sent_xml)
