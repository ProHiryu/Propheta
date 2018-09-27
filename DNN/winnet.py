#!/anaconda3/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2018 - songheqi <songheqi1996@gmail.com>


import tensorflow as tf
import numpy as np

import utils
import time

import os

os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

def linear_relu(inputs, output_dim, scope_name):
    '''
    A method that does linear + relu on inputs
    '''
    with tf.variable_scope(scope_name, reuse=tf.AUTO_REUSE) as scope:
        input_dim = inputs.shape[1]
        w = tf.get_variable("weights", [input_dim, output_dim], initializer=tf.contrib.layers.xavier_initializer())
        b = tf.get_variable("biases", [1, output_dim], initializer=tf.zeros_initializer())
    
    return tf.nn.relu(tf.matmul(inputs, w) + b, name=scope_name)

def dropout(inputs, keep_prob, scope_name):
    '''
    A method that does dropout
    '''
    with tf.variable_scope(scope_name, reuse=tf.AUTO_REUSE) as scope:
        drop = tf.nn.dropout(inputs, keep_prob, name=scope_name)
    
    return drop

def final(inputs, n_classes, scope_name):
    '''
    A method that does output
    '''
    with tf.variable_scope(scope_name, reuse=tf.AUTO_REUSE) as scope:
        input_dim = inputs.shape[1]
        w = tf.get_variable("weights", [input_dim, n_classes], initializer=tf.contrib.layers.xavier_initializer())
        b = tf.get_variable("biases", [1, n_classes], initializer=tf.zeros_initializer())
    
    return tf.matmul(inputs, w, name=scope_name) + b


class WinNet:
    def __init__(self):
        self.lr = 0.01
        self.batch_size = 128
        self.keep_prob = tf.constant(0.75)
        self.gstep = tf.Variable(0, dtype=tf.int32,
                                trainable=False, name="global_step")

        '''
        need to be decided self.n_test and self.traning
        '''
        self.n_classes = 2
        self.skip_step = 100
        self.n_test = 475
        self.trainning = None


    def import_data(self):
        with tf.name_scope("data"):
            train_data, test_data = utils.get_dataset(self.batch_size)
            iterator = tf.data.Iterator.from_structure(train_data.output_types,
                                                    train_data.output_shapes)
            self.game, self.label = iterator.get_next()

            self.train_init = iterator.make_initializer(train_data)   # initializer for train_data
            self.test_init = iterator.make_initializer(test_data)    # initializer for train_data


    def inference(self):
        '''
        Implement of forward propagation of the following model.
            LINEAR -> RELU -> LINEAR -> RELU -> LINEAR -> SIGMOID
        '''
        linear1 = linear_relu(self.game, 300, scope_name='linear1')
        dropout1 = dropout(linear1, self.keep_prob, scope_name='dropout1')
        linear2 = linear_relu(dropout1, 300, scope_name='linear2')
        dropout2 = dropout(linear2, self.keep_prob, scope_name='dropout2')
        linear3 = linear_relu(dropout2, 50, scope_name='linear3')
        dropout3 = dropout(linear3, self.keep_prob, scope_name='dropout3')
        self.logits = final(dropout3, self.n_classes, scope_name='output')


    def create_loss(self):
        '''
        define loss function
        use sigmoid cross entropy with logits as the loss function
        '''
        with tf.name_scope('loss'):
            entropy = tf.nn.softmax_cross_entropy_with_logits_v2(labels=self.label, logits=self.logits)
            self.loss = tf.reduce_mean(entropy, name='loss')        


    def optimize(self):
        '''
        Define training op
        using Adam Gradient Descent to minimize cost
        Don't forget to use global step
        '''
        with tf.name_scope('optimize'):
            self.opt = tf.train.AdamOptimizer(learning_rate=self.lr).minimize(loss=self.loss,
                                                                            global_step=self.gstep)

    def summary(self):
        '''
        Create summaries to write on TensorBoard
        Remember to track both training loss and test accuracy
        '''
        with tf.name_scope('summaries'):
            tf.summary.scalar('loss', self.loss)
            tf.summary.scalar('accuracy', self.accuracy)
            tf.summary.histogram('histogram loss', self.loss)
            self.summary_op = tf.summary.merge_all()

    def eval(self):
        '''
        Count the number of right predictions in a batch
        '''
        with tf.name_scope('predict'):
            preds = tf.nn.softmax(self.logits)
            correct_preds = tf.equal(tf.argmax(preds, 1), tf.argmax(self.label, 1))
            self.accuracy = tf.reduce_sum(tf.cast(correct_preds, tf.float32))

    
    def build(self):
        '''
        Build the computation graph
        '''
        self.import_data()
        self.inference()
        self.create_loss()
        self.optimize()
        self.eval()
        self.summary()

    
    def train_one_epoch(self, sess, saver, init, writer, epoch, step):
        start_time = time.time()
        sess.run(init)
        total_loss = 0
        n_batches = 0

        try:
            while True:
                # _, l = sess.run([self.opt, self.loss])
                _, l, summaries = sess.run([self.opt, self.loss, self.summary_op])
                writer.add_summary(summaries, global_step=step)
                if (step + 1) % self.skip_step == 0:
                    print('Loss at step {0}: {1}'.format(step, l))
                step += 1
                total_loss += l
                n_batches += 1
        except tf.errors.OutOfRangeError:
            pass
        
        saver.save(sess, 'checkpoints/winnet_layers/winnet', step)
        print('Average loss at epoch {0}: {1}'.format(epoch, total_loss/n_batches))
        print('Took: {0} seconds'.format(time.time() - start_time))
        return step
    
    
    def eval_once(self, sess, init, writer, epoch, step):
        '''
        make one prediction
        '''
        start_time = time.time()
        sess.run(init)
        total_correct_preds = 0
        try:
            while True:
                accuracy_batch, summaries = sess.run([self.accuracy, self.summary_op])
                # accuracy_batch = sess.run(self.accuracy)
                writer.add_summary(summaries, global_step=step)
                total_correct_preds += accuracy_batch
        except tf.errors.OutOfRangeError:
            pass

        print('Accuracy at epoch {0}: {1} '.format(epoch, total_correct_preds/self.n_test))
        print('Took: {0} seconds'.format(time.time() - start_time))


    def train(self, n_epochs):
        '''
        The train function alternates between training one epoch and evaluating
        '''
        utils.safe_mkdir('checkpoints')
        utils.safe_mkdir('checkpoints/winnet_layers')
        writer = tf.summary.FileWriter('./graphs/winnet_layers', tf.get_default_graph())

        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())
            saver = tf.train.Saver()
            ckpt = tf.train.get_checkpoint_state(os.path.dirname('checkpoints/winnet_layers/checkpoint'))
            if ckpt and ckpt.model_checkpoint_path:
                saver.restore(sess, ckpt.model_checkpoint_path)
            
            step = self.gstep.eval()

            for epoch in range(n_epochs):
                step = self.train_one_epoch(sess, saver, self.train_init, writer, epoch, step)
                self.eval_once(sess, self.test_init, writer, epoch, step)
        writer.close()


if __name__ == '__main__':
    model = WinNet()
    model.build()
    model.train(n_epochs=150)
