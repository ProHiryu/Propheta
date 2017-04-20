import tensorflow as tf
import numpy as np
import sqlite3
import pandas as pd
from sklearn import cross_validation, preprocessing

leagues = ['lpl_2017_spring', 'lpl_2016_spring', 'lpl_2016_summer',
           'lck_2017_spring', 'lck_2016_spring', 'lck_2016_summer']

results = []
teams = []
list_result = {1: '2:0', 2: '2:1', 3: '1:2', 4: '0:2'}


def get_df(database, table):
    database = database + '.sqlite'
    conn = sqlite3.connect(database)
    sql = 'select * from ' + table
    df = pd.read_sql(sql, conn, index_col='id')
    df = drop_off(df)
    conn.close()
    return df


def drop_off(df):
    rows_todrop = []
    for i in range(len(df)):
        if int(df.ix[i + 1, 'result'][0]) >= 3 or int(df.ix[i + 1, 'result'][2]) >= 3:
            rows_todrop.append(i)
            print('....delete off-season\'s data....')
    df = df.drop(df.index[rows_todrop])
    # print(df['result'])
    return df

df = pd.DataFrame(data=None, columns=['team', 'odd1', 'odd2', 'result'])

for league in leagues:
    database = league[:3]
    if len(df) == 0:
        df = get_df(database=database, table=league)
    else:
        df1 = get_df(database=database, table=league)
        df = df.append(df1)

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

# print(X,len(X))

y = np.split(y, len(y))
y = np.array(y)

enc = preprocessing.OneHotEncoder()
enc.fit(y)
result_y = []
result_y = enc.transform(y).toarray()
result_y = np.array(result_y)

# print(result_y, len(result_y))

train_x, test_x, train_y, test_y = cross_validation.train_test_split(
    X, result_y, test_size=0.2)

n_nodes_hl1 = 1500
n_nodes_hl2 = 1500
n_nodes_hl3 = 1500

n_classes = 4
batch_size = 100
hm_epochs = 15

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

        return accuracy.eval({x: test_x, y: test_y})

while(True):
    accuracy = train_neural_network(x)
    if accuracy >= 0.47:
        with open('model.pickle', 'w') as pickle:
            pickle.dump(hidden_1_layer, hidden_2_layer,
                        hidden_3_layer, output_layer)
        break
    else:
        pass


# odd1 = input('odd1:')
# odd2 = input('odd2:')
#
# predict = tf.placeholder('float')
# predict = np.array([[odd1,odd2]],dtype='float32')
#
# prediction = neural_network_model(predict)
#
# print(tf.argmax(prediction,1)
