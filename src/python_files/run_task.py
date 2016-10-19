from scoop import futures, shared
from reminder import *
import multiprocessing
from multiprocessing import Process, Manager
import misc
import misc2
import tests
from settings import *
from error import *
#from error import *

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


"""
def apply_heuristic_on_task_with_multiple_prime_input(settings_obj, inputObj, lOf_run_input_list):
    lOflOfPoints_out_of_heuristic = [] 
    lOflOfAllPointsTried = [] 
    if (settings_obj.runMode == "parallel"): 
        #the_lock = multiprocessing.Lock() 
        pool = multiprocessing.Pool(len(lOf_run_input_list)) 

    for iteration, run_input_list in enumerate(lOf_run_input_list): 
        try: 
            inputObj.set_run_input(run_input_list) 
            unique_point_list, lOfAllPointsTried, lOfPoints_out_of_heuristic, pointSet, input_Point_list, accurateSetUp, delimeter = apply_heuristic_on_task_with_one_prime_input(settings_obj, inputObj)
            for points in lOfPoints_out_of_heuristic:
                points.set_input_number(iteration)
            lOflOfPoints_out_of_heuristic.append(lOfPoints_out_of_heuristic)
            for points_ in lOfAllPointsTried:
                points_.set_input_number(iteration)
            lOflOfAllPointsTried.append(lOfAllPointsTried)
        except TaskError as er:
            raise BenchMarkError(er.error_name, er.input_obj, er.setUp)

    return lOflOfPoints_out_of_heuristic,lOflOfAllPointsTried
"""
def run_serial(settings_obj, in_inputObj, run_input_list, iteration):
        lOfPoints_out_of_heuristic_serial = [] 
        lOfAllPointsTried_serial = [] 
        #print "process vs image " + str(multiprocessing.current_process()._identity[0] - 1) + " " + str(run_input_list)
            
        try: 
            if (settings_obj.runMode == "parallel"): 
                inputObj = copy.deepcopy(in_inputObj) 
                inputObj.set_run_input(run_input_list) 
            else: 
                inputObj = in_inputObj
                inputObj.set_run_input(run_input_list) 
            
            #inputObj.set_run_input(run_input_list) 
            #inputObj = in_inputObj
            unique_point_list, lOfAllPointsTried, lOfPoints_out_of_heuristic, \
                    pointSet, input_Point_list, accurateSetUp, delimeter = \
                    apply_heuristic_on_task_with_one_prime_input(settings_obj,
                    inputObj)

            for points in lOfPoints_out_of_heuristic:
                points.set_input_number(iteration)
            lOfPoints_out_of_heuristic_serial = lOfPoints_out_of_heuristic
            for points_ in lOfAllPointsTried:
                points_.set_input_number(iteration)
            lOfAllPointsTried_serial = lOfAllPointsTried
        except TaskError as er:
            raise BenchMarkError(er.error_name, er.input_obj, er.setUp)
        
        return lOfPoints_out_of_heuristic_serial, lOfAllPointsTried_serial

def apply_heuristic_on_task_with_multiple_prime_input(settings_obj, inputObj, lOf_run_input_list):
    lOflOfPoints_out_of_heuristic = [] 
    lOflOfAllPointsTried = [] 

    if (settings_obj.runMode == "parallel"): 
        reminder(settings_obj.reminder_flag, "still not sure if paralleilsm work.\
        we know that if i want to throttle the number of cpus used (by using a negative\
        number), I get an error b/c some files are not defined. I am not sure if \
        I would have the same problem if the n_jobs exceed the num of cores in the system")
        reminder(settings_obj.reminder_flag, "for each processes we need to have\
                all_input_scenarios.txt* defined. This means that if we want to \
                run 5 processes we need to have 5 all_input_scnearios.txt*")
        reminder(settings_obj.reminder_flag, "with parallel execution, we can't\
        call run_a_tool more than once, this seems to be b/c for each run_a_tool\
        a set of processes are defined, hence we need more all_input_scenarios.txt* \
        files")
        num_cores = len(lOf_run_input_list) 
        
