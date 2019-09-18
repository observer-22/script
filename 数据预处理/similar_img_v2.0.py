# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 08:58:20 2019

@author: EHL
"""
import pandas as pd
import os
import shutil
import imagehash
from PIL import Image

path = os.getcwd()

goal_path = path + '\\same'
if os.path.exists(goal_path) == False:
    os.mkdir(goal_path)
jpg_list = [x for x in os.listdir(path) if x.endswith(".jpg")]


file_phash = {}

for jpg in jpg_list:
    try:
        jpg_file = Image.open(jpg)
        file_phash[jpg] = imagehash.phash(Image.open(jpg))
        jpg_file.close()
    except(OSError, NameError):
        print('OSError, Path:', jpg)

file_phash = pd.Series(file_phash)

similar_img = []

for i in file_phash.index:
    phash1 = file_phash[i].hash.flatten()
    file_phash = file_phash.drop(i)
    
    for left_i in file_phash.index:
        phash2 = file_phash[left_i].hash.flatten()
        distance = 0
        
        for j in range(0,64):
            if phash1[j] != phash2[j]:
                distance = distance + 1
                
        if distance < 5:
            similar_img.append(i)
            similar_img.append(left_i)
            
            
for s in similar_img:
    jpg_path = os.path.join(path, s)
    despath = os.path.join(goal_path, s)
    try:
    	if os.path.exists(jpg_path) == True:
        	shutil.move(jpg_path, despath)
    except:
    	pass