import pickle
import sqlite3
import pandas as pd
from sklearn import preprocessing, cross_validation, svm, neighbors
from sklearn.linear_model import LogisticRegression
import numpy as np

conn = sqlite3.connect('lpl.sqlite')

sql = 'select * from lpl_2017_spring'

results = []
teams = []
list_result = {1: '2:0', 2: '2:1', 3: '1:2', 4: '0:2'}

df = pd.read_sql(sql, conn, index_col='id')

X = np.array(df[['odd1', 'odd2']])

y = np.array(df['result'])

for i in range(len(y)):
    if y[i] == '2:0':
        y[i] = 1
    elif y[i] == '2:1':
        y[i] = 2
    elif y[i] == '1:2':
        y[i] = 3
    elif y[i] == '0:2':
        y[i] = 4

y = np.array(y,dtype="|S6")

print(y)

X_train, X_test, y_train, y_test = cross_validation.train_test_split(
    X, y, test_size=0.2)

clf = LogisticRegression(n_jobs=-1)

clf.fit(X_train, y_train)
accuracy = clf.score(X_test, y_test)

print(accuracy)

teama = input('odd1 : ')
teamb = input('odd2 : ')

example_measures = np.array([teama, teamb])

result = clf.predict(example_measures)

result = np.array_str(result)

print(result)
