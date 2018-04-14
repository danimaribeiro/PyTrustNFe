# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import urllib3
import requests
import suds.client
import suds_requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning


def get_authenticated_client(base_url, cert, key):
    cache_location = '/tmp/suds'
    cache = suds.cache.DocumentCache(location=cache_location)

    session = requests.Session()
    session.cert = (cert, key)
    return suds.client.Client(
        base_url,
        cache=cache,
        transport=suds_requests.RequestsTransport(session)
    )


def get_client(base_url):
    cache_location = '/tmp/suds'
    cache = suds.cache.DocumentCache(location=cache_location)

    session = requests.Session()

    return suds.client.Client(
        base_url,
        cache=cache,
        transport=suds_requests.RequestsTransport(session)
    )


class HttpClient(object):

    def __init__(self, url, cert_path, key_path):
        self.url = url
        self.cert_path = cert_path
        self.key_path = key_path

    def _headers(self, action, send_raw):
        if send_raw:
            return {
                'Content-type': 'text/xml; charset=utf-8;',
                'SOAPAction': "http://www.portalfiscal.inf.br/nfe/wsdl/%s" % action,
                'Accept': 'application/soap+xml; charset=utf-8',
            }

        return {
            'Content-type': 'application/soap+xml; charset=utf-8;',
            'SOAPAction': 'http://www.portalfiscal.inf.br/nfe/wsdl/%s' % action,
        }

    def post_soap(self, xml_soap, cabecalho, send_raw):
        header = self._headers(cabecalho.soap_action, send_raw)
        urllib3.disable_warnings(category=InsecureRequestWarning)
        res = requests.post(self.url, data=xml_soap.encode('utf-8'),
                            cert=(self.cert_path, self.key_path),
                            verify=False, headers=header)
        return res.text
