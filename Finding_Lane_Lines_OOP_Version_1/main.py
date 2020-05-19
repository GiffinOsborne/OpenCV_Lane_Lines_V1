import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2 as cv
import houghLines as hough

video = cv.VideoCapture("test_videos/solidWhiteRight.mp4")
#video = cv.VideoCapture("test_videos/solidYellowLeft.mp4") 
#video = cv.VideoCapture("test_videos/challenge.mp4")

while (video.isOpened()):
# ret = a boolean return value from getting the frame, frame = the current frame being projected in the video
    ret, frames = video.read()
    
    mask = hough.drawLines(frames)
    
    cv.imshow("Region of Interest", mask)

    if cv.waitKey(15) & 0xFF == ord('q'):
        break
# The following frees up resources and closes all windows
video.release()
cv.destroyAllWindows()
