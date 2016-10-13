import os
import sys
import multiprocessing
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
    for index, element in enumerate(lOfAllInputs):
        if (element.split("/")[0] == "~"):
            lOfAllInputs[index] = os.path.expanduser('~') + element[1:]
    lOfAllInputsConvertedToString = ' '.join(str(e) for e in lOfAllInputs)
    print "run with the following command"  + str(lOfAllInputsConvertedToString)
    #--here 
    string_to_check =  str(lOfAllInputsConvertedToString.split(" ")[1].split('/')[-1])
#    
#    if not( ((multiprocessing.current_process()._identity[0] - 1 == 0) and (string_to_check == "flowerpots_1_noisy.jpg")) or \
#            ((multiprocessing.current_process()._identity[0] - 1 == 1) and (string_to_check == "aloe_1_noisy.jpg"))):
#        print "not matching" + str(multiprocessing.current_process()._identity[0] - 1) + " " + string_to_check
    
    #print "not matching" + str(multiprocessing.current_process()._identity[0] - 1) + " " + string_to_check
    print   "./"+str(executableFileName) + " " + runInput1 + " " +  runInput2 + " " + runInput3 + " " + lOfAllInputsConvertedToString
    os.system("./"+str(executableFileName) + " " + runInput1 + " " +  runInput2 + " " + runInput3 + " " + lOfAllInputsConvertedToString)
    # if (error == 0):
        # print "the c program was terminated" 
        # exit()



