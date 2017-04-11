import pickle
import sqlite3
import pandas as pd
from sklearn import preprocessing, cross_validation, svm
from sklearn.linear_model import LinearRegression
import numpy as np

conn = sqlite3.connect("game_data.sqlite")

sql = "select * from Games"

results = []
teams = []
list_result = {1: (1, 0), 2: (2, 0), 3: (2, 1), 4: (3, 0), 5: (3, 1), 6: (
    3, 2), -1: (0, 1), -2: (0, 2), -3: (1, 2), -4: (0, 3), -5: (1, 3), -6: (2, 3)}

df = pd.read_sql(sql, conn, index_col='id')
with open('team_order.pickle', 'rb') as f:
    team_order = pickle.load(f)

# print(df.head())
# print(team_order.keys())

X = np.array(df[['team1', 'team2']])
x = preprocessing.scale(X)

y = np.array(df['result'])

X_train, X_test, y_train, y_test = cross_validation.train_test_split(
    x, y, test_size=0.2)

clf = LinearRegression(n_jobs=-1)

clf.fit(X_train, y_train)
accuracy = clf.score(X_test, y_test)

print(accuracy)

teama = 'OMG'
teamb = 'IG'

teama = team_order[teama]
teamb = team_order[teamb]

print(teama, teamb)

X = np.append(X, [[teama, teamb]], axis=0)

x = preprocessing.scale(X)

result = clf.predict(x[-1])

result = np.array_str(result)

print(list_result[int(result[2])])
