import os
def make():
    #print "blahblah"
    error = os.system("make"); 
    if (error):
        print "was not able to make"
        exit()
    #os.system("make clean; make"); 