#        l_iteration = range(len(lOf_run_input_list))
#        l_inputObj = []
#        for el in lOf_run_input_list:
#            new_inputObj = copy.deepcopy(inputObj) 
#            new_inputObj.set_run_input(el)
#            l_inputObj.append(new_inputObj)
#        
#        for el in l_inputObj:
#            print el.get_run_input()
#        
#        parallel_results = Parallel(n_jobs=num_cores)(delayed(run_serial)(settings_obj, in_inputObj,  run_input_list, iteration) for iteration, run_input_list,in_inputObj in zip(l_iteration, lOf_run_input_list, l_inputObj))
        #multiprocessing.Pool(processes=(multiprocessing.cpu_count() - 1)) 
        parallel_results = Parallel(n_jobs=num_cores)(delayed(run_serial)(settings_obj, inputObj,  run_input_list, iteration) for iteration, run_input_list in enumerate(lOf_run_input_list))
        lOflOfPoints_out_of_heuristic = map(lambda x: x[0], parallel_results)
        lOflOfAllPointsTried = map(lambda x: x[1], parallel_results)
        print len(parallel_results)
    elif(settings_obj.runMode == "serial"):
        for iteration, run_input_list in enumerate(lOf_run_input_list):
            lOfPoints_out_of_heuristic, lOfAllPointsTried = run_serial(settings_obj, inputObj, run_input_list, iteration)
            lOflOfPoints_out_of_heuristic.append(lOfPoints_out_of_heuristic)
            lOflOfAllPointsTried.append(lOfAllPointsTried)
    else:
        for iteration, run_input_list in enumerate(lOf_run_input_list):
            inputObj.set_run_input(run_input_list) 
            apply_heuristic_on_task_with_one_prime_input(settings_obj,
                    inputObj)

    return lOflOfPoints_out_of_heuristic,lOflOfAllPointsTried



