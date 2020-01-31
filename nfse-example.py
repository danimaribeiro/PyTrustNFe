import ipdb
import xml.dom.minidom
import os
from pytrustnfe.nfse.natal import recepcionar_lote_rps
from pytrustnfe.certificado import Certificado


rps_list = [
    {
        "numero": "1",
        "serie": "UNICA",
        "tipo_rps": "1",
        "data_emissao": "2010-06-16T21:00:00",
        "natureza_operacao": "1",
        "regime_tributacao": "1",
        "optante_simples": "1",
        "incentivador_cultural": "2",
        "status": "1",
        "servico": {
            "valor_servico": "1.00",
            "pis": "0",
            "cofins": "0",
            "inss": "0",
            "ir": "0",
            "csll": "0",
            "iss_retido": "2",
            "iss": "2",
            "retencoes": "2",
            "base_calculo": "0.00",
            "aliquota": "2",
            "codigo_servico": "01.07",
            "cnae_servico": "6209100",
            "discriminacao": "Sistema NFSe",
            "codigo_municipio": "2408102",
        },
        "prestador": {
            "cnpj": "23809070000190",
            "inscricao_municipal": "2143992"
        },
        "tomador": {
            "cpf_cnpj": "01812418000166",
            "inscricao_municipal": "2143992",
            "razao_social": "LEONIR",
            "endereco": "RUA GROBEIRO",
            "numero": "128",
            "complemento": "ANDAR 14",
            "bairro": "Lagoa Nova",
            "codigo_municipio": "3159506",
            "uf": "BH",
            "cep": "30160010",
            "email": "leonir@yahoo.com.br",
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
pfx_source = open(os.path.join(caminho, "tsmx-a1.pfx"), "rb").read()
pfx = Certificado(pfx_source, "12345678")

retorno = recepcionar_lote_rps(pfx, nfse=nfse, ambiente="homologacao")

dom = xml.dom.minidom.parseString(retorno['sent_xml']['nfseDadosMsg'])
sent_xml = dom.toprettyxml()
print(sent_xml)

myfile = open("sent_xml.xml", "w")
myfile.write(sent_xml)

dom = xml.dom.minidom.parseString(retorno['received_xml'])
received_xml = dom.toprettyxml()
print(received_xml)
