# ball_tracking_multiple.py can track both a red and green LED seperately
# Adapted from code by Adrian Rosebrock, https://www.pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/ 
# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time

# construct the argument parse and parse the arguments
# either use a given video, or webcam
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")

# buffer: size of the tail
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())

# HSV ranges for the two LEDs
# for red LED
rLower = (165, 50, 210)
rUpper = (255, 180, 255)

# for green LED
gLower = (60, 39, 210)
gUpper = (130, 255, 255)

pts = deque(maxlen=args["buffer"]) # deque of points, red LED
pts2 = deque(maxlen=args["buffer"]) # deque of points, green LED

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
	vs = VideoStream(src=0).start() # different src numbers = different streams

# otherwise, grab a reference to the video file
else:
	vs = cv2.VideoCapture(args["video"])
# allow the camera or video file to warm up
time.sleep(2.0)

firstLoop = True # check if this is the first loop
prevCenter = [0, 0] # previous center values
croppedFrame = [0, 0, 0, 0] #y1, y2, x1, x2

# keep looping
while True:
	# grab the current frame
	frame = vs.read()
	# handle the frame from VideoCapture or VideoStream
	frame = frame[1] if args.get("video", False) else frame
	#^ if it's video capture, it's a tuple [grabbed boolean, frame]

	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
	if frame is None:
		break # end of recorded video

	# resize the frame, blur it, and convert it to the HSV
	# color space
	frame = imutils.resize(frame, width=600)
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

	# mask for the two colors, and remove extra blobs
	mask = cv2.inRange(hsv, rLower, rUpper) # mask for red
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)

	mask2 = cv2.inRange(hsv, gLower, gUpper) # mask for green
	mask2 = cv2.erode(mask2, None, iterations=2)
	mask2 = cv2.dilate(mask2, None, iterations=2)

	# initialize ball centers
	center = None # x, y center, red
	center2 = None # x, y center, green

    # find contours for both
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)

	cnts2 = cv2.findContours(mask2.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts2 = imutils.grab_contours(cnts2)

	# only proceed if at least one contour was found, red LED
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / (M["m00"] + 0.0000001)), int(M["m01"] / (M["m00"] + 0.0000001))) # this is the center
		prevCenter = center

		if(firstLoop):
			centerStr = str(prevCenter[0])+','+str(prevCenter[1])
			print(centerStr)
			firstLoop = False
		else:
			centerStr = '\n'+str(prevCenter[0])+','+str(prevCenter[1])
	# update the points queue
	pts.appendleft(center) 


	# only proceed if at least one contour was found, green LED
	if len(cnts2) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts2, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center2 = (int(M["m10"] / (M["m00"] + 0.0000001)), int(M["m01"] / (M["m00"] + 0.0000001))) # this is the center
		prevCenter2 = center2

		if(firstLoop):
			centerStr2 = str(prevCenter2[0])+','+str(prevCenter2[1])
			print(centerStr2)
			firstLoop2 = False
		else:
			centerStr2 = '\n'+str(prevCenter2[0])+','+str(prevCenter2[1])

	# update the points queue
	pts2.appendleft(center2) 

    # loop over the set of tracked points, red LED
	for i in range(1, len(pts)):
		# if either of the tracked points are None, ignore
		# them
		if pts[i - 1] is None or pts[i] is None:
			continue
		# otherwise, compute the thickness of the line and
		# draw the connecting lines
		thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
		cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness) # draw line in red

	# loop over the set of tracked points, green LED
	for i in range(1, len(pts2)):
		# if either of the tracked points are None, ignore
		# them
		if pts2[i - 1] is None or pts2[i] is None:
			continue
		# otherwise, compute the thickness of the line and
		# draw the connecting lines
		thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
		cv2.line(frame, pts2[i - 1], pts2[i], (255, 0, 0), thickness) # draw line in blue


	# show the frame to our screen
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

cv2.waitKey(3000)
# close all windows
cv2.destroyAllWindows()