import os
import glob

def getNameOfFilesInAFolder(folderAddress):
    if not(os.path.isdir(folderAddress)):
            print "the folder (for which you requested to get the files for does not exist" 
            exit()
    else:
        return glob.glob(folderAddress + "/*")


## 
# @brief this module generates a folder with the following name (newFolderName + suffix) in the folderTOCopyTo. the suffix is one higher than the highest suffix in folderToCopyTo
# 
# @param folderToCopyTo
# @param folderToCopyFrom
# @param newFolderName
# 
# @return 
def generateBackup(folderToCopyTo, folderToCopyFrom, newFolderName):
    if not(os.path.isdir(folderToCopyTo)):
        print "folder with the name " + folderToCopyTo + "which is required for 'to copy to' folder does not exist"
        exit();
    
    if not(os.path.isdir(folderToCopyFrom)):
        print "folder with the name " + folderToCopyFrom + " which is required for 'to copy from' does not exist"
        exit();
    
    
    fileList = getNameOfFilesInAFolder(folderToCopyTo)
    
    if not(len(fileList) == 0): 
        newestFolder = max(glob.iglob(folderToCopyTo+"/*") , key=os.path.getctime) #getting the newst folder
        if((newestFolder[-3:]).isdigit()):
            suffix = newestFolder[-3:]
        elif((newestFolder[-2:]).isdigit()):
            suffix = newestFolder[-2:]
        elif((newestFolder[-1:]).isdigit()):
            suffix = newestFolder[-1:]
    else:
        suffix = -1 

     
    newFolderFullAddress = folderToCopyTo + "/" + newFolderName + str(int(suffix) + 1)
    error = os.system("mkdir " + newFolderFullAddress)
    if (error):
        print "*******************ERROR******" 
        print "some thing went wrong with generating a new folder with the name " + newFolderFullAddress
        exit() 
    fileList = getNameOfFilesInAFolder(folderToCopyFrom)
    if not(len(fileList) == 0): 
        os.system("cp -r " + folderToCopyFrom+ "/* " + newFolderFullAddress)
#
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#test
#print getNameOfFilesInAFolder("/home/polaris/behzad/python_collection")
#generateBackup("/home/polaris/behzad/copyTo", "/home/polaris/behzad/copyFrom", "newFolder")


