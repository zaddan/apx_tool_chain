import numpy as np
from PIL import Image
from PIL import ImageFile
import os
import sys
from sklearn.cluster import KMeans

class image:
    def __init__(self):
        self.image_name = ""
        self.image_addr = ""
        self.mean_vals = [] 
        self.std_vals = []
    
    def set_name(self, name):
        self.name = name
    def get_name(self):
        return self.name
    
    def set_addr(self, addr):
        self.addr = addr
    def get_addr(self):
        return self.addr 

    def set_mean(self, mean_vals):
        self.mean_vals = mean_vals
    def get_mean(self):
        return self.mean_vals 
    
    def set_std(self, std_vals):
        self.std_vals = std_vals
    def get_std(self ):
        return self.std_vals 

    def set_cluster(self, cluster_val):
        self.cluster_val = cluster_val

    def get_cluster(self):
        return self.cluster_val 


def get_RGB_values(imageName):
    try: 
        im = Image.open(imageName)
    except Exception as ex:
        print "an exception happend"

    
    im = Image.open(imageName)
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


def calc_image_mean_std(image_name):
    imageRVal, imageGVal, imageBVal, img_size = get_RGB_values(image_name)
    
    # ---- calculate the mean squared error
    mR = np.mean(np.asarray(imageRVal)) 
    mG = np.mean(np.asarray(imageGVal))
    mB = np.mean(np.asarray(imageBVal))
    
    stdR = np.std(np.asarray(imageRVal)) 
    stdG = np.std(np.asarray(imageGVal))
    stdB = np.std(np.asarray(imageBVal))


    # ---- Average mean square error of R, G, B.
    mse = (mR + mG + mB)/3;
    std = (stdR + stdG + stdB)/3;
    return mR, mG, mB, stdR, stdG, stdB


#--- calc mean,std of all the images within a directory
def calc_image_info(base_dir):
    l_of_files = os.listdir(base_dir)
    l_of_ppm_files  = []
    l_of_images = []
    
    #--- get all the files with ppm suffix
    counter = 0 
    for file_name in l_of_files:
        if (file_name[-3:] == "ppm"):
            l_of_ppm_files.append(file_name)
            if counter > 10:
                break
            counter +=1

    for image_name in l_of_ppm_files:
        new_image = image()
        new_image.set_name(image_name)
        new_image.set_addr(base_dir + image_name)
        mR, mG, mB, stdR, stdG, stdB = calc_image_mean_std(base_dir+image_name)
        new_image.set_mean([mR,mG,mB])
        new_image.set_std([stdR, stdG, stdB])
        l_of_images.append(new_image)
    """
    for el in l_of_images:
        print el.get_name() 
        print el.get_mean()
        print el.get_std()
        print "----------"
    """
    return l_of_images


def cluster_images(base_dir, n_clusters):
    #--- gather infor about each image 
    l_of_images = calc_image_info(base_dir);
    all_data = []
    
    #---- collect their infor in an array
    for el in l_of_images:
        data = []  
        data += el.get_std()
        data += el.get_mean()
        all_data.append(data) 


    #----instantiate a KMeans obj
    #n_clusters = 2 #--seting the num of clusters
    myKMeans = KMeans(k=n_clusters, init='k-means++', n_init=4, max_iter=300, tol=0.0001, precompute_distances='auto', verbose=0, random_state=None, copy_x=True, n_jobs=1)

    all_data_as_array = np.asarray(all_data) #data_2_dim needs to be a a list of arrays
    all_data_fitted = myKMeans.fit(all_data_as_array)
    
    for index,el in enumerate(l_of_images):
        el.set_cluster(all_data_fitted.labels_[index])

    return l_of_images 
    
    """ 
    print "labels are " + str(all_data_fitted.labels_)
    print "clusters_ceners are" + str(all_data_fitted.cluster_centers_)
    """

def main():
    base_dir = "/home/local/bulkhead/behzad/usr/local/apx_tool_chain/inputPics/"
    l_of_images = cluster_images(base_dir, 2)
    for el in l_of_images:
        print el.get_name() + ": " + str(el.get_cluster())


if __name__ == "__main__":
    main()


#print mR
#print mG
#print mB
#print stdR
#print stdG
#print stdB
