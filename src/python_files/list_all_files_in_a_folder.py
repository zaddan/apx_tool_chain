import os
import glob

def getNameOfFilesInAFolder(folderAddress):
    if not(os.path.isdir(folderAddress)):
            print "the folder with the name " + folderAddress + " (for which you requested to get the files for does not exist" 
            exit()
    else:
        return glob.glob(folderAddress + "/*")


## 
# @brief responsible for finding a suffix for back up floder.
    # to make this name, we add the newFolderNameInFolderToCopyTo with a number wich is aqcuired from 
    #finding the newest folder and adding one to the number that is the suffix of that folder
# 
# @param folderToCopyTo
# 
# @return 
def comeUpWithNewFolderNameAccordingly(folderToCopyTo):
    fileList = getNameOfFilesInAFolder(folderToCopyTo)
    if not(len(fileList) == 0): 
        newestFolder = max(glob.iglob(folderToCopyTo+"/*") , key=os.path.getctime) #getting the newst folder
        print newestFolder
        if((newestFolder[-3:]).isdigit()):
            suffix = newestFolder[-3:]
        elif((newestFolder[-2:]).isdigit()):
            suffix = newestFolder[-2:]
        elif((newestFolder[-1:]).isdigit()):
            suffix = newestFolder[-1:]
    else:
        suffix = -1 

    newFolderFullAddress = "backup_" + str(int(suffix) + 1)
    return newFolderFullAddress


## 
# @brief this module generates a folder with the following name (newFolderNameInFolderToCopyTo + suffix) in the folderTOCopyTo. the suffix is one higher than the highest suffix in folderToCopyTo
# 
# @param folderToCopyTo
# @param listOfFoldersToCopyFrom
# @param newFolderNameInFolderToCopyTo
# 
# @return 
def generateBackup(folderToCopyTo, listOfFoldersToCopyFrom, newFolderNameInFolderToCopyTo):
    #---------guide::: (error checking) check whether the required folders exist
    if not(os.path.isdir(folderToCopyTo)):
        print "folder with the name " + folderToCopyTo + "which is required for 'to copy to' folder does not exist"
        exit();
    
     
    for folderName in listOfFoldersToCopyFrom:
        if not(os.path.isdir(folderName)):
            print "**************ERROR****************" 
            print "folder with the name " + folderName + " which is required for 'to copy from' does not exist"
            exit();
    
    #---------guide:::  making the folder that we dump the 
    #---------guide:::  error checking with the name 
    newFolderFullAddress = folderToCopyTo + "/" + newFolderNameInFolderToCopyTo 
    error = os.system("mkdir " + newFolderFullAddress)
    if (error):
        print "*******************ERROR******" 
        print "some thing went wrong with generating a new folder with the name " + newFolderFullAddress
        exit() 
    
    #---------guide:::  copy the folders over
    for folderName in listOfFoldersToCopyFrom:
        fileList = getNameOfFilesInAFolder(folderName)
        if not(len(fileList) == 0): 
            os.system("cp -r " + folderName + " " + newFolderFullAddress)
#
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#test
#print getNameOfFilesInAFolder("/home/polaris/behzad/python_collection")
#generateBackup("/home/polaris/behzad/copyTo", "/home/polaris/behzad/copyFrom", "newFolder")


