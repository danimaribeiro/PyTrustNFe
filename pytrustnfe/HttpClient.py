#coding=utf-8
'''
Created on Jun 16, 2015

@author: danimar
'''
from httplib import HTTPSConnection

class HttpClient(object):
    
    def __init__(self, url, chave_pem, certificado_pem):
        self.url = url
        self.chave_pem = chave_pem
        self.certificado_pem = certificado_pem
    
    def _headers(self):
        return { 
                u'Content-type': u'application/soap+xml; charset=utf-8',
                u'Accept': u'application/soap+xml; charset=utf-8'
                }
        
    def post_xml(self, post, xml):
        
        conexao = HTTPSConnection(self.url, '443', key_file=self.chave_pem, 
                                  cert_file=self.certificado_pem)
        
        try:
            conexao.request(u'POST', post, xml, self._headers())
            response = conexao.getresponse()
            if response.status == 200:
                return response.read()
            return response.read()
        except Exception as e:
            print str(e)            
        finally:
            conexao.close()
        
        
        