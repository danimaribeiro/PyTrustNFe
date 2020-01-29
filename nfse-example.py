import xml.dom.minidom
import os
from pytrustnfe.nfse.natal import recepcionar_lote_rps
from pytrustnfe.certificado import Certificado


rps_list = [
    {
        "numero": "1",
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
            "descricao": "Sistema NFSe",
            "codigo_municipio": "2408102",
        },
        "prestador": {
            "cnpj": "23809070000190",
            "inscricao_municipal": "2143992",
            "razao_social": "SERVICOS DE TI",
            "fantasia": "SERVICOS DE TI",
            "endereco": "AV AMINTAS",
            "numero": "3755",
            "complemento": "SALA 32",
            "bairro": "Lagoa Nova",
            "codigo_municipio": "2408102",
            "uf": "RN",
            "cep": "59075810",
            "telefone": "4132095554",
            "email": "SUPORTE@EMAIL.COM.BR",
        },
        "tomador": {
            "cpf_cnpj": "01812418000166",
            "razao_social": "LEONIR",
            "endereco": "RUA GROBEIRO",
            "numero": "128",
            "bairro": "Lagoa Nova",
            "cidade": "3159506",
            "uf": "BH",
            "cep": "1231231313",
            "email": "leonir@yahoo.com.br",
            "orgao_gerador": {"codigo_municipio": "3159506"},
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
