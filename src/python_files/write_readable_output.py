import sys
import os
def writeReadableOutput(resultTuple, symbolsCollected, fileFullAddress):
    os.system("rm " + fileFullAddress)  #remove if exists 
    finalResultFileFullAddressP = open(fileFullAddress, "a")
    for i in range(0, len(resultTuple), 1):
        # finalResultFileFullAddressP.write("this is the inputFile used: " + inputFileNameList[i][0] + "\n")
        finalResultFileFullAddressP.write("this is symbol used for this input file: " + symbolsCollected[i] + "\n") 
         
        finalResultFileFullAddressP.write("pareto optimal values  are:\n")
        for element in resultTuple[i]:
            finalResultFileFullAddressP.write("paretoResult," +  " " + str(element) + "\n")
        finalResultFileFullAddressP.write("----------------------------------------------------------------------------------------\n")
        finalResultFileFullAddressP.write("----------------------------------------------------------------------------------------\n")
        finalResultFileFullAddressP.write("----------------------------------------------------------------------------------------\n")
    
    finalResultFileFullAddressP.close()
