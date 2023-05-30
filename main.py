import cv2
from matplotlib import pyplot as plt
from utils import *

def example_use():
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
        pixel_scale, _, _, _ = get_scale(images[i], N=500)
        images[i] = cropout_sidebar(images[i])
        ave, proc_img = get_ave_distance(images[i], pixel_scale)

        plt.subplot(2,3,i+4), plt.imshow(proc_img)
        plt.title(ave, fontsize = 4)
        plt.xticks([]),plt.yticks([])
    
    plt.show()


def main(mode, image_path, save_path='results/output.jpg'):
    if mode == 'example':
        print(f"generating examples of results...")
        example_use()

    elif mode == 'without-origin' or mode == 'over-origin':
        print(f"Loading image: {image_path}")
        ori_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        pixel_scale, _, _, _ = get_scale(ori_image, N=500)
        ori_image = cropout_sidebar(ori_image)

        print(f"Processing image: {image_path}")
        dist, image = get_ave_distance(ori_image, pixel_scale)
        if mode == 'over-origin': image = cv2.bitwise_or(image, ori_image)
        print("estimated average intertube distance of image is:\n", dist)

        _, ax = plt.subplots()
        ax.imshow(image, extent=(0,image.shape[1] * pixel_scale,0,image.shape[0]*pixel_scale))
        ax.set_xlabel("distance [nm]")
        ax.set_ylabel("distance [nm]")  

        plt.show()
        print(f"Saving image to {save_path}")
        cv2.imwrite(save_path, image)

    else:
        raise Exception("Invalid mode! Mode can only be:  \
                        example, without-origin, or over-origin")

    
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='calculate average itd of input image')

    parser.add_argument('-m','--mode', metavar='mode', required=True, 
                        help='mode can be: example, without-origin, or over-origin')
    parser.add_argument('-l','--loadpath', metavar='image load path', required=False,
                        help='path of image to be loaded')
    parser.add_argument('-s', '--savepath', metavar='image save path', required=False,
                        help='path to save image, default is in /result')
    
    args = parser.parse_args()

    if not ('without-origin' == args.mode or 'over-origin' == args.mode or 'example' == args.mode):
        parser.error('Invalid mode! Mode can only be: example, without-origin, or over-origin')

    if (('without-origin' == args.mode or 'over-origin' == args.mode) and
        ('loadpath' not in vars(args) or 'savepath' not in vars(args))):
        parser.error('Requires loadpath for image and savepath for processed image')

    main(mode=args.mode, image_path=args.loadpath, save_path=args.savepath)
    