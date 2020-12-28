import numpy as np
import math
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
from tensorflow.python.framework import graph_util

tra_data_dir = 'train.tfrecords'
val_data_dir = 'val.tfrecords'

max_learning_rate = 0.0002  # 0.0002
min_learning_rate = 0.0001
decay_speed = 2000.0
lr = tf.placeholder(tf.float32)
learning_rate = lr
W = 153
H = 128
Channels = 1
n_classes = 3


def read_and_decode2stand(tfrecords_file, batch_size):


    # make an input queue from the tfrecord file
    filename_queue = tf.train.string_input_producer([tfrecords_file])

    reader = tf.TFRecordReader()
    _, serialized_example = reader.read(filename_queue)
    img_features = tf.parse_single_example(
        serialized_example,
        features={
            'label': tf.FixedLenFeature([], tf.int64),
            'image_raw': tf.FixedLenFeature([], tf.string),
        })
    image = tf.decode_raw(img_features['image_raw'], tf.uint8)

    image = tf.reshape(image, [H, W, Channels])
    image = tf.cast(image, tf.float32) * (1.0 / 255)
    image = tf.image.per_image_standardization(image)  # standardization

    # all the images of notMNIST are 200*150, you need to change the image size if you use other dataset.
    label = tf.cast(img_features['label'], tf.int32)
    image_batch, label_batch = tf.train.batch([image, label],
                                              batch_size=batch_size,
                                              num_threads=64,
                                              capacity=2000)
    # Change to ONE-HOT
    label_batch = tf.one_hot(label_batch, depth=n_classes)
    label_batch = tf.cast(label_batch, dtype=tf.int32)
    label_batch = tf.reshape(label_batch, [batch_size, n_classes])
    print(label_batch)
    return image_batch, label_batch


def my_batch_norm(inputs):
    scale = tf.Variable(tf.ones([inputs.get_shape()[-1]]), dtype=tf.float32)
    beta = tf.Variable(tf.zeros([inputs.get_shape()[-1]]), dtype=tf.float32)
    batch_mean = tf.Variable(tf.zeros([inputs.get_shape()[-1]]), trainable=False)
    batch_var = tf.Variable(tf.ones([inputs.get_shape()[-1]]), trainable=False)

    batch_mean, batch_var = tf.nn.moments(inputs, [0, 1, 2])
    return inputs, batch_mean, batch_var, beta, scale


def build_network(height, width, channel):
    x = tf.placeholder(tf.float32, shape=[None, height, width, channel], name="input")  ####这个名称很重要！！！
    y = tf.placeholder(tf.int32, shape=[None, n_classes], name="labels_placeholder")

    def weight_variable(shape, name="weights"):
        initial = tf.truncated_normal(shape, stddev=0.1)
        return tf.Variable(initial, name=name)

    def bias_variable(shape, name="biases"):
        initial = tf.constant(0.1, shape=shape)
        return tf.Variable(initial, name=name)

    def conv2d(input, w):
        return tf.nn.conv2d(input, w, [1, 1, 1, 1], padding='SAME')

    def pool_max(input):
        return tf.nn.max_pool(input,
                              ksize=[1, 3, 3, 1],
                              strides=[1, 2, 2, 1],
                              padding='SAME',
                              name='pool1')

    def fc(input, w, b):
        return tf.matmul(input, w) + b

    # conv1
    with tf.name_scope('conv1_1') as scope:
        kernel = weight_variable([3, 3, Channels, 64])
        biases = bias_variable([64])
        conv1_1 = tf.nn.bias_add(conv2d(x, kernel), biases)
        inputs, pop_mean, pop_var, beta, scale = my_batch_norm(conv1_1)
        conv_batch_norm = tf.nn.batch_normalization(inputs, pop_mean, pop_var, beta, scale, 0.001)
        output_conv1_1 = tf.nn.relu(conv_batch_norm, name=scope)



    pool1 = pool_max(output_conv1_1)

    # conv2
    with tf.name_scope('conv2_1') as scope:
        kernel = weight_variable([3, 3, 64, 128])
        biases = bias_variable([128])
        conv2_1 = tf.nn.bias_add(conv2d(pool1, kernel), biases)
        inputs, pop_mean, pop_var, beta, scale = my_batch_norm(conv2_1)
        conv_batch_norm = tf.nn.batch_normalization(inputs, pop_mean, pop_var, beta, scale, 0.001)
        output_conv2_1 = tf.nn.relu(conv_batch_norm, name=scope)

    pool2 = pool_max(output_conv2_1)

    # conv3
    with tf.name_scope('conv3_1') as scope:
        kernel = weight_variable([3, 3, 128, 256])
        biases = bias_variable([256])
        conv3_1 = tf.nn.bias_add(conv2d(pool2, kernel), biases)
        inputs, pop_mean, pop_var, beta, scale = my_batch_norm(conv3_1)
        conv_batch_norm = tf.nn.batch_normalization(inputs, pop_mean, pop_var, beta, scale, 0.001)
        output_conv3_1 = tf.nn.relu(conv_batch_norm, name=scope)



    # fc6
    with tf.name_scope('fc6') as scope:
        shape = int(np.prod(output_conv3_1.get_shape()[1:]))
        kernel = weight_variable([shape, 120])
        # kernel = weight_variable([shape, 4096])
        # biases = bias_variable([4096])
        biases = bias_variable([120])
        pool5_flat = tf.reshape(output_conv3_1, [-1, shape])
        output_fc6 = tf.nn.relu(fc(pool5_flat, kernel, biases), name=scope)


    # fc8
    with tf.name_scope('fc8') as scope:
        # kernel = weight_variable([4096, n_classes])
        kernel = weight_variable([120, n_classes])
        biases = bias_variable([n_classes])
        output_fc8 = tf.nn.relu(fc(output_fc6, kernel, biases), name=scope)

    finaloutput = tf.nn.softmax(output_fc8, name="softmax")  ####这个名称很重要！！

    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=finaloutput, labels=y)) * 1000
    optimize = tf.train.AdamOptimizer(lr).minimize(cost)

    prediction_labels = tf.argmax(finaloutput, axis=1, name="output")  ####这个名称很重要！！！
    read_labels = tf.argmax(y, axis=1)

    correct_prediction = tf.equal(prediction_labels, read_labels)
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    correct_times_in_batch = tf.reduce_sum(tf.cast(correct_prediction, tf.int32))

    return dict(
        x=x,
        y=y,
        lr=lr,
        optimize=optimize,
        correct_prediction=correct_prediction,
        correct_times_in_batch=correct_times_in_batch,
        cost=cost,
        accuracy=accuracy,
    )


