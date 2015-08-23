
# Copyright (C) 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
# 

## 
# @file run_tool_chain.py
# @brief  this file run the  the whole tool chain 
# @author Behzad Boroujerdian
# @date 2015-07-01
import shutil
from os.path import expanduser 
import itertools
import pylab
import sys
import os
import datetime
from collections import defaultdict 

from src_parse_and_apx_op_space_gen import *
from modify_operator_sample_file import *
#from sample_operand_and_sweep_apx_space import *
import settings 
from extract_result_properties import *
from plot_generation import *
import matplotlib.pyplot as plt
from find_position import *
from write_readable_output import *
from clean_up import *
from simulating_annealer import *
from misc import *
from curve_fit import *
logFileAddress = "/home/polaris/behzad/apx_tool_chain/generated_text/" + settings.logFileName


def getOperandsInfoForOperatorCharacterization(operandsInfoForOperatorCharacterizationFullAddress, requiredOperandsInfoLengh):
    try:
        f = open(operandsInfoForOperatorCharacterizationFullAddress)
    except IOError:
        handleIOError(operandsInfoForOperatorCharacterizationFullAddress,
                "generating operands for characterization of operators")
        exit()

    else:
        operatoIndex = 0 
        operator_s_operandsInfoList = [] 
        with f:
            for line in f:
                if len(line) != 0:
                    operator_s_operandsInfoList.append([])
                    operator_s_operandsInfoList[operatorIndex] += line.replace(',', ' ').replace('/',' ').replace(';', ' ').split(' ') #find the lines with key word and write it to another file
                    assert(len(operator_s_operandsInfoList[operandIndex]) ==
                            requiredOperandsInfoListLengh), "take a lookat at the "
                    + str(operandsInfoForOperatorCharacterizationFullAddress) + " file. This file does not contain the correct format for the  operands. proper format needs to follow the listOfOperandOneGenValues variable order"
                    operatoIndex += 1
    
      
    print operator_s_operandsInfoList
    sys.exit()
    return operator_s_operandsInfoList
    

def parseLowUpBounderyFile(lowUpBounderyFileName, numberOfInputs):
    if not(os.path.isfile(lowUpBounderyFileName)):
        print "the source file doesn't exist"
        exit();

    upperBoundInputTurn = False
    upperBoundOutputTurn = False
    lowerBoundOutputTurn = False
    lowerBoundInputTurn = False
   
    upperBoundInput =[]
    lowerBoundInput = []
    upperBoundOutput = []
    lowerBoundOutput = []
    for i in range(numberOfInputs):
        upperBoundInput.append([])
        lowerBoundInput.append([])
 
    with open(lowUpBounderyFileName) as f:
        for line in f:
            words =  line.replace(',', ' ').replace('/',' ').replace(';', ' ').split(' ') #find the lines with key word and write it to another file
            if "upperBoundInput:" in words:
                number = 0
                upperBoundInputTurn = True
                upperBoundOutputTurn = False
                lowerBoundOutputTurn = False
                lowerBoundInputTurn = False
                continue
            
            if "upperBoundOutput:" in words:
                number = 0
                upperBoundInputTurn = False 
                upperBoundOutputTurn = True
                lowerBoundOutputTurn = False
                lowerBoundInputTurn = False
                continue


            
            if "lowerBoundOutput:" in words:
                number = 0 
                upperBoundInputTurn = False 
                upperBoundOutputTurn = False 
                lowerBoundOutputTurn = True 
                lowerBoundInputTurn = False
                continue
            
            if "lowerBoundInput:" in words:
                number = 0 
                upperBoundInputTurn = False 
                upperBoundOutputTurn = False 
                lowerBoundOutputTurn = False 
                lowerBoundInputTurn = True 
                continue
        
            if upperBoundInputTurn:
                print number 
                upperBoundInput[number] = [int(i) for i in words]
                number +=1
                continue
            
            if lowerBoundInputTurn:
                lowerBoundInput[number] = [int(i) for i in words]
                number +=1
                continue

            if upperBoundOutputTurn:
                upperBoundOutput = [int(i) for i in words]
                continue

            
            if lowerBoundOutputTurn:
                lowerBoundOutput =  [int(i) for i in words]
                continue

            
    
    return upperBoundInput, upperBoundOutput, lowerBoundInput, lowerBoundOutput 

