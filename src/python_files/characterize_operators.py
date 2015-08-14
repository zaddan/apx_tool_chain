
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

import itertools
import pylab
import sys
import os
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
import datetime

def generateOperandList(numberOfOperands, operandExactValueLowerBound, operandExactValueUpperBound, maxDevPercentage, workWithNegativeNumbers, operandExactValueStep, numberOfValuesBetweenExactAndDeviation):
    
    if (numberOfOperands != 2):
        print "*************ERROR*********"
        print "generateOperandList module is not functional for operators with more than 2 operands" 
        exit()
    
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

    
    results = {} 
    resultsPermutedDic = {}

    #---------guide:::  go through the exact values
    for  operandOneExactValue in range(operandOneExactValueLowerBound, operandOneExactValueUpperBound, operandOneExactValueStep):
        #---------guide:::  find the boundaries for each exact values
        deviationUpperBound = int(maxOneDevPercentage*operandOneExactValue)
        deviationLowerBound = int(maxOneDevPercentage*operandOneExactValue)
        deviationStep =  int(deviationUpperBound/numberOfValuesBetweenExactAndDeviationOne)
        operandValueUpperBound = operandOneExactValue + deviationUpperBound
        operandValueLowerBound = operandOneExactValue - deviationLowerBound
        if (operandValueLowerBound < 0):
            operandValueLowerBound = 0
        
        #---------guide:::  go through the values within the radius of the deviation for each exact value
        for value in range(operandValueLowerBound, operandValueUpperBound, deviationStep):
            if not((operandOneExactValue, deviationUpperBound) in results.keys()):
                results[(operandOneExactValue, deviationUpperBound)] = [value]
            else:
                results[(operandOneExactValue, deviationUpperBound)] += [value]


    operandOneResults = copy.copy(results)
    results = {} 
    resultsPermutedDic = {}


    #---------guide:::  go through the exact values
    for  operandTwoExactValue in range(operandTwoExactValueLowerBound, operandTwoExactValueUpperBound, operandTwoExactValueStep):
        #---------guide:::  find the boundaries for each exact values
        deviationUpperBound = int(maxTwoDevPercentage*operandTwoExactValue)
        deviationLowerBound = int(maxTwoDevPercentage*operandTwoExactValue)
        deviationStep =  int(deviationUpperBound/numberOfValuesBetweenExactAndDeviationTwo)
        operandValueUpperBound = operandTwoExactValue + deviationUpperBound
        operandValueLowerBound = operandTwoExactValue - deviationLowerBound
        if (operandValueLowerBound < 0):
            operandValueLowerBound = 0
        
        #---------guide:::  go through the values within the radius of the deviation for each exact value
        for value in range(operandValueLowerBound, operandValueUpperBound, deviationStep):
            if not((operandTwoExactValue, deviationUpperBound) in results.keys()):
                results[(operandTwoExactValue, deviationUpperBound)] = [value]
            else:
                results[(operandTwoExactValue, deviationUpperBound)] += [value]


    operandTwoResults = copy.copy(results)

#    #---------guide::: permuting the results
    for key1 in operandOneResults.keys():
        for key2 in operandTwoResults.keys(): 
            beforePermutationList = [operandOneResults[key1], operandTwoResults[key2]]
            beforePermutationTuple = tuple(beforePermutationList) 
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

