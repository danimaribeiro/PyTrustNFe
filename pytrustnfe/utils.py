# coding=utf-8
'''
Created on 22/06/2015

@author: danimar
'''
from datetime import date, datetime

def date_tostring(data):
    assert isinstance(data, date), "Objeto date requerido"
    return data.strftime("%d-%m-%y")

def datetime_tostring(data):
    assert isinstance(data, datetime), "Objeto datetime requerido"
    return data.strftime("%d-%m-%y %H:%M:%S")