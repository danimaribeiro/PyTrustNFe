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

    env.filters["normalize"] = filters.strip_line_feed
    env.filters["normalize_str"] = filters.normalize_str
    env.filters["format_percent"] = filters.format_percent
    env.filters["format_datetime"] = filters.format_datetime
    env.filters["format_date"] = filters.format_date

    template = env.get_template(template_name)

    xml = template.render(**nfe)
    parser = etree.XMLParser(remove_blank_text=True, remove_comments=True)
    root = etree.fromstring(xml, parser=parser)
    if remove_empty:
        context = etree.iterwalk(root)
        for dummy, elem in context:
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
