# coding=utf-8
'''
Created on Jun 14, 2015

@author: danimar
'''
import unittest
from datetime import datetime
from pytrustnfe.xml.filters import normalize_str
from pytrustnfe.xml.filters import strip_line_feed
from pytrustnfe.xml.filters import format_percent
from pytrustnfe.xml.filters import format_date
from pytrustnfe.xml.filters import format_datetime


class test_xmlfilters(unittest.TestCase):

    def test_xmlfilters(self):
        word = normalize_str('ação café pó pá veêm')
        self.assertEqual(word, 'acao cafe po pa veem')
        self.assertEqual(1.5, format_percent(150))
        self.assertEqual('aa', format_date('aa'))
        self.assertEqual('aa', format_datetime('aa'))

        dt = datetime(2016, 9, 17, 12, 12, 12)
        self.assertEqual('2016-09-17', format_date(dt.date()))
        self.assertEqual('2016-09-17T12:12:12', format_datetime(dt))

        word = strip_line_feed(u"olá\ncomo vai\r senhor ")
        self.assertEqual(word, u"olá como vai senhor")
