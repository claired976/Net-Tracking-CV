# ball_tracking_feed2.py
# Adapted from code by Adrian Rosebrock, https://www.pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/ 
# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time

# file to write center positions to
file = open("feed2.txt", "w")

# parse arguments
ap = argparse.ArgumentParser()

# if using prerecorded video
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")

# set buffer (size of [osition trail])
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())

# set range for colors
greenLower = (60, 39, 210)
greenUpper = (130, 255, 255)

# deque to store previous object locations
pts = deque(maxlen=args["buffer"])

# use webcam or USB connected camera if no prerecorded video
if not args.get("video", False):
    # src determines USB port
	vs = VideoStream(src=1).start() 

# using prerecorded video
else:
	vs = cv2.VideoCapture(args["video"])

# allow the camera or video file to warm up
time.sleep(2.0)

firstLoop = True # check if this is the first loop
prevCenter = [0, 0] # value for previous center location

while True:
	frame = vs.read() # read current frame

	# if this is from a camera, it's a tuple of [grabbed boolean, frame]
	frame = frame[1] if args.get("video", False) else frame

	# if this is the end of the video
	if frame is None:
		break

	# resize the frame, blur it, and convert to the HSV
	frame = imutils.resize(frame, width=600)
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

	# construct mask based on color range
	# erosions, dilations help remove small blobs
	mask = cv2.inRange(hsv, greenLower, greenUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)

	# initialize ball center
	center = None # x, y center

	# find contours in the masked image
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)

	# only if at least one contour found
	if len(cnts) > 0:

		# find largest contour, the circle enclosing it, and its centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / (M["m00"] + 0.0000001)), int(M["m01"] / (M["m00"] + 0.0000001))) # this is the center
		prevCenter = center # update the previous center

		# if this is the first loop don't include newline in the position string
		if(firstLoop):
			centerStr = str(prevCenter[0])+','+'0,'+str(prevCenter[1])
			firstLoop = False
		else:
			centerStr = '\n' + str(prevCenter[0])+','+'0,'+str(prevCenter[1])
		
		# write string for position of center of object to text file
		file.write(centerStr)
		file.flush()

	# update the points deque
	pts.appendleft(center) 
	
    # loop over points to display in object's trail 
	for i in range(1, len(pts)):
		# ignore if this or previous point are None
		if pts[i - 1] is None or pts[i] is None:
			continue

		# calculate line thickness and display trail of object
		thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
		cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

	# show this frame
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break

# if we are not using a video file, stop the camera video stream
if not args.get("video", False):
	vs.stop()

# otherwise, release the camera
else:
	vs.release()

# wait, then close all windows
cv2.waitKey(3000)
cv2.destroyAllWindows()