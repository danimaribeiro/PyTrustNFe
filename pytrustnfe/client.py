# -*- coding: utf-8 -*-
# © 2016 Danimar Ribeiro, Trustcode
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import requests
import suds.client
import suds_requests


def get_authenticated_client(base_url, cert, key):
    cache_location = "/tmp/suds"
    cache = suds.cache.DocumentCache(location=cache_location)

    session = requests.Session()
    session.cert = (cert, key)  

    # Testa sessao https
    r = requests.get(base_url, cert=(cert, key))
    if r.status_code == 403:
        print("ERROR: Falha na conexão utilizando o certificado digital e senha infomados. Verifique a validade do certificado")
        exit()
    return suds.client.Client(
        base_url, cache=cache, transport=suds_requests.RequestsTransport(session)
    )


def get_client(base_url):
    cache_location = "/tmp/suds"
    cache = suds.cache.DocumentCache(location=cache_location)

    session = requests.Session()

    return suds.client.Client(
        base_url, cache=cache, transport=suds_requests.RequestsTransport(session)
    )
