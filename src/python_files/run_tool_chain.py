from scoop import futures, shared
from reminder import *
import multiprocessing
from multiprocessing import Process, Manager
import misc
import misc2
import tests
from settings import *

def get_quality_energy_values_directly(lOfPoints, symbol, points_to_graph,index, limit=False, lower_bound=-100, upper_bound=100):
    lOfQualityVals = map(lambda x: x.get_quality(), lOfPoints)
    lOfEnergyVals = map(lambda x: x.get_energy(), lOfPoints)
    if (limit):
        result = filter(lambda x: x[0] > lower_bound and x[0] <upper_bound, zip(lOfQualityVals, lOfEnergyVals))
        lOfQualityVals = map(lambda x: x[0], result)
        lOfEnergyVals = map(lambda x: x[1], result)
    points_to_graph.append([lOfQualityVals, lOfEnergyVals, symbol, index])
 


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


import time
import pickle
import copy
import pylab
import sys
import os

from extract_unique_noise import *
from inputs import *#this file contains all the inputs
from search_heuristic_algorithm import *
from deap import algorithms
from points_class import *
from deap import base
from deap import creator
from deap import tools
from src_parse_and_apx_op_space_gen import *
from modify_operator_sample_file import *
#from sample_operand_and_sweep_apx_space import *
from make_run import *
from debug_helpers import *
import settings 
from extract_result_properties import *
from plot_generation import *
import matplotlib.pyplot as plt
plt.ioff()
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



def generate_snr_energy_graph(dealingWithPics, lOfPoints, plotPareto, symbolsToChooseFrom, lOfAccurateValues, symbolIndex, maxY, maxX, settings_obj):
    symbolsCollected = [] 
    lOfPoints_refined =[]
    """ 
    if plotPareto:
        print "noer" 
        lOfPoints_refined = pareto_frontier(lOfPoints,maxX, maxY); 
    else:
        print "ere" 
        lOfPoints_refined = lOfPoints 
    """
    lOfPoints_refined = lOfPoints 
    if(eval(dealingWithPics)): 
        lOfPSNR = [] 
        lOfEnergy = [] 
        for point in lOfPoints_refined:
            if point.get_PSNR() != avgAccurateValue:
                lOfQualityValues.append(point.get_PSNR())
                lOfEnergy.append(point.get_energy())
        generateGraph(lOfPSNR,lOfEnergy, "PSNR", "Energy", symbolsToChooseFrom[symbolIndex])
        symbolsCollected.append(symbolsToChooseFrom[symbolIndex]) 
    else:
        lOfQualityValues = [] 
        lOfEnergy = [] 
        if (settings_obj.quality_mode == "snr"): 
            for point in lOfPoints_refined:
                if point.quality_calculatable:
                    lOfQualityValues.append(point.get_quality())
                    lOfEnergy.append(point.get_energy())
        else:
            for point in lOfPoints_refined:
                assert(point.quality_calculatable) 
                lOfQualityValues.append(point.get_quality())
                lOfEnergy.append(point.get_energy())

        symbolsCollected.append(symbolsToChooseFrom[symbolIndex]) 
        print "List of Quality Values: " + str(lOfQualityValues)
        generateGraph(lOfQualityValues,lOfEnergy, "QualityValues", "Energy", symbolsToChooseFrom[symbolIndex])
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

#def main():
def run_task_and_collect_points():
#if __name__ == "__main__":
    start = time.time() 
    
    #---------guide:::  promting ther user regarding the required input
