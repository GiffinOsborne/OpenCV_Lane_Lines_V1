import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2 as cv
import math

line_collection = []


#take the original frame and convert it to greyscale
def apply_greyscale(image):
    return cv.cvtColor(image, cv.COLOR_RGB2GRAY)

#apply a Gaussian Blur to the greyed image
def add_blur(grey):
    kernel_size = 5
    return cv.GaussianBlur(grey,(kernel_size, kernel_size), 0)

#Implemented the canny algorithim on the Blurred photo
def apply_canny(grey):
    blur_grey = add_blur(grey)

    #declare the low and high thresholds. The Canny algorithim will identify edges where the gradient is near the midpoint of those
    # two values
    low_threshold = 60
    high_threshold = 100
    return cv.Canny(blur_grey, low_threshold, high_threshold)

#add a mask to try to eliminate the amount of edges that are displayed in the final photo
def add_mask(image, edges):
    mask = np.zeros_like(edges)
    ignore_mask_color = 255

    imshape = image.shape


    vertices = np.array([[(0, imshape[0]),(450, 290), (490, 290), (imshape[1],imshape[0])]], dtype=np.int32)
    cv.fillPoly(mask, vertices, ignore_mask_color)
    return cv.bitwise_and(edges, mask)

#check if a point is within the valid area (within the region of interest)
def valid_point(x, y, left, right, top, bottom):
    if(x >= left and x <= right):
        if(y >= bottom and y <= top):
            return True
    return False

#compare the lines on the edge of the region of interest to the lane lines (or any edges found)
def compare_lines(x1, y1, x2, y2, start, end, is_left):
    compared_slope = ((end[1] - start[1])/(end[0]- start[0]))
    drawn_slope = ((y2-y1)/(x2-x1))

    #left side
    if(is_left):
        #compare to the left side of the region of interest
        if(valid_point(x1, y1, start[0], end[0], end[1], start[1]) and valid_point(x2, y2, start[0], end[0], end[1], start[1]) ):
            #return whether the slope of the edge is less than the slope of the left edge of the region of interest
            return (compared_slope > drawn_slope)
    elif(not is_left):
            #not left side so flip the slope
            compared_slope = -compared_slope
            drawn_slope = -drawn_slope
            if(valid_point(x1, y1, end[0], start[0], start[1], end[1]) and valid_point(x2, y2, end[0], start[0], start[1], end[1])):
                return (compared_slope > drawn_slope)

    return (compared_slope > drawn_slope)

#draw the lines on the image
def drawLines(image):
    #create a greyscaled image
    grey = apply_greyscale(image)
    #apply the canny algorithim to the grey photo
    edges = apply_canny(grey)

    # add the mask to the image
    mask = add_mask(image, edges)

    #declare the parameters for the HoughLines function
    rho = 1
    theta = np.pi/180
    threshold = 1
    min_line_length = 10
    max_line_gap = 1
    line_image = np.copy(image)*0

    lines = cv.HoughLinesP(mask, rho, theta, threshold, np.array([]), min_line_length, max_line_gap)

    #define the edges of the rgion of interest
    left_bottom = (135, 539)
    right_bottom = (940,539)
    apex = (489, 300)

    for line in lines:
        for x1,y1,x2,y2 in line:
            #to the left of the apex (compute the values accordingly)
            if(x1 < apex[0] and x2 <= apex[0]):
                if(compare_lines(x1, y1, x2, y2, left_bottom, apex, True)):
                    #valid points draw the line
                    line_collection.append([x1, y1, x2, y2, (y2-y1/x2-x1), math.sqrt((x2-x1)**2 + (y2-y1)**2)])
                    cv.line(line_image,(x1,y1),(x2,y2),(255,0,0),10)
            elif(x1 > apex[0] and x2 >= apex[0]):
                if(compare_lines(x1, y1, x2, y2, right_bottom, apex, False)):
                    line_collection.append([x1, y1, x2, y2, (y2-y1/x2-x1), math.sqrt((x2-x1)**2 + (y2-y1)**2)])
                    cv.line(line_image,(x1,y1),(x2,y2),(255,0,0),10)

    color_edges = np.dstack((edges, edges, edges))

    for drawn in line_collection:
        print(drawn, "\n")

    #return the completed images
    return cv.addWeighted(image, 0.8, line_image, 1, 0)