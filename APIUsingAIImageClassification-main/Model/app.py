import flask
from flask_restful import Resource, Api, reqparse
import tflearn
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
import cv2
import numpy as np
from numpy import array
import werkzeug

app = flask.Flask(__name__)
api = Api(app)

# load model
IMG_SIZE = 50
LR = 1e-3
MODEL_NAME = 'SkinCancer-{}-{}.model'.format(LR, '6conv-basic')
convnet = input_data(shape=[None, IMG_SIZE, IMG_SIZE, 1], name='input')
convnet = conv_2d(convnet, 32, 5, activation='relu')
convnet = max_pool_2d(convnet, 5)
convnet = conv_2d(convnet, 64, 5, activation='relu')
convnet = max_pool_2d(convnet, 5)
convnet = conv_2d(convnet, 128, 5, activation='relu')
convnet = max_pool_2d(convnet, 5)
convnet = conv_2d(convnet, 64, 5, activation='relu')
convnet = max_pool_2d(convnet, 5)
convnet = conv_2d(convnet, 32, 5, activation='relu')
convnet = max_pool_2d(convnet, 5)
convnet = fully_connected(convnet, 1024, activation='relu')
convnet = dropout(convnet, 0.8)
convnet = fully_connected(convnet, 2, activation='softmax')
convnet = regression(convnet, optimizer='adam', learning_rate=LR, loss='categorical_crossentropy', name='targets')

model = tflearn.DNN(convnet, tensorboard_dir='log')
model.load(MODEL_NAME)

parser = reqparse.RequestParser()

@app.route('/', methods=['GET', 'POST'])
def handle_request():
        imageFile = flask.request.files['image']
        fileName = werkzeug.utils.secure_filename(imageFile.filename)
        print("\nReceived image File name : " + imageFile.filename)
        imageFile.save(fileName)
        img = cv2.imread(fileName, cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
        data = img.reshape(1, IMG_SIZE, IMG_SIZE, 1)
        modelOut = model.predict(data)
        strLabel = ""
        if np.argmax(modelOut) == 1:
            strLabel = 'Not Melanoma'
        else:
            strLabel = 'Melanoma'
        return strLabel, 200
   

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)