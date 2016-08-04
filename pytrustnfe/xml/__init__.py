import os.path
from lxml import etree
from jinja2 import Environment, FileSystemLoader
from . import filters


def render_xml(path, template_name, **nfe):
    env = Environment(
        loader=FileSystemLoader(path), extensions=['jinja2.ext.with_'])

    env.filters["normalize"] = filters.normalize_str
    env.filters["format_percent"] = filters.format_percent
    env.filters["format_datetime"] = filters.format_datetime
    env.filters["format_date"] = filters.format_date

    template = env.get_template(template_name)

    xml = template.render(**nfe)
    xml = xml.replace('&', '&amp;')
    parser = etree.XMLParser(remove_blank_text=True, remove_comments=True)
    elem = etree.fromstring(xml, parser=parser)
    return etree.tostring(elem)


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