def generateOperandList(numberOfOperands, operandExactValueLowerBound, operandExactValueUpperBound, maxDevPercentage, workWithNegativeNumbers, operandExactValueStep, numberOfValuesBetweenExactAndDeviation):
    
    assert (numberOfOperands == 2), "generateOperandList module is not functional for operators with more than 2 operands"
    
    results = {} 
    resultsPermutedDic = {}
    
    #---------guide:::  go through the exact values
    for  operandExactValue in range(operandExactValueLowerBound, operandExactValueUpperBound, operandExactValueStep):
        #---------guide:::  find the boundaries for each exact values
        deviationUpperBound = int(maxDevPercentage*operandExactValue)
        deviationLowerBound = int(maxDevPercentage*operandExactValue)
        deviationStep =  int(deviationUpperBound/numberOfValuesBetweenExactAndDeviation)
        if (deviationStep == 0):
            deviationStep = 1
        operandValueUpperBound = operandExactValue + deviationUpperBound + deviationStep
        operandValueLowerBound = operandExactValue - deviationLowerBound
        if (operandValueLowerBound < 0):
            operandValueLowerBound = 0
        
        #---------guide:::  go through the values within the radius of the deviation for each exact value
        for value in range(operandValueLowerBound, operandValueUpperBound, deviationStep):
            if not((operandExactValue, deviationUpperBound) in results.keys()):
                results[(operandExactValue, deviationUpperBound)] = [value]
            else:
                results[(operandExactValue, deviationUpperBound)] += [value]

    
    
    for key1 in results.keys():
        for key2 in results.keys(): 
            beforePermutationList = [results[key1], results[key2]]
            beforePermutationTuple = tuple(beforePermutationList) 
            #resultsPermuted = list(itertools.product(*(results[key], results[key])))
            resultsPermuted = list(itertools.product(*beforePermutationTuple))
            resultsPermutedDic[(key1[0], key1[1],key2[0],key2[1])] = resultsPermuted 

   
#    #---------guide::: permuting the results
#    for key in results.keys(): 
#        beforePermutationList = []
#        for i in range(0, numberOfOperands + 1, 1):
#            beforePermutationList += [results[key]]
#        beforePermutationTuple = tuple(beforePermutationList) 
#        #resultsPermuted = list(itertools.product(*(results[key], results[key])))
#        resultsPermuted = list(itertools.product(*beforePermutationTuple))
##        print "********" 
##        print resultsPermuted
#        resultsPermutedDic[key] = resultsPermuted 
#

    return resultsPermutedDic 


## 
# @brief generates operands if the operands do not have the same lower,upper bounds, etc. For now, it is only functional for two input operators
# 
# @param numberOfOperands
# @param operandOneExactValueLowerBound
# @param operandOneExactValueUpperBound
# @param maxOneDevPercentage
# @param workWithNegativeNumbers
# @param operandOneExactValueStep
# @param numberOfValuesBetweenExactAndDeviationOne
# @param operandTwoExactValueLowerBound
# @param operandTwoExactValueUpperBound
# @param maxTwoDevPercentage
# @param operandTwoExactValueStep
# @param numberOfValuesBetweenExactAndDeviationTwo
# 
# @return 
def generateOperandListEachOperandUnique(numberOfOperands, operandOneExactValueLowerBound, operandOneExactValueUpperBound, maxOneDevPercentage, workWithNegativeNumbers, operandOneExactValueStep, numberOfValuesBetweenExactAndDeviationOne,  operandTwoExactValueLowerBound, operandTwoExactValueUpperBound, maxTwoDevPercentage, operandTwoExactValueStep, numberOfValuesBetweenExactAndDeviationTwo):
    if (numberOfOperands != 2):
        print "*************ERROR*********"
        print "generateOperandListEachOperandUnique module is not functional for operators with more than 2 operands" 
        exit()

    
    #---------guide:::  go through the exact values
    results = defaultdict(list)
    for  operandOneExactValue in range(int(operandOneExactValueLowerBound),
            int(operandOneExactValueUpperBound), int(operandOneExactValueStep)):
        #---------guide:::  find the boundaries for each exact values
        deviationUpperBound = int(maxOneDevPercentage*operandOneExactValue)
        deviationLowerBound = int(maxOneDevPercentage*operandOneExactValue)
        deviationStep =  int(deviationUpperBound/numberOfValuesBetweenExactAndDeviationOne)
        if (deviationStep == 0):
            deviationStep = 1

        operandValueUpperBound = operandOneExactValue + deviationUpperBound
        operandValueLowerBound = operandOneExactValue - deviationLowerBound
        if (operandValueLowerBound < 0):
            operandValueLowerBound = 0
        
        #---------guide:::  go through the values within the radius of the deviation for each exact value
        for value in range(operandValueLowerBound, operandValueUpperBound, deviationStep):
            results[(operandOneExactValue, deviationUpperBound)].append(value)
    operandOneResults = copy.copy(results)
    
    
    #---------guide:::  go through the exact values
    results = {} 
    results = defaultdict(list)
    for  operandTwoExactValue in range(int(operandTwoExactValueLowerBound),
            int(operandTwoExactValueUpperBound), int(operandTwoExactValueStep)):
        #---------guide:::  find the boundaries for each exact values
        deviationUpperBound = int(maxTwoDevPercentage*operandTwoExactValue)
        deviationLowerBound = int(maxTwoDevPercentage*operandTwoExactValue)
        deviationStep =  int(deviationUpperBound/numberOfValuesBetweenExactAndDeviationTwo)
        if (deviationStep == 0):
            deviationStep = 1
        operandValueUpperBound = operandTwoExactValue + deviationUpperBound
        operandValueLowerBound = operandTwoExactValue - deviationLowerBound
        if (operandValueLowerBound < 0):
            operandValueLowerBound = 0
         
        #---------guide:::  go through the values within the radius of the deviation for each exact value
        for value in range(operandValueLowerBound, operandValueUpperBound, deviationStep):
            results[(operandTwoExactValue, deviationUpperBound)].append(value)
    operandTwoResults = copy.copy(results)

    #---------guide::: permuting the results
    resultsPermutedDic = {}
    for key1 in operandOneResults.keys():
        for key2 in operandTwoResults.keys(): 
            beforePermutationList = [operandOneResults[key1], operandTwoResults[key2]]
            beforePermutationTuple = tuple(beforePermutationList) 
            print beforePermutationTuple
            #resultsPermuted = list(itertools.product(*(results[key], results[key])))
            resultsPermuted = list(itertools.product(*beforePermutationTuple))
            resultsPermutedDic[(key1[0], key1[1],key2[0],key2[1])] = resultsPermuted 
            #resultsPermutedDic[(key1,key2)] = resultsPermuted 

    return resultsPermutedDic 



