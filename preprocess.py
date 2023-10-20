import cv2
import numpy as np
from skimage.morphology import skeletonize, medial_axis, thin


""" Tools for preprocessing images
"""

def remove_background(image):
    """
    Args:
        image (image): grayscale image

    Returns:
        image with backgroud set to black
    """
    
    # TODO: experiment for param of GaussianBlur and OSTU threshold for better
    #       removing background
    mask = cv2.GaussianBlur(image, (15,15), 0)
    _,mask = cv2.threshold(mask,0,255,cv2.THRESH_OTSU)

    image = cv2.bitwise_and(image, image, mask=mask)

    return image


def thinning(image, max_num_iter=None):
    """
    Args:
        image (image): grayscale image
        max_num_iter (int, optional): max number of iteration for thinning algo-
        rithm, i.e. algorithm will stop thinning after max_num_iter iterations. 
        Defaults to None, then thinning is equivalent to skeletonize.

    Returns:
        (image): grayscale image of thinned image or skeleton of image
    """
    # use skeletonize to thinning patterns
    if max_num_iter == None:
        image = skeletonize(image, method='lee') # notice return type is bool array
    else:
        image = thin(image, max_num_iter=max_num_iter)

    image = np.where(image, 255, 0)
    image = image.astype(np.uint8)

    return image

def get_medial_axis(image):
    """
    Args:
        image (image): grayscale image
    Returns:
        (image): grayscale image of medial_axis(image)
    """    

    image, _ = medial_axis(image, return_distance=True)

    image = np.where(image, 255, 0)
    image = image.astype(np.uint8)  # notice gra

    return image


# TODO: 
#   do we need Canny Algorithm (the following) for edge detector
#   experiment for params if needed
def detect_edges(image):

    image = cv2.Canny(image, 100, 200) 

    return image


 
"""Preprocessing functions
"""

def preprocess(image):
    # equalizeHist
    image = cv2.equalizeHist(image)
    # cv2.imwrite("results/00img_equalizeHist.jpg", image)


    # Remove background 
    image = remove_background(image)
    # cv2.imwrite("results/01background_removed.jpg", image)
 
    # Gaussian Blur   
    image = cv2.GaussianBlur(image, (5,5), 0)
    # cv2.imwrite("results/03gaussian_blur.jpg", image)

    # Binarization 
    # Ostu's thresholding after Gaussian filtering  
    _,image = cv2.threshold(image,0,255,cv2.THRESH_OTSU)

    return image

def preprocess1(image):
    """_summary_
       this method first gets color blocks of foreground nanotubes in image,
       then using thinning algorithm reduce blocks into skeletons of foreground
       nanotubes, which can be easily used for estimate center-to-center average
       inter tube distance. 
    
    """
    image = preprocess(image)

    # Thinning for getting skeleton of nanotubes
    image = thinning(image, 35)
    # cv2.imwrite("results/05thinning.jpg", image)

    return image



def preprocess2(image):
    """_summary_
    This method first gets rough edge of foreground nanotubes in image, followed
    by morphology to get rid of noise, finally uses thinning algorithm to reduce
    all edges to one-pixel width

    This preprocessing is adapted by Qiu Di's idea.
    """

    # equalizeHist
    image = cv2.equalizeHist(image)

    # Remove background 
    image = remove_background(image)

    # Gaussian Blur
    image = cv2.GaussianBlur(image, (5,5), 0)

    # Binarization 
    # Adaptive_mean thresholding after Gaussian filtering  
    image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, 
                                       cv2.THRESH_BINARY, 21, 10)

    # Morphology for reducing noice
    kernel_open = np.ones((5,5),np.uint8)
    image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel_open)

    kernel_close = np.ones((5,5),np.uint8)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel_close)

    image = cv2.bitwise_not(image)

    # Thinning for getting one-pixel-width edges of nanotubes
    image = thinning(image)

    return image
