
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
from db_create_table_python_IP import *
from db_retrieve_table_python_IP import *

logFileAddress = "/home/polaris/behzad/apx_tool_chain/generated_text/" + settings.logFileName

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
def generateOperandListEachOperandUnique(numberOfOperands,
        operandOneExactValueLowerBound, operandOneExactValueUpperBound, maxOneDevPercentage, workWithNegativeNumbers, operandOneExactValueStep, numberOfValuesBetweenExactAndDeviationOne,  operandTwoExactValueLowerBound, operandTwoExactValueUpperBound, maxTwoDevPercentage, operandTwoExactValueStep, numberOfValuesBetweenExactAndDeviationTwo):
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


def characterize_all_operators(CSrcFolderAddress,
        CSrcFileAddress,generateMakeFile, rootFolder, finalResultFileName,
        operatorArchiveAddress,  percentageOfDataUsedForTraining,
        workWithNegativeNumbers, degreeNPolyMultiVarMinDegree,
        degreeNPolyMultiVarMaxDegree, signalToNoiseRatio,
        listOfOperandOneGenValues, listOfOperandTwoGenValues, moduleFunctionality):
    operandDicList = []
    lOfbestFittedFunc_degree_tuple = [] 
    funcCoeffList = []
    funcErrorDicList = [] 
    numberOfOperands = 2 
    rootResultFolderName = rootFolder + "/" + settings.generatedTextFolderName
    operandsInfoForOperatorCharacterizationFullAddress = rootFolder + "/" + settings.operandsInfoForOperatorCharacterizationName
    lAllOpsInSrcFile = [] 
    
    assert(os.path.isfile(CSrcFileAddress)), str(CSrcFileAddress) + " does not exist" 
    # CSrcFileAddress = originalCSrcFileAddress + "copy" 
    # shutil.copy(originalCSrcFileAddress, CSrcFileAddress) 
    sourceFileParse(CSrcFileAddress, lAllOpsInSrcFile)
   
    assert(len(lAllOpsInSrcFile) == len(listOfOperandOneGenValues)), "number of operators in the src file need to be the same as the number of GenValues for operandOne(or two)"
    lOfAcceptableModes = [ "all", "findLowUpBounery", "genOperandDicAndFindLowUpBounery", "genOperandDic","FindBestFittedCurve"]
    assert(moduleFunctionality in lOfAcceptableModes), str(moduleFunctionality) + " is not and acceptable mode"
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ 
    # ---- generating operands
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ 
    dbFileName = "operandDic.db"
    tableName = "operandDic" 
    propsType = ["int", "listTuple", "listList"]
    if (moduleFunctionality == "all" or moduleFunctionality == "genOperandDic"):
        for index,item in enumerate(lAllOpsInSrcFile):
            assert(item in ['MultiplicationOp', 'AdditionOp']), str(item) + " is not a valid operator" 
            operandOneExactValueLowerBound, operandOneExactValueUpperBound,operandOneExactValueStep, maxInputOperandDeviationOne, numberOfValuesBetweenExactAndDeviationOne = listOfOperandOneGenValues[index]
            operandTwoExactValueLowerBound, operandTwoExactValueUpperBound, operandTwoExactValueStep, maxInputOperandDeviationTwo, numberOfValuesBetweenExactAndDeviationTwo = listOfOperandTwoGenValues[index]
            # ---- generating the operand dictionary
            operandDic = generateOperandListEachOperandUnique(numberOfOperands, operandOneExactValueLowerBound, operandOneExactValueUpperBound, maxInputOperandDeviationOne, workWithNegativeNumbers, operandOneExactValueStep, numberOfValuesBetweenExactAndDeviationOne, operandTwoExactValueLowerBound, operandTwoExactValueUpperBound, maxInputOperandDeviationTwo, operandTwoExactValueStep, numberOfValuesBetweenExactAndDeviationTwo)
            operandDicList.append(operandDic) 
        print "operandDicList: " + str(operandDicList)
         
        # ---- writing operandDIc in a DB
        
        propsName = ["operandNumber", "operandGen", "LOfOperandCombo"]
        propList = [range(len(operandDicList)), [operandDic.keys() for operandDic in operandDicList], [operandDic.values() for operandDic in operandDicList]]
        
        # ---- body
        propsTypeConverted = [convert_python_types_to_sqlite(argType) for argType in propsType]
        propsValuesConverted = [convert_python_values_to_sqlite_compatible_values(argType,value) for argType,value in zip(propsType,propList)] 
        # ---- creating
        createDB(dbFileName, tableName, propsName, propsTypeConverted, propsValuesConverted)
        
       

    # ---- retreiving
    props, propNames, _= retrieveDB(dbFileName , tableName)
    operatorNumber,lOfOperandGens,lOfOperandCombo= [impose_type(propsType[index], prop) for index,prop in enumerate(props)]
    operandDicList = []
    for index in range(len(lOfOperandGens)):
        operandDicList.append(dict(zip(lOfOperandGens[index], lOfOperandCombo[index])))
    
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ 
    # ---- finding lower and upper bounds 
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ 
    dbFileName = "lowUpBoundery.db" 
    tableName = "lowUpBoundery"
    propsType = ["int", "listList", "listInt", "listList", "listInt" ]
    if (moduleFunctionality == "all" or moduleFunctionality == "findLowUpBounery"  or moduleFunctionality == "genOperandDicAndFindLowUpBounery"):
        reshapedUpperBoundInput = []
        reshapedLowerBoundInput = []
        upperBoundOutputList = []  
        lowerBoundOutputList = []  
        for index,item in enumerate(lAllOpsInSrcFile):
            assert(item in ['MultiplicationOp', 'AdditionOp']), str(item) + " is not a valid operator" 
            try:
                operatorAddress = operatorArchiveAddress + "/" + str(item) + ".cpp"
                shutil.copy(operatorAddress, CSrcFileAddress) 
            except IOError:
                print "*****************ERROR*********************" 
                print "can not copy " + str(operatorAddress) + " to " + str(CSrcFileAddress)
                exit()
            else: 
                # ---- probably can loop here
                reshapedUpperBoundInputTemp = [] #we need to reshape the input so it can be fed to curv_fit
                reshapedLowerBoundInputTemp = []
                upperBoundOutputTempList = [] 
                lowerBoundOutputTempList = [] 
                upperBoundInputList, upperBoundOutputTempList, lowerBoundInputList, lowerBoundOutputTempList = findLowAndUpBounderies(CSrcFolderAddress, CSrcFileAddress , generateMakeFile ,
                        finalResultFileName, rootFolder, operandDicList[index])
                upperBoundOutputList.append(upperBoundOutputTempList)
                lowerBoundOutputList.append(lowerBoundOutputTempList)
                # ---- reshaping and writing the boundery result
                for variableNumber in range(0, len(upperBoundInputList[0])):
                      reshapedUpperBoundInputTemp.append([])
                      for inputNumber in range(0, len(upperBoundInputList)):
                        reshapedUpperBoundInputTemp[variableNumber].append(upperBoundInputList[inputNumber][variableNumber])
                for variableNumber in range(0, len(lowerBoundInputList[0])):
                    reshapedLowerBoundInputTemp.append([])
                    for inputNumber in range(0, len(lowerBoundInputList)):
                        reshapedLowerBoundInputTemp[variableNumber].append(lowerBoundInputList[inputNumber][variableNumber])
                
                reshapedUpperBoundInput.append(reshapedUpperBoundInputTemp) #we need to reshape the input so it can be fed to curv_fit
                reshapedLowerBoundInput.append(reshapedLowerBoundInputTemp) #we need to reshape the input so it can be fed to curv_fit
                
            # ---- writing
            
        propsName = ["operatorNumber", "reshapedUpperBoundInput", "upperBoundOutputList", "reshapedLowerBoundInput", "lowerBoundOutputList"]
        propList = [range(len(reshapedUpperBoundInput)), reshapedUpperBoundInput, upperBoundOutputList, reshapedLowerBoundInput, lowerBoundOutputList]
        
        propsTypeConverted = [convert_python_types_to_sqlite(argType) for argType in propsType]
        propsValuesConverted = [convert_python_values_to_sqlite_compatible_values(argType,value) for argType,value in zip(propsType,propList)] 
       
        # ---- creating
        createDB(dbFileName, tableName, propsName, propsTypeConverted, propsValuesConverted)

    # ---- retreiving
    props, propNames, _= retrieveDB(dbFileName , tableName)
    operatorNumber, reshapedUpperBoundInput, upperBoundOutputList, reshapedLowerBoundInput, lowerBoundOutputList = [impose_type(propsType[index], prop) for index,prop in enumerate(props)]
    # print "lowerBoundOutputList : " + str(lowerBoundOutputList )
    # print "reshapedLowerBoundInput: " + str(reshapedLowerBoundInput)
    # print "upperBoundOutputList: " + str(upperBoundOutputList)
    # print "reshapedUpperBoundInput: " + str(reshapedUpperBoundInput)
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ 
    # ---- finding the best fitted graph
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ 
    dbFileName = "funcInfo.db" 
    tableName = "funcInfo"
    propsType = ["integer", "tuple", "listFloat"]
    if (moduleFunctionality == "all"  or moduleFunctionality =="FindBestFittedCurve"): 
        lOfbestFittedFunc_degree_tuple =[]
        funcCoeffList = []
        funcErrorDicList =[]
        for index,item in enumerate(lAllOpsInSrcFile):
            # reshapedUpperBoundInput, upperBoundOutputList, reshapedLowerBoundInput,
            # lowerBoundOutputList = parseLowUpBounderyFile(rootResultFolderName +
                    # "/" + settings.lowUpBounderyFileName, numberOfInputs)
            numberOfInputsForTraining = int(percentageOfDataUsedForTraining * len(reshapedUpperBoundInput[index][0]))
            
            upperValuesInputTrainingDataRaw =  [varValues[:numberOfInputsForTraining] for varValues in reshapedUpperBoundInput[index]]  
            print "upperValuesInputTrainingDataRaw : " + str(upperValuesInputTrainingDataRaw )
            upperValuesOutputTrainingData = [varValues[:numberOfInputsForTraining] for varValues in [upperBoundOutputList[index]]][0]
            print "upperValuesOutputTrainingData : " + str(upperValuesOutputTrainingData)
            upperValuesInputTestDataRaw = [varValues[numberOfInputsForTraining:] for varValues in reshapedUpperBoundInput[index]]  
            print "upperValuesInputTestDataRaw : " + str(upperValuesInputTestDataRaw )
            upperValuesOutputTestData = [varValues[numberOfInputsForTraining:] for varValues in [upperBoundOutputList[index]]][0]  
            print "upperValuesOutputTestData : " + str(upperValuesOutputTestData )
            
            lowerValuesInputTrainingDataRaw = [varValues[:numberOfInputsForTraining] for varValues in reshapedLowerBoundInput[index]]  
            print "lowerValuesInputTrainingDataRaw : " + str(lowerValuesInputTrainingDataRaw )
            lowerValuesOutputTrainingData = [varValues[:numberOfInputsForTraining] for varValues in [lowerBoundOutputList[index]]][0]
            print "lowerValuesOutputTrainingData : " + str(lowerValuesOutputTrainingData )
            lowerValuesInputTestDataRaw = [varValues[numberOfInputsForTraining:] for varValues in reshapedLowerBoundInput[index]]  
            print "lowerValuesInputTestDataRaw : " + str(lowerValuesInputTestDataRaw )
            lowerValuesOutputTestData = [varValues[numberOfInputsForTraining:] for varValues in [lowerBoundOutputList[index]]][0]
            print "lowerValuesOutputTestData : " + str(lowerValuesOutputTestData )

             
            minDegree = degreeNPolyMultiVarMinDegree
            maxDegree = degreeNPolyMultiVarMaxDegree
            
            maximumAcceptableError = (1 - signalToNoiseRatio)*numpy.float64(sum(upperValuesOutputTestData)/len(upperValuesOutputTestData))
            bestFittedFunc, funcCoeff, funcErrorDic = findBestFitFunction(upperValuesInputTrainingDataRaw, upperValuesOutputTrainingData, upperValuesInputTestDataRaw, upperValuesOutputTestData, all_funcs.funcNumberOfCoeffDic,maxDegree, minDegree, maximumAcceptableError)
            lOfbestFittedFunc_degree_tuple.append(str((bestFittedFunc[0].__name__, bestFittedFunc[1])))
            funcCoeffList.append(funcCoeff)
            funcErrorDicList.append(funcErrorDic)

        # ---- writing the results in a DB file
        propsName = ["opNumber", "funcName", "funcCoeff"]
        propList = [range(len(lOfbestFittedFunc_degree_tuple)),lOfbestFittedFunc_degree_tuple, [list(arrayElement) for arrayElement in funcCoeffList]]
        propsTypeConverted = [convert_python_types_to_sqlite(argType) for argType in propsType]
        propsValuesConverted = [convert_python_values_to_sqlite_compatible_values(argType,value) for argType,value in zip(propsType,propList)] 
        # ---- creating
        createDB(dbFileName, tableName, propsName, propsTypeConverted, propsValuesConverted)
       
    # lOfFunc_degree_tuple = [] #contains the (func, degree) tuple
    # props, propNames, _= retrieveDB("funcInfo.db" , "funcInfo")
    # propsName = ["opNumber", "funcName", "funcCoeff"]
    # propsType = ["int"] +["tuple"] + ["listFloat"] 
    # props, propNames, _= retrieveDB(dbFileName , tableName)
    # lOfOpNumber, lOffuncName_degree_tuple, lOfFuncCoeff = [impose_type(propsType[index], prop) for index,prop in enumerate(props)]
    # print lOfOpNumber
    # print lOffuncName_degree_tuple
    # print lOfFuncCoeff
    # print funcErrorDicList 
    return lOfbestFittedFunc_degree_tuple, funcCoeffList, funcErrorDicList

        # stringToWrite =  " ".join(str(e) for e in funcCoeff)
        # operatorsCoeffFileP.write("coeffs: \n")
        # operatorsCoeffFileP.write(stringToWrite + " \n")
        # operatorsCoeffFileP.write("functionError: \n")
        # operatorsCoeffFileP.write(str(funcErrorDic[bestFittedFunc]))
        # sys.exit()


    # characterizeOperator(CSrcFolderAddress, CSrcFileAddress, generateMakeFile, rootFolder, finalResultFileName, moduleFunctionality, percentageOfDataUsedForTraining)
    # operatorsCoeffFileP.close() 
    # print funcCoeff
    #
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# test2 = True
test2 = False
if (test2):
    home = expanduser("~") 
    originalCSrcFileAddress = home + "/apx_tool_chain/CSrc_examples/simple_dfg_2_operator.cpp"
    assert(os.path.isfile(originalCSrcFileAddress)), str(originalCSrcFileAddress) + " does not exist" 
    
    CSrcFolderAddress =  home + "/apx_tool_chain/src/CSrc/"
    CSrcFileAddress = home + "/apx_tool_chain/src/CSrc/test.cpp"
    # ---- copying because characterize_operators will modify the source file that it uses
    # ---- thus we keep the original file somewhere else and copy it over
    shutil.copy(originalCSrcFileAddress, CSrcFileAddress) 
    
    generateMakeFile = "YES"
    rootFolder  = home +  "/apx_tool_chain"
    finalResultFileName =  "finalResult2.txt"
    
    lOfAcceptableModes = [ "all", "findLowUpBounery", "genOperandDicAndFindLowUpBounery", "genOperandDic","FindBestFittedCurve"]
    moduleFunctionality = "all"
    # moduleFunctionality = "genOperandDic"
    # moduleFunctionality = "findLowUpBounery" 
    # moduleFunctionality = "genOperandDicAndFindLowUpBounery"
    # moduleFunctionality = "FindBestFittedCurve"
    percentageOfDataUsedForTraining = .7
    workWithNegativeNumbers = False
    numberOfOperands = 2 
    signalToNoiseRatio = .1
    degreeNPolyMultiVarMinDegree = 1 
    degreeNPolyMultiVarMaxDegree = 3
    # ---- prepare inputs for operand generation and write in a table
    write_operands_info_for_operator_characterization()
    # ---- retrieve the infr from the table above
    listOfOperandOneGenValues, listOfOperandTwoGenValues = retrieve_operands_info_for_operator_characterization()
    operatorArchiveAddress = home + "/apx_tool_chain/operator_archive"
    characterize_all_operators(CSrcFolderAddress, CSrcFileAddress, generateMakeFile,
            rootFolder, finalResultFileName, operatorArchiveAddress,  percentageOfDataUsedForTraining,
            workWithNegativeNumbers, degreeNPolyMultiVarMinDegree,
            degreeNPolyMultiVarMaxDegree, signalToNoiseRatio,
            listOfOperandOneGenValues, listOfOperandTwoGenValues, moduleFunctionality)
    

    # # ---- retievig the data from the dbfile
    # lOfFunc_degree_tuple = [] #contains the (func, degree) tuple
    # props, propNames, _= retrieveDB("funcInfo.db" , "funcInfo")
    # propsName = ["opNumber", "funcName", "funcCoeff"]
    # propsType = ["int"] +["tuple"] + ["listFloat"] 
    # # props, propNames, _= retrieveDB(dbFileName , tableName)
    # lOfOpNumber, lOffuncName_degree_tuple, lOfFuncCoeff = [impose_type(propsType[index], prop) for index,prop in enumerate(props)]
    
    # print "last round" 
    # print lOfOpNumber
    # print lOffuncName_degree_tuple
    # print lOfFuncCoeff

    # for funcName_degree_tuple_string_tuple in lOffuncName_degree_string_tuple: 
        # lOfFunc_degree_tuple.append(tuple((eval(eval(funcName_degree_tuple_string_tuple)[0]), eval(funcName_degree_tuple_string_tuple)[1])))
    
    # print lOfFunc_degree_tuple
    
   