def writeOperandInOperandFile(operand, operandFileName):
    operandFileP = open(operandFileName ,"w");  
    operandFileP.write(operand) 
    operandFileP.close()


def findApxBitRange(config, noiseList, desiredNoise):
    #        for setUp in config[operandIndex]:
#             apxBitList[operandIndex].append(getApxBit(setUp))
#
    
    noiseArray = numpy.array(noiseList)
    sortedNoiseArray = numpy.sort(noiseArray)        
    sortedNoiseArrayIndex = numpy.argsort(noiseArray)

    #print "\nnoise is: " +str(noiseList) 
    #sortedNoiseIndexList = [sortedNoise.index(x) for x in sortedNoise)




    upBoundary = -1
    lowBoundary = -1
    for noiseIndex in range(0, len(sortedNoiseArray)):
        if (sortedNoiseArray[noiseIndex] > desiredNoise):
            if (noiseIndex == 0):
                print "*****ERROR***"
                print "no noise satisfied the condition" 
                exit()


            upBoundary = noiseIndex
            break;   
        if (noiseIndex == len(sortedNoiseArray)-1):
            upBoundary = len(sortedNoiseArray)
            break;  

    acceptableIndexArray = sortedNoiseArrayIndex[:upBoundary]

    for i in range(acceptableIndexArray.min(), acceptableIndexArray.max()+ 1,1):
        if not(i in acceptableIndexArray):
            print "****ERROR****"
            print "this operator is not continuous. This means that there are some bits in the middle of the range that do not satisfy the nosie requirements. this means that the operator is not completely increasing or decreasing"
            print exit()

    upperBound = acceptableIndexArray.max()
    lowerBound = acceptableIndexArray.min()
    #print upperBound
    #print lowerBound
    return upperBound, lowerBound


def polishSetup(setUp):
    result = []  
    for element in setUp: 
        resultElement = ' '.join(str(e) for e in element) 
        result.append(resultElement)
    return [result] 


