import cv2
import numpy as np
from preprocess import *

def get_scale(image, N):
    """
    Args:
        image: image to find scale_bar
        N (int): scale_bar corresponds to real distance in nanometer

    Returns:
        N / scale_pixels: nanometer one pixel corresponds to 
        scale_pixels:     pixels N nanometer corresponds to 
        first_non_image_row: first row of image comments
        left_idx: left x coordinate of scale bar
        right_idx: right x coordinate of scale bar
    """
    original_image = image

    # We exploit sample image 
    first_non_image_row = image.shape[1]

    # After getting first_all_white_row, we extract scale from original_image
    left_idx, right_idx = 0, 0
    first_all_white = original_image[first_non_image_row]
    # print(first_all_white)


    for col in range(image.shape[1]-1):
        if (left_idx == 0
            and (first_all_white[col] == 255)
            and (first_all_white[col+1] != 255)):
            left_idx = col

        if (left_idx != 0
            and (first_all_white[col] != 255)
            and (first_all_white[col+1] == 255)):
            right_idx = col

    # print(left_idx)
    # print(right_idx)
    
    scale_pixels = right_idx - left_idx

    return N / scale_pixels, scale_pixels, first_non_image_row, left_idx, right_idx


# naive method getting average inter-nanotube distance
# TODO: adapt following functions for our latest version of preprocessing (edge_detecting)

def get_row_ave(image_line):
    """
    Args:
        image_line: row of an image (1d array of pixels)

    Returns:
        row_ave: average end-to-end inter-tube distance of a row of image
        intersection_list: a list of tube edges x-axis value in a row of image
    Notes:
        end-to-end distance of the image (where |T| denotes the tube)
            |T|                               |T|
            |T|<-----end-to-end distance----->|T|
            |T|                               |T|
             |<---center-to-center distance--->|

        intersection_list:
            |T|        |T|   |T|        |T|   |T|  (an image line)
            x x        x x   x x        x x   x x
            is list of x-coordinates of x's
        
        Notice the list can be easily used to modify the following function 
        for calculating center-to-center inter-tube distance.
    """
    total_distance = 0
    distance_cnt = 0
    left_idx = 0
    intersection_list = []
    for i in range(len(image_line)-1):
        if image_line[i] == 255 and image_line[i+1] != 255:
            left_idx = i
            intersection_list.append(i)
        if (left_idx != 0 and
            image_line[i] != 255 and image_line[i+1] == 255):
            distance_cnt += 1
            total_distance += (i - left_idx)
            intersection_list.append(i)
    
    row_ave = 0 if distance_cnt == 0 else total_distance / distance_cnt
    
    return row_ave, intersection_list

def get_ave(image, test_range):
    """
    Args:
        image : image to be processed 
        test_range as (x1, x2), (y1, y2) : ((int, int), (int, int)): 
            [x1, y1) x [x2, y2) is rectangle of range where we do get_row_ave of 
            all sliced rows[x1,x2) in [y1,y2).
    Returns:
        average end-to-end inter-tube distance in test_range of the image
    """
    ((x1, x2), (y1, y2)) = test_range

    sum_ave = 0
    total_intersect = []
    for i in range(y1, y2):
        image_line = image[i][x1:x2]
        line_ave, line_intersect = get_row_ave(image_line)
        sum_ave += line_ave
        total_intersect.append(line_intersect)
    
    return sum_ave / (y2-y1), total_intersect
        

def get_ave_distance(image, show_contour = False):
    """
    Args:
        image: image to be processed 
        save_path (string): path to save processed image
        show_contour (bool, optional): 
            if set to True, contour of tubes will be
            highlighted in saved image, used for testing if we indeed find tubes
            when calculating average distance. Defaults to True.

    Returns:
        average end-to-end inter-tube distance of the image
        image processed
    Note:
        end-to-end distance of the image (where |T| denotes the tube)
            |T|                               |T|
            |T|<-----end-to-end distance----->|T|
            |T|                               |T|
             |<---center-to-center distance--->|
    """
    
    # Get Scale bar
    pixel_scale, scale, y, x1, x2 = get_scale(image, 500)
    # visualize indeed get scale bar (for debug)
    # image = cv2.circle(image, center=(x1, y), radius=5, color=(255,0,0), thickness=-1)
    # image = cv2.circle(image, center=(x2, y), radius=5, color=(255,0,0), thickness=-1)

    # Crop out the area for 
    image_width = image.shape[1]
    origin_image = image[:(image_width+1)]

    # Preprocess the image
    image = preprocess1(origin_image)

    # Calculate inter tube average distance
    test_range = ((0, image_width), (0, y))
    average, all_intersects = get_ave(image, test_range)
    average_nm = average * pixel_scale

    
    if show_contour:
        image = cv2.cvtColor(image,cv2.COLOR_GRAY2RGB)

        for (i, x_list) in enumerate(all_intersects):
            for x in x_list:
                cv2.circle(image, center=(x, i), radius=2, color=(0,0,255), thickness=-1)

    return round(average_nm, 7), image


