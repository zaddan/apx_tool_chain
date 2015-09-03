
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
import pickle
import copy
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
from points_class import *

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
    if len(sys.argv) < 9:
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
        print "8. pickled_file"
        #print "8. noiseToSignalRatio"
        exit()


    home = expanduser("~")
    #---------guide:::  acquaring the inputs
    for index, element in enumerate(sys.argv):
        if element.split("/")[0] == "~":
            sys.argv[index] = home + sys.argv[index][1:]

    CSrcFolderAddress = sys.argv[1] #src file to be analyzet
    CSrcFileAddress = sys.argv[2] #src file to be analyzet
    #executableName = sys.argv[3] #src file to be analyzed
    generateMakeFile = sys.argv[3]
    rootFolder = sys.argv[4] 
    AllOperandScenariosInOneFiles = sys.argv[5]
    AllOperandsFileOrDirectoryName = sys.argv[6]
    finalResultFileName = sys.argv[7]
    PIK = sys.argv[8]  
    #noiseToSignalRatio = float(sys.argv[8])
    
    
   
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
    
    
    # print "please provide the inputs to the executable. when done, type type" 
    # input = raw_input('provide the input: ')
    # while (input != "done"):
        # executableInputList.append(input)
        # input = raw_input('provide the next input: ')
    
   
    #checking whether the file (or directory) containging the operands(input) exist or no
    if (AllOperandScenariosInOneFiles): #if a file
        print AllOperandsFileOrDirectoryName
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
            AllOperandsFolderName = AllOperandsFileOrDirectoryName

    
    
    
                                                 #inputs. This means that we have multiple operand sets)
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
    
    numberOfTriesList = [] 
    numberOfSuccessfulTriesList = []
    noiseRequirementList = []
    noiseDiffList =[] #contains the difference between the noise request and the noise recieved from simulated annealing ( in percentage)
     
    allPossibleScenariosForEachOperator = generateAllPossibleScenariosForEachOperator(rootResultFolderName, lAllOpsInSrcFile)
    #---------guide:::  generate all possible apx setUps Possible (mainly used for full permutation design exploration, otherwise called exhustive search)
    allPossibleApxScenarioursList = generateAllPossibleApxScenariousList(allPossibleScenariosForEachOperator)
    IOAndProcessCharFileName = rootResultFolderName + "/" + settings.IOAndProcessCharFileName
    IOAndProcessCharP = open(IOAndProcessCharFileName, "w")
    
    open(settings.annealerProgressionOutputFileName, "w").close()
    open(rootResultFolderName +  "/" + settings.annealerOutputFileName, "w").close()
    
    #---------guide::: go through operand files and sweep the apx space
    lOfOperandSet = [] 
    timeBeforeFindingResults = datetime.datetime.now()
    for operandSampleFileName in nameOfAllOperandFilesList:
        countSoFar = 0 
        #clearly state where the new results associated with the new input starts 
        CSourceOutputForVariousSetUpFileName =  rootResultFolderName + "/" + settings.rawResultFolderName + "/" + settings.csourceOutputFileName + str(inputNumber) + ".txt" #where to collect C++ source results
        lOfPoints = []  
        lOfOperandSet.append(operandSet(get_operand_values(operandSampleFileName))) 
        
        accurateValues = []
        noise.append([])
        energy.append( [])
        config.append( [])
        inputFileNameList.append([])
        mode = settings.mode 
        operatorSampleFileFullAddress = rootResultFolderName + "/"+ settings.operatorSampleFileName
        
        
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
                print "\n" + str(100*float(apxIndexSetUp)/len(allPossibleApxScenarioursList)) + "% done" 
                status, setUp = generateAPossibleApxScenarios(rootResultFolderName + "/" + settings.AllPossibleApxOpScenarios, allPossibleApxScenarioursList , apxIndexSetUp, mode) 
                energyValue = [calculateEnergy(map(getFirstTwo, setUp))]
                configValue = polishSetup(setUp) #just to make it more readable
                inputFileNameListValue = [operandSampleFileName] 
                CSourceOutputForVariousSetUpP = open(CSourceOutputForVariousSetUpFileName, "w").close()
                modifyOperatorSampleFile(operatorSampleFileFullAddress, setUp)
                make_run(executableName, executableInputList, rootResultFolderName, CSourceOutputForVariousSetUpFileName, CBuildFolder, operandSampleFileName)
                noiseValue = [extractNoiseForOneInput(CSourceOutputForVariousSetUpFileName , accurateValues)]

                newPoint = points()
                newPoint.set_noise(noiseValue[0])
                newPoint.set_energy(energyValue[0])
                newPoint.set_setUp(configValue[0])
                newPoint.set_setUp_number(apxIndexSetUp)
                lOfPoints.append(copy.deepcopy(newPoint)) 
                
                # noise[operandIndex] += noiseValue
                # energy[operandIndex] += energyValue
                # config[operandIndex] +=configValue
                inputFileNameList[operandIndex] += inputFileNameListValue
                apxIndexSetUp +=1
                if (status == "done"):
                    break;

            lOfOperandSet[operandIndex].set_lOfPoints(copy.deepcopy(lOfPoints))
            operandIndex += 1
            inputNumber +=1
        elif (mode == "simulated_annealing"):
            outP = open("out", "w") 
            annealerOutputFileP = open(rootResultFolderName + "/" + 
                    settings.annealerOutputFileName, "a")
            lOfNoiseDiff = []  
            lOfNoiseRequirement = [] 
            
            # symbolsToChooseFrom = ['1', 'x', "o", "+", "*", "-", "^", "*"] #symbols to draw the plots with
            
            # symbolsToChooseFrom = ['1', '2', "3", "4", "o", "+", "^", "*", "x", "-"] #symbols to draw the plots with
            
            symbolsToChooseFrom = ['g1', 'rx', "bo", "y+", "*", "-", "^", "*"] #symbols to draw the plots with
            for noiseRequirementsPosition, noiseToSignalRatio in enumerate(
                    settings.noiseToSignalRatioRange):
                
                noiseRequirement = noiseToSignalRatio*int(accurateValues[0])
                outP.write(str(noiseRequirement) + "\n") 
                initialSetUp = pickInitialSetUpIndexForSimmulatedAnnelaing(
                        allPossibleApxScenarioursList[0], noiseRequirement,
                        operatorSampleFileFullAddress,executableName, 
                        executableInputList, rootResultFolderName, 
                        CSourceOutputForVariousSetUpFileName, CBuildFolder, 
                        operandSampleFileName, accurateValues)
                
                numberOfApxBitsStepSize =  settings.numberOfApxBitsStepSize 
                numberOfApxBitsInitialTemperature = settings.numberOfApxBitsInitialTemperature 
                operatorPickInitialTemperature = settings.operatorPickInitialTemperature 
                operatorPickStepSize = settings.operatorPickStepSize 
                
                resultPoint, otherPointsTried, noiseRequirement, simulatedAnnealingResults,numberOfTriesList, numberOfSuccessfulTriesList = improvedSimulatedAnnealing2(
                        initialSetUp, noiseRequirement, 
                        numberOfApxBitsInitialTemperature, 
                        numberOfApxBitsStepSize, operatorPickInitialTemperature,
                        operatorPickStepSize, operatorSampleFileFullAddress,
                        executableName, executableInputList, rootResultFolderName, 
                        CSourceOutputForVariousSetUpFileName, CBuildFolder, 
                        operandSampleFileName, accurateValues, noiseRequirementsPosition,
                        len(settings.noiseToSignalRatioRange) - 1)
                
                
                outP.write("here is the noise" + str(resultPoint.get_noise()) + "\n") 
                lOfPoints.append(copy.deepcopy(resultPoint))
                noiseDiffPercentage =  math.fabs(noiseRequirement - resultPoint.get_noise())/(noiseRequirement)
                lOfNoiseDiff.append(noiseDiffPercentage)
                lOfNoiseRequirement.append(noiseRequirement)
        
            # # ---- here
                # generateGraph(map(lambda x: x.get_noise(),otherPointsTried), map(lambda x: x.get_energy(),otherPointsTried),"Noise", "Energy", 'gx') 
            # for index, element in enumerate(lOfPoints): 
                # generateGraph(map(lambda x: x.get_noise(),[element]), map(lambda x: x.get_energy(),[element]),"Noise", "Energy",  symbolsToChooseFrom[index])
            # finalResultFileFullAddress = rootResultFolderName + "/" + finalResultFileName
            # pylab.savefig(finalResultFileFullAddress[:-4]+".png") #saving the figure generated by generateGraph
            # sys.exit() 
            # # ---- here
            for index, pointItem in enumerate(lOfPoints):
                annealerOutputFileP.write( str("*******************************") + "\n")
                print "********************"
                annealerOutputFileP.write("noiseRequirement: " + str(lOfNoiseRequirement[index]) + "\n") 
                annealerOutputFileP.write("noise: " + str(pointItem.get_noise()) + "\n") 
                annealerOutputFileP.write("noiseDiffPercentage: " + str(lOfNoiseDiff[index])+ "\n") 
                annealerOutputFileP.write("energy: " + str(pointItem.get_energy()) + "\n") 
                annealerOutputFileP.write("setUp: " + str(pointItem.get_setUp()) + "\n") 
                # annealerOutputFileP.write("setUp: " + str(pointItem.get_setUp()) + "\n") 

                
                annealerOutputFileP.write( str("*******************************") + "\n")
                
                inputFileNameList[operandIndex] += [operandSampleFileName] 
            
            lOfOperandSet[operandIndex].set_lOfPoints(copy.deepcopy(lOfPoints))
            
            operandIndex += 1
            inputNumber +=1
            annealerOutputFileP.close()
    
   

    #---------guide:::  getting the end time
    timeAfterFindingResults = datetime.datetime.now()
    totalTime = findTotalTime(timeBeforeFindingResults, timeAfterFindingResults) 
    print totalTime 
    
    
    #---------guide::: populating the IOAndProcessCharP 
    IOAndProcessCharP.write("the mode is: " + mode + "\n")
    IOAndProcessCharP.write("number of operators in the CSource file: " + str(len(lAllOpsInSrcFile)) + "\n")
    IOAndProcessCharP.write("number of Operands: " + str(len(nameOfAllOperandFilesList)) +"\n")
    IOAndProcessCharP.write("numberOfTriesList: " + str(numberOfTriesList) + "\n")
    IOAndProcessCharP.write("numberOfSuccessfulTriesList: " + str(numberOfSuccessfulTriesList) + "\n")
    
    #---------guide:::  find the pareto points and store them in resultTuple
    # resultTuple = [] #this is a list of pareto Triplets(setup, noise, energy) associated with each 
                       #one of the inputs 
    #setting up the resultTupleList with the right length 
    # for i in range(0, len(noise),1):
        # resultTuple.append([])
   

    symbolsToChooseFrom = ['*', 'x', "o", "+", "*", "-", "^", "1", "2", "3", "4"] #symbols to draw the plots with
    symbolsCollected = [] #this list contains the symbols collected for every new input 
    #---------guide:::  get the noise for each input
    for i,operandSetItem in enumerate(lOfOperandSet):
        paretoNoise = []  #cleaning the previous values if exist
        paretoEnergy = [] #cleaning the previous values if exist         
        #---------guide:::  get the pareto set
        if (mode == "allPermutations"): 
            # lOfParetoPoints =  operand.get_lOfPoints()
            lOfParetoPoints = pareto_frontier(operandSetItem.get_lOfPoints(), maxX= False, maxY = False)
            operandSetItem.set_lOf_pareto_points(lOfParetoPoints)
        elif (mode == "simulated_annealing"):
            lOfParetoPoints = operandSetItem.get_lOfPoints() 
            operandSetItem.set_lOf_pareto_points(lOfParetoPoints)
        #---------guide:::  find the setUps that corresponds to the pareto Points
        setUpNumberList = [] #contains the list of setUp numbers associated with the pareto set 
                             #this is used to avoid duplicate
        
