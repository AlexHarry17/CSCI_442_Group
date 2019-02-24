import cv2 as cv
import numpy as np


def get_image_range(image, lower, upper):
    new_image = cv.inRange(image, lower, upper)  # Shows colors in the color range set above
    new_image = cv.GaussianBlur(new_image, (5, 5), 0)  # Blurs the image in case of color range discrepancies.
    return new_image


def get_keypoints(image):
    kernel = np.ones((10, 10), np.uint8)
    image = cv.erode(image, kernel, 1)
    # image = cv.dilate(image, kernel, 1)
    params = cv.SimpleBlobDetector_Params()
    params.filterByArea = True
    params.minArea = 500
    params.filterByCircularity = True
    blob_detection = cv.SimpleBlobDetector_create(params)  # Creates the blob detector
    return blob_detection.detect(
        cv.bitwise_not(image))  # Blob detection doesn't work with a black background.  bitwise_not fixes this.


original_image = cv.imread("imagesWOvideo/one.jpg")
# initial code helped from source: https://thecodacus.com/opencv-object-tracking-colour-detection-python/
image = cv.GaussianBlur(original_image, (7, 7), 0)  # Blurs the image
image = cv.cvtColor(image, cv.COLOR_BGR2HSV)  # Converts the image to HSV

# Bound values for colors
green_lower = np.array([65, 85, 34])
green_upper = np.array([84, 260, 245])
blue_lower = np.array([84, 80, 40])
blue_upper = np.array([166, 255, 255])
yellow_lower = np.array([28, 0, 0])
yellow_upper = np.array([33, 255, 255])
orange_lower = np.array([10, 100, 20])
orange_upper = np.array([25, 255, 255])
brown_lower = np.array([10, 0, 0])
brown_upper = np.array([20, 255, 255])

green_image = get_image_range(image, green_lower, green_upper)
blue_image = get_image_range(image, blue_lower, blue_upper)
yellow_image = get_image_range(image, yellow_lower, yellow_upper)
orange_image = get_image_range(image, orange_lower, orange_upper)
brown_image = get_image_range(image, brown_lower, brown_upper)

num_blue = get_keypoints(blue_image)
num_green = get_keypoints(green_image)
num_yellow = get_keypoints(yellow_image)
num_orange = get_keypoints(orange_image)
num_brown = get_keypoints(brown_image)

print(len(num_blue))
cv.putText(original_image, "Blue: " + str(len(num_blue)), (10, 50), cv.FONT_HERSHEY_PLAIN, 2, [255, 255, 255])
cv.putText(original_image, "Green: " + str(len(num_green)), (200, 50), cv.FONT_HERSHEY_PLAIN, 2, [255, 255, 255])
cv.putText(original_image, "Yellow: " + str(len(num_yellow)), (10, 100), cv.FONT_HERSHEY_PLAIN, 2, [255, 255, 255])

cv.imshow("Candy Image original", original_image)

cv.imshow("Candy Image", orange_image)

cv.waitKey(0)
