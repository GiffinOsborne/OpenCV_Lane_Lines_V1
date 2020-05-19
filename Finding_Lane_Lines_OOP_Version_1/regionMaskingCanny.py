import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2 as cv

img = mpimg.imread("test_images/solidWhiteRight.jpg")
#img = mpimg.imread("test_images/solidYellowLeft.jpg")
#img = mpimg.imread("test_images/whiteCarLaneSwitch.jpg")
grey = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

kernel_size = 5
blur_grey = cv.GaussianBlur(grey,(kernel_size, kernel_size), 0)

low_threshold = 40
high_threshold = 120

edges = cv.Canny(blur_grey, low_threshold, high_threshold)

mask = np.zeros_like(edges)
ignore_mask_color = 255

imshape = img.shape


vertices = np.array([[(0, imshape[0]),(450, 290), (490, 290), (imshape[1],imshape[0])]], dtype=np.int32)
cv.fillPoly(mask, vertices, ignore_mask_color)
masked_edges = cv.bitwise_and(edges, mask)

rho = 1
theta = np.pi/180
threshold = 1
min_line_length = 10
max_line_gap = 1
line_image = np.copy(img)*0

lines = cv.HoughLinesP(masked_edges, rho, theta, threshold, np.array([]), min_line_length, max_line_gap)

for line in lines:
    for x1,y1,x2,y2 in line:
         cv.line(line_image,(x1,y1),(x2,y2),(255,0,0),10)

color_edges = np.dstack((edges, edges, edges))

combo = cv.addWeighted(img, 0.8, line_image, 1, 0)
plt.imshow(combo)
plt.show()
