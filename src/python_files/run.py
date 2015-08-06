import os
def run(executableFileName, runInput1, runInput2, runInput3, runInput4):
    #print executable + " " + ' '.join(executableInputList);
    error = os.system("./"+str(executableFileName) + " " + runInput1 + " " +  runInput2 + " " + runInput3 + " " + runInput4)
    if (error == 0):
        print "the c program was terminated" 
        exit()