def run_task_with_one_set_up_and_collect_info(settings_obj, inputObj, input_setUp):
    start = time.time() 
    timeBeforeFindingResults = datetime.datetime.now()
    print "ISA : " + str(input_setUp)
    sys.stdout.flush()
    #--------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------
    #----- initializing variables 
    #--------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------
    symbolsToChooseFrom = ['*', 'x', "o", "+", "*", "-", "^", "1", "2", "3", "4"] #symbols to draw the plots with
    run_input_list = inputObj.get_run_input()
    inputObj.expandAddress()
    maxX = settings_obj.maxX
    maxY = settings_obj.maxY
    mode = settings_obj.mode 
    lOfAllPointsTried = []
    lOfPoints_out_of_heuristic = []  
    lOfAccurateValues = [] #list of accurate values associated with the primary inputs
    lOfPoints = []  
    allPointsTried = []
    unique_point_list = []
    output_list = []
    input_setUp_list_element_list = []
    lOf_UTC_PF = [] 
    pareto_frontier_of_lOfPoints_out_of_heuristic = []
    pareto_frontier_of_lOfAllPointsTried  = []
    opIndexSelectedFile =settings_obj.opIndexSelectedFile
    open(opIndexSelectedFile, "w").close()
    CSrcFolderAddress = inputObj.CSrcFolderAddress
    lOfCSrcFileAddress = inputObj.lOfCSrcFileAddress 
    CBuildFolderName = inputObj.CBuildFolderName 
    generateMakeFile = inputObj.generateMakeFile
    rootFolder = inputObj.rootFolder 
    rootResultFolderName = rootFolder + "/" + settings_obj.generatedTextFolderName
    operatorSampleFileFullAddress = rootResultFolderName + "/"+ settings_obj.operatorSampleFileName + str(0) + ".txt"
    AllInputScenariosInOneFile = inputObj.AllInputScenariosInOneFile
    AllInputFileOrDirectoryName = inputObj.AllInputFileOrDirectoryName 
    finalResultFileName = inputObj.finalResultFileName
    PIK_all_points = inputObj.PIK_all_points
    PIK_pareto  = inputObj.PIK_pareto
    PIK_pareto_of_all = inputObj.PIK_pareto_of_all 
    PIK_UTC_file = inputObj.PIK_UTC_file
    input_for_s4_file = inputObj.input_for_s4_file
    bench_suit_name = inputObj.bench_suit_name; 
    
    #--------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------
    #-----sanity checking the variabels
    #--------------------------------------------------------------------------------
    #---------guide:::  checking the validity of the input and making necessary files and folders
    #--------------------------------------------------------------------------------
    rootResultFolderBackupName =  rootFolder + "/" + settings_obj.resultsBackups # is used to get a back up of the results generated in the previuos run of this program
    if not(os.path.isdir(rootResultFolderBackupName)):
        os.system("mkdir" + " " + rootResultFolderBackupName)
    os.system("rm -r " + rootResultFolderName)
    os.system("mkdir " + rootResultFolderName)
    executableName = "tool_exe" #src file to be analyzed
    CBuildFolder = rootFolder + "/" + CBuildFolderName
    #get the input to the executable 
    executableInputList = []
    #if (settings_obj.runMode == "parallel"): 
        #the_lock = multiprocessing.Lock() 
        #pool = multiprocessing.Pool() 
    #-------checking whether the file (or directory) containging the operands(input) exist or no
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
    #----------removing the result file
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
    os.system("mkdir" + " " + rootResultFolderName + "/" + settings_obj.rawResultFolderName)
    #---------guide:::  if the operands were all given in a file: separate them to different files
    #...................else: use the folder that they are in, as an input to the C source files
    #if all in one file 
    if (AllInputScenariosInOneFile):
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
                    print ("input Number is ", inputNumber) 
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
    
    #---------guide:::  sampling operands
    
    if (inputObj.settings_obj.runMode == "parallel"): 
        print "ERROR: we don't have the capability for parallelizing this yet"
    
    nameOfAllOperandFilesList  = [AllOperandsFolderName +"/" + "0.txt"]
    #nameOfAllOperandFilesList = getNameOfFilesInAFolder(AllOperandsFolderName)
    


    numberOfTriesList = [] 
    numberOfSuccessfulTriesList = []
    errorRequirementList = []
    errorDiffList =[] #contains the difference between the error request and the error recieved from simulated annealing ( in percentage)
     
    allPossibleScenariosForEachOperator, limitedListIndecies, ignoreListIndecies, accurateSetUp = generateAllPossibleScenariosForEachOperator(rootResultFolderName, lAllOpsInSrcFile, settings_obj)
    workingList = generateWorkingList(ignoreListIndecies, allPossibleScenariosForEachOperator )
    
    #---------guide:::  generate all possible apx setUps Possible (mainly used for full permutation design exploration, otherwise called exhustive search)
    IOAndProcessCharFileName = rootResultFolderName + "/" + settings_obj.IOAndProcessCharFileName
    IOAndProcessCharP = open(IOAndProcessCharFileName, "w")
    open(settings_obj.annealerProgressionOutputFileName, "w").close()
    open(rootResultFolderName +  "/" + settings_obj.annealerOutputFileName, "w").close()
    



    #--------------------------------------------------------------------------
    #--------------------------------------------------------------------------
    #---------gather list of accurate values associated with the primary inputs
    #--------------------------------------------------------------------------
    #--------------------------------------------------------------------------
    for inputNumber,operandSampleFileName in enumerate(nameOfAllOperandFilesList):
         
        process_id = 0 
        
        CSourceOutputForVariousSetUpFileName =  rootResultFolderName + "/" + settings_obj.rawResultFolderName + "/" + settings_obj.csourceOutputFileName + str(inputNumber) + ".txt" #where to collect C++ source results
        modifyOperatorSampleFile(operatorSampleFileFullAddress, accurateSetUp)
        
        if not(settings_obj.errorTest): 
            print("\n........running to get accurate values\n"); 
            reminder(settings_obj.reminder_flag,"make sure to change make_run to make_run_compile if you change the content of any of the cSRC files")
            reminder(settings_obj.reminder_flag,"the parallel execution requires all_input_scenarious.txt (to the number of inputs) even for sd-vbs that does not really uses them, hence, make sure you have have all_inut_scnearios.txt$(number) where number if the lenght of the input")
            make_run_compile(executableName, executableInputList, rootResultFolderName, CSourceOutputForVariousSetUpFileName, CBuildFolder, operandSampleFileName, bench_suit_name, process_id, settings_obj,
                    run_input_list) #first make_run
            accurateValues = extractCurrentValuesForOneInput(CSourceOutputForVariousSetUpFileName, inputObj, settings_obj)
            
        else:
            newPath = "/home/local/bulkhead/behzad/usr/local/apx_tool_chain/src/python_files/scratch/acc.txt"
            accurateValues = extractCurrentValuesForOneInput(newPath, inputObj, settings_obj)
        
        try:
            if (accurateValues == None or len(accurateValues)==0):
                raise AccurateValueNoneError
        except AccurateValueNoneError as er:
            raise TaskError(type(er).__name__, inputObj, map(lambda x: x[2],  accurateSetUp))

            exit()
        #assert(accurateValues != None)
        
        lOfAccurateValues.append(accurateValues)

        input_Point_list = [] 
        
        numberOfIndividualsToStartWith = settings_obj.numberOfIndividualsToStartWith
        tempAcc = accurateSetUp
        opIndexSelectedFile  = settings_obj.opIndexSelectedFile
        limitedListValues = getLimitedList(opIndexSelectedFile)
        allConfs = generateInitialPopulation(tempAcc, numberOfIndividualsToStartWith, inputObj,ignoreListIndecies, limitedListValues, limitedListIndecies, settings_obj)
        possibly_worse_case_setup = generate_possibly_worse_case_setup(tempAcc, settings_obj)
        population = []

        
        #---geting the possibly_worse_case_result info 
        possibly_worse_case_setup_individual = map (lambda x: x[2],  possibly_worse_case_setup[0])
        print("\n.......running to get possibly_worse_case_result\n"); 
        try: 
            possibly_worse_case_result = specializedEval(False, 1, accurateSetUp, [], accurateSetUp, inputObj,nameOfAllOperandFilesList, rootResultFolderName, executableName, executableInputList, CBuildFolder, operandSampleFileName,lOfAccurateValues, allPointsTried,True, unique_point_list, output_list,[], 0, settings_obj, run_input_list, possibly_worse_case_setup_individual)
        except WithinSpecEval as er:
            raise TaskError(er.error_name, inputObj, er.setUp)
            exit()          
        
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
        
        try: 
            result = specializedEval(True, possibly_worse_case_result_quality, accurateSetUp, [], accurateSetUp, inputObj,nameOfAllOperandFilesList, rootResultFolderName, executableName,
                executableInputList, CBuildFolder, operandSampleFileName,lOfAccurateValues, allPointsTried,True, unique_point_list, output_list,[], 0, settings_obj, run_input_list,
                input_setUp)
        except WithinSpecEval as er:
            raise TaskError(er.error_name, inputObj, er.setUp)
            exit()          

        newPoint = points() 
        newPoint.set_varios_values(result[0], result[1],modifyMold(accurateSetUp, input_setUp), input_setUp, 0, 0)
        return newPoint