def findLowAndUpBounderies(CSrcFolderAddress, CSrcFileAddress , generateMakeFile , finalResultFileName, rootFolder,operandDic):
    
    #---------guide:::  checking the validity of the input and making necessary files
    #and folders
    rootResultFolderName = rootFolder + "/" + settings.generatedTextFolderName
    rootResultFolderBackupName =  rootFolder + "/" + settings.resultsBackups # is used to get a back up of the results generated in the previuos run of this program
    if not(os.path.isdir(rootResultFolderBackupName)):
        os.system("mkdir" + " " + rootResultFolderBackupName)
    os.system("rm -r " + rootResultFolderName)
    os.system("mkdir " + rootResultFolderName)
    executableName = "tool_exe" #src file to be analyzed
    CBuildFolder = rootFolder + "/" + settings.CBuildFolderName
    
    executableInputList = [] #not necessary anymore
    #only the src file needs to be validated. The other inputs will be valideated in the lateer stages
    if not(os.path.isfile(CSrcFileAddress)):
        print "the file with the name: " + CSrcFileAddress + "which contains the csource file address does not exist"
        exit();
    
    #---------guide:::  generate make file or no
    if not((generateMakeFile == "YES") or (generateMakeFile == "NO")): 
        print generateMakeFile 
        print "generateMakeFile can only take YES or NO value (capital letters)"
        exit()

    #removing the result file
    os.system("rm " + rootResultFolderName + "/" + settings.rawresultFileName)

    
    #---if make file needs to be re generated (generated) 
    if (generateMakeFile == "YES"): 
        currentDir = os.getcwd() #getting the current directory
        #CBuildFolder = "./../../" 
        os.chdir(rootFolder) #chaning the directory
        os.system("cp CMakeLists_tool_chain.txt CMakeLists.txt") #restoring the correct CMakeLists.txt file
        os.chdir(currentDir) 
        #generate the makefile using CMAKE 
        print "**********************************************************************"
        print "******************************GENERATING MAKE FILE********************"
        print "**********************************************************************"
        currentDir = os.getcwd() #getting the current directory
        if not(os.path.isdir(CBuildFolder)):
            os.system("mkdir " + CBuildFolder); #making a new one
        os.chdir(CBuildFolder) #chaning the directory
        os.system("cmake ..");
        print "**********************************************************************"
        print "done generating the makeFile using CMake"
        print "**********************************************************************"
        
        os.chdir(currentDir) #chaning the directory
        #done generating the make file 

    
    #---------guide:::  removing the results associated with the previous runs
    os.system("rm -r" + " " +  rootResultFolderName + "/" +settings.AllOperandsFolderName)
    os.system("rm -r" + " " +  rootResultFolderName + "/" + settings.rawResultFolderName)
    os.system("mkdir" + " " + rootResultFolderName + "/" + settings.rawResultFolderName)
    AllOperandsFolderName = rootResultFolderName + "/"+ settings.AllOperandsFolderName
    os.system("mkdir " + AllOperandsFolderName)
    operandFileName = AllOperandsFolderName + "/" + str('0') +".txt"
    operandFileP = open(operandFileName ,"w");  


    lAllOpsInSrcFile = [] 
    sourceFileParse(CSrcFileAddress, lAllOpsInSrcFile)
    
    
    settings.totalNumberOfOpCombinations = 1;
    energy = []
    noise = []
    config = []
    inputFileNameList = []
    
    #---------guide:::  sampling operands
    nameOfAllOperandFilesList = getNameOfFilesInAFolder(AllOperandsFolderName)
    operandIndex = 0
    
    apxBitList = [] 
    
    upperBoundList = [] #contains info of the upperBound bits for each operand
    lowerBoundList = []
    operandInfoApxBitsUpperBoundsDic = {}
    operandInfoApxBitsLowerBoundsDic = {}
        


    operandInfoNoiseDic = {} 
    for i in range(0, len(nameOfAllOperandFilesList),1):
        apxBitList.append([])
    
   
    #---------guide:::  generate a list of all possible cases for each operator
    allPossibleScenariosForEachOperator = generateAllPossibleScenariosForEachOperator(rootResultFolderName, lAllOpsInSrcFile)
    
    logFileP = open(logFileAddress, "w")
    logFileP.write("all possible scenaris for each operator " +
            str(allPossibleScenariosForEachOperator) + "\n")
    logFileP.write("make sure that this list is tuned using settings file\n")
    logFileP.close() 
    
    #---------guide:::  generate all possible apx setUps Possible (mainly used for full permutation design exploration, otherwise called exhustive search)
    allPossibleApxScenarioursList = generateAllPossibleApxScenariousList(allPossibleScenariosForEachOperator)
    IOAndProcessCharFileName = rootResultFolderName + "/" + settings.IOAndProcessCharFileName
    IOAndProcessCharP = open(IOAndProcessCharFileName, "w")
    
    open(settings.annealerProgressionOutputFileName, "w").close()
    open(rootResultFolderName +  "/" + settings.annealerOutputFileName, "w").close()
    
    #---------guide::: go through operand files and sweep the apx space
    timeBeforeFindingResults = datetime.datetime.now()
    
    mode = "allPermutations"
    desiredNoise = 4
    
        
    numberOfKeys = len(operandDic.keys()) 
    firstTime = True 
    keyIndex = 0 
    OneTimeImplementationTime = 0 
    for operand,operandUnfolded in operandDic.items(): 
        # ---- getting timing info
        if (firstTime):
            timeBeforeFindingResults = datetime.datetime.now()

        operandString = ' '.join(str(e) for e in [operand[0], operand[2]])
        writeOperandInOperandFile(operandString, operandFileName)
        CSourceOutputForVariousSetUpFileName =  rootResultFolderName + "/" + settings.rawResultFolderName + "/" + settings.csourceOutputFileName + str('0') + ".txt" #where to collect C++ source results
        operatorSampleFileFullAddress = rootResultFolderName + "/" + settings.operatorSampleFileName
        
        #---------guide:::  getting accurate values associated with the CSource output
        apxIndexSetUp = 0 #zero is associated with the accurate results (this is a contract that needs to be obeyed)
        status, setUp = generateAPossibleApxScenarios(rootResultFolderName + "/" + settings.AllPossibleApxOpScenarios, allPossibleApxScenarioursList , apxIndexSetUp, mode) 
        #---------guide:::  erasing the previuos content of the file
        CSourceOutputForVariousSetUpP = open(CSourceOutputForVariousSetUpFileName, "w").close()
        #---------guide:::  modify the operator sample file
        modifyOperatorSampleFile(operatorSampleFileFullAddress, setUp)
        #---------guide:::  run the CSrouce file with the new setUp(operators)
        make_run(executableName, executableInputList, rootResultFolderName, CSourceOutputForVariousSetUpFileName, CBuildFolder, operandFileName)
        accurateValues = extractAccurateValues(CSourceOutputForVariousSetUpFileName)
        
        # ---- got through each operandElement and find noise with various apx
        #    ops
        lowerBounderyDic = defaultdict(list)        
        upperBounderyDic = defaultdict(list)        
        noise = [[] for i in range(len(operandUnfolded))]
        config = [[] for i in range(len(operandUnfolded))]
        operandIndex = 0 
        for operandElement in operandUnfolded:
            apxIndexSetUp = 0 #zero is associated with the accurate results (this is a contract that needs to be obeyed)
            print operandElement 
            if not(firstTime): 
                print ":::::::::::::::::::::::" 
                print "\ntime remaining: " + str((numberOfKeys - keyIndex)*OneTimeImplementationTime) + " second   " + " or " +  str(((numberOfKeys - keyIndex)*OneTimeImplementationTime)/60) + " in minute"
                print ":::::::::::::::::::::::" 
            
           
            operatorSampleFileFullAddress = rootResultFolderName + "/" + settings.operatorSampleFileName
            operandElementString = ' '.join(str(e) for e in operandElement)
            
            writeOperandInOperandFile(operandElementString, operandFileName)
            CSourceOutputForVariousSetUpFileName =  rootResultFolderName + "/" + settings.rawResultFolderName + "/" + settings.csourceOutputFileName + str('0') + ".txt" #where to collect C++ source results
            
            #---------guide:::  make a apx set up and get values associated with it
            while (True): #break when a signal is raised as done
                status, setUp = generateAPossibleApxScenarios(rootResultFolderName
                        + "/" + settings.AllPossibleApxOpScenarios, allPossibleApxScenarioursList , apxIndexSetUp,  "allPermutations")
                
                #---------guide:::  collect data
                configValue = polishSetup(setUp) #just to make it more readable
                inputFileNameListValue = [operandFileName] 
                CSourceOutputForVariousSetUpP = open(CSourceOutputForVariousSetUpFileName, "w").close()
                modifyOperatorSampleFile(operatorSampleFileFullAddress, setUp)
                make_run(executableName, executableInputList, rootResultFolderName, CSourceOutputForVariousSetUpFileName, CBuildFolder, operandFileName)
                noiseValue = [int(extractNoiseForOneInput(CSourceOutputForVariousSetUpFileName
                    , accurateValues))]
                noise[operandIndex] += noiseValue
                config[operandIndex] +=configValue
                apxIndexSetUp +=1
                if (status == "done"):
                    break;
            
            #---------guide:::  collect the noise information
            operandInfoNoiseDic[operandIndex] = noise[operandIndex]
            #print operandInfoNoiseDic
            
            #---------guide:::  find the low and high bit that places the noise within the desired one
            uniqueNoiseValues = list(set(noise[operandIndex])) 
            for uniqueValue in uniqueNoiseValues: 
                upperBounderyDic[uniqueValue].append(max([i for i,j in zip(count(), 
                    noise[operandIndex])if j == uniqueValue]))
                lowerBounderyDic[uniqueValue].append(min([i for i,j in zip(count(), 
                    noise[operandIndex])if j == uniqueValue]))
                # lowerBoundList.append(min([i for i,j in zip(count(), 
                    # noise[operandIndex])if j == uniqueValue]))
            
            # upperBound, lowerBound = findApxBitRange(config[operandIndex], noise[operandIndex], desiredNoise)
            
            # upperBoundList.append(upperBound)
            # lowerBoundList.append(lowerBound)

            operandIndex += 1
        
        
        print  operandUnfolded
        print noise 
        print lowerBounderyDic
        print upperBounderyDic
        for deltaY in lowerBounderyDic:
            operandInfoApxBitsLowerBoundsDic[operand + tuple([deltaY])] = max(lowerBounderyDic[deltaY])
        for deltaY in upperBounderyDic:
            operandInfoApxBitsUpperBoundsDic[operand + tuple([deltaY])] = min(upperBounderyDic[deltaY])
        
        # operandInfoApxBitsUpperBoundsDic[operand] = min(upperBoundList)
        # operandInfoApxBitsLowerBoundsDic[operand] = max(lowerBoundList)
        upperBoundList = []
        lowerBoundList = []
        
        if (firstTime): 
            timeAfterFindingResults = datetime.datetime.now()
            OneTimeImplementationTime = findTotalTimeInSecond(timeBeforeFindingResults, timeAfterFindingResults) 
            firstTime = False
                    
        keyIndex +=1

    
    
    
    
     
    upperBoundInputList =  operandInfoApxBitsUpperBoundsDic.keys()
    upperBoundOutputList =  operandInfoApxBitsUpperBoundsDic.values()
    
    lowerBoundInputList =  operandInfoApxBitsLowerBoundsDic.keys()
    lowerBoundOutputList =  operandInfoApxBitsLowerBoundsDic.values()

    cleanUpExtras(rootResultFolderName) 
    
    
    return upperBoundInputList, upperBoundOutputList, lowerBoundInputList, lowerBoundOutputList 
    
    #---------guide::: show the graph
    #plt.show() 






