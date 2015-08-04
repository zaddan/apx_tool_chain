import os
import glob

def getNameOfFilesInAFolder(folderAddress):
    if not(os.path.isdir(folderAddress)):
            print "the folder (for which you requested to get the files for does not exist" 
            exit()
    else:
        return glob.glob(folderAddress + "/*")


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#test
#print getNameOfFilesInAFolder("/home/polaris/behzad/python_collection")

