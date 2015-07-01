# coding=utf-8
'''
Created on Jun 16, 2015

@author: danimar
'''
import mock
import unittest
import datetime
from pytrustnfe.utils import date_tostring, datetime_tostring


class test_utils(unittest.TestCase):

    def test_date_tostring(self):
        hoje = datetime.date.today()
        data = date_tostring(hoje)
        self.assertEqual(data, hoje.strftime("%d-%m-%y"),
                         "Não convertido corretamente")
        self.assertRaises(Exception, date_tostring, "Not a date")

    def test_datetime_tostring(self):
        hoje = datetime.datetime.now()
        data = datetime_tostring(hoje)
        self.assertEqual(data, hoje.strftime("%d-%m-%y %H:%M:%S"),
                         "Não convertido corretamente")
        self.assertRaises(Exception, datetime_tostring, "Not a date")