## 
# @brief this is the main function (which takes care of the description mentioned in the file description)
# 
# @return : no return
def characterizeOperator(CSrcFolderAddress, CSrcFileAddress, generateMakeFile,
                rootFolder, finalResultFileName,moduleFunctionality, percentageOfDataUsedForTraining,
            workWithNegativeNumbers , numberOfOperands , listOfOperandOneGenValues, listOfOperandTwoGenValues,
            minDegree , maxDegree, signalToNoiseRatio):

# characterizeOperator(CSrcFolderAddress, CSrcFileAddress, generateMakeFile,
        # rootFolder, finalResultFileName, moduleFunctionality, percentageOfDataUsedForTraining,workWithNegativeNumbers = False,numberOfOperands = 2 
        # ,operandExactValueLowerBound = 10
        # ,operandExactValueUpperBound = 14
        # ,operandExactValueStep = 3
        # ,maxInputOperandDeviation = .2
        # ,numberOfValuesBetweenExactAndDeviation = 2, minDegree=2, maxDegree = 4, signalToNoiseRatio = .1):
    
    bestFittedFunc = lambda x: x
    funcCoeff = [] 
    funcErrorDic = {}
    if not(moduleFunctionality in ["all", "generateOperAndFindBoundery", "onlyFindFittedCurve"]):
        print "****ERROR****"
        print "module functionality needs to be one of the followings"
        print  ["all", "generateOperAndFindBoundery", "onlyFindFittedCurve"]
        exit()

    
    if (moduleFunctionality == "onlyFindFittedCurve"): 
        rootResultFolderName = rootFolder + "/" + settings.generatedTextFolderName
    if (moduleFunctionality == "all" or moduleFunctionality == "generateOperAndFindBoundery"):
        #---------guide:::  genrate operands
        # workWithNegativeNumbers = False 
        # numberOfOperands = 2 
        # operandExactValueLowerBound = 10
        # operandExactValueUpperBound = 14
        # operandExactValueStep = 3
        # maxInputOperandDeviation = .2
        # numberOfValuesBetweenExactAndDeviation = 2
        #---------guide::: uncomment the following lines only if your want to use generateOperandListEachOperandUnique. This function is used in situations where we want the input to the operator to 
        #------------------have different properites (such as lowerBound, upperBound, etc)
         
        

        operandOneExactValueLowerBound, operandOneExactValueUpperBound,operandOneExactValueStep, maxInputOperandDeviationOne, numberOfValuesBetweenExactAndDeviationOne = listOfOperandOneGenValues

        operandTwoExactValueLowerBound, operandTwoExactValueUpperBound, operandTwoExactValueStep, maxInputOperandDeviationTwo, numberOfValuesBetweenExactAndDeviationTwo = listOfOperandTwoGenValues
        operandDic = generateOperandListEachOperandUnique(numberOfOperands,
                operandOneExactValueLowerBound, operandOneExactValueUpperBound,
                maxInputOperandDeviationOne, workWithNegativeNumbers,
                operandOneExactValueStep,
                numberOfValuesBetweenExactAndDeviationOne, operandTwoExactValueLowerBound, operandTwoExactValueUpperBound, maxInputOperandDeviationTwo, operandTwoExactValueStep, numberOfValuesBetweenExactAndDeviationTwo)
      
        #operandDic2 = generateOperandList(numberOfOperands, operandExactValueLowerBound, operandExactValueUpperBound, maxInputOperandDeviation, workWithNegativeNumbers, operandExactValueStep, numberOfValuesBetweenExactAndDeviation)

        upperBoundInputList, upperBoundOutputList, lowerBoundInputList, lowerBoundOutputList = findLowAndUpBounderies(CSrcFolderAddress, CSrcFileAddress , generateMakeFile , finalResultFileName, rootFolder, operandDic)
        reshapedUpperBoundInput = [] #we need to reshape the input so it can be fed to curv_fit
                
        for variableNumber in range(0, len(upperBoundInputList[0])):
            reshapedUpperBoundInput.append([])
        
        for variableNumber in range(0, len(upperBoundInputList[0])):
            for inputNumber in range(0, len(upperBoundInputList)):
                reshapedUpperBoundInput[variableNumber].append(upperBoundInputList[inputNumber][variableNumber])
        
       
        reshapedLowerBoundInput = [] #we need to reshape the input so it can be fed to curv_fit
        for variableNumber in range(0, len(lowerBoundInputList[0])):
            reshapedLowerBoundInput.append([])
        
        for variableNumber in range(0, len(lowerBoundInputList[0])):
            for inputNumber in range(0, len(lowerBoundInputList)):
                reshapedLowerBoundInput[variableNumber].append(lowerBoundInputList[inputNumber][variableNumber])


        #---------guide:::  writing the results to the output
        rootResultFolderName = rootFolder + "/" + settings.generatedTextFolderName
        lowUpBounderyFileP = open(rootResultFolderName + "/" + settings.lowUpBounderyFileName ,"w"); 
        
        lowUpBounderyFileP.write("upperBoundInput: \n")
        for element in reshapedUpperBoundInput:
            lowUpBounderyFileP.write(" ".join(str(e) for e in element))
            lowUpBounderyFileP.write("\n")

        lowUpBounderyFileP.write("upperBoundOutput: \n")
        lowUpBounderyFileP.write(" ".join(str(e) for e in upperBoundOutputList))
        lowUpBounderyFileP.write("\n")
        
        lowUpBounderyFileP.write("lowerBoundInput: \n")
        for element in reshapedLowerBoundInput:
            stringToWrite =  " ".join(str(e) for e in element)
            lowUpBounderyFileP.write(stringToWrite)
            lowUpBounderyFileP.write("\n")
        
        lowUpBounderyFileP.write("lowerBoundOutput: \n")
        stringToWrite =  " ".join(str(e) for e in lowerBoundOutputList)
        lowUpBounderyFileP.write(stringToWrite)
        
         
        lowUpBounderyFileP.close()
    numberOfInputs = 5
    if (moduleFunctionality == "all" or moduleFunctionality ==
    "onlyFindFittedCurve"): 
        reshapedUpperBoundInput, upperBoundOutputList, reshapedLowerBoundInput,
        lowerBoundOutputList = parseLowUpBounderyFile(rootResultFolderName +
                "/" + settings.lowUpBounderyFileName, numberOfInputs)
        numberOfInputsForTraining = int(percentageOfDataUsedForTraining * len(reshapedUpperBoundInput[0]))
        
        upperValuesInputTrainingDataRaw = [varValues[:numberOfInputsForTraining] for varValues in reshapedUpperBoundInput]  
        upperValuesOutputTrainingData = [varValues[:numberOfInputsForTraining] for varValues in [upperBoundOutputList]][0]
        print "upperValuesOutputTrainingData : " + str(upperValuesOutputTrainingData )
        upperValuesInputTestDataRaw = [varValues[numberOfInputsForTraining:] for varValues in reshapedUpperBoundInput]  
        upperValuesOutputTestData = [varValues[numberOfInputsForTraining:] for varValues in [upperBoundOutputList]][0]  
        
        lowerValuesInputTrainingDataRaw = [varValues[:numberOfInputsForTraining] for varValues in reshapedLowerBoundInput]  
        lowerValuesOutputTrainingData = [varValues[:numberOfInputsForTraining] for varValues in [lowerBoundOutputList]][0]
        lowerValuesInputTestDataRaw = [varValues[numberOfInputsForTraining:] for varValues in reshapedLowerBoundInput]  
        lowerValuesOutputTestData = [varValues[numberOfInputsForTraining:] for varValues in [lowerBoundOutputList]][0]

                
        maximumAcceptableError = (1 - signalToNoiseRatio)*numpy.float64(sum(upperValuesOutputTestData)/len(upperValuesOutputTestData))
        bestFittedFunc, funcCoeff, funcErrorDic = findBestFitFunction(upperValuesInputTrainingDataRaw, upperValuesOutputTrainingData, upperValuesInputTestDataRaw, upperValuesOutputTestData, all_funcs.funcNumberOfCoeffDic,maxDegree, minDegree, maximumAcceptableError)
        
        
    return bestFittedFunc, funcCoeff, funcErrorDic