#    print "the following inputs needs to be provided in the " + str(settings.userInputFile)
#    print "1.source folder address"
#    print "2.source file address"
#    print "3.generate Makefile (with YES or NO)"
#    print "4.CBuilderFolder"
#    print "5.AllInputScenariosInOneFile" #whether all the operand scenarios can be found in one file or no
#    print "6. AllInputFileOrDirectoryName" #the user should be providing a file name if AllInputScenariosInOneFile is true and a direcoty other   
#    print "7. finalResulstFileName"
#    
    symbolsToChooseFrom = ['*', 'x', "o", "+", "*", "-", "^", "1", "2", "3", "4"] #symbols to draw the plots with
    settings_obj = settingsClass()
    inputObj = inputClass(settings_obj)
    inputObj.expandAddress()
    maxX = settings_obj.maxX
    maxY = settings_obj.maxY
    lOfAllPointsTried = []
    lOfPoints_out_of_heuristic = []  
    opIndexSelectedFile =settings_obj.opIndexSelectedFile
    open(opIndexSelectedFile, "w").close()
    CSrcFolderAddress = inputObj.CSrcFolderAddress
    lOfCSrcFileAddress = inputObj.lOfCSrcFileAddress 
    CBuildFolderName = inputObj.CBuildFolderName 
    generateMakeFile = inputObj.generateMakeFile
    rootFolder = inputObj.rootFolder 
    AllInputScenariosInOneFile = inputObj.AllInputScenariosInOneFile
    AllInputFileOrDirectoryName = inputObj.AllInputFileOrDirectoryName 
    finalResultFileName = inputObj.finalResultFileName
    PIK_all_points = inputObj.PIK_all_points
    PIK_pareto  = inputObj.PIK_pareto
    PIK_pareto_of_all = inputObj.PIK_pareto_of_all 
    PIK_UTC_file = inputObj.PIK_UTC_file
    input_for_s4_file = inputObj.input_for_s4_file
    bench_suit_name = inputObj.bench_suit_name; 
    
    #---------guide:::  checking the validity of the input and making necessary files
    #and folders
    rootResultFolderName = rootFolder + "/" + settings_obj.generatedTextFolderName
    rootResultFolderBackupName =  rootFolder + "/" + settings_obj.resultsBackups # is used to get a back up of the results generated in the previuos run of this program
    if not(os.path.isdir(rootResultFolderBackupName)):
        os.system("mkdir" + " " + rootResultFolderBackupName)
    os.system("rm -r " + rootResultFolderName)
    os.system("mkdir " + rootResultFolderName)
    executableName = "tool_exe" #src file to be analyzed
    CBuildFolder = rootFolder + "/" + CBuildFolderName
    #get the input to the executable 
    executableInputList = []
    if (settings_obj.runMode == "parallel"): 
        #the_lock = multiprocessing.Lock() 
        pool = multiprocessing.Pool() 


    
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
    os.system("rm " + rootResultFolderName + "/" + settings_obj.rawresultFileName)

    
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
    os.system("mkdir" + " " + rootResultFolderName + "/" + settings_obj.rawResultFolderName)
    #---------guide:::  if the operands were all given in a file: separate them to different files
    #...................else: use the folder that they are in, as an input to the C source files
    #if all in one file 
    if (AllInputScenariosInOneFile):
        #check for error 
        if not(os.path.isfile(AllOperandScenariosFullAddress)):
            print AllOperandScenariosFullAddress + " does not exist"
            exit();

        #make a directory for all operand inputs 
        AllOperandsFolderName = rootResultFolderName + "/" + settings_obj.AllOperandsFolderName
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
        lAllOpsInSrcFile += sourceFileParse(CSrcFileAddressItem, settings_obj)
    settings_obj.totalNumberOfOpCombinations = 1;
    energy = []
    error = []
    config = []
    inputFileNameList = []
    
    #---------guide:::  sampling operands
    inputNumber = 0 
    nameOfAllOperandFilesList = getNameOfFilesInAFolder(AllOperandsFolderName)
    #operandIndex = 0
    
    numberOfTriesList = [] 
    numberOfSuccessfulTriesList = []
    errorRequirementList = []
    errorDiffList =[] #contains the difference between the error request and the error recieved from simulated annealing ( in percentage)
     
    allPossibleScenariosForEachOperator, limitedListIndecies, ignoreListIndecies, accurateSetUp = generateAllPossibleScenariosForEachOperator(rootResultFolderName, lAllOpsInSrcFile, settings_obj)
    #---------guide:::  generate all possible apx setUps Possible (mainly used for full permutation design exploration, otherwise called exhustive search)
    IOAndProcessCharFileName = rootResultFolderName + "/" + settings_obj.IOAndProcessCharFileName
    IOAndProcessCharP = open(IOAndProcessCharFileName, "w")
    
    open(settings_obj.annealerProgressionOutputFileName, "w").close()
    open(rootResultFolderName +  "/" + settings_obj.annealerOutputFileName, "w").close()
    
    #---------guide::: go through operand files and sweep the apx space
    # lOfOperandSet = [] 
    timeBeforeFindingResults = datetime.datetime.now()
    lOfAccurateValues = []
    for inputNumber,operandSampleFileName in enumerate(nameOfAllOperandFilesList):
        countSoFar = 0 
        #clearly state where the new results associated with the new input starts 
        CSourceOutputForVariousSetUpFileName =  rootResultFolderName + "/" + settings_obj.rawResultFolderName + "/" + settings_obj.csourceOutputFileName + str(inputNumber) + ".txt" #where to collect C++ source results
        # newOperand =  operandSet(get_operand_values(operandSampleFileName))
        
        accurateValues = []
        error.append([])
        energy.append( [])
        config.append( [])
        inputFileNameList.append([])
        mode = settings_obj.mode 
        operatorSampleFileFullAddress = rootResultFolderName + "/"+ settings_obj.operatorSampleFileName + str(0) + ".txt"
        
        
        #---------guide:::  getting accurate values associated with the CSource output
        #accurateSetUp,workingList = generateAccurateScenario(allPossibleScenariosForEachOperator,ignoreListIndecies )
        workingList = generateWorkingList(ignoreListIndecies, allPossibleScenariosForEachOperator )
        
        apxIndexSetUp = 0 #zero is associated with the accurate results (this is a contract that needs to be obeyed)
        # status, setUp = generateAPossibleApxScenarios(rootResultFolderName + "/" + settings.AllPossibleApxOpScenarios, allPossibleApxScenarioursList , apxIndexSetUp, mode) 
        #---------guide:::  erasing the previuos content of the file
        CSourceOutputForVariousSetUpP = open(CSourceOutputForVariousSetUpFileName, "w").close()
        #---------guide:::  modify the operator sample file
        modifyOperatorSampleFile(operatorSampleFileFullAddress, accurateSetUp)
        
        
        sys.stdout.flush()
        #---------guide:::  run the CSrouce file with the new setUp(operators)
        if not(settings_obj.errorTest): 
            print("\n........running to get accurate values\n"); 
            reminder(settings_obj.reminder_flag,"make sure to change make_run to make_run_compile if you change the content of any of the cSRC files")
            make_run(executableName, executableInputList, rootResultFolderName, CSourceOutputForVariousSetUpFileName, CBuildFolder, operandSampleFileName, bench_suit_name, 0, settings_obj) #first make_run
            accurateValues = extractCurrentValuesForOneInput(CSourceOutputForVariousSetUpFileName, inputObj, settings_obj)
        else:
            newPath = "/home/local/bulkhead/behzad/usr/local/apx_tool_chain/src/python_files/scratch/acc.txt"
            accurateValues = extractCurrentValuesForOneInput(newPath, inputObj, settings_obj)
        
        assert(accurateValues != None)
        lOfAccurateValues.append(accurateValues)
        # print lOfAccurateValues
        # lOfOperandSet.append(newOperand)
        #---------guide:::  make a apx set up and get values associated with it
        
    lOfPoints = []  
    allPointsTried = []
    unique_point_list = []
    output_list = []
    previous_ideal_setUp_list = []
    #previous_ideal_setUp_output_list = []
    previous_ideal_setUp_list_reduced = []
    # ---- read previous ideal setUps and populate the ideal_pts(only contain the # of apx bits)
    print "right here" 
    sys.stdout.flush()
    

    if(settings_obj.get_UTC_optimal_configs or settings_obj.adjust_NGEN): 
        ideal_pts = []
        with open(PIK_UTC_file , "rb") as f:
            while True: 
                try: 
                    point = pickle.load(f)
                    ideal_pts.append(point) 
                    # listOfPeople.append(copy.copy(person))# 
                except Exception as ex:
                    if not (type(ex).__name__ == "EOFError"):
                        print type(ex).__name__ 
                        print ex.args
                        print "something went wrong"
                    break
        
         
        for pt in ideal_pts:
            previous_ideal_setUp_list.append(pt.get_raw_setUp())
            #previous_ideal_setUp_output_list.append(pt.get_raw_values())
    
        #from here
        lOf_UTC_PF = pareto_frontier(ideal_pts, maxX, maxY, settings_obj) 
        previous_ideal_setUp_list = []  
        for el in lOf_UTC_PF: 
            previous_ideal_setUp_list.append(el.get_raw_setUp())
        with open("lOf_UTC_PF", "wb") as f:
            for el in lOf_UTC_PF:     
                pickle.dump(copy.deepcopy(el), f)

        #to here
        
        # ---- santiy check
        assert not(settings_obj.get_UTC_optimal_configs and len(previous_ideal_setUp_list)== 0)
    
        # ---- more sanity check
        for el in previous_ideal_setUp_list: 
            print "accurate and el" 
            print accurateSetUp
            print el
            assert (len(accurateSetUp) == len(el))
   
        # ---- reduce the ideal_setUp_list to reduce computation time
        #previous_ideal_setUp_list_reduced = reduce_ideal_setUp_list(previous_ideal_setUp_list, previous_ideal_setUp_output_list)
        previous_ideal_setUp_list_reduced = reduce_ideal_setUp_list(previous_ideal_setUp_list)
    
    
    if (settings_obj.adjust_NGEN):
        NGEN_to_use = settings_obj.NGEN*len(previous_ideal_setUp_list_reduced)
    else:
        NGEN_to_use = settings_obj.NGEN
    
    if not(settings_obj.get_UTC_optimal_configs):
        previous_ideal_setUp_list_reduced = [(map(lambda x:x[2], accurateSetUp))]
        previous_ideal_setUp_output_list = []



    print "NGEN_to_use" + str(NGEN_to_use) 
    if (mode == "allPermutations"): 
        lengthSoFar = 1 
        
        """ ---- guide: making sure that it is possible to use permuation
                 if the number of permutations are too big to be held in memoery
                 we error out """
        for opOptions in allPossibleScenariosForEachOperator:
            print opOptions
            lengthSoFar *= len(opOptions)
            assert(lengthSoFar < settings_obj.veryHugeNumber), """numbr of permuations:""" + str(lengthSoFar)+""" is too big. 
            it is bigger than:""" + str(settings_obj.veryHugeNumber)

        allPossibleApxScenarioursList = generateAllPossibleApxScenariousList(allPossibleScenariosForEachOperator)
        for previous_ideal_setUp in previous_ideal_setUp_list_reduced:
            for index,config in enumerate(allPossibleApxScenarioursList):
                individual = map(lambda x: x[2], config) 
                specializedEval(False, 1, accurateSetUp, ignoreListIndecies, accurateSetUp, inputObj,nameOfAllOperandFilesList, rootResultFolderName, executableName,
                executableInputList, CBuildFolder, operandSampleFileName,lOfAccurateValues, allPointsTried, True, unique_point_list, output_list, previous_ideal_setUp, 0, settings_obj, individual)
            lOfPoints_out_of_heuristic = allPointsTried
    elif (mode == "genetic_algorithm" or mode == "swarm_particle"):
        input_Point_list = [] 
        if (settings_obj.runMode == "parallel"): 
            the_lock = multiprocessing.Lock() 
        
        allConfs = [] #first generation
        numberOfIndividualsToStartWith = settings_obj.numberOfIndividualsToStartWith
        tempAcc = accurateSetUp
        opIndexSelectedFile  = settings_obj.opIndexSelectedFile
        limitedList = [] 
        limitedListValues = getLimitedList(opIndexSelectedFile)
        allConfs = generateInitialPopulation(tempAcc, numberOfIndividualsToStartWith, inputObj,ignoreListIndecies, limitedListValues, limitedListIndecies, settings_obj)
        possibly_worse_case_setup = generate_possibly_worse_case_setup(tempAcc, settings_obj)
        population = []

        #---geting the possibly_worse_case_result info 
        possibly_worse_case_setup_individual = map (lambda x: x[2],  possibly_worse_case_setup[0])
        print("\n.......running to get possibly_worse_case_result\n"); 
        possibly_worse_case_result = specializedEval(False, 1, accurateSetUp, [], accurateSetUp, inputObj,nameOfAllOperandFilesList, rootResultFolderName, executableName,
                executableInputList, CBuildFolder, operandSampleFileName,lOfAccurateValues, allPointsTried,True, unique_point_list, output_list,[], 0, settings_obj,
                possibly_worse_case_setup_individual)
        possibly_worse_case_result_energy = possibly_worse_case_result[0]   
        possibly_worse_case_result_quality = possibly_worse_case_result[1]   
        
        if (settings_obj.benchmark_name == "sift"): 
             
            #print "here is the possibly_worse_case quality " + str(possibly_worse_case_result_quality)
            possibly_worse_case_result_energy = 1
            possibly_worse_case_result_quality = 1
        #----printing the possibly_worse_case_result info and exiting
        if (settings_obj.DEBUG): 
            print "worse_case energy: " + str(possibly_worse_case_result[0])
            print "worse_case quality: " + str(possibly_worse_case_result[1])
 
        
        
        print "total Number of itrations: " + str(len(previous_ideal_setUp_list_reduced))
        for iteration,previous_ideal_setUp in enumerate(previous_ideal_setUp_list_reduced):
            print  "iteration number: " + str(iteration)
            print "\n...... running the  accurate version of the succeeding stage with " + str(iteration) + "th"  + "iteration"
            UTC_acc = specializedEval(False, 1, accurateSetUp, [], accurateSetUp, inputObj,nameOfAllOperandFilesList, rootResultFolderName, executableName,
                    executableInputList, CBuildFolder, operandSampleFileName,lOfAccurateValues, allPointsTried,False, unique_point_list, output_list,[], 0, settings_obj,
                    previous_ideal_setUp)
            previous_ideal_setUp_energy = UTC_acc[0]   
            previous_ideal_setUp_quality = UTC_acc[1]   
            
            input_Point = points()
            input_Point.set_energy(UTC_acc[0])
            input_Point.set_quality(UTC_acc[1])
            input_Point.set_setUp(previous_ideal_setUp)
            #input_Point.set_raw_setUp(new_individual_raw_setUp)
            input_Point.set_input_number(iteration) 
            input_Point.set_setUp_number(0)
            input_Point_list.append(input_Point) 
             


            print "energy associated with acc version of idealSet of iteration number" + str(iteration) + ": " + str(previous_ideal_setUp_energy)
            print "quality associated with acc version of idealSet of iteration number" + str(iteration) + ": " + str(previous_ideal_setUp_quality)
             
            if (mode == "genetic_algorithm"): 
                population = run_spea2(population,
                            CSourceOutputForVariousSetUpFileName, operatorSampleFileFullAddress,
                            executableName, executableInputList, rootResultFolderName, CBuildFolder,

                            operandSampleFileName, lOfAccurateValues, nameOfAllOperandFilesList, inputObj, ignoreListIndecies, possibly_worse_case_result_quality, accurateSetUp, allConfs, NGEN_to_use,
                            settings_obj.MU, settings_obj.LAMBDA, unique_point_list, output_list,allPointsTried,  previous_ideal_setUp, iteration, settings_obj)
            
            elif (mode == "swarm_particle"):
                population = run_SP(population, NGEN_to_use,
                            CSourceOutputForVariousSetUpFileName, operatorSampleFileFullAddress,
                            executableName, executableInputList, rootResultFolderName, CBuildFolder,
                            operandSampleFileName, lOfAccurateValues, nameOfAllOperandFilesList, inputObj, ignoreListIndecies, possibly_worse_case_result_quality, accurateSetUp, allConfs,
                            unique_point_list, output_list, allPointsTried, previous_ideal_setUp, settings_obj)
            else:
                print "this mode" + str(mode) +" not defined"
                exit()

            #---some sanity check 
            #if (settings.get_UTC_optimal_configs): 
            assert (len(unique_point_list) > 0)
            assert(len(output_list) > 0)
            assert(len(allPointsTried) > 0)
            
            #--store all the points acquired by the heuristic in the list
            for individual in population:
                newPoint = points()
                if(eval(inputObj.dealingWithPics)): 
                    newPoint.set_PSNR(individual.fitness.values[1])
                else:
                    newPoint.set_quality((individual.fitness.values[1])) 
                newPoint.set_energy(individual.fitness.values[0])
                newPoint.set_setUp(modifyMold(accurateSetUp, individual))
                individual_converted_to_list = map(lambda x: x, individual)
                newPoint.set_raw_setUp(individual_converted_to_list)
                newPoint.set_setUp_number(0)
                newPoint.set_input_number(iteration) 
                #print "here is newPoint" + str(newPoint.get_input_number()) 
                lOfPoints_out_of_heuristic.append(newPoint)
        
        with open(input_for_s4_file, "w") as f:
            for el in input_Point_list:
                pickle.dump(el, f)   
        # lOfOperandSet[operandIndex].set_lOfPoints(copy.deepcopy(lOfPoints))
        #operandIndex += 1
    
    # --- update output_list, unique_point_list
    #if (settings.get_UTC_optimal_configs): 
