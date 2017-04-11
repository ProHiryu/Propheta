# -*- coding:utf-8 -*-
import sqlite3
import pandas as pd
import numpy as np
from sklearn import preprocessing, cross_validation, svm
from sklearn.linear_model import LogisticRegression
import pickle

conn1 = sqlite3.connect('game_data.sqlite')
cur = conn1.cursor()

cur.executescript('''
DROP TABLE IF EXISTS Games;

CREATE TABLE Games (
    id             INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    team1          INTEGER,
    team2          INTEGER,
    result         INTEGER
);
''')


def team_order_change(x):
    return team_order[x]

coon = sqlite3.connect('lol.sqlite')
sql = "select * from Games"

df = pd.read_sql(sql, coon, index_col='id')

results = []
teams = []
list_result = {1: (1, 0), 2: (2, 0), 3: (2, 1), 4: (3, 0), 5: (3, 1), 6: (
    3, 2), -1: (0, 1), -2: (0, 2), -3: (1, 2), -4: (0, 3), -5: (1, 3), -6: (2, 3)}

for line in df.values:
    if line[3] not in teams:
        teams.append(line[3])
    if line[2] not in teams:
        teams.append(line[2])
    if [line[4], line[5]] == [1, 0]:
        results.append(1)
    elif [line[4], line[5]] == [2, 0]:
        results.append(2)
    elif [line[4], line[5]] == [2, 1]:
        results.append(3)
    elif [line[4], line[5]] == [3, 0]:
        results.append(4)
    elif [line[4], line[5]] == [3, 1]:
        results.append(5)
    elif [line[4], line[5]] == [3, 2]:
        results.append(6)
    elif [line[5], line[4]] == [1, 0]:
        results.append(-1)
    elif [line[5], line[4]] == [2, 0]:
        results.append(-2)
    elif [line[5], line[4]] == [2, 1]:
        results.append(-3)
    elif [line[5], line[4]] == [3, 0]:
        results.append(-4)
    elif [line[5], line[4]] == [3, 1]:
        results.append(-5)
    elif [line[5], line[4]] == [3, 2]:
        results.append(-6)
    else:
        results.append(np.nan)

df['results'] = results

teams = sorted(teams)
team_order = dict()

for i in range(len(teams)):
    team_order[teams[i]] = (i + 1)

with open("team_order.pickle","wb") as f:
    pickle.dump(team_order,f)

team1 = []
team2 = []

for line in df.values:
    team1.append(team_order_change(line[2]))
    team2.append(team_order_change(line[3]))

df = df.fillna(value=0)

df['team1'] = team1
df['team2'] = team2

X = np.array(df[['team1', 'team2']])
x = preprocessing.scale(X)

# print(x)
# print(X.shape)

y = np.array(df['results'])
# print(y)

for line in df.values:
    cur.execute('''INSERT INTO Games (team1,team2,result) VALUES ( ?, ?, ?)''',
                (line[2], line[3], line[7]))
    print("{:8d}{:8d}{:6d}".format(line[2], line[3], line[7]))

conn1.commit()

X_train, X_test, y_train, y_test = cross_validation.train_test_split(
    x, y, test_size=0.2)

clf = LogisticRegression(n_jobs=-1)

# print(y)

clf.fit(X_train, y_train)
accuracy = clf.score(X_test, y_test)
# forecast_set = clf.predict(X_lately)
print(accuracy)

# teama = 'SKT'
# teamb = 'AHQ'
#
# teama = team_order_change(teama)
# teamb = team_order_change(teamb)
#
# print(teama, teamb)
#
# X = np.append(X, [[75, 233]], axis=0)
#
# x = preprocessing.scale(X)
#
# # print(X.shape)
# # print(x)
#
# # print(x[-1])
#
# result = clf.predict(x[-1])
#
# # print(type(result))
#
# result = np.array_str(result)
#
# # print(type(result))
# #
# print(list_result[int(result[2])])

# print (team_order)

# print(team_order_change('TSM'))

# print(len(results),len(df))
#
# print(df.head())

# print(df.head(), len(df))
#
# print(df.columns)


coon.close()
conn1.close()
