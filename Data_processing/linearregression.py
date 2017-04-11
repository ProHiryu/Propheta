import pickle
import sqlite3
import pandas as pd

conn = sqlite3.connect("game_data.sqlite")

sql = "select * from Games"

df = pd.read_sql(sql,conn,index_col='id')
with open('team_order.pickle','rb') as f:
    team_order = pickle.load(f)

# print(df.head())
# print(team_order.keys())
