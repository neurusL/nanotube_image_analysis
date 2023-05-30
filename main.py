import cv2
from matplotlib import pyplot as plt
from utils import *

def main():

    # TODO: modify main function to get better visualized result

    images = []
    tested_dists = [101.6719893 + 28.55156/2, 
                    120.9297889 + 29.03056/2, 
                    119.9225223 + 27.19728/2] 
    
    images.append(cv2.imread('data/Sample P297 w- Characterization/wafers4 2nm_80kx_n2.tif', cv2.IMREAD_GRAYSCALE))
    images.append(cv2.imread('data/Sample P298 w- Characterization/wafers4 2_5nm_80kx_n2.tif', cv2.IMREAD_GRAYSCALE))
    images.append(cv2.imread('data/Sample P299 w- Characterization/wafers4 3nm_80kx_n2.tif', cv2.IMREAD_GRAYSCALE))

    for i in range(3):
        plt.subplot(2,3,i+1), plt.imshow(images[i])
        plt.title(tested_dists[i], fontsize = 4)
        plt.xticks([]),plt.yticks([])

    for i in range(3):
        ave, proc_img = get_ave_distance(images[i])

        plt.subplot(2,3,i+4), plt.imshow(proc_img)
        plt.title(ave, fontsize = 4)
        plt.xticks([]),plt.yticks([])
    
    # plt.show()
    plt.savefig("results/output.pdf", bbox_inches='tight', dpi=600)

if __name__ == "__main__":
    main()