#            
#            lOfPoints_out_of_heuristic.append(newPoint)




def apply_heuristic_on_task_with_one_prime_input(settings_obj, inputObj):
    start = time.time() 
    timeBeforeFindingResults = datetime.datetime.now()
    
    #--------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------
    #----- initializing variables 
    #--------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------
    symbolsToChooseFrom = ['*', 'x', "o", "+", "*", "-", "^", "1", "2", "3", "4"] #symbols to draw the plots with
    run_input_list = inputObj.get_run_input()
    inputObj.expandAddress()
    maxX = settings_obj.maxX
    maxY = settings_obj.maxY
    mode = settings_obj.mode 
    lOfAllPointsTried = []
    lOfPoints_out_of_heuristic = []  
    lOfAccurateValues = [] #list of accurate values associated with the primary inputs
    lOfPoints = []  
    allPointsTried = []
    unique_point_list = []
    output_list = []
    input_setUp_list_element_list = []
    lOf_UTC_PF = [] 
    pareto_frontier_of_lOfPoints_out_of_heuristic = []
    pareto_frontier_of_lOfAllPointsTried  = []
    opIndexSelectedFile =settings_obj.opIndexSelectedFile
    open(opIndexSelectedFile, "w").close()
    CSrcFolderAddress = inputObj.CSrcFolderAddress
    lOfCSrcFileAddress = inputObj.lOfCSrcFileAddress 
    CBuildFolderName = inputObj.CBuildFolderName 
    generateMakeFile = inputObj.generateMakeFile
    rootFolder = inputObj.rootFolder 
    rootResultFolderName = rootFolder + "/" + settings_obj.generatedTextFolderName
    if (settings_obj.runMode == "parallel"):
        operatorSampleFileFullAddress = rootResultFolderName + "/"+ settings_obj.operatorSampleFileName + str(multiprocessing.current_process()._identity[0] - 1) + ".txt"
    else:
        operatorSampleFileFullAddress = rootResultFolderName + "/"+ settings_obj.operatorSampleFileName + str(0) + ".txt"
       
    AllInputScenariosInOneFile = inputObj.AllInputScenariosInOneFile
    AllInputFileOrDirectoryName = inputObj.AllInputFileOrDirectoryName 
    finalResultFileName = inputObj.finalResultFileName
    PIK_all_points = inputObj.PIK_all_points
    PIK_pareto  = inputObj.PIK_pareto
    PIK_pareto_of_all = inputObj.PIK_pareto_of_all 
    PIK_UTC_file = inputObj.PIK_UTC_file
    input_for_s4_file = inputObj.input_for_s4_file
    bench_suit_name = inputObj.bench_suit_name; 
    
    #--------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------
    #-----sanity checking the variabels
    #--------------------------------------------------------------------------------
    #---------guide:::  checking the validity of the input and making necessary files and folders
    #--------------------------------------------------------------------------------
    rootResultFolderBackupName =  rootFolder + "/" + settings_obj.resultsBackups # is used to get a back up of the results generated in the previuos run of this program
    if not(os.path.isdir(rootResultFolderBackupName)):
        os.system("mkdir" + " " + rootResultFolderBackupName)
    os.system("rm -r " + rootResultFolderName)
    os.system("mkdir " + rootResultFolderName)
    executableName = "tool_exe" #src file to be analyzed
    CBuildFolder = rootFolder + "/" + CBuildFolderName
    #get the input to the executable 
    executableInputList = []
    #if (settings_obj.runMode == "parallel"): 
        #the_lock = multiprocessing.Lock() 
        #pool = multiprocessing.Pool() 
    #-------checking whether the file (or directory) containging the operands(input) exist or no
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
    #----------removing the result file
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
    if (settings_obj.runMode == "parallel"): 
        print "fuckitye" + str( AllInputFileOrDirectoryName)
        AllOperandScenariosFullAddress = AllInputFileOrDirectoryName + str(multiprocessing.current_process()._identity[0] - 1)
    else: 
        AllOperandScenariosFullAddress = AllInputFileOrDirectoryName 
    print "goh begire " + AllOperandScenariosFullAddress 
    inputNumber = 0 
    os.system("mkdir" + " " + rootResultFolderName + "/" + settings_obj.rawResultFolderName)
    #---------guide:::  if the operands were all given in a file: separate them to different files
    #...................else: use the folder that they are in, as an input to the C source files
    #if all in one file 
    if (AllInputScenariosInOneFile):
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
                    if (settings_obj.runMode == "parallel"): 
                        fileToWriteName = AllOperandsFolderName + "/" + str(inputNumber) +".txt" + str(multiprocessing.current_process()._identity[0] - 1)
                    else:
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
    
    #---------guide:::  sampling operands
    if (inputObj.settings_obj.runMode == "parallel"): 
        nameOfAllOperandFilesList = [AllOperandsFolderName +"/" + "0.txt" + str(multiprocessing.current_process()._identity[0] - 1)]
    else:
        nameOfAllOperandFilesList  = [AllOperandsFolderName +"/" + "0.txt"]
    numberOfTriesList = [] 
    numberOfSuccessfulTriesList = []
    errorRequirementList = []
    errorDiffList =[] #contains the difference between the error request and the error recieved from simulated annealing ( in percentage)
     
    allPossibleScenariosForEachOperator, limitedListIndecies, ignoreListIndecies, accurateSetUp = generateAllPossibleScenariosForEachOperator(rootResultFolderName, lAllOpsInSrcFile, settings_obj)
    workingList = generateWorkingList(ignoreListIndecies, allPossibleScenariosForEachOperator )
    
    #---------guide:::  generate all possible apx setUps Possible (mainly used for full permutation design exploration, otherwise called exhustive search)
    IOAndProcessCharFileName = rootResultFolderName + "/" + settings_obj.IOAndProcessCharFileName
    IOAndProcessCharP = open(IOAndProcessCharFileName, "w")
    open(settings_obj.annealerProgressionOutputFileName, "w").close()
    open(rootResultFolderName +  "/" + settings_obj.annealerOutputFileName, "w").close()
    



    #--------------------------------------------------------------------------
    #--------------------------------------------------------------------------
    #---------gather list of accurate values associated with the primary inputs
    #--------------------------------------------------------------------------
    #--------------------------------------------------------------------------
    for inputNumber,operandSampleFileName in enumerate(nameOfAllOperandFilesList):
        if (settings_obj.runMode == "parallel"): 
            process_id = multiprocessing.current_process()._identity[0] - 1
        else: 
            process_id = 0 
        CSourceOutputForVariousSetUpFileName =  rootResultFolderName + "/" + settings_obj.rawResultFolderName + "/" + settings_obj.csourceOutputFileName + str(process_id) + ".txt" #where to collect C++ source results
        modifyOperatorSampleFile(operatorSampleFileFullAddress, accurateSetUp)
        
        if not(settings_obj.errorTest): 
            print("\n........running to get accurate values\n"); 
            reminder(settings_obj.reminder_flag,"make sure to change make_run to make_run_compile if you change the content of any of the cSRC files")
            make_run_compile(executableName, executableInputList, rootResultFolderName, CSourceOutputForVariousSetUpFileName, CBuildFolder, operandSampleFileName, bench_suit_name, process_id, settings_obj,
                    run_input_list) #first make_run
            accurateValues = extractCurrentValuesForOneInput(CSourceOutputForVariousSetUpFileName, inputObj, settings_obj)
        else:
            newPath = "/home/local/bulkhead/behzad/usr/local/apx_tool_chain/src/python_files/scratch/acc.txt"
            accurateValues = extractCurrentValuesForOneInput(newPath, inputObj, settings_obj)
        
        
        #-----sanity check
        try:
            if (accurateValues == None or len(accurateValues)==0):
                raise AccurateValueNoneError
        except AccurateValueNoneError as er:
            raise TaskError(type(er).__name__, inputObj, map(lambda x: x[2],  accurateSetUp))
            exit()
        #assert(accurateValues != None)
        lOfAccurateValues.append(accurateValues)
    
    #--------------------------------------------------------------------------
    #--------------------------------------------------------------------------
    #---------run a heuristic to collect points
    #--------------------------------------------------------------------------
    #--------------------------------------------------------------------------
