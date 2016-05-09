'''
Created on 24/06/2015

@author: danimar
'''

def validar_schema():
    arquivo_esquema = ''
    xml = tira_abertura(self.xml).encode('utf-8')

    esquema = etree.XMLSchema(etree.parse(arquivo_esquema))
    esquema.validate(etree.fromstring(xml))

    namespace = '{http://www.portalfiscal.inf.br/nfe}'
    return "\n".join([x.message.replace(namespace, '') for x in esquema.error_log])
