import tensorflow as tf
#from tensorflow.examples.tutorials.mnist import input_data
import pickle
import numpy as np
import sqlite3
import pandas as pd
from sklearn import cross_validation, preprocessing

conn = sqlite3.connect('game_data.sqlite')

sql = 'select * from Games'

results = []
teams = []
list_result = {1: (1, 0), 2: (2, 0), 3: (2, 1), 4: (3, 0), 5: (3, 1), 6: (
    3, 2), -1: (0, 1), -2: (0, 2), -3: (1, 2), -4: (0, 3), -5: (1, 3), -6: (2, 3)}

df = pd.read_sql(sql, conn, index_col='id')
with open('team_order.pickle', 'rb') as f:
    team_order = pickle.load(f)

X = np.array(df[['team1', 'team2']])

Y = np.array(df['result'])

for i in range(len(Y)):
    if(Y[i] == -1):
        Y[i] = 7
    elif(Y[i] == -2):
        Y[i] = 8
    elif(Y[i] == -3):
        Y[i] = 9
    elif(Y[i] == -4):
        Y[i] = 10
    elif(Y[i] == -5):
        Y[i] = 11
    elif(Y[i] == -6):
        Y[i] = 12

Y = np.split(Y, len(Y))
Y = np.array(Y)
enc = preprocessing.OneHotEncoder()
enc.fit(Y)

result_y = []

result_y = enc.transform(Y).toarray()

result_y = np.array(result_y)

train_x, test_x, train_y, test_y = cross_validation.train_test_split(
    X, result_y, test_size=0.2)

n_nodes_hl1 = 1500
n_nodes_hl2 = 1500
n_nodes_hl3 = 1500

n_classes = 13
batch_size = 100
hm_epochs = 10

x = tf.placeholder('float')
y = tf.placeholder('float')

hidden_1_layer = {'f_fum': n_nodes_hl1,
                  'weight': tf.Variable(tf.random_normal([len(train_x[0]), n_nodes_hl1])),
                  'bias': tf.Variable(tf.random_normal([n_nodes_hl1]))}

hidden_2_layer = {'f_fum': n_nodes_hl2,
                  'weight': tf.Variable(tf.random_normal([n_nodes_hl1, n_nodes_hl2])),
                  'bias': tf.Variable(tf.random_normal([n_nodes_hl2]))}

hidden_3_layer = {'f_fum': n_nodes_hl3,
                  'weight': tf.Variable(tf.random_normal([n_nodes_hl2, n_nodes_hl3])),
                  'bias': tf.Variable(tf.random_normal([n_nodes_hl3]))}

output_layer = {'f_fum': None,
                'weight': tf.Variable(tf.random_normal([n_nodes_hl3, n_classes])),
                'bias': tf.Variable(tf.random_normal([n_classes])), }


# Nothing changes
def neural_network_model(data):

    l1 = tf.add(tf.matmul(data, hidden_1_layer[
                'weight']), hidden_1_layer['bias'])
    l1 = tf.nn.relu(l1)

    l2 = tf.add(tf.matmul(l1, hidden_2_layer[
                'weight']), hidden_2_layer['bias'])
    l2 = tf.nn.relu(l2)

    l3 = tf.add(tf.matmul(l2, hidden_3_layer[
                'weight']), hidden_3_layer['bias'])
    l3 = tf.nn.relu(l3)

    output = tf.matmul(l3, output_layer['weight']) + output_layer['bias']

    return output


def train_neural_network(x):
    prediction = neural_network_model(x)
    cost = tf.reduce_mean(
        tf.nn.softmax_cross_entropy_with_logits(logits=prediction, labels=y))
    optimizer = tf.train.AdamOptimizer(learning_rate=0.001).minimize(cost)

    with tf.Session() as sess:
        sess.run(tf.initialize_all_variables())

        for epoch in range(hm_epochs):
            epoch_loss = 0
            i = 0
            while i < len(train_x):
                start = i
                end = i + batch_size
                batch_x = np.array(train_x[start:end])
                batch_y = np.array(train_y[start:end])

                _, c = sess.run([optimizer, cost], feed_dict={x: batch_x,
                                                              y: batch_y})
                epoch_loss += c
                i += batch_size

            print('Epoch', epoch + 1, 'completed out of',
                  hm_epochs, 'loss:', epoch_loss)
        correct = tf.equal(tf.argmax(prediction, 1), tf.argmax(y, 1))
        accuracy = tf.reduce_mean(tf.cast(correct, 'float'))

        print('Accuracy:', accuracy.eval({x: test_x, y: test_y}))

conn.close()

train_neural_network(x)
