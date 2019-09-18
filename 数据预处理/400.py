# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 10:48:49 2019

@author: EHL
"""

import cv2
import os
import shutil

path = os.getcwd()

path1 = path + '\\小于400'
if os.path.exists(path1) == False:
    os.mkdir(path1)

path2 = path + '\\大于400'
if os.path.exists(path2) == False:
    os.mkdir(path2)
    
jpg_list = [x for x in os.listdir(path) if x.endswith(".jpg")]

for jpg in jpg_list:
    img = cv2.imread(jpg)
    h = img.shape[0]
    w = img.shape[1]
    if h <= 400 and w <= 400:
        jpg_path = os.path.join(path, jpg)
        despath = os.path.join(path1, jpg)
        shutil.move(jpg_path, despath)
    else:
        jpg_path = os.path.join(path, jpg)
        despath = os.path.join(path2, jpg)
        shutil.move(jpg_path, despath)