#

def characterize_all_operators(CSrcFolderAddress,
        CSrcFileAddress,generateMakeFile, rootFolder, finalResultFileName,
        operatorArchiveAddress,  percentageOfDataUsedForTraining,
        workWithNegativeNumbers, degreeNPolyMultiVarMinDegree,
        degreeNPolyMultiVarMaxDegree, signalToNoiseRatio,
        listOfOperandOneGenValues, listOfOperandTwoGenValues):

    numberOfOperands = 2 
    # degreeNPolyMultiVarMinDegree = 2
    # degreeNPolyMultiVarMaxDegree = 4
    # signalToNoiseRatio = .1


    # operandOneExactValueLowerBound = 13
    # operandOneExactValueUpperBound = 20 
    # operandOneExactValueStep = 3
    # maxInputOperandDeviationOne = .2
    # numberOfValuesBetweenExactAndDeviationOne = 2

    # operandTwoExactValueLowerBound = 10 
    # operandTwoExactValueUpperBound = 20 
    # operandTwoExactValueStep = 3
    # maxInputOperandDeviationTwo = .2
    # numberOfValuesBetweenExactAndDeviationTwo = 5
        
        
    moduleFunctionality = "all"
    rootResultFolderName = rootFolder + "/" + settings.generatedTextFolderName
    operandsInfoForOperatorCharacterizationFullAddress = rootFolder + "/" + settings.operandsInfoForOperatorCharacterizationName
    
    # requiredOperandsInfoLengh =  10 
    

  #   write_operands_info_for_operator_characterization()
    # listOfOperandOneGenValues, listOfOperandTwoGenValues = retrieve_operands_info_for_operator_characterization()


    
    # moduleFunctionality = "onlyFindFittedCurve"
    # moduleFunctionality = "generateOperAndFindBoundery"
    lAllOpsInSrcFile = [] 
    sourceFileParse(CSrcFileAddress, lAllOpsInSrcFile)
    
    # operatorsCoeffFileFullAddress = rootFolder + "/" + settings.generatedTextFolderName + "/" + settings.operatorsCoeffFile
    # print operatorsCoeffFileFullAddress 
    # operatorsCoeffFileP = open(operatorsCoeffFileFullAddress, "w")
    
    write_operands_info_for_operator_characterization()
    listOfOperandOneGenValues, listOfOperandTwoGenValues = retrieve_operands_info_for_operator_characterization()


    for index,item in enumerate(lAllOpsInSrcFile):
        assert(item in ['MultiplicationOp', 'AdditionOp']), str(item) + " is not a valid operator" 
        try:
            operatorAddress = operatorArchiveAddress + "/" + str(item) + ".cpp"
            print operatorAddress 
            shutil.copy(operatorAddress, CSrcFileAddress) 
        except IOError:
            print "*****************ERROR*********************" 
            print "can not copy " + str(operatorAddress) + " to " + str(CSrcFileAddress)
            exit()
    
        
        bestFittedFunc, funcCoeff, funcErrorDic = characterizeOperator(CSrcFolderAddress, CSrcFileAddress, generateMakeFile,
                rootFolder, finalResultFileName,moduleFunctionality, percentageOfDataUsedForTraining,
            workWithNegativeNumbers, numberOfOperands,
            listOfOperandOneGenValues[index], listOfOperandTwoGenValues[index],
              degreeNPolyMultiVarMinDegree, degreeNPolyMultiVarMaxDegree, signalToNoiseRatio)
        
        operatorsCoeffFileP.write("function: \n")
        operatorsCoeffFileP.write(str(bestFittedFunc[0].__name__) + " " +
                str(bestFittedFunc[1]) + "\n")

        print bestFittedFunc 
        
        # stringToWrite =  " ".join(str(e) for e in funcCoeff)
        # operatorsCoeffFileP.write("coeffs: \n")
        # operatorsCoeffFileP.write(stringToWrite + " \n")
        # operatorsCoeffFileP.write("functionError: \n")
        # operatorsCoeffFileP.write(str(funcErrorDic[bestFittedFunc]))
        # sys.exit()


    # characterizeOperator(CSrcFolderAddress, CSrcFileAddress, generateMakeFile, rootFolder, finalResultFileName, moduleFunctionality, percentageOfDataUsedForTraining)
    operatorsCoeffFileP.close() 
    # print funcCoeff
    #
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
test1 = True
# test1 = False