## 
# @brief this is the main function (which takes care of the description mentioned in the file description)
# 
# @return : no return
def main():
    #---------guide:::  promting ther user regarding the required input 
    print "the following inputs with the order mentioned needs to be provided"
    print "1.source folder address"
    print "2.source file address"
    print "3.generate Makefile (with YES or NO)"
    print "4.CBuilderFolder"
    print "***********"
    print "5.AllOperandScenariosInOneFiles" #whether all the operand scenarios can be found in one file or no
    print "6. AllOperandsFileOrDirectoryName" #the user should be providing a file name if AllOperandScenariosInOneFiles is true and a direcoty other   
    print "7. finalResulstFileName"
    #print "8. noiseRequirement"
    
   

    #---------guide:::  validating the number of inputs
    if len(sys.argv) < 8:
        print "***ERROR***"
        print "the following inputs with the order mentioned needs to be provided"
        print "the following inputs with the order mentioned needs to be provided"
        print "1.source folder address"
        print "2.source file address"
        print "3.generate Makefile (with YES or NO)"
        print "4.CBuilderFolder"
        print "***********"
        print "5.AllOperandScenariosInOneFiles" #whether all the operand scenarios can be found in one file or no
        print "6. AllOperandsFileOrDirectoryName" #the user should be providing a file name if AllOperandScenariosInOneFiles is true and a direcoty other   
        print "7. finalResulstFileName"
        #print "8. signalToNoiseRatio"
        exit()

    
   

    #---------guide:::  acquaring the inputs
    CSrcFolderAddress = sys.argv[1] #src file to be analyzet
    CSrcFileAddress = sys.argv[2] #src file to be analyzet
    #executableName = sys.argv[3] #src file to be analyzed
    generateMakeFile = sys.argv[3]
    rootFolder = sys.argv[4] 
    AllOperandScenariosInOneFiles = sys.argv[5]
    AllOperandsFileOrDirectoryName = sys.argv[6]
    finalResultFileName = sys.argv[7]
    #signalToNoiseRatio = float(sys.argv[8])
    
    
   
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
    #get the input to the executable 
    executableInputList = []
    print "please provide the inputs to the executable. when done, type type" 
    input = raw_input('provide the input: ')
    while (input != "done"):
        executableInputList.append(input)
        input = raw_input('provide the next input: ')
    
    #only the src file needs to be validated. The other inputs will be valideated in the lateer stages
    if not(os.path.isfile(CSrcFileAddress)):
        print "the file with the name: " + CSrcFileAddress + "which contains the csource file address does not exist"
        exit();
    
    #checking whether the file (or directory) containging the operands(input) exist or no
    if (AllOperandScenariosInOneFiles): #if a file
        if not(os.path.isfile(AllOperandsFileOrDirectoryName)):
                print "All OperandsFile does not exist"
                exit();
    else: #checking for the directory
        if not(os.path.isdir(AllOperandsFileOrDirectoryName)):
            print "All OperandsDir does not exist"
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
    AllOperandScenariosFullAddress = AllOperandsFileOrDirectoryName
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
    
    workWithNegativeNumbers = False 
    numberOfOperands = 2 
    operandExactValueLowerBound = 3 
    operandExactValueUpperBound = 7 
    operandExactValueStep = 3 
    maxInputOperandDeviation = .8
    numberOfValuesBetweenExactAndDeviation = 2
   
    #---------guide::: uncomment the following lines only if your want to use generateOperandListEachOperandUnique. This function is used in situations where we want the input to the operator to 
    #------------------have different properites (such as lowerBound, upperBound, etc)
#    operandTwoExactValueLowerBound = 400

#    operandTwoExactValueUpperBound = 600
#    operandTwoExactValueStep = 100 
#    maxInputOperandDeviationTwo = .2
#    numberOfValuesBetweenExactAndDeviationTwo = 5 
#    


    #operandDic = generateOperandListEachOperandUnique(numberOfOperands, operandExactValueLowerBound, operandExactValueUpperBound, maxInputOperandDeviation, workWithNegativeNumbers, operandExactValueStep, numberOfValuesBetweenExactAndDeviation, operandTwoExactValueLowerBound, operandTwoExactValueUpperBound, maxInputOperandDeviationTwo, operandTwoExactValueStep, numberOfValuesBetweenExactAndDeviationTwo)
    operandDic = generateOperandList(numberOfOperands, operandExactValueLowerBound, operandExactValueUpperBound, maxInputOperandDeviation, workWithNegativeNumbers, operandExactValueStep, numberOfValuesBetweenExactAndDeviation)
#    for  key in operandDic:
#        print "*********" 
#        print key 
#        print operandDic[key]
#

