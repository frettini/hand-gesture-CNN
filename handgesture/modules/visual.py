import cv2 as cv2
import numpy as np
import imutils
import os

from keras.models import Sequential
from keras.models import load_model



def run_avg(image, aWeight):
    global bg
    # initialize the background
    if bg is None:
        bg = image.copy().astype("float")
        return

    # compute weighted average, accumulate it and update the background
    cv2.accumulateWeighted(image, bg, aWeight)


def segment(image, threshold=25):
    global bg
    # find the absolute difference between background and current frame
    diff = cv2.absdiff(bg.astype("uint8"), image)

    # threshold and get contours the diff image so that we get the foregrounds
    thresholded = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)[1]
    (cnts, _) = cv2.findContours(thresholded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # return None, if no contours detected
    if len(cnts) == 0:
        return
    else:
        # based on contour area, get the maximum contour which is the hand
        segmented = max(cnts, key=cv2.contourArea)
        return (thresholded, segmented)


# global variables
bg = None
aWeight = 0.5

# region of interest (ROI) coordinates
top, right, bottom, left = 10, 350, 225, 590
num_frames = 0

#loading model
modelhg = load_model("D:\\work\\EPSRC\\ParasiteApp\\handgesture\\data\\handgesture_model.h5")
x = []

cv2.VideoCapture().release()
capture = cv2.VideoCapture(0 + cv2.CAP_DSHOW)



lookup = dict()
reverselookup = dict()
count = 0
for j in os.listdir("D:\\work\\EPSRC\\ParasiteApp\\handgesture\\leapGestRecog\\00\\"):
    if not j.startswith('.'): # If running this code locally, this is to 
                              # ensure you aren't reading in hidden folders
        lookup[j] = count
        reverselookup[count] = j
        count = count + 1
print(reverselookup)



if not capture.isOpened:
    print('Unable to open: ')
    exit(0)

while True:
    
    ret, frame = capture.read()
    

    if frame is None:
        print("couldn't read frame")
        break
    # get the current frame

    # reshape the frame
    frame = imutils.resize(frame, width=700)
    frame = cv2.flip(frame, 1)
    clone = frame.copy()
    (height, width) = frame.shape[:2]

    # get the ROI
    roi = frame[top:bottom, right:left]

    # convert the roi to grayscale and blur it
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)

    # to get the background, keep looking till a threshold is reached
    # so that our running average model gets calibrated
    if num_frames < 30:
        run_avg(gray, aWeight)
    else:
        # segment the hand region
        hand = segment(gray)

        # check whether hand region is segmented
        if hand is not None:
            # if yes, unpack the thresholded image and
            # segmented region
            (thresholded, segmented) = hand

            # draw the segmented region and display the frame
            cv2.drawContours(clone, [segmented + (right, top)], -1, (0, 0, 255))
            cv2.dilate(thresholded, (7,7), iterations=2)
            result = cv2.bitwise_and(gray, gray, mask=thresholded)
            

            result = cv2.resize(thresholded, (320, 120))
            cv2.imshow("Result", result)
            result = np.reshape(result, [1, 120, 320, 1])
            

            predicted_label = modelhg.predict(result)
            i = np.flatnonzero(predijupycted_label[0] == 1)
            j = np.array(i).tolist()

            if i.size :  

                print(j[0])
                
                cv2.putText(clone, reverselookup[j[0]], (150, 150), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255))

    # draw the segmented hand
    cv2.rectangle(clone, (left, top), (right, bottom), (0,255,0), 2)

    # increment the number of frames
    num_frames += 1

    # display the frame with segmented hand
    cv2.imshow("Video Feed", clone)
    
    
    
    keyboard = cv2.waitKey(30)
    if keyboard == 'q' or keyboard == 27:
        break
    
cv2.VideoCapture().release()