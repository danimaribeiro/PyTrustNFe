# coding=utf-8
'''
Created on Jun 17, 2015

@author: danimar
'''

import xml.etree.ElementTree as ET
from lxml.etree import Element, tostring
from __builtin__ import str


class DynamicXml(object):

    def __getattr__(self, name):
        try:
            return object.__getattribute__(self, name)
        except:
            self.__setattr__(name, None)
            return object.__getattribute__(self, name)

    def __setattr__(self, obj, val):
        if(obj == "value" or obj == "atributos" or obj == "_indice"):
            object.__setattr__(self, obj, val)
        else:
            self._indice = self._indice + 1
            object.__setattr__(self, obj, DynamicXml(val, self._indice))

    def __init__(self, value, indice=0):
        self.value = unicode(value, 'utf-8') if isinstance(value,
                                                           str) else value
        self.atributos = {}
        self._indice = indice

    def __str__(self):
        return unicode(self.value)

    def __call__(self, *args, **kw):
        if(len(kw) > 0):
            self.atributos = kw
        if(len(args) > 0):
            self.value = args[0]
        else:
            return self.value

    def __getitem__(self, i):
        if not isinstance(self.value, list):
            self.value = []
        if(i + 1 > len(self.value)):
            self.value.append(DynamicXml(None))
        return self.value[i]

    def render(self, pretty_print=False):
        root = Element(self.value)
        self._gerar_xml(root, self)
        return tostring(root, pretty_print=pretty_print)

    def _gerar_xml(self, xml, objeto):
        items = sorted(
            objeto.__dict__.items(),
            key=lambda x: x[1]._indice if isinstance(x[1], DynamicXml) else 0
        )
        for attr, value in items:
            if(attr != "value" and attr != "atributos" and attr != "_indice"):
                if isinstance(value(), list):
                    for item in value():
                        sub = ET.SubElement(xml, attr)
                        self._gerar_xml(sub, item)
                else:
                    sub = ET.SubElement(xml, attr)
                    if(unicode(value) != u"None"):
                        sub.text = unicode(value)
                    self._gerar_xml(sub, value)
            elif(attr == "atributos"):
                for atr, val in value.items():
                    xml.set(atr.replace("__", ":"), str(val))
