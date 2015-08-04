import os
import sys
import settings
def cleanUp(rootResultFolderName):
	os.system("rm " + rootResultFolderName + "/" + settings.operatorSampleFileName) 