#    for key in operandDic.keys(): 
#        #operandList = [[2,4], [3,5]]
#        operandList = operandDic[key]
#        print key 
#        print operandList 
     
    numberOfKeys = len(operandDic.keys()) 
    firstTime = True 
    keyIndex = 0 
    OneTimeImplementationTime = 0 
    for key in operandDic.keys(): 
        if not(firstTime): 
            print "\n" 
            print "\ntime remaining: " + str((numberOfKeys - keyIndex)*OneTimeImplementationTime) + " second   " + " or " +  str(((numberOfKeys - keyIndex)*OneTimeImplementationTime)/60) + " in minute"
        else:
            timeBeforeFindingResults = datetime.datetime.now()

        #operandList = [[2,4], [3,5]]
        operandList = operandDic[key]
        
        for operandElement in operandList:
            if not(firstTime): 
                print ":::::::::::::::::::::::" 
                print OneTimeImplementationTime 
                print "\ntime remaining: " + str((numberOfKeys - keyIndex)*OneTimeImplementationTime) + " second   " + " or " +  str(((numberOfKeys - keyIndex)*OneTimeImplementationTime)/60) + " in minute"
                print ":::::::::::::::::::::::" 
            operand = ' '.join(str(e) for e in operandElement)
            
            #---------guide:::  write the operand in the operandFile
            writeOperandInOperandFile(operand, operandFileName)
            
            #clearly state where the new results associated with the new input starts 
            CSourceOutputForVariousSetUpFileName =  rootResultFolderName + "/" + settings.rawResultFolderName + "/" + settings.csourceOutputFileName + str('0') + ".txt" #where to collect C++ source results
            accurateValues = []
            noise.append([])
            config.append( [])
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

            #---------guide::: noise
            accurateValues = extractAccurateValues(CSourceOutputForVariousSetUpFileName)
            
            #---------guide:::  make a apx set up and get values associated with it
            while (True): #break when a signal is raised as done
                #---------guide:::  get a possible setUp
                status, setUp = generateAPossibleApxScenarios(rootResultFolderName + "/" + settings.AllPossibleApxOpScenarios, allPossibleApxScenarioursList , apxIndexSetUp,  "allPermutations")

                #---------guide:::  collect data
                configValue = polishSetup(setUp) #just to make it more readable
                inputFileNameListValue = [operandFileName] 

                #---------guide:::  erasing the previuos content of the file
                CSourceOutputForVariousSetUpP = open(CSourceOutputForVariousSetUpFileName, "w").close()

                #---------guide:::  modify the operator sample file
                modifyOperatorSampleFile(operatorSampleFileFullAddress, setUp)
                #---------guide:::  run the CSrouce file with the new setUp(operators)
                make_run(executableName, executableInputList, rootResultFolderName, CSourceOutputForVariousSetUpFileName, CBuildFolder, operandFileName)

                #---------guide::: noise
                noiseValue = [extractNoiseForOneInput(CSourceOutputForVariousSetUpFileName , accurateValues)]

                #---------guide:::  if havn't gotten the accurate value yet, the first value provided is. Thus, this value is the accurate value

                noise[operandIndex] += noiseValue
                config[operandIndex] +=configValue
                apxIndexSetUp +=1
                if (status == "done"):
                    break;

            #---------guide:::  collect the noise information
            operandInfoNoiseDic[operandIndex] = noise[operandIndex]
            #print operandInfoNoiseDic
            
            #---------guide:::  find the low and high bit that places the noise within the desired one
            upperBound, lowerBound = findApxBitRange(config[operandIndex], noise[operandIndex], desiredNoise)
            
            upperBoundList.append(upperBound)
            lowerBoundList.append(lowerBound)

            operandIndex += 1
        
        
        operandInfoApxBitsUpperBoundsDic[key] = min(upperBoundList)
        operandInfoApxBitsLowerBoundsDic[key] = max(lowerBoundList)
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
    
    
    print operandInfoApxBitsUpperBoundsDic
    print operandInfoApxBitsLowerBoundsDic
    
    print "***************"
    print upperBoundInputList
    print upperBoundOutputList
    return upperBoundInputList, upperBoundOutputList, lowerBoundInputList, lowerBoundInputList 
    
    #---------guide::: show the graph
    #plt.show() 



main()
