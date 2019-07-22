#deprecated module, the new sort image code is in the jupyter notebook

import os
import tensorflow as tf

import numpy as np
import matplotlib.pyplot as plt
import cv2

from sklearn.model_selection import train_test_split

print(tf.version)



def find_imagepath(currentpath):
    imagepaths = []
    # count = 0
    for root, dirs, files in os.walk(currentpath, topdown=False): 
        for name in files:
            path = os.path.join(root, name)
            if path.endswith("png"):
                imagepaths.append(path)
            # count += 1
            # if count == 10:
            #     return imagepaths
    return imagepaths


def plot_image(path):
    #loading image to X
    img = cv2.imread(path)
    img_cvt = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print(img_cvt.shape) # Prints the shape of the image just to check
    plt.grid(False) # Without grid so we can see better
    plt.imshow(img_cvt) # Shows the image
    plt.xlabel("Width")
    plt.ylabel("Height")
    plt.title("Image " + path)



def sortarrays(currentpath, imagepaths):
    X = []
    y = []

    # Loops through imagepaths to load images and labels into arrays
    for path in imagepaths:
        img = cv2.imread(path) # Reads image and returns np.array
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Converts into the corret colorspace (GRAY)
        img = cv2.resize(img, (320, 120)) # Reduce image size so training can be faster
        X.append(img)
      
        # Processing label in image path
        category = path.split("\\")[-2]
        
        label = int(category.split("_")[0][1]) # We need to convert 10_down to 00_down, or else it crashes
        y.append(label)
        print(label)

    print("ArrayPath Finished")

    # Turn X and y into np.array to speed up train_test_split
    X = np.array(X, dtype="uint8")
    X = X.reshape(len(imagepaths), 120, 320, 1) # Needed to reshape so CNN knows it's different images
    y = np.array(y)

    print("Images loaded: ", len(X))
    print("Labels loaded: ", len(y))

    print(y[0], imagepaths[0]) # Debugging

    ts = 0.2 # Percentage of images that we want to use for testing. The rest is used for training.
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=ts, random_state=42)


    
    np.save(currentpath + "\\data\\X_train.npy", X_train)
    np.save(currentpath + "\\data\\X_test.npy", X_test)
    np.save(currentpath + "\\data\\y_train.npy", y_train)
    np.save(currentpath + "\\data\\y_test.npy", y_test)



