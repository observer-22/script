# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import cv2
import os
import shutil

path = os.getcwd()

vedio_list = [x.split('.')[0] for x in os.listdir(path) if x.endswith(".mp4")]

path1 = path + '\\720p'
if os.path.exists(path1) == False:
    os.mkdir(path1)
    
path2 = path + '\\小于720p'
if os.path.exists(path2) == False:
    os.mkdir(path2)
    
for v in vedio_list:
    v = v +'.mp4'
    cap = cv2.VideoCapture(v)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()
    
    if width >= 1280 and height >= 720:
        vedio_path = os.path.join(path, v)
        despath = os.path.join(path1, v)
        if os.path.exists(vedio_path) == True:
            shutil.move(vedio_path, despath)

    else:
        vedio_path = os.path.join(path, v)
        despath = os.path.join(path2, v)
        if os.path.exists(vedio_path) == True:
            shutil.move(vedio_path, despath)