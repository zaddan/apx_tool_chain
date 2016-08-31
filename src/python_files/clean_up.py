import os
import sys
import settings

def cleanUpExtras(rootResultFolderName, settings_obj):
	os.system("rm " + rootResultFolderName + "/" + settings_obj.operatorSampleFileName) 
    
def cleanUpEveryThing(rootFolder):
    os.system("rm -r " + rootFolder + "/" + settings_obj.generatedTextFolderName)
    os.system("rm -r " + rootFolder + "/" + settings_obj.CBuildFolderName)
    print "rm " + rootFolder + "/" + "src/python_files *pyc"
    os.system("rm " + rootFolder + "/" + "src/python_files/*pyc")




