# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import requests

ak='8f8839902ac04cb1a29b5b9de1f9a071'
file_name = '539.csv'
error_list = []


def address(address):
    url="http://restapi.amap.com/v3/geocode/geo?key=%s&address=%s"%(ak, address)
    data=requests.get(url)
    contest=data.json()
    contest=contest['geocodes'][0]['location']
    return contest



data = pd.read_csv(file_name, header=None)
col_num = data.shape[1]
data.columns = np.arange(1,col_num+1, 1)

for i in np.arange(3,col_num+1,1):
	for j in data.index:
		if pd.isnull(data[i][j]) == False:
			try:
				address(data[i][j])
			except IndexError:
				error_list.append(str(j)+'行'+str(i)+'列')
			else:
				pass


print(error_list)
data.to_csv('1.csv')
f = open('error.txt','w')
f.write(str(error_list))