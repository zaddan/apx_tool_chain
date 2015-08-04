import os
import sys
import settings

def cleanUpExtras(rootResultFolderName):
	os.system("rm " + rootResultFolderName + "/" + settings.operatorSampleFileName) 
    
def cleanUpEveryThing(rootFolder):
    os.system("rm -r " + rootFolder + "/" + settings.generatedTextFolderName)
    os.system("rm -r " + rootFolder + "/" + settings.CBuildFolderName)



