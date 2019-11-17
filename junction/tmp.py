import cv2
import numpy as np

im = cv2.imread("tmp.png")
gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
print(gray)
# Setup SimpleBlobDetector parameters.
params = cv2.SimpleBlobDetector_Params()

# Change thresholds
# params.minThreshold = 10;
# params.maxThreshold = 200;
#
# # Filter by Area.
# params.filterByArea = True
# params.minArea = 3
#
# # Filter by Circularity
# params.filterByCircularity = True
# params.minCircularity = 0.5
#
# # Filter by Convexity
# params.filterByConvexity = True
# params.minConvexity = 0.87
#
# # Filter by Inertia
params.filterByInertia = True
params.minInertiaRatio = 0.1

params.filterByColor = True
params.blobColor = 255

detector = cv2.SimpleBlobDetector_create(params)

keypoints = detector.detect(im)
print(keypoints)
im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
cv2.imshow("Keypoints", im_with_keypoints)
cv2.waitKey(0)