#    for el in lOfPoints_out_of_heuristic: 
#        print "999" 
#        el.get_raw_values() 
#        update_unique(el, output_list, unique_point_list)
#
    
    #-- dumping the the points associated w/ new input to a file
    if (settings_obj.write_UTC_optimal_configs): 
        with open(PIK_UTC_file, "wb") as f:
            reminder(settings_obj.reminder_flag,"if UTC is used to extract rawValues and AccurateValues associated with points an error would happen b/c we empty the two list out. We did this to avoid the massive size of UTC otherwise")
            for el in unique_point_list:
                el.lOfAccurateValues = [] #I empty out the list b/c the size of the file would be massive
                                          #other wise
                el.lOfRawValues = [] 
                pickle.dump(copy.deepcopy(el), f)

    for individual in allPointsTried:
        newPoint = points()
        # newPoint.set_SNR(individual.fitness.values[1])
        if(eval(inputObj.dealingWithPics)): 
            newPoint.set_PSNR(individual.get_quality())
        else:
            newPoint.set_quality(individual.get_quality()) #normalizing the quality to the possibly_worse_case
        newPoint.set_energy(individual.get_energy())
        newPoint.set_setUp(list(individual.get_setUp()))
        newPoint.set_raw_setUp(individual.get_raw_setUp())
        newPoint.set_setUp_number(0)
        newPoint.set_input_number(individual.get_input_number()) 
        lOfAllPointsTried.append(newPoint)
    
    #---uncomment to compare prob_heur_points to genetic algo
    """
    #----note: lOfAllPointsTried need to be populated
    prob_heur_points = probabilistic_heuristic(pareto_frontier(lOfPoints_out_of_heuristic, maxX, maxY), CSourceOutputForVariousSetUpFileName, operatorSampleFileFullAddress,
                        executableName, executableInputList, rootResultFolderName, CBuildFolder,
                        operandSampleFileName, lOfAccurateValues, nameOfAllOperandFilesList, inputObj, ignoreListIndecies, possibly_worse_case_result_quality, accurateSetUp, allConfs,
                        lOfAllPointsTried)

    lOfAllPointsTried_cleaned_of_doubles = clean_doubles(lOfAllPointsTried)
    all_pareto_fronts_list = all_pareto_frontiers(lOfAllPointsTried_cleaned_of_doubles, maxX, maxY)
    
    #---- preparing the initial population for the next genetic run 
    new_allConfs =[]
    for el in lOfPoints_out_of_heuristic:
        new_allConfs.append(el.get_setUp())

    new_NGEN = int((len(lOfPoints_out_of_heuristic)*settings.number_of_probabilistic_trial)/settings.MU) + 1
    print "new_NGEN is " +str(new_NGEN)

    _, population = run_spea2(population, CSourceOutputForVariousSetUpFileName, operatorSampleFileFullAddress, executableName, executableInputList, rootResultFolderName, CBuildFolder,
            operandSampleFileName, lOfAccurateValues, nameOfAllOperandFilesList, inputObj, ignoreListIndecies, possibly_worse_case_result_quality, accurateSetUp, new_allConfs, new_NGEN,
            settings.MU, settings.LAMBDA, unique_point_list, output_list)


    lOfPoints_out_of_heuristic_2nd_round = []
    for individual in population:
        newPoint = points()
        # newPoint.set_SNR(individual.fitness.values[1])
        if(eval(inputObj.dealingWithPics)): 
            newPoint.set_PSNR(individual.fitness.values[1])
        else:
            newPoint.set_quality((individual.fitness.values[1])) 
        newPoint.set_energy(individual.fitness.values[0])
        newPoint.set_setUp(modifyMold(accurateSetUp, individual))
        individual_converted_to_list = map(lambda x: x, individual)
        newPoint.set_raw_setUp(individual_converted_to_list)
        newPoint.set_setUp_number(0)
        #lOfPoints.append(newPoint)
        lOfPoints_out_of_heuristic_2nd_round.append(newPoint)

#    if (tests.test_extracting_all_pareto_frontiers):
#        points_to_graph = [] 
#        for index, lOfPoints in enumerate(all_pareto_fronts_list):
#            get_quality_energy_values_directly(lOfPoints,symbolsToChooseFrom[index],  points_to_graph, symbolsToChooseFrom[index])
#            if (index >=2):
#                break
#        generateGraph_for_all(points_to_graph, "1/quality", "energy", "blah") 
#        
#        pylab.savefig("results.png") #saving the figure generated by generateGraph
#        print all_pareto_fronts_list
#        sys.exit()
    
    """
    """ 
    while(True): 
        number = raw_input('provide the num: ')
        total = 0 
        for el in my_histogram.keys():
            if my_histogram[el] > int(number):
                total +=1;
        print "\n" + str(total) + "number of moves"    
    """
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
   
    # ---- pickle and write the results
    if not(mode == "only_read_values"):
        with open(PIK_pareto, "wb") as f:
            points_to_dump = pareto_frontier(lOfPoints_out_of_heuristic, maxX, maxY, settings_obj)
            for point in points_to_dump:
                pickle.dump(copy.deepcopy(point), f)
        with open(PIK_all_points, "wb") as f:
            points_to_dump = lOfAllPointsTried
            #points_to_dump = pareto_frontier(prob_heur_points[:], maxX, maxY)
            for point in points_to_dump:
                pickle.dump(copy.deepcopy(point), f)
        with open(PIK_pareto_of_all, "wb") as f:
            #points_to_dump = pareto_frontier(lOfPoints_out_of_heuristic_2nd_round, maxX, maxY) #righthere
            points_to_dump = pareto_frontier(lOfAllPointsTried, maxX, maxY, settings_obj) #righthere
            for point in points_to_dump:
                pickle.dump(copy.deepcopy(point), f)




    # ---- reading the values back
    if (mode == "only_read_values"):
        with open(PIK_pareto, "rb") as f:
            # pickle.load(f)
            while True: 
                try: 
                    point = pickle.load(f)
                    print point 
                    lOfPoints_out_of_heuristic.append(point) 
                    # listOfPeople.append(copy.copy(person))# 
                except Exception as ex:
                    if not (type(ex).__name__ == "EOFError"):
                        print type(ex).__name__ 
                        print ex.args
                        print "something went wrong"
                    break
        with open(PIK_all_points, "rb") as f:
            # pickle.load(f)
            while True: 
                try: 
                    point = pickle.load(f)
                    lOfAllPointsTried.append(point) 
                    # listOfPeople.append(copy.copy(person))# 
                except Exception as ex:
                    if not (type(ex).__name__ == "EOFError"):
                        print type(ex).__name__ 
                        print ex.args
                        print "something went wrong"
                    break
        with open(PIK_pareto_of_all, "rb") as f:
            # pickle.load(f)
            while True: 
                try: 
                    point = pickle.load(f)
                    lOfAllPointsTried.append(point) 
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
    """ 
    if settings.method == "localParetoPieceParetoResult":
        resultPoints = pareto_frontier(lOfPoints, maxX, maxY)
        delimeter = [workingList[0], workingList[-1] +1] 
        pointSet  = point_set(resultPoints, "pareto", maxX, maxY);
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
    """ 
    #resultPoints = lOfPoints_out_of_heuristic
    pareto_points =  pareto_frontier(lOfPoints_out_of_heuristic, maxX, maxY, settings_obj)
    pointSet= point_set(pareto_points, "pareto", maxX, maxY)
    #fix req: delmiter should be defined properly, change the numbers
    pointSet.set_delimeter(delimeter)
    if not(settings_obj.get_UTC_optimal_configs): 
        with open(settings_obj.lOfParetoSetFileName, "a") as f:
            pickle.dump(copy.deepcopy(pointSet), f)
