from math import *
import os
import sys
import matplotlib.pyplot as plt
import settings
from list_all_files_in_a_folder import *
import numpy
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import numpy as np
from matplotlib import cm


## 
# @brief : name is self explanatory
# 
# @param accurateValues
# @param currentValues
# 
# @return 
def calculateError(accurateValues, currentValues):
    if not(len(accurateValues) == len(currentValues)):
        print "**********ERROR********" 
        print "here is the accurate values: " + str(accurateValues)
        print "here is the current values: " + str(currentValues)
        print "number of results subelements for currentValues and accuratValues are not the same"
        print "check the " + settings.rawresultFileName + " file"
        print "**********ERROR********" 
        exit()
    
    result = 0 
    for accurateValue,currentValue in zip(accurateValues,currentValues):
        result += pow(int(accurateValue) - int(currentValue), 2)

    return sqrt(result)/len(accurateValues)


def extractAccurateValues(sourceFileName ):
    start = 0 
    currentValues = []
    #whether the file exist or no 
    if not(os.path.isfile(sourceFileName)):
        print "source file with the name " + sourceFileName + "doesn't exist"
        exit();
    
    with open(sourceFileName) as f:
        for line in f:
            if len(line.split()) >0: 
                for words in line.rstrip().replace(',', ' ').replace('/',' ').replace(';', ' ').split(' '): #find the lines with key word and write it to another file
                    if "end" in words: 
                        return currentValues #if havn't gotten accurate values
                    elif (start==1):
                        currentValues.append(words)
                        break 
                    elif "start" in words: 
                        start = 1 
                        break
                    else:
                        break








## 
# @brief name is explantory
# 
# @param sourceFileName
# 
# @return 
def extractErrorForOneInput(sourceFileName, accurateValues):
    start = 0 
    currentValues = []
    #whether the file exist or no 
    if not(os.path.isfile(sourceFileName)):
        print "source file with the name " + sourceFileName + "doesn't exist"
        exit();
    error = [] 
    setup = 0 #the specific setup(same configuration but different type of operators) 
    with open(sourceFileName) as f:
        for line in f:
            if len(line.split()) >0: 
                for words in line.rstrip().replace(',', ' ').replace('/',' ').replace(';', ' ').split(' '): #find the lines with key word and write it to another file
                    if "end" in words: 
                        error = calculateError(accurateValues, currentValues)
                        currentValues = [] 
                        start = 0
                        break 
                    elif (start==1):
                        currentValues.append(words)
                        #print "\nfound currentValues; " + str(currentValues) 
                        break 
                    elif "start" in words: 
                        start = 1 
                        break
                    else:
                        break


    return error 





## 
# @brief name is explantory
# 
# @param sourceFileName
# 
# @return 
def extractInputFileName(sourceFileName):
    start = 0 
    #whether the file exist or no 
    if not(os.path.isfile(sourceFileName)):
        print "source file with the name " + sourceFileName + "doesn't exist"
        exit();
    with open(sourceFileName) as f:
        for line in f:
            if len(line.split()) >0: 
                for words in line.rstrip().replace(',', ' ').replace('/',' ').replace(';', ' ').split(' '): #find the lines with key word and write it to another file
                    if ("INPUT" in words): 
                        return line.split()[3]
    print "*****ERROR*******"
    print "the source file with the name of: " + str(sourceFileName) + " required for getting the inputFileName does not contain the proper format"
    print "*****ERROR******"
    




def calculateAdderEnergy(numberOfBits):
#    print "&&&" 
#    print numberOfBits
#    print "&&&" 
    return numberOfBits



def calculateMultiplierEnergy(numberOfBits):
    return 31*calculateAdderEnergy(numberOfBits)

## 
# @brief : name is self explanatory
# 
# @param accurateValues
# @param currentValues
# 
# @return 
def calculateEnergy(operatorNumberOfBitsList):
    result = 0 
    for element in operatorNumberOfBitsList:
        if (element[0][-1] == 'a'):  #it is an adder
            result += calculateAdderEnergy(int(element[1])) 
        elif (element[0][-1] == 'm'):  #it is an mulitplier 
            result += calculateMultiplierEnergy(int(element[1])) 
        else:
            print "**************************ERROR*****************"
            print "the operator with the name: " + element[0] + " is operator is not defined"
            exit()
    
    return result 

## 
# @brief name is explantory
# 
# @param sourceFileName
# 
# @return 
def extractEnergyAndConfig(sourceFileName):
    start = 0 
    values = []
    configValues = []
    config = [] 
    #whether the file exist or no 
    if not(os.path.isfile(sourceFileName)):
        print "************EROR******" 
        print "the source file with the Name " + sourceFileName + " necessary for calculateing energy does not exist"

        exit();
    energy = [] 
    
    with open(sourceFileName) as f:
        for line in f:
            if len(line.split()) > 0: 
                for words in line.rstrip().replace(',', ' ').replace('/',' ').replace(';', ' ').split(' '): #find the lines with key word and write it to another file
                    values.append((line.split()[0], int(line.split()[1]) - int(line.split()[2])))
                    configValues.append(line.rstrip())
                    break


    return [configValues]


## 
# @brief self explan
# 
# @param sourceFileName
# 
# @return 
#def extract_properties(operatorSampleFileName, rawResultsFolderName, resultFileName, gotAccurateValue, accurateValues, operandFileName):
#    inputFileNameList = [] 
#    error = [] 
#    if not(os.path.isdir(rawResultsFolderName)):
#        print "rawResultFolder with the Name " + rawResultsFolderName + " does not exist"
#        exit();
# 
#    nameOfAllResultsList = getNameOfFilesInAFolder(rawResultsFolderName)
#    #config = extractEnergyAndConfig(operatorSampleFileName)
#    error = extractErrorForOneInput(resultFileName, gotAccurateValue, accurateValues)
#    result = error
#    
#    return result
#


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#******The rest of the file is for testing the modules defined above
def energyTest():
	#testing the modules defined in this file
	#print calculateEnergy([4,6])
	print extractEnergyAndConfig("/home/polaris/behzad/apx_tool_chain/input_output_text_files/all_possible_apx_operators_scenarios.txt")
	
	
def errorTest():
	#testing the modules defined in this file
	#print calculateError([4,6],[4,0,3])
	print extractErrorForOne("/home/polaris/behzad/apx_tool_chain/input_output_text_files/raw_result_foraw_results.txt")




def extractPropertyTest():
    energy, error= extract_properties("/home/polaris/behzad/apx_tool_chain/input_output_text_files/all_possible_apx_operators_scenarios.txt","/home/polaris/behzad/apx_tool_chain/input_output_text_files/raw_result_folder")
    print energy
    for errorElement in error:
        print errorElement

#energyTest()
#errorTest()
#extractPropertyTest()
