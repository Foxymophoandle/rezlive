#!/usr/bin/env python

__author__ = 'davide'
__date__ = ' 27 June 2017'

def remove_namespaces(xml):
    try:
        for el in xml.iter():
            if '}' in el.tag:
                el.tag = el.tag.split('}', 1)[1]
    except AttributeError:
        # USING DEPRECATED FOR PYTHON 2.6
        for el in xml.getiterator():
            if '}' in el.tag:
                el.tag = el.tag.split('}', 1)[1]