if (test1):
    home = expanduser("~") 
    CSrcFolderAddress =  home + "/apx_tool_chain/src/CSrc/"
    CSrcFileAddress = home + "/apx_tool_chain/src/CSrc/test.cpp"
    generateMakeFile = "YES"
    rootFolder  = home +  "/apx_tool_chain"
    finalResultFileName =  "finalResult2.txt"
    moduleFunctionality = "all"
    #moduleFunctionality = "onlyFindFittedCurve"
    # moduleFunctionality = "generateOperAndFindBoundery"
    percentageOfDataUsedForTraining = .7
    workWithNegativeNumbers = False
    numberOfOperands = 2 
    signalToNoiseRatio = .1
    
    write_operands_info_for_operator_characterization()
    listOfOperandOneGenValues, listOfOperandTwoGenValues = retrieve_operands_info_for_operator_characterization()
    degreeNPolyMultiVarMinDegree = 2
    degreeNPolyMultiVarMaxDegree = 4

    bestFittedFunc, funcCoeff, funcErrorDic = characterizeOperator(CSrcFolderAddress, CSrcFileAddress, generateMakeFile,
            rootFolder, finalResultFileName,moduleFunctionality, percentageOfDataUsedForTraining,
            workWithNegativeNumbers, numberOfOperands,
            listOfOperandOneGenValues[0], listOfOperandTwoGenValues[0],
              degreeNPolyMultiVarMinDegree, degreeNPolyMultiVarMaxDegree, signalToNoiseRatio)
    
    print bestFittedFunc
    # print funcCoeff
    # funcErrorDic 

