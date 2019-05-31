# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
from sklearn.preprocessing import OneHotEncoder

df = pd.DataFrame({'id':[2131414,3214123,4355678],
                   'sex':['male','female','famale'],
                   'level':['high','low','middle']})
df_new = df.copy()

#使用pandas标志转换
for col_num,col_name in enumerate(df):
    print(col_num,col_name)
    col_data = df[col_name]
    col_type = col_data.dtype
    if col_type == 'object':
        df_new = df_new.drop(col_name,axis=1)
        value_sets = col_data.unique()
        for value_unique in value_sets:
            col_name_new = col_name + ' ' + value_unique
            col_tmp = df.iloc[:,col_num]
            new_col = (col_tmp == value_unique)
            df_new[col_name_new] = new_col
print(df_new)

#使用sklearn标志转换
df2 = pd.DataFrame({'id':[4324351,3214212,5432423],
                    'sex':[1,2,2],
                    'level':[3,1,2]})

id_data = df2.values[:,:1]
transform_data = df2.values[:,1:]
enc = OneHotEncoder()
enc.fit_transform(transform_data).toarray()
df2_all = pd.concat([(pd.DataFrame(id_data)),(pd.DataFrame(transform_data))],axis=1)
print(df2_all)