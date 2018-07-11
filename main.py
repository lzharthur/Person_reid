#!/usr/bin/env python
# -*- coding_utf-8 -*-
"""
    Author: Zhenghan Lee
    Date: 2018/07/10
"""
import os
import tensorflow as tf
import cv2
from generate_face import gene_face
import numpy as np
import argparse
import sys
import time
import warnings

warnings.filterwarnings('ignore')

def prewhiten(x):
    mean = np.mean(x)
    std = np.std(x)
    std_adj = np.maximum(std, 1.0/np.sqrt(x.size))
    y = np.multiply(np.subtract(x, mean), 1/std_adj)
    return y

def main(args):
    root_dir = args.model_dir
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    with tf.Session() as sess:
        saver = tf.train.import_meta_graph(os.path.join(root_dir,'model-20180711.meta'))
        saver.restore(sess, tf.train.latest_checkpoint(root_dir))
        #a = np.load(os.path.join(root_dir,'lee.npy'))
        cap = cv2.VideoCapture(0)
        time.sleep(0.5)
        images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
        embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
        phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")

        file1 = tf.read_file('/Users/lees/Desktop/Person_reid/t2.png')

        img1 = tf.image.decode_png(file1, channels=1)
        image1 = tf.image.resize_images(img1, (160, 160), method=1)

        #while True:
        ret, img = cap.read()
        #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #faces = face_cascade.detectMultiScale(img, 1.3, 5)

        cv2.imwrite(os.path.join(root_dir,'t1.png'),img)
        print(os.path.join(root_dir,'t1.png'))
        img2 = cv2.imread(os.path.join(root_dir,'t1.png'))
        # for (x1, y, w, h) in faces:
        #     face = img[y:y + h, x1:x1 + w]
        r = gene_face(img2, os.path.join(root_dir,'t2.png'))
        if r == True:
            file2 = tf.read_file(os.path.join(root_dir,'t2.png'))

            img2 = tf.image.decode_png(file2, channels=1)
            image2 = tf.image.resize_images(img2, (160, 160), method=1)
            img1_pre = tf.image.per_image_standardization(image1)
            img2_pre = tf.image.per_image_standardization(image2)
            img1, img2 = sess.run([img1_pre, img2_pre])
            img = np.array([img1, img2])
            emb1 = sess.run(embeddings, feed_dict={images_placeholder: img, phase_train_placeholder: False})
            dist = np.sum(np.square(emb1[0] - emb1[1]))
            print(dist)
        else:
            pass
        # if os.path.exists(os.path.join(root_dir, 't1.png')):
        #     os.remove(os.path.join(root_dir, 't1.png'))
        # if os.path.exists(os.path.join(root_dir, 't2.png')):
        #     os.remove(os.path.join(root_dir, 't2.png'))

            # for (x1, y, w, h) in faces:
            #     face = img[y:y + h-20, x1+20:x1 + w-40]
            #     cv2.rectangle(img, (x1+20, y), (x1 + w-40, y + h-20), (255, 0, 0), 2)
            #
            #     cv2.imwrite(os.path.join(root_dir,'t1.png'),face)
            #     file2 = tf.read_file(os.path.join(root_dir,'t1.png'))
            #
            #     img2 = tf.image.decode_png(file2, channels=1)
            #     image2 = tf.image.resize_images(img2, (160, 160), method=1)
            #     img1_pre = tf.image.per_image_standardization(image1)
            #     img2_pre = tf.image.per_image_standardization(image2)
            #
            #     img1, img2 = sess.run([img1_pre, img2_pre])
            #     img_total = np.array([img1, img2])
            #     emb1 = sess.run(embeddings, feed_dict={images_placeholder: img_total, phase_train_placeholder: False})
            #     dist1 = np.sum(np.square(emb1[0] - emb1[1]))
            #     # dist2 = np.sum(np.square(emb1[2] - emb1[1]))
            #     #
            #     print(dist1)
        #cv2.imshow('img', img)

        #if cv2.waitKey(10) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
            #break



def parse(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_dir', type=str,
                        help='Directory where model in.',default='/Users/lees/Desktop/model')
    return parser.parse_args(argv)


if __name__ == '__main__':
    main(parse(sys.argv[1:]))

