# -*- coding: utf-8 -*-


import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import cv2
import numpy as np
import pandas as pd
import xlrd
import requests
import os
import shutil
import imagehash
from PIL import Image

ak='8f8839902ac04cb1a29b5b9de1f9a071'

def address(address):
			url="http://restapi.amap.com/v3/geocode/geo?key=%s&address=%s"%(ak, address)
			data=requests.get(url)
			contest=data.json()
			contest=contest['geocodes'][0]['location']
			return contest


class qitool(QWidget):
	def __init__(self, parent=None):
		super(qitool, self).__init__(parent)
		layout = QVBoxLayout()
		self.btn = QPushButton("图片查重")
		self.btn.clicked.connect(self.director1_msg)
		layout.addWidget(self.btn)
		self.btn1 = QPushButton("文本批量检测")
		self.btn1.clicked.connect(self.xls_msg)
		layout.addWidget(self.btn1)
		self.btn2 = QPushButton("720p视频分类")
		self.btn2.clicked.connect(self.video_msg)
		layout.addWidget(self.btn2)
		self.setLayout(layout)
		self.setWindowTitle("质检工具")
		self.resize(300,100)

	def director1_msg(self):
		directory1 = QFileDialog.getExistingDirectory(self,"选取文件夹","./")
		goal_path = directory1 + '/same'

		if os.path.exists(goal_path) == False:
			os.mkdir(goal_path)
        
		jpg_list = [x for x in os.listdir(directory1) if x.endswith(".jpg")]

		file_phash = {}

		for jpg in jpg_list:
			try:
				jpg_path = directory1 + '/' + jpg
				jpg_file = Image.open(jpg_path)
				file_phash[jpg_path] = imagehash.phash(Image.open(jpg_path))
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
			try:
				if os.path.exists(s) == True:
					shutil.move(s, goal_path)
			except:
				pass
		print('查重完成!')


	def xls_msg(self):
		fileName1, filetype = QFileDialog.getOpenFileName(self,"选取文件","./","*.xls;;*.xlsx")
		
		data = xlrd.open_workbook(fileName1)
		table = data.sheets()[0]
		rows_num = table.nrows
		cols_num = table.ncols

		for i in np.arange(0,rows_num,1):
			for j in np.arange(2,cols_num,1):
				a = table.cell(i,j).value
				if a == '':
					continue
				else:
					try:
						address(a)
					except IndexError:
						print(str(i+1)+'行'+str(j+1)+'列')
		print('检测完成！')


	def video_msg(self):
		directory2 = QFileDialog.getExistingDirectory(self,"选取文件夹","./")
		print(directory2)
		
		vedio_list = [x.split('.')[0] for x in os.listdir(directory2) if x.endswith(".mp4")]

		path1 = directory2 + '/720p及以上'
		if os.path.exists(path1) == False:
			os.mkdir(path1)

		path2 = directory2 + '/小于720p'
		if os.path.exists(path2) == False:
			os.mkdir(path2)

		for v in vedio_list:
			v = directory2 + '/' + v +'.mp4'
			cap = cv2.VideoCapture(v)
			width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
			height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
			cap.release()

			if width >= 1280 and height >= 720:
				if os.path.exists(v) == True:
					shutil.move(v, path1)

			else:
				if os.path.exists(v) == True:
					shutil.move(v, path2)
		print('分类完成！')

if __name__ == '__main__':
	app = QApplication(sys.argv)
	qi = qitool()
	qi.show()
	sys.exit(app.exec_())