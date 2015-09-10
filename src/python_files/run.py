import os
import sys
## 
# @brief this is a helper module is for some behaviour testing. it parses a file and prints the lines in the file
# 
# @param srcFileName
# 
# @return 
def parseAndReturn(srcFileName):
    srcFilePtr = open(srcFileName, "r")
    for line in srcFilePtr:
        return line
    srcFilePtr.close()



def run(executableFileName, runInput1, runInput2, runInput3, runInput4):
    #print executable + " " + ' '.join(executableInputList);
    operandSampleFileName = runInput4 
    lOfAllInputs = parseAndReturn(operandSampleFileName).split()
    lOfAllInputsConvertedToString = ' '.join(str(e) for e in lOfAllInputs)
    error = os.system("./"+str(executableFileName) + " " + runInput1 + " " +  runInput2 + " " + runInput3 + " " + lOfAllInputsConvertedToString)
    if (error == 0):
        print "the c program was terminated" 
        exit()



