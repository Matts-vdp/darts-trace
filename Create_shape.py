######################
# Matts Van Der Poel #
######################

import cv2
import numpy as np
from copy import deepcopy

# displays all frames of the video with contours until q is pressed
# file   : filename of input video
# return : the selected frame, contours of the frame
def select_frame(file):
    # Open video
    vid = cv2.VideoCapture(file)
    if (vid.isOpened()== False):
        print("Error opening video file")
    backSub = cv2.createBackgroundSubtractorKNN(detectShadows=True)
    while True:
        ret, frame = vid.read()
        fgMask = backSub.apply(frame)
        contours, hierarchy = cv2.findContours(fgMask.astype(np.uint8), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        img = deepcopy(frame)
        cv2.drawContours(frame, contours, -1, (255, 0, 0), 2)
        cv2.imshow('Press q when the contour of the dart is fully seperated',frame)
        if cv2.waitKey(50) & 0xFF == ord('q'):
            break
    # Close video
    vid.release()
    cv2.destroyAllWindows()
    return img, contours

# selects the contour that is the closest to the passed point
# contours : all contours
# pt       : point in format (x,y)
# return   : closest contour
def filter_contour(contours, pt):
    m = -99999
    for c in contours:
        dst = cv2.pointPolygonTest(c, pt, True) 
        if dst > m:
            m = dst
            cm = c
    return cm

# callback function for contour selection
# when left mouse is pressed the coordinates are stored and 
# the closest contour is drawn
pt = None
def callback(event, x, y, flags, param):
    frame, contour, title = param
    global pt
    if event == cv2.EVENT_LBUTTONDOWN:
        pt = (x, y)
        cm = filter_contour(contour, pt)
        img = deepcopy(frame)
        cv2.drawContours(img, [cm], -1, (255, 0, 0), 2)
        cv2.imshow(title, img)
        print(pt)

# shows the selected frame and lets the user select a contour
# frame   : image to show
# contour : all contours 
# return  : selected point
def select_shape(frame, contour):
    title = "select the dart contour press q to save the coordinates"
    cv2.namedWindow(title)
    cv2.setMouseCallback(title, callback,[frame,contour, title])
    cv2.imshow(title, frame)
    key = cv2.waitKey(0) & 0xFF
    return pt

# Asks the user for the input filename
# return : input file name
def ask_input():
    print("Give the filename with extention of the input video")
    file = input(">>")
    if file == "":
        file = "examples/straight.mp4"
    return file

def main():
    shape = "shape"
    file = ask_input()
    frame, contour = select_frame(file)
    pt = select_shape(frame, contour)
    cm = filter_contour(contour, pt)
    np.save(shape, cm, False)
    print(f'Shape stored as : {shape}.npy')

if __name__ == "__main__":
    main()
