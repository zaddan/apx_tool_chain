
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


#**--------------------**
#**--------------------**
#----disclaimers::: if dealingwith Pic and we are feeding couple of operands,
#----we need to collect their psnr in a list and get an avg. This should be done
#--- this requries adding a PSNR (or SNR) list to the points
#---
#--- for both SNR and PSNR, not sure how to deal with it when the error is zero.
#----right now, I set the SNR to the avg of accurate values and not show it in the graph
#----but for PSNR, i set the error to something very very small
#**--------------------**
#--------------------**



import pickle
import copy
import pylab
import sys
import os

from extract_unique_noise import *
from inputs import *#this file contains all the inputs
from genetic_algorithm import *
from deap import algorithms
from points_class import *
from deap import base
from deap import creator
from deap import tools
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
from points_class import *
#from pareto_set_class import *
from point_set_class import *

def polishSetup(setUp):
    result = []  
    for element in setUp: 
        resultElement = ' '.join(str(e) for e in element) 
        result.append(resultElement)
    return [result] 



def generate_snr_energy_graph(dealingWithPics, lOfPoints, plotPareto, symbolsToChooseFrom, lOfAccurateValues, symbolIndex, maxY, maxX):
    symbolsCollected = [] 
    lOfPoints_refined =[]
    if plotPareto:
        lOfPoints_refined = pareto_frontier(lOfPoints,maxX, maxY); 
    else:
        lOfPoints_refined = lOfPoints 
    if(eval(dealingWithPics)): 
        lOfPSNR = [] 
        lOfEnergy = [] 
        for point in lOfPoints_refined:
            if point.get_PSNR() != avgAccurateValue:
                lOfSNR.append(point.get_PSNR())
                lOfEnergy.append(point.get_energy())
        generateGraph(lOfPSNR,lOfEnergy, "PSNR", "Energy", symbolsToChooseFrom[symbolIndex])
        symbolsCollected.append(symbolsToChooseFrom[symbolIndex]) 
    else:
        avgAccurateValue =  numpy.mean(map(lambda x: sum(map (lambda y: float(y), x))/len(x), lOfAccurateValues))
        lOfSNR = [] 
        lOfEnergy = [] 
        for point in lOfPoints_refined:
            if point.get_SNR() != avgAccurateValue:
                lOfSNR.append(point.get_SNR())
                lOfEnergy.append(point.get_energy())
        
        symbolsCollected.append(symbolsToChooseFrom[symbolIndex]) 
        print "List of SNR: " + str(lOfSNR)
        generateGraph(lOfSNR,lOfEnergy, "SNR", "Energy", symbolsToChooseFrom[symbolIndex])
    return symbolsCollected

def getLimitedList(src):
    with open(src) as f:
        opListSlectedIndex = [] 
        counter = 0 
        for line in f:
            if counter == 0: 
                for i in line.split():
                    opListSlectedIndex.append([])
            counter +=1 
            if len(line.split())>0: 
                for opIndex in range(opListSlectedIndex):
                    opListSlectedIndex[opIndex].append(line.split(opIndex))

    return opListSlectedIndex