#    if (runMode == "parallel"): 
#        print str(multiprocessing.current_process()._identity)
#        print str(multiprocessing.current_process()._identity[0])  + "at the end" 
    # ---- drawing the pareto set
    symbolsCollected = [] #this list contains the symbols collected for every new input 
    symbolIndex = 0  
    # ---- generate the graph
#    if settings.runToolChainGenerateGraph: 
#        plotPareto =settings.runToolChainPlotPareto
#        #symbolsCollected = generate_snr_energy_graph(inputObj.dealingWithPics, resultPoints, plotPareto, symbolsToChooseFrom, lOfAccurateValues, symbolIndex, maxY, maxX) 
#        if(len(lOfAllPointsTried) > 0):
#            symbolsCollected = generate_snr_energy_graph(inputObj.dealingWithPics, lOfAllPointsTried, plotPareto, symbolsToChooseFrom, lOfAccurateValues, 1, maxY, maxX) 
#        symbolsCollected = generate_snr_energy_graph(inputObj.dealingWithPics, pareto_points, plotPareto, symbolsToChooseFrom, lOfAccurateValues, 3, maxY, maxX) 
    # symbolsCollected.append(symbolsToChooseFrom[symbolIndex]) 
    #generateGraph(map(lambda x: x.get_lOfError(), lOfParetoPoints), map(lambda x: x.get_energy(), lOfParetoPoints), "Noise", "Energy", symbolsToChooseFrom[i])
            
        
    
    # ---- collecting the result in a list (for later printing)
    resultPoints = pareto_points
    resultTuple = [] 
    for index, point in enumerate(resultPoints):
        print index 
        if(eval(inputObj.dealingWithPics)): 
            resultTuple.append((point.get_setUp(), point.get_PSNR(), point.get_energy()))
        else:
            resultTuple.append((point.get_setUp(), point.get_quality(), point.get_energy()))

    if(settings_obj.DEBUG):
        print "---printing the results:" 
        for el in resultTuple:
            print el
    
    finalResultFileFullAddress = rootResultFolderName + "/" + finalResultFileName
#    if (settings.runToolChainGenerateGraph): 
#        writeReadableOutput(resultTuple,  symbolsCollected, finalResultFileFullAddress)
#        pylab.savefig(finalResultFileFullAddress[:-4]+".png") #saving the figure generated by generateGraph
    #----:::  getting back up of the results
    folderToCopyToNameProcessed = comeUpWithNewFolderNameAccordingly(rootFolder + "/" + settings_obj.resultsBackups) 
    listOfFoldersToCopyFrom = [rootResultFolderName, CSrcFolderAddress]  
    #generateBackup(rootResultFolderBackupName, listOfFoldersToCopyFrom, folderToCopyToNameProcessed) #generating a back of the results
    cleanUpExtras(rootResultFolderName, settings_obj) 
    #---------guide::: show the graph
    #plt.show() 
    end = time.time()
    #print "here is the total time:"

    #print end - start
    sys.stdout.flush()



if __name__ == "__main__":
    run_task_and_collect_points()
    #    main()
