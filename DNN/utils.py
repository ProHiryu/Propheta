#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# Copyright (c) 2018 - songheqi <songheqi1996@gmail.com>


import tensorflow as tf
import numpy as np

import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

def safe_mkdir(path):
    """ Create a directory if there isn't one already. """
    try:
        os.mkdir(path)
    except OSError:
        pass


def parse_data(path, dataset, flatten):
    pass



def read_data(path, flatten=True, num_train=55000):
    pass



def get_dataset(batch_size):
    # Step 1: Read in data
    train, val, test = read_data('/', flatten=True, num_train=55000)

    # Step 2: Create datasets and iterator
    train_data = tf.data.Dataset.from_tensor_slices(train)
    train_data = train_data.shuffle(10000) # if you want to shuffle your data
    train_data = train_data.batch(batch_size)

    test_data = tf.data.Dataset.from_tensor_slices(test)
    test_data = test_data.batch(batch_size)

    return train_data, test_data
