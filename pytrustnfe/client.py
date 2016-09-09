# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import requests
import suds.client
import suds_requests


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

    def _headers(self, action):
        return {
            u'Content-type': u'application/soap+xml; charset=utf-8; action="http://www.portalfiscal.inf.br/nfe/wsdl/%s"' % action,
            u'Accept': u'application/soap+xml; charset=utf-8'
        }

    def post_soap(self, xml_soap, cabecalho):
        header = self._headers(cabecalho.soap_action)
        res = requests.post(self.url, data=xml_soap,
                            cert=(self.cert_path, self.key_path),
                            verify=False, headers=header)
        return res.text
