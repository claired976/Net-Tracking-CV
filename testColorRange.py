# Use testColorRange.py to test color filtering ranges
# import the necessary packages
import numpy as np
import argparse
import cv2

image = cv2.imread("orangeled.jpg") # test image
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# test HSV color range
rangeLower = (0, 50, 210)
rangeUpper = (20, 150, 255)

mask = cv2.inRange(hsv, rangeLower, rangeUpper)

cv2.imshow("images", mask)

cv2.waitKey(0)