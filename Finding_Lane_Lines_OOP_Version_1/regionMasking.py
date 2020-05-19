import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np

img = mpimg.imread("test_images/solidWhiteRight.jpg")

ysize = img.shape[0]
xsize = img.shape[1]

color_select = np.copy(img)
line_image = np.copy(img)

red_threshold = 200
green_threshold = 155
blue_threshold = 150

rgb_threshold = [red_threshold, green_threshold, blue_threshold]

left_bottom = [135, 539]
right_bottom = [875,539]
apex = [489, 300]

fit_left = np.polyfit((left_bottom[0], apex[0]),(left_bottom[1],apex[1]), 1)
fit_right = np.polyfit((right_bottom[0], apex[0]),(right_bottom[1],apex[1]), 1)
fit_bottom = np.polyfit((left_bottom[0], right_bottom[0]),(left_bottom[1],right_bottom[1]), 1)

color_thresholds = (img[:,:,0] < rgb_threshold[0]) \
    | (img[:,:,1] < rgb_threshold[1]) \
    | (img[:,:,2] < rgb_threshold[2])

XX, YY = np.meshgrid(np.arange(0, xsize), np.arange(0, ysize))
region_thresholds = (YY > (XX*fit_left[0] + fit_left[1])) & \
    (YY > (XX*fit_right[0] + fit_right[1])) & \
    (YY < (XX*fit_bottom[0] + fit_bottom[1]))

color_select[color_thresholds] = [0,0,0]
line_image[~color_thresholds & region_thresholds] = [255,0, 0]

plt.imshow(color_select)
plt.imshow(line_image)
plt.show()