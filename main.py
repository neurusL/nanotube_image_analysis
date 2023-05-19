import cv2
from matplotlib import pyplot as plt
from utils import *

def main():
    images = []
    tested_dists = [101.6719893, 120.9297889, 119.9225223]
    images.append(cv2.imread('data/Sample P297 w- Characterization/wafers4 2nm_80kx_n2.tif', cv2.IMREAD_GRAYSCALE))
    images.append(cv2.imread('data/Sample P298 w- Characterization/wafers4 2_5nm_80kx_n2.tif', cv2.IMREAD_GRAYSCALE))
    images.append(cv2.imread('data/Sample P299 w- Characterization/wafers4 3nm_80kx_n2.tif', cv2.IMREAD_GRAYSCALE))
    # image = cv2.imread('data/CNT Sample 5.tif', cv2.IMREAD_GRAYSCALE)
    # for i in range(0,3):
    #     plt.subplot(3,2,i+1), plt.imshow(images[i])
    #     plt.title(tested_dists[i], fontsize = 4)
    #     plt.xticks([]),plt.yticks([])

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
    plt.savefig("tests/output.pdf", bbox_inches='tight', dpi=600)

    # for image in [i]:
    # tested
    # 297: 101.6719893		
    # 298: 120.9297889		
    # 299: 119.9225223	

    # (blur, threshold) = (25, 105)
    # 297: 127.61927524638833
    # 298: 110.71299261746259    
    # 299: 152.36017772646608 	

    # (blur, threshold) = (35, 105)
    # 297: 149.01932829873778 	
    # 298: 126.9038352772457    
    # 299: 180.16339028170458 

    # (blur, threshold) = (45, 105)
    # 297: 173.51124021628078
    # 298: 143.98052258516495  
    # 299: 208.9879682311323

    # (blur, threshold) = ((21,63), OSTU)
    # 297: 129.72941787097747
    # 298: 131.6015646984223   
    # 299: 165.8498304454962

    # (blur, threshold) = ((15,45), OSTU)
    # 297: 123.25520135089062
    # 298: 126.89567442130596  
    # 299: 162.39318399296235

    # 1:  105.63828037043903
    # 2:  68.45049350929334
    # 3:  71.52129888154816
    # 4:  76.89617901080902
    # 5:  184.87847820995134


if __name__ == "__main__":
    main()