import pickle
import sqlite3
import pandas as pd
from sklearn import preprocessing, cross_validation, svm, neighbors
from sklearn.linear_model import LogisticRegression
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

# print(X)

y = np.array(df['result'])

# print(y)

X_train, X_test, y_train, y_test = cross_validation.train_test_split(
    X, y, test_size=0.2)

clf = neighbors.KNeighborsClassifier()

clf.fit(X_train, y_train)
accuracy = clf.score(X_test, y_test)

print(accuracy)

teama = input('team1 : ')
teamb = input('team2 : ')

teama = team_order[teama]
teamb = team_order[teamb]

print(teama, teamb)

example_measures = np.array([teama, teamb])

result = clf.predict(example_measures)
result = np.array_str(result)

# print(result[1])

if result[1] == '-':
    print(list_result[int(result[2])])
else:
    print(list_result[int(result[1])])
