# coding=utf-8
'''
Created on Jun 16, 2015

@author: danimar
'''
import requests


class HttpClient(object):

    def __init__(self, url, cert_path, key_path):
        self.url = url
        self.cert_path = cert_path
        self.key_path = key_path

    def _headers(self):
        return {
                u'Content-type': u'application/soap+xml; charset=utf-8; action="http://www.portalfiscal.inf.br/nfe/wsdl/NfeAutorizacao/nfeAutorizacaoLote',
                u'Accept': u'application/soap+xml; charset=utf-8'        
                }

    def post_xml(self, post, xml):                
        try:
            url = 'https://nfe-homologacao.sefazrs.rs.gov.br/ws/NfeAutorizacao/NFeAutorizacao.asmx'
            res = requests.post(url, data=xml, cert=(self.cert_path, self.key_path),
                                verify=False, headers=self._headers())
            return res.text            
        except Exception as e:
            print(str(e))

