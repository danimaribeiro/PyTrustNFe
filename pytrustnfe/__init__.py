# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import requests


class HttpClient(object):

    def __init__(self, url):
        self.url = url

    def _headers(self, action):
        return {
            u'Content-type':
            u'text/xml; charset=utf-8;',
            u'Accept': u'application/soap+xml; charset=utf-8',
            u'SOAPAction': action
        }

    def post_soap(self, xml_soap, action):
        header = self._headers(action)
        res = requests.post(self.url, data=xml_soap, headers=header)
        return res.text
