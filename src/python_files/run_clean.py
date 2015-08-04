import sys
from clean_up import *

def runCleanUpEverything():
    if (len(sys.argv) < 2):  
        print "******ERROR*******"
        print "you need to provide the following command line inputs, with the order mentioned"
        print "1.root Folder"
        exit() 
    rootFolder = sys.argv[1]
    cleanUpEveryThing(rootFolder)


runCleanUpEverything()
