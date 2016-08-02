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
