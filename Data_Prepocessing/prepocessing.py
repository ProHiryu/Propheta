# -*- coding:utf-8 -*-
import sqlite3
import pandas as pd

coon = sqlite3.connect('lol.sqlite')
sql = "select * from Games"

df = pd.read_sql(sql,coon,index_col='id')
print(df.head(),len(df))

