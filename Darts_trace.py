######################
# Matts Van Der Poel #
######################

import cv2
import numpy as np

# finds the point of the contour with the highest and lowest x coordinate
# cc     : contour of the object
# return : point with lowest x, point with highest x 
def find_extremes(cc):
    cc = cv2.convexHull(cc)
    mn, mx = 9999, 0
    cmn, cmx = 9999,9999
    for p in cc:
        x,y = p[0]
        if x < mn:
            mn = x
            cmn = (x,y)
        if x > mx:
            mx = x
            cmx = (x,y)
    return cmn, cmx

# Determines if a new location is valid
# It looks at the last 3 points and checks if the new
# point is further than 2 of them to eliminate false detections.
# cm     : location on x axis of new point
# points : list of points
# return : True if valid
def is_good(cm, points):
    if len(points) > 3:
        good = 0
        for i in range(1, 3):
            if cm < points[-i][0][0]: 
                good += 1
        if good > 1:  
            return True
        return False
    else:
        return True

# Finds the contour that matches the given contour best
# The used parameters are: area, perimeter, location.
# Because a dart continues flying to the same direction 
# contours behind the previous point are skipped
# fgMask : the foreground mask of the image
# cm     : the shape the contour has to match
# points : the previous found points
# return : best shape, the difference score 
def best_contour(fgMask, cm, points):
    contours, hierarchy = cv2.findContours(fgMask.astype(np.uint8), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    area = cv2.contourArea(cm)
    per = cv2.arcLength(cm,True)
    mn = 9999999
    cm2 = None
    for c in contours:
        cc = c
        sz = cv2.contourArea(cc)
        per2 = cv2.arcLength(cc,True)
        off = abs(area-sz)/area + abs(per-per2)/per
        cmn, cmx = find_extremes(c)
        if off < mn:
            if is_good(cmn[0], points):
                mn = off
                cm2 = c
    return cm2, mn

# Connects areas with closing
# mask   : input mask that has to be cleaned
# return : processed mask
def clean_mask(mask):
    ker = np.ones((5,5),np.uint8)
    maskf = cv2.dilate(mask, ker, iterations=1)
    maskf = cv2.erode(maskf, ker, iterations=1)
    return maskf

# draws a line connecting the points of the lowest and highest x coordinates
# with their respective previous locations
# img    : image to draw lines on
# pos    : list of points to draw between in format [[[x1,y1], [x2,y2]], ...]
#          x1,y1 is the point with the lowest x and x2,y2 with the highest 
# return : image with the lines drawn
def draw_pos(img, pos):
    for i in range(len(pos)-1):
        img = cv2.line(img, pos[i][0], pos[i+1][0], (255,0,0), 2)
        img = cv2.line(img, pos[i][1], pos[i+1][1], (0,255,0), 2)
    return img

# processes the video and draws the path of the tail and point of the dart
# file  : filename of input video has to be in mp4 format
# out   : filename of input video has to be in mp4 format
# shape : filename of the shape vector
# th    : threshold that determines how precise the shape has to be 
def process(file, out="out.mp4", shape="shape", th=1.2):
    cm = np.load(shape+".npy", allow_pickle=False)
    # Open video
    vid = cv2.VideoCapture(file)
    if (vid.isOpened()== False):
        print("Error opening video file")

    backSub = cv2.createBackgroundSubtractorKNN(detectShadows=True)
    ret, im = vid.read()
    # open video writer
    h, w, d = im.shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(out, fourcc, 30, (w, h))
    frames = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))\
    # process frames
    cnt = 0
    points = []
    while ret:
        cnt += 1
        print(f"Processing frame: {cnt}/{frames}", end="\r")
        frame = im
        fgMask = backSub.apply(frame)
        fgMask = clean_mask(fgMask)
        cc, mn = best_contour(fgMask, cm, points)
        if mn < th:
            cv2.drawContours(frame, [cc], -1, (0, 0, 255), 1)
            cmn, cmx = find_extremes(cc)
            points.append([cmn, cmx])
        frame = draw_pos(frame, points) 
        writer.write(frame)
        ret, im = vid.read()

    # Close video
    vid.release()
    writer.release()
    print("\nProcessing complete")
    title = "Flight path"
    cv2.namedWindow(title)
    # show result
    cv2.imshow(title, frame)
    key = cv2.waitKey(0) & 0xFF

# Asks the user for the input and output filename
# return : input, output filename
def ask_input():
    print("Give the filename with extention of the input video")
    file = input(">>")
    if file == "":
        file = "examples/wobble.mp4"
    print("Give the filename of the output video")
    print("Leave empty for 'out.mp4'")
    out = input(">>")
    if out == "":
        out = "out.mp4"
    return file, out

def main():
    file, out = ask_input()
    print(f"{file} -> {out}")
    process(file, out)

if __name__ == "__main__":
    main()

    