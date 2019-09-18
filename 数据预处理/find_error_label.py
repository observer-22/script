# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from lxml import etree
import os
import shutil

label_list = ['gb','banner']
path = os.getcwd()

goal_path = path + '\\error'
if os.path.exists(goal_path) == False:
    os.mkdir(goal_path)

xml_list = [x for x in os.listdir(path) if x.endswith(".xml")]

error_list = []

for x in xml_list:
    html = etree.parse(x, etree.HTMLParser())
    result = html.xpath('//name/text()')
    union_list = list(set(result).union(set(label_list)))
    if union_list != label_list:
        error_list.append(x)
        
for t in error_list:
    xml_path = os.path.join(path, t)
    despath = os.path.join(goal_path, t)
    shutil.move(xml_path, despath)