# mode = "only_read_values"
# mode = "read_values_and_get_pareto"
    if not(mode == "only_read_values" or mode == "read_values_and_get_pareto"):
        for operandSetItem in lOfOperandSet: 
            with open(PIK, "wb") as f:
                pickle.dump(operandSetItem, f)

    
    # ---- reading the values back
    if (mode == "only_read_values" or mode == "read_values_and_get_pareto"):
        lOfOperandSet = [] 
        with open(PIK, "rb") as f:
            # pickle.load(f)
            while True: 
                try: 
                    operandSetItem = pickle.load(f)# 
                    lOfOperandSet.append(operandSetItem)# 
                    # listOfPeople.append(copy.copy(person))# 
                except Exception as ex:
                    if not (type(ex).__name__ == "EOFError"):
                        print type(ex).__name__ 
                        print ex.args
                    break
    resultTuple = [] 
    for index, operandSetItem in enumerate(lOfOperandSet):
        resultTuple.append([]) 
        for j,point in enumerate(operandSetItem.get_lOf_pareto_points()):
            resultTuple[index].append((point.get_setUp_number(), point.get_setUp(), point.get_noise(), point.get_energy()))
        generateGraph(map(lambda x: x.get_noise(),operandSetItem.get_lOf_pareto_points()), map(lambda x: x.get_energy(),operandSetItem.get_lOf_pareto_points()),"Noise", "Energy", symbolsToChooseFrom[i%len(symbolsToChooseFrom)])
        symbolsCollected.append(symbolsToChooseFrom[index%len(symbolsToChooseFrom)])

        
    #---- generate pareto graph
    
         
    finalResultFileFullAddress = rootResultFolderName + "/" + finalResultFileName
    writeReadableOutput(resultTuple,  symbolsCollected, finalResultFileFullAddress)
    pylab.savefig(finalResultFileFullAddress[:-4]+".png") #saving the figure generated by generateGraph
    
    #---------guide:::  getting back up of the results
    folderToCopyToNameProcessed = comeUpWithNewFolderNameAccordingly(rootFolder + "/" + settings.resultsBackups) 
    listOfFoldersToCopyFrom = [rootResultFolderName, CSrcFolderAddress]  
    generateBackup(rootResultFolderBackupName, listOfFoldersToCopyFrom, folderToCopyToNameProcessed) #generating a back of the results

    cleanUpExtras(rootResultFolderName) 
    #---------guide::: show the graph
    #plt.show() 



main()
