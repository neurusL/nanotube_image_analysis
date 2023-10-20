import cv2
import numpy as np
from preprocess import *

def draw_circle(image, row, col, radius):
    image_new = cv2.circle(image, (row,col), radius, (255,255,255), 2)
    return image_new

def check_circlefit(image, row, col, radius):
    y = image.shape[0]
    x = image.shape[1]
    # pay attention to the direction of x,y-axis
    # +-------> x
    # |
    # | IMAGE
    # |
    # \/ y
    y1 = row-radius
    y2 = row+radius
    x1 = col-radius
    x2 = col+radius
    
    if (y1 < 0 or y2 > y or x1 < 0 or x2 > x):
        return 0   

    diameter = radius * 2
    mask = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(diameter, diameter))      
    maskResult = image[y1:y2, x1:x2] & mask

    while (y1 > 0 and y2 < y and x1 > 0 and x2 < x and np.all(maskResult == 0)):
        radius += 1
        diameter = radius * 2
        mask = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(diameter, diameter))
        y1 = row-radius
        y2 = row+radius
        x1 = col-radius
        x2 = col+radius
        maskResult = image[y1:y2, x1:x2] & mask
    
    return radius-1

def find_largest_circle(image):

    # take in preprocessed image
    y = image.shape[0]
    x = image.shape[1]

    max_radius = 1
    (max_row, max_col) = (0,0)

    for row in range (1,y-1):
        for col in range(1,x-1):
              r = check_circlefit(image, row, col, max_radius)
              if r != 0 and r > max_radius:
                   max_radius = r
                   (max_row, max_col) = (row, col)
                #    print(r,"coord:", row, col)
    
    
    return (max_row, max_col, max_radius)

# if __name__ == "__main__":
#     img = cv2.imread('results/04otsu_thresh.jpg', cv2.IMREAD_GRAYSCALE)

#     img = img.astype(np.uint8)
    
#     (max_row, max_col, max_radius) = find_largest_circle(img)

#     print(max_row, max_col, max_radius)
#     print(check_circlefit(img, max_row, max_col, max_radius-1))
#     img = draw_circle(img, max_col, max_row, max_radius)
#     cv2.imwrite("results/06largest_circle.jpg", img)