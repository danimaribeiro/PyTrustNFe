# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import unicodedata
from lxml import etree

from lxml import objectify
from jinja2 import Environment, FileSystemLoader
from . import filters


def recursively_empty(e):
    if e.text:
        return False
    return all((recursively_empty(c) for c in e.iterchildren()))


def render_xml(path, template_name, remove_empty, **nfe):
    env = Environment(
        loader=FileSystemLoader(path), extensions=['jinja2.ext.with_'])

    env.filters["normalize"] = filters.normalize_str
    env.filters["format_percent"] = filters.format_percent
    env.filters["format_datetime"] = filters.format_datetime
    env.filters["format_date"] = filters.format_date

    template = env.get_template(template_name)

    xml = template.render(**nfe)
    parser = etree.XMLParser(remove_blank_text=True, remove_comments=True)
    root = etree.fromstring(xml, parser=parser)
    if remove_empty:
        context = etree.iterwalk(root)
        for action, elem in context:
            parent = elem.getparent()
            if recursively_empty(elem):
                parent.remove(elem)
        return root
    return etree.tostring(root)


def sanitize_response(response):
    response = unicode(response)
    response = unicodedata.normalize('NFKD', response).encode('ascii',
                                                              'ignore')

    tree = etree.fromstring(response)
    # Remove namespaces inuteis na resposta
    for elem in tree.getiterator():
        if not hasattr(elem.tag, 'find'):
            continue
        i = elem.tag.find('}')
        if i >= 0:
            elem.tag = elem.tag[i+1:]
    objectify.deannotate(tree, cleanup_namespaces=True)
    return response, objectify.fromstring(etree.tostring(tree))


def valida_schema(xml, arquivo_xsd):
        '''Função que valida um XML usando lxml do Python via arquivo XSD'''
        # Carrega o esquema XML do arquivo XSD
        xsd = etree.XMLSchema(file=arquivo_xsd)
        # Converte o XML passado em XML do lxml
        xml = etree.fromstring(str(xml))
        # Verifica a validade do xml
        erros = []
        if not xsd(xml):
            # Caso tenha erros, cria uma lista de erros
            for erro in xsd.error_log:
                erros.append({
                    'message': erro.message,
                    'domain': erro.domain,
                    'type': erro.type,
                    'level': erro.level,
                    'line': erro.line,
                    'column': erro.column,
                    'filename': erro.filename,
                    'domain_name': erro.domain_name,
                    'type_name': erro.type_name,
                    'level_name': erro.level_name
                })
        # Retorna os erros, sendo uma lista vazia caso não haja erros
        return erros
