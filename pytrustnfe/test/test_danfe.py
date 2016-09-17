# coding=utf-8

import unittest
from pytrustnfe.pdf import Danfe


class test_danfe(unittest.TestCase):

    def test_generate_danfe(self):
        danfe = Danfe(None)
        danfe.gerar()
