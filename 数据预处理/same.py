# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 15:12:53 2019

@author: zz
"""

import os
import shutil

path = os.getcwd()

jpg_list = [x.split('.')[0] for x in os.listdir(path) if x.endswith(".jpg")]
xml_list = [x.split('.')[0] for x in os.listdir(path) if x.endswith(".xml")]
a = [x for x in jpg_list if x in xml_list]  #两个列表都存在
goal_path = path + '\\same'
if os.path.exists(goal_path) == False:
    os.mkdir(goal_path)
 
for num, i in enumerate(a):
    jpg_file = i +'.jpg'
    jpg_path = os.path.join(path, jpg_file)
    despath = os.path.join(goal_path, jpg_file)
    shutil.move(jpg_path, despath)
    
    xml_file = i +'.xml'
    xml_path = os.path.join(path, xml_file)
    despath = os.path.join(goal_path, xml_file)
    shutil.move(xml_path, despath)