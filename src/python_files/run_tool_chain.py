
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
    print "8. noiseRequirement"
    
   

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
        print "8. noiseRequirement"
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
    noiseRequirement = sys.argv[8]
    
    
   
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
    inputNumber = 0 
    os.system("rm -r" + " " +  rootResultFolderName + "/" +settings.AllOperandsFolderName)
    os.system("rm -r" + " " +  rootResultFolderName + "/" + settings.rawResultFolderName)
    os.system("mkdir" + " " + rootResultFolderName + "/" + settings.rawResultFolderName)
    
    #---------guide:::  if the operands were all given in a file: separate them to different files
    #...................else: use the folder that they are in, as an input to the C source files
    #if all in one file 
    if (AllOperandScenariosInOneFiles):
        #check for error 
        if not(os.path.isfile(AllOperandScenariosFullAddress)):
            print AllOperandScenariosFullAddress + " does not exist"
            exit();

        #make a directory for all operand inputs 
        AllOperandsFolderName = rootResultFolderName + "/" + "all_operands_folder"
        os.system("mkdir " + AllOperandsFolderName)
        #---------guide::: separates operands and put in a folder 
        with open(AllOperandScenariosFullAddress) as f:
            for line in f:
                if len(line.split())>0: 
                    fileToWriteName = AllOperandsFolderName + "/" + str(inputNumber) +".txt"
                    fileToWriteP = open(fileToWriteName ,"w");  
                    fileToWriteP.write(line)
                    fileToWriteP.close()
                    inputNumber +=1
    else: #this case is the case in which they are in a foler already ready
        if not(os.path.isdir(AllOperandScenariosFullAddress)):
            print "***********************ERRROR**************" 
            print "the folder that is told to contain the operands does not exist: " + AllOperandsFolderName
            exit();
        else: 
            AllOperandsFolderName = AllOperandsFileOrDirectoryName

    
    
    
    #---------guide:::   parse the C source file to collect all the operands that can 
    #                        be approximatable
    lAllOpsInSrcFile = [] 
    sourceFileParse(CSrcFileAddress, lAllOpsInSrcFile)
    
    
    settings.totalNumberOfOpCombinations = 1;
    energy = []
    noise = []
    config = []
    inputFileNameList = []
    
    #---------guide:::  sampling operands
    inputNumber = 0 
    nameOfAllOperandFilesList = getNameOfFilesInAFolder(AllOperandsFolderName)
    operandIndex = 0
    
    
   
    #---------guide:::  generate a list of all possible cases for each operator
    allPossibleScenariosForEachOperator = generateAllPossibleScenariosForEachOperator(rootResultFolderName, lAllOpsInSrcFile)
    #---------guide:::  generate all possible apx setUps Possible (mainly used for full permutation design exploration, otherwise called exhustive search)
    allPossibleApxScenarioursList = generateAllPossibleApxScenariousList(allPossibleScenariosForEachOperator)
    
    #---------guide::: go through operand files and sweep the apx space
    for operandSampleFileName in nameOfAllOperandFilesList:
        countSoFar = 0 
        #clearly state where the new results associated with the new input starts 
        CSourceOutputForVariousSetUpFileName =  rootResultFolderName + "/" + settings.rawResultFolderName + "/" + settings.csourceOutputFileName + str(inputNumber) + ".txt" #where to collect C++ source results
        accurateValues = []
        noise.append([])
        energy.append( [])
        config.append( [])
        inputFileNameList.append([])
        #mode = "allPermutations" 
        mode = "simulated_annealing" 
        operatorSampleFileFullAddress = rootResultFolderName + "/" + settings.operatorSampleFileName
        
        
        #---------guide:::  getting accurate values associated with the CSource output
        apxIndexSetUp = 0 #zero is associated with the accurate results (this is a contract that needs to be obeyed)
        status, setUp = generateAPossibleApxScenarios(rootResultFolderName + "/" + settings.AllPossibleApxOpScenarios, allPossibleApxScenarioursList , apxIndexSetUp, mode) 
        
        #---------guide:::  erasing the previuos content of the file
        CSourceOutputForVariousSetUpP = open(CSourceOutputForVariousSetUpFileName, "w").close()
        #---------guide:::  modify the operator sample file
        modifyOperatorSampleFile(operatorSampleFileFullAddress, setUp)
        #---------guide:::  run the CSrouce file with the new setUp(operators)
        make_run(executableName, executableInputList, rootResultFolderName, CSourceOutputForVariousSetUpFileName, CBuildFolder, operandSampleFileName)

        #---------guide::: noise
        accurateValues = extractAccurateValues(CSourceOutputForVariousSetUpFileName)

            #---------guide:::  make a apx set up and get values associated with it
        if (mode == "allPermutations"): 
            while (True): #break when a signal is raised as done
                #---------guide:::  get a possible setUp
                status, setUp = generateAPossibleApxScenarios(rootResultFolderName + "/" + settings.AllPossibleApxOpScenarios, allPossibleApxScenarioursList , apxIndexSetUp, mode) 

                #---------guide:::  collect data
                energyValue = [calculateEnergy(map(getFirstTwo, setUp))]
                configValue = polishSetup(setUp) #just to make it more readable
                inputFileNameListValue = [operandSampleFileName] 

                #---------guide:::  erasing the previuos content of the file
                CSourceOutputForVariousSetUpP = open(CSourceOutputForVariousSetUpFileName, "w").close()

                #---------guide:::  modify the operator sample file
                modifyOperatorSampleFile(operatorSampleFileFullAddress, setUp)
                #---------guide:::  run the CSrouce file with the new setUp(operators)
                make_run(executableName, executableInputList, rootResultFolderName, CSourceOutputForVariousSetUpFileName, CBuildFolder, operandSampleFileName)

                #---------guide::: noise
                noiseValue = [extractNoiseForOneInput(CSourceOutputForVariousSetUpFileName , accurateValues)]

                #---------guide:::  if havn't gotten the accurate value yet, the first value provided is. Thus, this value is the accurate value

                noise[operandIndex] += noiseValue

                energy[operandIndex] += energyValue
                config[operandIndex] +=configValue
                inputFileNameList[operandIndex] +=inputFileNameListValue
                apxIndexSetUp +=1
                if (status == "done"):
                    break;

            operandIndex += 1
            inputNumber +=1
