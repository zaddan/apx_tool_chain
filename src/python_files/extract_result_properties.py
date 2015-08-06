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
def calculateNoise(accurateValues, currentValues):
    if not(len(accurateValues) == len(currentValues)):
        print "**********ERROR********" 
        print "number of results subelements for currentValues and accuratValues are not the same"
        print "check the " + settings.rawresultFileName + " file"
        print "**********ERROR********" 
        sys.exit()
    
    result = 0 
    for accurateValue,currentValue in zip(accurateValues,currentValues):
        result += pow(int(accurateValue) - int(currentValue), 2)

    return sqrt(result)/len(accurateValues)




## 
# @brief name is explantory
# 
# @param sourceFileName
# 
# @return 
def extractNoiseForOneInput(sourceFileName, gotAccurateValue, accurateValues):
    start = 0 
    accurateValuesReached = True 
    currentValues = []
    #whether the file exist or no 
    if not(os.path.isfile(sourceFileName)):
        print "source file with the name " + sourceFileName + "doesn't exist"
        exit();
    noise = [] 
    setup = 0 #the specific setup(same configuration but different type of operators) 
    with open(sourceFileName) as f:
        for line in f:
            if len(line.split()) >0: 
                for words in line.rstrip().replace(',', ' ').replace('/',' ').replace(';', ' ').split(' '): #find the lines with key word and write it to another file
                    if "end" in words: 
                        if not(gotAccurateValue): #if havn't gotten accurate values
                            return currentValues
                        else: 
                            noise.append(calculateNoise(accurateValues, currentValues))
                        currentValues = [] 
                        start = 0
                        break 
                    elif (start==1):
                        currentValues.append(words)
                        break 
                    elif "start" in words: 
                        start = 1 
                        break
                    else:
                        break


    return noise 





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
            print "this operator is not defined"
            sys.exit()
    
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
        print "the source file with the Name " + sourceFileName + " does not exist"
        exit();
    energy = [] 
    
    with open(sourceFileName) as f:
        for line in f:
            if len(line.split()) > 0: 
                for words in line.rstrip().replace(',', ' ').replace('/',' ').replace(';', ' ').split(' '): #find the lines with key word and write it to another file
                    if "end" in words: 
                        start = 0
                        config.append(configValues) 
                        energy.append(calculateEnergy(values))
                        values = [] 
                        configValues = [] 
                        break 
                    elif (start==1):
                        values.append((line.split()[0], int(line.split()[1]) - int(line.split()[2])))
                        configValues.append(line.rstrip())
                        break 
                    elif "start" in words: 
                        start = 1 
                        break


    return energy, config


## 
# @brief self explan
# 
# @param sourceFileName
# 
# @return 
def extract_properties(all_possible_apx_operators_scenarios_file_name, rawResultsFolderName, resultFileName, gotAccurateValue, accurateValues):
    inputFileNameList = [] 
    noise = [] 
    if not(os.path.isdir(rawResultsFolderName)):
        print "rawResultFolder with the Name " + rawResultsFolderName + " does not exist"
        exit();
 
    nameOfAllResultsList = getNameOfFilesInAFolder(rawResultsFolderName)
    energy,config = extractEnergyAndConfig(all_possible_apx_operators_scenarios_file_name)
    noise = extractNoiseForOneInput(resultFileName, gotAccurateValue, accurateValues)
    inputFileNameList = extractInputFileName(resultFileName)
    
    result = (energy, noise, config, [inputFileNameList])

    return result



#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#******The rest of the file is for testing the modules defined above
def energyTest():
	#testing the modules defined in this file
	#print calculateEnergy([4,6])
	print extractEnergyAndConfig("/home/polaris/behzad/apx_tool_chain/input_output_text_files/all_possible_apx_operators_scenarios.txt")
	
	
def noiseTest():
	#testing the modules defined in this file
	#print calculateNoise([4,6],[4,0,3])
	print extractNoiseForOne("/home/polaris/behzad/apx_tool_chain/input_output_text_files/raw_result_foraw_results.txt")




def extractPropertyTest():
    energy, noise= extract_properties("/home/polaris/behzad/apx_tool_chain/input_output_text_files/all_possible_apx_operators_scenarios.txt","/home/polaris/behzad/apx_tool_chain/input_output_text_files/raw_result_folder")
    print energy
    for noiseElement in noise:
        print noiseElement

#energyTest()
#noiseTest()
#extractPropertyTest()
