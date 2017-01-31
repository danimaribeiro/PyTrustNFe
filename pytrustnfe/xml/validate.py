# -*- coding: utf-8 -*-
# © 2016 Alessandro Fernandes Martini <alessandrofmartini@gmail.com>, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import os
import re

from lxml import etree

PATH = os.path.dirname(os.path.abspath(__file__))
SCHEMA = os.path.join(PATH, 'schemas/nfe_v3.10.xsd')


def pop_encoding(xml):
    xml = xml.split('\n')
    if re.match(r'<\?xml version=', xml[0]):
        xml.pop(0)
    return '\n'.join(xml)


def valida_nfe(nfe):
    xml = pop_encoding(nfe).encode('utf-8')
    nfe = etree.fromstring(xml)
    esquema = etree.XMLSchema(etree.parse(SCHEMA))
    esquema.validate(nfe)
    erros = [x.message for x in esquema.error_log]
    error_msg = '{field} inválido: {valor}.'
    unexpected = '{unexpected} não é esperado. O valor esperado é {expected}'
    namespace = '{http://www.portalfiscal.inf.br/nfe}'
    mensagens = []
    for erro in erros:
        campo = re.findall(r"'([^']*)'", erro)[0]
        nome = campo[campo.find('}') + 1: ]
        valor = nfe.find('.//' + campo).text
        if 'Expected is' in erro:
            expected_name = re.findall('\(.*?\)', erro)
            valor = unexpected.format(unexpected=nome, expected=expected_name)
        mensagem = error_msg.format(field=campo.replace(namespace, ''),
                                    valor=valor)
        mensagens.append(mensagem)
    return "\n".join(mensagens)
