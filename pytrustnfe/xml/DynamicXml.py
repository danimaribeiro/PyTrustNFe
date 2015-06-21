'''
Created on Jun 17, 2015

@author: danimar
'''

import xml.etree.ElementTree as ET
from collections import OrderedDict

class DynamicXml(object):    
    def __getattr__(self, name):
        try:          
            return object.__getattribute__(self,name)
        except:           
            self.__setattr__(name, None)
            return object.__getattribute__(self,name)
            
    def __setattr__(self, obj, val):
        if(obj=="value" or obj=="atributos"):
            object.__setattr__(self,obj, val)
        else:
            object.__setattr__(self,obj, DynamicXml(val))

    def __init__(self, value):
        self.value = value
        self.atributos={}  
        object.__setattr__(self, '__dict__', OrderedDict())
               
    def __str__(self):
        return str(self.value)
    def __call__(self, *args, **kw):        
        if(len(kw)>0):
            self.atributos=kw
        if(len(args)>0):
            self.value= args[0]
        else:
            return self.value

    def __getitem__(self, i):
        print(self.value)
        if(i >= len(self.value)):
            self.value.append(DynamicXml(None))
        return self.value[i]


def gerar_xml(xml, objeto):
    for attr, value in objeto.__dict__.items():
        if(attr!="value" and attr!="atributos"):
            if(type(value()) == type([])):
                for item in value():
                    print(item)
                    gerar_xml(xml, item)
            else:
                sub = ET.SubElement(xml,attr)                
                if(str(value)!="None"):
                    sub.text = str(value)
                gerar_xml(sub, value)
        elif(attr=="atributos"):
            for atr, val in value.items():                
                xml.set(atr.replace("__", ":"), str(val))







