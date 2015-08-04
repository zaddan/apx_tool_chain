import settings
import os
import sys
from sample_apx_space_and_run import sample_apx_space_and_run
from list_all_files_in_a_folder import *
## 
# @brief sampling needs to be re written if the input changes. This function is responsible for sampling the operands and then sweeping the results for all apx configurations
# 
# @param CSrcFolder
# @param executableName
# @param executableInputList
# @param rootResultFolderName: where all the files/folders related to result will be stored in
# @param resultFileName
# @param CBuildFolder
# 
# @return 
def sampleOperandAndSweepApxSpace(executableName, executableInputList, rootResultFolderName, resultFileName, CBuildFolder, AllOperandScenariosInOneFiles, AllOperandsFolderName):
    
    inputNumber = 0 
    nameOfAllOperandFilesList = getNameOfFilesInAFolder(AllOperandsFolderName)
    #---------guide::: go through operand files and sweep the apx space
    for operandSampleFileName in nameOfAllOperandFilesList:
        #clearly state where the new results associated with the new input starts 
        rawResultFileName =  rootResultFolderName + "/" + settings.rawResultFolderName + "/" + settings.csourceOutputFileName + str(inputNumber) + ".txt"
        rawresultsP = open(rawResultFileName, "w")
        rawresultsP.write("---------------------------------------------------------------------\n")
        rawresultsP.write("---------------------------------------------------------------------\n")
        rawresultsP.write("INPUT RELATED TO " + operandSampleFileName + "\n") 
        rawresultsP.write("---------------------------------------------------------------------\n")
        rawresultsP.write("---------------------------------------------------------------------\n")
        rawresultsP.close()
#       #starting sampling from the apx configurations and write the result
        sample_apx_space_and_run(executableName, executableInputList, rootResultFolderName, rawResultFileName, CBuildFolder, operandSampleFileName);
        inputNumber +=1

