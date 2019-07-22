#deprecated file : look at te jupyter notebook for better code

import os
import numpy as np

from keras.models import Sequential
from keras.models import load_model

from modules import model
from modules import sortimage

currentpath = os.getcwd()
# currentpath =  os.path.dirname(os.path.realpath(__file__))

print(os.path.isfile(currentpath + "\\data\\y_train.npy"))
#D:\work\EPSRC\ParasiteApp\handgesture

if not os.path.isfile(currentpath + "\\data\\y_train.npy"):
    
    print("Status : need to sort image for processing")

    imagepaths = []

    imagepaths = sortimage.find_imagepath(currentpath)

    sortimage.sortarrays(currentpath, imagepaths)

X_train = np.load(currentpath + "\\data\\X_train.npy")
X_test  = np.load(currentpath + "\\data\\X_test.npy")
y_train = np.load(currentpath + "\\data\\y_train.npy")
y_test  = np.load(currentpath + "\\data\\y_test.npy")

if not os.path.isfile("D:\work\EPSRC\ParasiteApp\handgesture\data\handrecognition_model.h5"):

    print("Status : build and train model")

    modelHg = Sequential()
    modelHg = model.constructmodel()
    model.trainmodel(currentpath, modelHg, X_train, y_train, X_test, y_test)

modelHg = load_model(currentpath + "\\data\\handrecognition_model.h5")

test_loss, test_acc = modelHg.evaluate(X_test, y_test)

print('Test accuracy: {:2.2f}%'.format(test_acc*100))


    



