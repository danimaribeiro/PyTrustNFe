# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from decimal import Decimal
from datetime import date
from datetime import datetime
from unicodedata import normalize


def normalize_str(string):
    """
    Remove special characters and strip spaces
    """
    if string:
        if not isinstance(string, unicode):
            string = unicode(string, 'utf-8', 'replace')

        string = string.encode('utf-8')
        return normalize(
            'NFKD', string.decode('utf-8')).encode('ASCII', 'ignore')
    return ''


def strip_line_feed(string):
    if string:
        if not isinstance(string, unicode):
            string = unicode(string, 'utf-8', 'replace')
        remap = {
            ord(u'\t'): u' ',
            ord(u'\n'): u' ',
            ord(u'\f'): u' ',
            ord(u'\r'): None,      # Delete
        }
        return string.translate(remap).strip()
    return string


def format_percent(value):
    if value:
        return Decimal(value) / 100


def format_datetime(value):
    """
    Format datetime
    """
    dt_format = '%Y-%m-%dT%H:%M:%I'
    if isinstance(value, datetime):
        return value.strftime(dt_format)
    return value


def format_date(value):
    """
    Format date
    """
    dt_format = '%Y-%m-%d'
    if isinstance(value, date):
        return value.strftime(dt_format)
    return value