## 
# @brief this is the main function (which takes care of the description mentioned in the file description)
# 
# @return : no return
def main():
    #---------guide:::  promting ther user regarding the required input
    print "the following inputs needs to be provided in the " + str(settings.userInputFile)
    print "1.source folder address"
    print "2.source file address"
    print "3.generate Makefile (with YES or NO)"
    print "4.CBuilderFolder"
    print "***********"
    print "5.AllInputScenariosInOneFile" #whether all the operand scenarios can be found in one file or no
    print "6. AllInputFileOrDirectoryName" #the user should be providing a file name if AllInputScenariosInOneFile is true and a direcoty other   
    print "7. finalResulstFileName"
    #print "8. errorRequirement"
    
   
    #---------guide:::  validating the number of inputs
    # if len(sys.argv) < 9:
        # print "***ERROR***"
        # print "the following inputs with the order mentioned needs to be provided"
        # print "the following inputs with the order mentioned needs to be provided"
        # print "1.source folder address"
        # print "2.source file address"
        # print "3.generate Makefile (with YES or NO)"
        # print "4.CBuilderFolder"
        # print "***********"
        # print "5.AllInputScenariosInOneFile" #whether all the operand scenarios can be found in one file or no
        # print "6. AllInputFileOrDirectoryName" #the user should be providing a file name if AllInputScenariosInOneFile is true and a direcoty other   
        # print "7. finalResulstFileName"
        # print "8. pickled_file"
        # #print "8. errorToSignalRatio"
        # exit()

    inputObj = inputClass()
    inputObj.expandAddress()
    maxX = settings.maxX
    maxY = settings.maxY

    # print inputObj.allInputs
    # sys.exit() 
   #  home = expanduser("~")
    # #---------guide:::  acquaring the inputs
    # for index, element in enumerate(sys.argv):
        # if element.split("/")[0] == "~":
            # sys.argv[index] = home + sys.argv[index][1:]

    # CSrcFolderAddress = sys.argv[1] #src file to be analyzet
    
    # # CSrcFileAddress = sys.argv[2] #src file to be analyzet
    # lOfCSrcFileAddress = inputs.lOfCSrcFileAddress 
    # #executableName = sys.argv[3] #src file to be analyzed
    # generateMakeFile = sys.argv[3]
    # rootFolder = sys.argv[4] 
    # AllInputScenariosInOneFile = sys.argv[5]
    # AllInputFileOrDirectoryName = sys.argv[6]
    # finalResultFileName = sys.argv[7]
    # PIK = sys.argv[8]  
    #errorToSignalRatio = float(sys.argv[8])
    
    opIndexSelectedFile =settings.opIndexSelectedFile
    open(opIndexSelectedFile, "w").close()
    
    CSrcFolderAddress = inputObj.CSrcFolderAddress
    lOfCSrcFileAddress = inputObj.lOfCSrcFileAddress 
    generateMakeFile = inputObj.generateMakeFile
    rootFolder = inputObj.rootFolder 
    AllInputScenariosInOneFile = inputObj.AllInputScenariosInOneFile
    AllInputFileOrDirectoryName = inputObj.AllInputFileOrDirectoryName 
    finalResultFileName = inputObj.finalResultFileName
    PIK = inputObj.PIK
    lOfInputs = []   #for debugging purposes
    lOfInputs += [CSrcFolderAddress, lOfCSrcFileAddress, generateMakeFile, rootFolder, AllInputScenariosInOneFile , AllInputFileOrDirectoryName, finalResultFileName, PIK ]
    bench_suit_name = inputObj.bench_suit_name; 
    assert(len(lOfInputs) == 8) 
    
    #---------guide:::  checking the validity of the input and making necessary files
    #and folders
    rootResultFolderName = rootFolder + "/" + settings.generatedTextFolderName
    rootResultFolderBackupName =  rootFolder + "/" + settings.resultsBackups # is used to get a back up of the results generated in the previuos run of this program
    if not(os.path.isdir(rootResultFolderBackupName)):
        os.system("mkdir" + " " + rootResultFolderBackupName)
    os.system("rm -r " + rootResultFolderName)
    os.system("mkdir " + rootResultFolderName)
    executableName = "tool_exe" #src file to be analyzed
    CBuildFolder = rootFolder + "/" + CBuildFolderName
    #get the input to the executable 
    executableInputList = []
    
    
    # print "please provide the inputs to the executable. when done, type type" 
    # input = raw_input('provide the input: ')
    # while (input != "done"):
        # executableInputList.append(input)
        # input = raw_input('provide the next input: ')
    
   
    #checking whether the file (or directory) containging the operands(input) exist or no
    if (AllInputScenariosInOneFile): #if a file
        #print AllInputFileOrDirectoryName
        if not(os.path.isfile(AllInputFileOrDirectoryName)):
            print "All OperandsFile:" + AllInputFileOrDirectoryName + " does not exist"
            exit();
    else: #checking for the directory
        if not(os.path.isdir(AllInputFileOrDirectoryName)):
            print "All OperandsDir does not exist"
            exit();

    #---------guide:::  generate make file or no
    if not((generateMakeFile == "YES") or (generateMakeFile == "NO")): 
        #print generateMakeFile 
        print "generateMakeFile can only take YES or NO value (capital letters)"
        exit()

    #removing the result file
    os.system("rm " + rootResultFolderName + "/" + settings.rawresultFileName)

    
    #---if make file needs to be re generated (generated) 
    if (generateMakeFile == "YES"): 
        currentDir = os.getcwd() #getting the current directory
        #CBuildFolder = "./../../" 
        os.chdir(rootFolder) #chaning the directory
        # os.system("cp CMakeLists_tool_chain.txt CMakeLists.txt") #restoring the correct CMakeLists.txt file
        os.chdir(currentDir) 
        #generate the makefile using CMAKE 
        print "**********************************************************************"
        print "******************************GENERATING MAKE FILE********************"
        print "**********************************************************************"
        currentDir = os.getcwd() #getting the current directory
        if not(os.path.isdir(CBuildFolder)):
            os.system("mkdir " + CBuildFolder); #making a new one
        os.chdir(CBuildFolder) #chaning the directory
        # os.system("export CC=clang++; export CXX=clang++") 
        os.environ["CC"] = "clag++";
        os.environ["CXX"] = "clag++";
        os.system("cmake ..");
        print "**********************************************************************"
        print "done generating the makeFile using CMake"
        print "**********************************************************************"
        
        os.chdir(currentDir) #chaning the directory
        #done generating the make file 

    
    #---------guide:::  removing the results associated with the previous runs
    AllOperandScenariosFullAddress = AllInputFileOrDirectoryName
    inputNumber = 0 
    #os.system("rm -r" + " " +  rootResultFolderName + "/" +settings.AllOperandsFolderName)
    #os.system("rm -r" + " " +  rootResultFolderName + "/" + settings.rawResultFolderName)
    os.system("mkdir" + " " + rootResultFolderName + "/" + settings.rawResultFolderName)
    #---------guide:::  if the operands were all given in a file: separate them to different files
    #...................else: use the folder that they are in, as an input to the C source files
    #if all in one file 
    if (AllInputScenariosInOneFile):
        #check for error 
        if not(os.path.isfile(AllOperandScenariosFullAddress)):
            print AllOperandScenariosFullAddress + " does not exist"
            exit();

        #make a directory for all operand inputs 
        AllOperandsFolderName = rootResultFolderName + "/" + settings.AllOperandsFolderName
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
            AllOperandsFolderName = AllInputFileOrDirectoryName

    
    
    
                                                 #inputs. This means that we have multiple operand sets)
    #---------guide:::   parse the C source file to collect all the operands that can 
    #                        be approximatable
    lAllOpsInSrcFile = [] 
    for CSrcFileAddressItem in lOfCSrcFileAddress:
        lAllOpsInSrcFile += sourceFileParse(CSrcFileAddressItem)
    settings.totalNumberOfOpCombinations = 1;
    energy = []
    error = []
    config = []
    inputFileNameList = []
    
    #---------guide:::  sampling operands
    inputNumber = 0 
    nameOfAllOperandFilesList = getNameOfFilesInAFolder(AllOperandsFolderName)
    operandIndex = 0
    
    numberOfTriesList = [] 
    numberOfSuccessfulTriesList = []
    errorRequirementList = []
    errorDiffList =[] #contains the difference between the error request and the error recieved from simulated annealing ( in percentage)
     
    allPossibleScenariosForEachOperator, limitedListIndecies, ignoreListIndecies, accurateSetUp = generateAllPossibleScenariosForEachOperator(rootResultFolderName, lAllOpsInSrcFile)
    #---------guide:::  generate all possible apx setUps Possible (mainly used for full permutation design exploration, otherwise called exhustive search)
    IOAndProcessCharFileName = rootResultFolderName + "/" + settings.IOAndProcessCharFileName
    IOAndProcessCharP = open(IOAndProcessCharFileName, "w")
    
    open(settings.annealerProgressionOutputFileName, "w").close()
    open(rootResultFolderName +  "/" + settings.annealerOutputFileName, "w").close()
    
    #---------guide::: go through operand files and sweep the apx space
    # lOfOperandSet = [] 
    timeBeforeFindingResults = datetime.datetime.now()
    lOfAccurateValues = []
    for inputNumber,operandSampleFileName in enumerate(nameOfAllOperandFilesList):
        countSoFar = 0 
        #clearly state where the new results associated with the new input starts 
        CSourceOutputForVariousSetUpFileName =  rootResultFolderName + "/" + settings.rawResultFolderName + "/" + settings.csourceOutputFileName + str(inputNumber) + ".txt" #where to collect C++ source results
        # newOperand =  operandSet(get_operand_values(operandSampleFileName))
        accurateValues = []
        error.append([])
        energy.append( [])
        config.append( [])
        inputFileNameList.append([])
        mode = settings.mode 
        operatorSampleFileFullAddress = rootResultFolderName + "/"+ settings.operatorSampleFileName
        
        
        #---------guide:::  getting accurate values associated with the CSource output
        #accurateSetUp,workingList = generateAccurateScenario(allPossibleScenariosForEachOperator,ignoreListIndecies )
        workingList = generateWorkingList(ignoreListIndecies, allPossibleScenariosForEachOperator )
        
        apxIndexSetUp = 0 #zero is associated with the accurate results (this is a contract that needs to be obeyed)
        # status, setUp = generateAPossibleApxScenarios(rootResultFolderName + "/" + settings.AllPossibleApxOpScenarios, allPossibleApxScenarioursList , apxIndexSetUp, mode) 
        #---------guide:::  erasing the previuos content of the file
        CSourceOutputForVariousSetUpP = open(CSourceOutputForVariousSetUpFileName, "w").close()
        #---------guide:::  modify the operator sample file
        modifyOperatorSampleFile(operatorSampleFileFullAddress, accurateSetUp)
        
        
        #---------guide:::  run the CSrouce file with the new setUp(operators)
        make_run(executableName, executableInputList, rootResultFolderName, CSourceOutputForVariousSetUpFileName, CBuildFolder, operandSampleFileName, bench_suit_name)
        
        #---------guide::: error
        accurateValues = extractAccurateValues(CSourceOutputForVariousSetUpFileName)
        assert(accurateValues != None)
        print "-------------" 
        lOfAccurateValues.append(accurateValues)
        # print lOfAccurateValues
        # lOfOperandSet.append(newOperand)
        #---------guide:::  make a apx set up and get values associated with it
        
    lOfPoints = []  
    if (mode == "allPermutations"): 
        lengthSoFar = 0 
        
        """ ---- guide: making sure that it is possible to use permuation
                 if the number of permutations are too big to be held in memoery
                 we error out """
        for opOptions in allPossibleScenariosForEachOperator:
            lengthSoFar += len(opOptions)
            assert(lengthSoFar < settings.veryHugeNumber), """numbr of permuations is too big. 
            it is bigger that """ + str(settings.veryHugeNumber)

        allPossibleApxScenarioursList = generateAllPossibleApxScenariousList(allPossibleScenariosForEachOperator)
        while (True): #break when a signal is raised as done
            newPoint = points()
            status, setUp = generateAPossibleApxScenarios(rootResultFolderName + "/" + settings.AllPossibleApxOpScenarios, allPossibleApxScenarioursList , apxIndexSetUp, mode) 
            for operandIndex, operandSampleFileName in enumerate(nameOfAllOperandFilesList):
                print "\n" + str(100*float(apxIndexSetUp)/len(allPossibleApxScenarioursList)) + "% done" 
                energyValue = [calculateEnergy(map(getFirstTwo, setUp))]
                configValue = polishSetup(setUp) #just to make it more readable
                inputFileNameListValue = [operandSampleFileName] 
                CSourceOutputForVariousSetUpP = open(CSourceOutputForVariousSetUpFileName, "w").close()
                modifyOperatorSampleFile(operatorSampleFileFullAddress, setUp)
                make_run(executableName, executableInputList, rootResultFolderName, CSourceOutputForVariousSetUpFileName, CBuildFolder, operandSampleFileName, bench_suit_name)
                errorValue = [extractErrorForOneInput(CSourceOutputForVariousSetUpFileName , lOfAccurateValues[operandIndex])]
                rawValues = [extractCurrentValuesForOneInput(CSourceOutputForVariousSetUpFileName)]
                
                sys.exit(0) 
                newPoint.append_raw_values(rawValues[0])  
                newPoint.append_error(errorValue[0])
                newPoint.set_energy(energyValue[0])
                setUpPolished =[] 
                for setUpElement in configValue[0]:
                    setUpEelementPolished = [] 
                    for index, setUpSubEl in enumerate(setUpElement.split()):
                        if index != 0:
                            setUpEelementPolished.append(float(setUpSubEl))
                        else:
                            setUpEelementPolished.append(setUpSubEl)
                    setUpPolished.append(setUpEelementPolished)
                # newPoint.set_setUp(configValue[0].)
                
                newPoint.set_setUp(setUpPolished)
                newPoint.set_setUp_number(apxIndexSetUp)
                #print configValue[0] 
                #print newPoint.get_setUp()
                newPoint.append_lOf_operand(get_operand_values(operandSampleFileName))
                newPoint.append_accurate_values(lOfAccurateValues[operandIndex])
                newPoint.set_dealing_with_pics(eval(inputObj.dealingWithPics))
                newPoint.set_input_obj(inputObj)
                # newPoint.calculate_SNR()
                if eval(inputObj.dealingWithPics): 
                    newPoint.calculate_PSNR()
                inputFileNameList[operandIndex] += inputFileNameListValue
                lOfPoints.append(newPoint)
          
             
            if not(eval(inputObj.dealingWithPics)): 
                newPoint.calculate_SNR()
            apxIndexSetUp += 1  
            if (status == "done"):
                break;
 
    elif (mode == "genetic_algorithm"):
        allConfs = [] #first generation
        # remainingPopulation = allPossibleApxScenarioursList[:]
        # numberOfIndividualsToStartWith = min(settings.numberOfIndividualsToStartWith, len(allPossibleApxScenarioursList)) 
        numberOfIndividualsToStartWith = settings.numberOfIndividualsToStartWith
        tempAcc = accurateSetUp
        # tempAcc[8][2] = 5
        opIndexSelectedFile  = settings.opIndexSelectedFile
        limitedList = [] 
        limitedListValues = getLimitedList(opIndexSelectedFile)
        # allConfs = generateInitialPopulation(accurateSetUp, numberOfIndividualsToStartWith, inputObj,ignoreIndexList)
        allConfs = generateInitialPopulation(tempAcc, numberOfIndividualsToStartWith, inputObj,ignoreListIndecies, limitedListValues, limitedListIndecies)
        # for index in range(numberOfIndividualsToStartWith):
            # indexToChoose =  random.choice(range(0, len(remainingPopulation), 1))
            # sampleSetUp =  remainingPopulation[indexToChoose]
            # remainingPopulation.pop(indexToChoose) 
        #     allConfs.append(sampleSetUp)
           
        creator.create("FitnessMin", base.Fitness, weights=(-1.0, 1.0))
        creator.create("Individual", list, fitness=creator.FitnessMin)
        toolbox = base.Toolbox()

        # Operator registering
        toolbox.register("individual", tools.initRepeat, creator.Individual)
        # toolbox.register("population", tools.initRepeat, list, toolbox.individual )
        population = []
        for index in range(len(allConfs)):
            myGenerator = return_conf(allConfs[index])
            population.append(toolbox.individual(lambda: next(myGenerator), len(allConfs[index])))
        
        
        NGEN = settings.NGEN
        MU = settings.MU#number of indi for the next gen
        LAMBDA = settings.LAMBDA#number of children
        CXPB = settings.CXPB 
        MUTPB = settings.MUTPB
        population = run_spea2(NGEN, MU, LAMBDA, CXPB, MUTPB, population,
                    CSourceOutputForVariousSetUpFileName, operatorSampleFileFullAddress,
                    executableName, executableInputList, rootResultFolderName, CBuildFolder,
                    operandSampleFileName, lOfAccurateValues, toolbox, nameOfAllOperandFilesList, inputObj, ignoreListIndecies)
        # print population
        # sys.exit()
        lOfPoints = []  
        for individual in population:
            newPoint = points()
            # newPoint.set_SNR(individual.fitness.values[1])
            if(eval(inputObj.dealingWithPics)): 
                newPoint.set_PSNR(individual.fitness.values[1])
            else:
                newPoint.set_SNR(individual.fitness.values[1])
            newPoint.set_energy(individual.fitness.values[0])
            newPoint.set_setUp(list(individual))
            newPoint.set_setUp_number(0)
            lOfPoints.append(newPoint)
        
        # lOfOperandSet[operandIndex].set_lOfPoints(copy.deepcopy(lOfPoints))
        operandIndex += 1
    
    
    #---------guide:::  getting the end time
    timeAfterFindingResults = datetime.datetime.now()
    totalTime = findTotalTime(timeBeforeFindingResults, timeAfterFindingResults) 
    print "total Time: " + str(totalTime)
    
    
    #---------guide::: populating the IOAndProcessCharP 
    IOAndProcessCharP.write("the mode is: " + mode + "\n")
    IOAndProcessCharP.write("number of operators in the CSource file: " + str(len(lAllOpsInSrcFile)) + "\n")
    IOAndProcessCharP.write("number of Operands: " + str(len(nameOfAllOperandFilesList)) +"\n")
    IOAndProcessCharP.write("numberOfTriesList: " + str(numberOfTriesList) + "\n")
    IOAndProcessCharP.write("numberOfSuccessfulTriesList: " + str(numberOfSuccessfulTriesList) + "\n")
    
    #---------guide:::  find the pareto points and store them in resultTuple
    # resultTuple = [] #this is a list of pareto Triplets(setup, error, energy) associated with each 
                       #one of the inputs 
    #setting up the resultTupleList with the right length 
    # for i in range(0, len(error),1):
        # resultTuple.append([])
   

    
    if not(mode == "only_read_values" or mode == "read_values_and_get_pareto"):
        with open(PIK, "wb") as f:
            for point in lOfPoints: 
                pickle.dump(copy.deepcopy(point), f)

    

    # ---- reading the values back
    if (mode == "only_read_values" or mode == "read_values_and_get_pareto"):
        with open(PIK, "rb") as f:
            # pickle.load(f)
            while True: 
                try: 
                    point = pickle.load(f)
                    print point 
                    lOfPoints.append(point) 
                    # listOfPeople.append(copy.copy(person))# 
                except Exception as ex:
                    if not (type(ex).__name__ == "EOFError"):
                        print type(ex).__name__ 
                        print ex.args
                        print "something went wrong"
                    break
   #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ 
   #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ 
    # ---- find the pareto curve of lOfPoints
    delimeter = [workingList[0], workingList[-1] +1] 
    if settings.method == "localParetoPieceParetoResult":
        resultPoints = pareto_frontier(lOfPoints, maxX= True, maxY = False)
        delimeter = [workingList[0], workingList[-1] +1] 
        #moduleParetoSet  = pareto_set(resultPoints, True, False)
        pointSet  = point_set(resultPoints, "pareto", True, False);
        pointSet.set_delimeter(delimeter)
        with open(settings.lOfParetoSetFileName, "a") as f:
            pickle.dump(copy.deepcopy(pointSet), f)

    elif settings.method == "uniqueNoiseParetoResult":
        lOfUniqueNoisePoints = extract_unique_noise(lOfPoints, inputObj.dealingWithPics)
        
        resultPoints = lOfUniqueNoisePoints
        opIndexSelectedFile = open(settings.opIndexSelectedFile, "w");
        for myPoints in lOfUniqueNoisePoints:
            #fix req: we shouldn't be writing the whole set up but only part of it
            opIndexSelectedFile.write(str(myPoints.get_setUp())) 
        
        #fix req: we don't need a paretoSet, instead a point set as a parent,
        #and then later the child is the type of the set such as pareto set
        pointSet= point_set(resultPoints, "unique")
        #fix req: delmiter should be defined properly, change the numbers
        pointSet.set_delimeter(delimeter)
        with open(settings.lOfParetoSetFileName, "w") as f:
            pickle.dump(copy.deepcopy(pointSet), f)
    elif (settings.method == "allPoints"):
        resultPoints = lOfPoints 
        pointSet= point_set(resultPoints, "all")
        #fix req: delmiter should be defined properly, change the numbers
        pointSet.set_delimeter(delimeter)
        with open(settings.lOfParetoSetFileName, "a") as f:
            pickle.dump(copy.deepcopy(pointSet), f)
    else:
        print "this method is not defined"
        exit()
    
    
    # ---- drawing the pareto set
    symbolsCollected = [] #this list contains the symbols collected for every new input 
    symbolsToChooseFrom = ['*', 'x', "o", "+", "*", "-", "^", "1", "2", "3", "4"] #symbols to draw the plots with
    symbolIndex = 0  
    # ---- generate the graph
    if settings.runToolChainGenerateGraph: 
        plotPareto =settings.runToolChainPlotPareto
        symbolsCollected = generate_snr_energy_graph(inputObj.dealingWithPics, resultPoints, plotPareto, symbolsToChooseFrom, lOfAccurateValues, symbolIndex, maxY, maxX) 
        
    # symbolsCollected.append(symbolsToChooseFrom[symbolIndex]) 
    #generateGraph(map(lambda x: x.get_lOfError(), lOfParetoPoints), map(lambda x: x.get_energy(), lOfParetoPoints), "Noise", "Energy", symbolsToChooseFrom[i])
            
        
    
    # ---- collecting the result in a list (for later printing)
    resultTuple = [] 
    for index, point in enumerate(resultPoints):
        if(eval(inputObj.dealingWithPics)): 
            resultTuple.append((point.get_setUp(), point.get_PSNR(), point.get_energy()))
        else:
            resultTuple.append((point.get_setUp(), point.get_SNR(), point.get_energy()))

    finalResultFileFullAddress = rootResultFolderName + "/" + finalResultFileName
    writeReadableOutput(resultTuple,  symbolsCollected, finalResultFileFullAddress)
    pylab.savefig(finalResultFileFullAddress[:-4]+".png") #saving the figure generated by generateGraph
    #----:::  getting back up of the results
    folderToCopyToNameProcessed = comeUpWithNewFolderNameAccordingly(rootFolder + "/" + settings.resultsBackups) 
    listOfFoldersToCopyFrom = [rootResultFolderName, CSrcFolderAddress]  
    generateBackup(rootResultFolderBackupName, listOfFoldersToCopyFrom, folderToCopyToNameProcessed) #generating a back of the results
    cleanUpExtras(rootResultFolderName) 
    #---------guide::: show the graph
    #plt.show() 


if __name__ == "__main__":
    main()
