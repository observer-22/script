# -*- coding: utf-8 -*-
"""
Created on Sat Aug 10 09:52:21 2019

@author: zz
"""

import pandas as pd

raw_data = pd.read_excel('文本标注地点宜宾1368.xlsx',index_col='序号')

data = pd.merge(raw_data, pd.DataFrame(raw_data['地点'].str.split('、',expand=True)), how='left', left_index=True,right_index=True)
writer = pd.ExcelWriter('output.xlsx')
data.to_excel(writer,'Sheet1')
writer.save()