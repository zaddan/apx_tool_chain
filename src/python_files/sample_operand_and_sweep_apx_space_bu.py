import settings
import os
import sys
from sample_apx_space_and_run import sample_apx_space_and_run
## 
# @brief sampling needs to be re written if the input changes. This function is responsible for sampling the operands and then sweeping the results for all apx configurations
# 
# @param CSrcFolder
# @param executableName
# @param executableInputList
# @param resultFolderName
# @param resultFileName
# @param CBuildFolder
# 
# @return 
def sampleOperandAndSweepApxSpace(CSrcFolderName , executableName, executableInputList, resultFolderName, resultFileName, CBuildFolder, AllOperandScenariosInOneFiles, AllOperandsFileOrDirectoryName):
    #whether the file exist or no 

    AllOperandScenariosFullAddress = resultFolderName + "/" +settings.AllOperandScenarios;
    operandSampleFullAddress = resultFolderName + "/" +settings.operandSampleFileName
   

    if not(os.path.isfile(AllOperandScenariosFullAddress)):
        print AllOperandScenariosFullAddress + " does not exist"
        exit();
    
    inputNumber = 0 
    if (AllOperandScenariosInOneFiles):
        separate it to different files
    else:
        go through the folder


    with open(AllOperandScenariosFullAddress) as f:
        for line in f:
            if len(line.split()) >0: 
                #get a sample for operandSample file 
                operandSampleFullAddressP = open(operandSampleFullAddress, "w")
                operandSampleFullAddressP.write(line)
                operandSampleFullAddressP.close()
                #clearly state where the new results associated with the new input starts 
                rawresultsP = open(resultFolderName + "/" +settings.rawresultFileName, "a")
                rawresultsP.write("---------------------------------------------------------------------\n")
                rawresultsP.write("---------------------------------------------------------------------\n")
                rawresultsP.write("----------------------------NEWINPUT---------------------------------\n")
                rawresultsP.write("inputNumber is " + str(inputNumber) + "\n") 
                rawresultsP.close()
                #starting sampling from the apx configurations and write the result
                sample_apx_space_and_run(CSrcFolderName, executableName, executableInputList, resultFolderName, settings.rawresultFileName, CBuildFolder);
            inputNumber += 1

