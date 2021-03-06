import numpy as np
from PIL import Image
from PIL import ImageFile
import math 
ImageFile.LOAD_TRUNCATED_IMAGES = True
import multiprocessing
import os
import sys
# ---- get the RGB values of an image
def get_RGB_values(imageName):
    
    try: 
        im = Image.open(imageName)
    except Exception as ex:
        print "an exception happend"
        print "process num: " + str(multiprocessing.current_process()._identity[0] - 1)
        print "image Name: " + str(imageName)
        exit()
    pix = im.load()
    RValues = []
    GValues = []
    BValues = []
    for i in range(im.size[0]):
        for j in range(im.size[1]):
            RValues.append(pix[i, j][0])
            GValues.append(pix[i, j][1])
            BValues.append(pix[i, j][2])

    return(RValues, GValues, BValues, im.size)

# ---- calculate the psnr of two images
def calculate_psnr(refImage, noisyImage):
    # ---- get R,G,B values of the two image
    
    
    refImageRVal, refImageGVal, refImageBVal, img_size = get_RGB_values(refImage)
    noisyImageRVal, noisyImageGVal, noisyImageBVal,_  = get_RGB_values(noisyImage)
    
    # ---- calculate the mean squared error
    img_total_size = img_size[0]*img_size[1] 
    mseR = np.sum((np.asarray(refImageRVal) - np.asarray(noisyImageRVal)) **2)/img_total_size
    mseG = np.sum((np.asarray(refImageGVal) - np.asarray(noisyImageGVal)) **2)/img_total_size
    mseB = np.sum((np.asarray(refImageBVal) - np.asarray(noisyImageBVal)) **2)/img_total_size
    
    # ---- Average mean square error of R, G, B.
    mse = (mseR + mseG + mseB)/3;

    # ---  Calculate PSNR (Peak Signal to noise ratio).
    really_small_number =  .0000000001

    if mse < really_small_number:
        print "you need to make really_small_number smaller b/c mse for some case\
                has ended up being smaller: mse" + str(mse) + " really_small_number: "\
                + str(really_small_number)
    
    if mse == 0:
        mse = really_small_number
    
    print "here is mse " + str(mse)
    PSNR_Value = 10 * math.log10( 255*255 / mse);
    print "here is PSNR"
    return PSNR_Value


def calculate_mean_acc_for_image(refImage, noisyImage):
    # ---- get R,G,B values of the two image
    refImageRVal, refImageGVal, refImageBVal, img_size = get_RGB_values(refImage)
    # ---- calculate the mean squared error
    img_total_size = img_size[0]*img_size[1] 
    return np.sum((np.asarray(refImageRVal)) **2)/img_total_size

def calculate_error_for_image(refImage, noisyImage):
    # ---- get R,G,B values of the two image
    noisyImage_ppm = noisyImage[:-4]+".ppm" 
    refImage_ppm =  refImage[:-4]+".ppm" 
    print "1nononono " + refImage_ppm
    print "2nononono " + noisyImage_ppm
    os.system("convert " + noisyImage + " " + noisyImage_ppm)
    refImageRVal, refImageGVal, refImageBVal, img_size = get_RGB_values(refImage_ppm)
    noisyImageRVal, noisyImageGVal, noisyImageBVal,_  = get_RGB_values(noisyImage_ppm)
    # ---- calculate the mean squared error
    img_total_size = img_size[0]*img_size[1] 
    mseR = np.sum((np.asarray(refImageRVal) - np.asarray(noisyImageRVal)) **2)/img_total_size
    mseG = np.sum((np.asarray(refImageGVal) - np.asarray(noisyImageGVal)) **2)/img_total_size
    mseB = np.sum((np.asarray(refImageBVal) - np.asarray(noisyImageBVal)) **2)/img_total_size
    
    # ---- Average mean square error of R, G, B.
    mse = (mseR + mseG + mseB)/3;
    return mse





#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# # ---- testing
# def main():
    # refImage = "roki.jpg";
    # noisyImage = 'roki_2.jpg'
    # psnr = calculate_psnr(refImage, noisyImage)
    # print psnr

# if __name__ == "__main__":
#     main()