# test2 = True
# test2 = False
if (test2):
    home = expanduser("~") 
    CSrcFolderAddress =  home + "/apx_tool_chain/src/CSrc/"
    CSrcFileAddress = home + "/apx_tool_chain/src/CSrc/test.cpp"
    generateMakeFile = "YES"
    rootFolder  = home +  "/apx_tool_chain"
    finalResultFileName =  "finalResult2.txt"
    
    percentageOfDataUsedForTraining = .7
    workWithNegativeNumbers = False
    degreeNPolyMultiVarMinDegree = 2
    degreeNPolyMultiVarMaxDegree = 5 
    signalToNoiseRatio = .1
    operatorArchiveAddress = home + "/apx_tool_chain/operator_archive"
    
    write_operands_info_for_operator_characterization()
    listOfOperandOneGenValues, listOfOperandTwoGenValues = retrieve_operands_info_for_operator_characterization()

    characterize_all_operators(CSrcFolderAddress, CSrcFileAddress, generateMakeFile,
            rootFolder, finalResultFileName, operatorArchiveAddress,  percentageOfDataUsedForTraining,
            workWithNegativeNumbers, degreeNPolyMultiVarMinDegree,
            degreeNPolyMultiVarMaxDegree, signalToNoiseRatio,
            listOfOperandOneGenValues, listOfOperandTwoGenValues)