#	    
        elif (mode == "simulated_annealing"):
            simulatedAnnelaingResult  = [] #result of running the simulatedAnnealing()
            initialSetUpIndex = random.choice(range(0, len(allPossibleApxScenarioursList)))
            print "initialSetUpIndex: " +  str(allPossibleApxScenarioursList[initialSetUpIndex])
            initialSetUp = allPossibleApxScenarioursList[initialSetUpIndex] 
            stepSize = .05  #
            initialTemperature = 1
            simulatedAnnelaingResult = simulatedAnnealing(initialSetUp, noiseRequirement, initialTemperature, stepSize, operatorSampleFileFullAddress,executableName, executableInputList, rootResultFolderName, CSourceOutputForVariousSetUpFileName, CBuildFolder, operandSampleFileName, accurateValues)
            print simulatedAnnelaingResult 
            sys.exit()


    
    
    #---------guide:::  find the pareto points and store them in resultTuple
    resultTuple = [] #this is a list of pareto Triplets(setup, noise, energy) associated with each 
                       #one of the inputs 
    #setting up the resultTupleList with the right length 
    for i in range(0, len(noise),1):
        resultTuple.append([])
   

    symbolsToChooseFrom = ['*', 'x', "o", "+", "*", "-", "^"] #symbols to draw the plots with
    symbolsCollected = [] #this list contains the symbols collected for every new input 
    #---------guide:::  get the noise for each input
    for i in range(0, len(noise), 1):
        paretoNoise = []  #cleaning the previous values if exist
        paretoEnergy = [] #cleaning the previous values if exist         
        #---------guide:::  get the pareto set
        paretoNoise, paretoEnergy = pareto_frontier(noise[i], energy[i], maxX= False, maxY = False)
        #---------guide:::  find the setUps that corresponds to the pareto Points
        setUpNumberList = [] #contains the list of setUp numbers associated with the pareto set 
                             #this is used to avoid duplicate
        for j in range(0, len(paretoNoise), 1):
            pair =  (paretoNoise[j], paretoEnergy[j]) #pair to look for
            setUpNumber = findPosition(pair, noise[i], energy[i], setUpNumberList)
            setUpNumberList.append(setUpNumber) 
            #---------guide:::  the reason that we are provided with a list is that it is possible
            #to find the pair (noise,energy) in multiple setUps (configurations)
            resultTuple[i].append((setUpNumber,config[i][setUpNumber], paretoNoise[j], paretoEnergy[j]))
        
        #---------guide:::  generate pareto graph
        generateGraph(paretoNoise,paretoEnergy, "Noise", "Energy", symbolsToChooseFrom[i%len(symbolsToChooseFrom)])
        symbolsCollected.append(symbolsToChooseFrom[i%len(symbolsToChooseFrom)])
         
      
    #---------guide:::  writing the result back
    finalResultFileFullAddress = rootResultFolderName + "/" + finalResultFileName
    #---------guide:::  writing the result in human readable format to a file
    writeReadableOutput(resultTuple, inputFileNameList, symbolsCollected, finalResultFileFullAddress)
    pylab.savefig(finalResultFileFullAddress[:-4]+".png") #saving the figure generated by generateGraph
    
    #---------guide:::  getting back up of the results
    folderToCopyToNameProcessed = comeUpWithNewFolderNameAccordingly(rootFolder + "/" + settings.resultsBackups) 
    listOfFoldersToCopyFrom = [rootResultFolderName, CSrcFolderAddress]  
    generateBackup(rootResultFolderBackupName, listOfFoldersToCopyFrom, folderToCopyToNameProcessed) #generating a back of the results

    cleanUpExtras(rootResultFolderName) 
    #---------guide::: show the graph
    #plt.show() 



main()