#    if (mode == "allPermutations"): 
#        lengthSoFar = 1 
#        
#        """ ---- guide: making sure that it is possible to use permuation
#                 if the number of permutations are too big to be held in memoery
#                 we error out """
#        for opOptions in allPossibleScenariosForEachOperator:
#            print opOptions
#            lengthSoFar *= len(opOptions)
#            assert(lengthSoFar < settings_obj.veryHugeNumber), """numbr of permuations:""" + str(lengthSoFar)+""" is too big. 
#            it is bigger than:""" + str(settings_obj.veryHugeNumber)
#
#        allPossibleApxScenarioursList = generateAllPossibleApxScenariousList(allPossibleScenariosForEachOperator)
#        for input_setUp_list_element in inputObj.get_lOfSetUps():
#            for index,config in enumerate(allPossibleApxScenarioursList):
#                individual = map(lambda x: x[2], config) 
#                specializedEval(False, 1, accurateSetUp, ignoreListIndecies, accurateSetUp, inputObj,nameOfAllOperandFilesList, rootResultFolderName, executableName,
#                executableInputList, CBuildFolder, operandSampleFileName,lOfAccurateValues, allPointsTried, True, unique_point_list, output_list, input_setUp_list_element, 0, settings_obj, individual)
#            lOfPoints_out_of_heuristic = allPointsTried
    if (mode == "genetic_algorithm" or mode == "swarm_particle"):
        input_Point_list = [] 
        #if (settings_obj.runMode == "parallel"): 
        #    the_lock = multiprocessing.Lock() 
        
        numberOfIndividualsToStartWith = settings_obj.numberOfIndividualsToStartWith
        tempAcc = accurateSetUp
        opIndexSelectedFile  = settings_obj.opIndexSelectedFile
        limitedListValues = getLimitedList(opIndexSelectedFile)
        allConfs = generateInitialPopulation(tempAcc, numberOfIndividualsToStartWith, inputObj,ignoreListIndecies, limitedListValues, limitedListIndecies, settings_obj)
        possibly_worse_case_setup = generate_possibly_worse_case_setup(tempAcc, settings_obj)
        population = []

        #---geting the possibly_worse_case_result info 
        possibly_worse_case_setup_individual = map (lambda x: x[2],  possibly_worse_case_setup[0])
        print("\n.......running to get possibly_worse_case_result\n"); 
        
        try: 
            print possibly_worse_case_setup_individual
            accurateSetUp_stuff = map(lambda x: x[2], accurateSetUp) 
            possibly_worse_case_result = specializedEval(False, 1, accurateSetUp, [], accurateSetUp, inputObj,nameOfAllOperandFilesList, rootResultFolderName, executableName,
                    executableInputList, CBuildFolder, operandSampleFileName,lOfAccurateValues, allPointsTried,True, unique_point_list, output_list,[], 0, settings_obj, run_input_list,
                    #accurateSetUp_stuff)
                    possibly_worse_case_setup_individual)
            print "PSNR for accurate version for " + inputObj.refImage_name + " is : " + str(possibly_worse_case_result[1])
            print "E for accurate version for " + inputObj.refImage_name + " is : " + str(possibly_worse_case_result[0])
            reminder(settings_obj.reminder_flag, "replace accurateSetUp_stuff with possibly_worse_case_setup_individual")
        except WithinSpecEval as er:
            raise TaskError(er.error_name, inputObj, er.setUp)
            exit()
        
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
        
        #print "total Number of itrations: " + str(len(inputObj.get_lOfSetUps()))
        #print accurateSetUp
        if (inputObj.is_primary_input):
            inputObj.set_lOfSetUps([accurateSetUp])
        
        for iteration, input_setUp_list_element_complete in enumerate(inputObj.get_lOfSetUps()):
            print "got here now"
            input_setUp_list_element = map(lambda x: x[2], input_setUp_list_element_complete)
            #-----collecting the input point 
            
           

            try:
                UTC_acc = specializedEval(False, 1, accurateSetUp, [], accurateSetUp, inputObj,nameOfAllOperandFilesList, rootResultFolderName, executableName,
                    executableInputList, CBuildFolder, operandSampleFileName,lOfAccurateValues, allPointsTried,False, unique_point_list, output_list,[], 0, settings_obj, run_input_list,
                    input_setUp_list_element)
            except WithinSpecEval as er:
                raise TaskError(er.error_name, inputObj, er.setUp)
                exit()          

            input_Point = points()
            input_Point.set_varios_values(UTC_acc[0], UTC_acc[1], modifyMold(accurateSetUp, input_setUp_list_element), input_setUp_list_element, iteration, 0)
            input_Point_list.append(input_Point) 
             
            #-----run genetic algo for an iteration 
            NGEN_to_use = settings_obj.NGEN 
            if (mode == "genetic_algorithm"): 
                try: 
                    population = run_spea2(population,
                            CSourceOutputForVariousSetUpFileName, operatorSampleFileFullAddress,
                            executableName, executableInputList, rootResultFolderName, CBuildFolder,

                            operandSampleFileName, lOfAccurateValues, nameOfAllOperandFilesList, inputObj, ignoreListIndecies, possibly_worse_case_result_quality, accurateSetUp, allConfs, NGEN_to_use,
                            settings_obj.MU, settings_obj.LAMBDA, unique_point_list, output_list,allPointsTried,  input_setUp_list_element, iteration, settings_obj, run_input_list)
                except WithinSpecEval as er:
                    raise TaskError(er.error_name, inputObj, er.setUp)
                    exit()
            elif (mode == "swarm_particle"):
                population = run_SP(population, NGEN_to_use,
                            CSourceOutputForVariousSetUpFileName, operatorSampleFileFullAddress,
                            executableName, executableInputList, rootResultFolderName, CBuildFolder,
                            operandSampleFileName, lOfAccurateValues, nameOfAllOperandFilesList, inputObj, ignoreListIndecies, possibly_worse_case_result_quality, accurateSetUp, allConfs,
                            unique_point_list, output_list, allPointsTried, input_setUp_list_element, settings_obj)
            else:
                print "this mode" + str(mode) +" not defined"
                exit()

            #---some sanity check 
            assert (len(unique_point_list) > 0)
            assert(len(output_list) > 0)
            assert(len(allPointsTried) > 0)
            
            #--store all the points acquired by the heuristic in the list
            for individual in population:
                newPoint = points() 
                newPoint.set_varios_values(individual.fitness.values[0], individual.fitness.values[1],modifyMold(accurateSetUp, individual), map(lambda x: x, individual), iteration, 0)
                
                lOfPoints_out_of_heuristic.append(newPoint)
        
    #---collect all the points tried in a list 
    for individual in allPointsTried:
        newPoint = points() 
        newPoint.set_varios_values(individual.get_energy(), individual.get_quality(), list(individual.get_setUp()),individual.get_raw_setUp(), individual.get_input_number(), 0)
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
   

    #--- extract pareto points 
    pareto_points =  pareto_frontier(lOfPoints_out_of_heuristic, maxX, maxY, settings_obj)
    
    
    #pareto_points =  lOfPoints_out_of_heuristic
    pointSet= point_set(pareto_points, "pareto", maxX, maxY)
    pointSet.set_delimeter(delimeter)
    
   

    #--------------------------------------------------------------------------
    #--------------------------------------------------------------------------
    # ---- collecting the result in a list (for later printing)
    #--------------------------------------------------------------------------
    #--------------------------------------------------------------------------
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
    folderToCopyToNameProcessed = comeUpWithNewFolderNameAccordingly(rootFolder + "/" + settings_obj.resultsBackups) 
    listOfFoldersToCopyFrom = [rootResultFolderName, CSrcFolderAddress]  
    cleanUpExtras(rootResultFolderName, settings_obj) 
    end = time.time()
    

    reminder(settings_obj.reminder_flag, "returning parto points instead of the lOfPoints_out_of heuristic. Don't think this will be problematic, but consider as a source of error")
    return unique_point_list, lOfAllPointsTried, pareto_points, pointSet, input_Point_list, accurateSetUp, delimeter
    #return unique_point_list, lOfAllPointsTried, lOfPoints_out_of_heuristic, pointSet, input_Point_list, accurateSetUp, delimeter
