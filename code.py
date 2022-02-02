import os
import glob
import numpy as np
import cv2
import tensorflow as tf
from fr_utils import *
from inception_blocks_v2 import *
from keras import backend as K
from PIL import Image as I

facelist = []

def coltogray(img):
    arr = np.asarray(img, dtype='uint8')
    x, y, _ = arr.shape
    k = np.array([[[0.2989, 0.587, 0.114]]])
    arr2 = np.round(np.sum(arr * k, axis=2)).astype(np.uint8).reshape((x, y))
    img = I.fromarray(arr2)
    img.save('chb.jpg', 'JPEG')

def start(mimg):
    print("that's OK")
    K.set_image_data_format('channels_first')
    PADDING = 30
    ready_to_detect_identity = True
    FRmodel = faceRecoModel(input_shape=(3, 96, 96))
    FRmodel.compile(optimizer='adam', loss=triplet_loss, metrics=['accuracy'])
    load_weights_from_FaceNet(FRmodel)
    database = prepare_database(FRmodel)
    coltogray(mimg)
    mimg = cv2.imread('chb.jpg')
    image_face_recognizer(database, mimg, FRmodel, PADDING, ready_to_detect_identity)
    return facelist

def triplet_loss(y_true, y_pred, alpha=0.3):
    anchor, positive, negative = y_pred[0], y_pred[1], y_pred[2]
    pos_dist = tf.reduce_sum(tf.square(tf.subtract(anchor, positive)), axis=-1)
    neg_dist = tf.reduce_sum(tf.square(tf.subtract(anchor, negative)), axis=-1)
    basic_loss = tf.add(tf.subtract(pos_dist, neg_dist), alpha)
    loss = tf.reduce_sum(tf.maximum(basic_loss, 0.0))
    return loss

def prepare_database(FRmodel):
    database = {}
    for file in glob.glob("bd/*"):
        identity = os.path.splitext(os.path.basename(file))[0]
        if (identity != "desktop") :
            database[identity] = img_path_to_encoding(file, FRmodel)
    return database


def image_face_recognizer(database, img, FRmodel, PADDING, ready_to_detect_identity):
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    if ready_to_detect_identity:
        img = process_frame(img, face_cascade, PADDING, database, FRmodel)

def process_frame(img, face_cascade, PADDING, database, FRmodel):
    global ready_to_detect_identity
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    identities = []
    for (x, y, w, h) in faces:
        x1 = x-PADDING
        y1 = y-PADDING
        x2 = x+w+PADDING
        y2 = y+h+PADDING
        img = cv2.rectangle(img,(x1, y1),(x2, y2),(255,0,0),2)
        identity = find_identity(img, x1, y1, x2, y2, database, FRmodel)
        if identity is not None:
            identities.append(identity)
    return img


def find_identity(img, x1, y1, x2, y2, database, FRmodel):
    height, width, channels = img.shape
    part_image = img[max(0, y1):min(height, y2), max(0, x1):min(width, x2)]
    return who_is_it(part_image, database, FRmodel)

def who_is_it(image, database, model):
    encoding = img_to_encoding(image, model)
    dists = []
    names = []
    for (name, db_enc) in database.items():
        dist = np.linalg.norm(db_enc - encoding)
        dists.insert(0, dist)
        names.insert(0, "bd/" + name + ".jpg")
    global facelist
    facelist = list(zip(dists, names))
    facelist.sort()
    return None