def train_network(graph, batch_size, num_epochs, pb_file_path):
    tra_image_batch, tra_label_batch = read_and_decode2stand(tfrecords_file=tra_data_dir,
                                                             batch_size=batch_size)
    val_image_batch, val_label_batch = read_and_decode2stand(tfrecords_file=val_data_dir,
                                                             batch_size=batch_size)
    init = tf.global_variables_initializer()
    with tf.Session() as sess:
        sess.run(init)
        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(sess=sess, coord=coord)
        epoch_delta = 1
        best_accuracy = 0
        best_accuracy_train=0
        try:
            for epoch_index in range(num_epochs):
                learning_rate = min_learning_rate + (max_learning_rate - min_learning_rate) * math.exp(
                    -epoch_index / decay_speed)
                tra_images, tra_labels = sess.run([tra_image_batch, tra_label_batch])
                accuracy, mean_cost_in_batch, return_correct_times_in_batch, _ = sess.run(
                    [graph['accuracy'], graph['cost'], graph['correct_times_in_batch'], graph['optimize']], feed_dict={
                        graph['x']: tra_images,
                        graph['lr']: learning_rate,
                        graph['y']: tra_labels
                    })
                if epoch_index % epoch_delta == 0:
                    # 开始在 train set上计算一下accuracy和cost
                    print("index[%s]".center(50, '-') % epoch_index)
                    print("Train: cost_in_batch：{},correct_in_batch：{},accuracy：{}".format(mean_cost_in_batch,
                                                                                           return_correct_times_in_batch,
                                                                                           accuracy))

                    # 开始在 test set上计算一下accuracy和cost
                    val_images, val_labels = sess.run([val_image_batch, val_label_batch])
                    mean_cost_in_batch, return_correct_times_in_batch = sess.run(
                        [graph['cost'], graph['correct_times_in_batch']], feed_dict={
                            graph['x']: val_images,
                            graph['y']: val_labels
                        })
                    print("***Val: cost_in_batch：{},correct_in_batch：{},accuracy：{}".format(mean_cost_in_batch,
                                                                                            return_correct_times_in_batch,
                                                                                            return_correct_times_in_batch / batch_size))

                if best_accuracy_train<accuracy:
                    best_accuracy_train=accuracy
                    print("train",best_accuracy_train)

                if best_accuracy < (return_correct_times_in_batch / batch_size):
                    best_accuracy = (return_correct_times_in_batch / batch_size)
                    constant_graph = graph_util.convert_variables_to_constants(sess, sess.graph_def, ["output"])
                     
                    with tf.gfile.FastGFile(pb_file_path, mode='wb') as f:
                        f.write(constant_graph.SerializeToString())
                    
                    print("Val",best_accuracy)
        except tf.errors.OutOfRangeError:
            print('Done training -- epoch limit reached')
        finally:
            print("test",best_accuracy_train)
            print("Val",best_accuracy)
            coord.request_stop()
        coord.join(threads)
        sess.close()


if __name__ == "__main__":
    batch_size = 16
    num_epochs = 200

    pb_file_path = "SFL-1228-6.pb"
    g = build_network(height=H, width=W, channel=1)
    train_network(g, batch_size, num_epochs, pb_file_path)