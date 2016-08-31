import pickle
import copy
import sys
import os
from plot_generation import *
from compare_pareto_curves import getPoints
import multiprocessing
from search_heuristic_algorithm import *
import matplotlib
matplotlib.use('Agg') 

import pylab
import matplotlib.pyplot as plt
#plt.ioff()
from inputs import *#this file contains all the inputs
from scipy.spatial import distance
from src_parse_and_apx_op_space_gen import *
from modify_operator_sample_file import *
#from sample_operand_and_sweep_apx_space import *
from settings import *
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
import pickle
from points_class import *
from list_all_files_in_a_folder import *
from src_parse_and_apx_op_space_gen import *
from pareto_set_class import *
#**--------------------**
#**--------------------**
#----disclaimers::: if dealingwith Pic and we are feeding couple of operands,
#----we need to collect their psnr in a list and get an avg. This should be done
#--- this requries adding a PSNR (or SNR) list to the points
#--- avgAccuratValue needs to be set
#**--------------------**
#--------------------**


def get_point_set(file1_name):     
    lOfPointSet =[]
    with open(file1_name, "rb") as f:
        # pickle.load(f)
        while True: 
            try: 
                pointSet = pickle.load(f)
                lOfPointSet.append(pointSet) 
                # listOfPeople.append(copy.copy(person))# 
            except Exception as ex:
                if not (type(ex).__name__ == "EOFError"):
                    print type(ex).__name__ 
                    print ex.args
                    print "something went wrong"
                break

    # lOfParetoPoints = pareto_frontier(lOfPoints, maxX= True, maxY = False)
    return lOfPointSet


 

#def point_combine(srcFile):

def run_combine_pareto():
    settings_obj = settingsClass()
    srcFile = "pareto_set_file.txt" #file containing paretoSets
    inputObj = inputClass(settings_obj)
    inputObj.expandAddress()
    CSrcFolderAddress = inputObj.CSrcFolderAddress
    lOfCSrcFileAddress = inputObj.lOfCSrcFileAddress 
    generateMakeFile = inputObj.generateMakeFile
    rootFolder = inputObj.rootFolder 
    AllInputScenariosInOneFile = inputObj.AllInputScenariosInOneFile
    AllInputFileOrDirectoryName = inputObj.AllInputFileOrDirectoryName 
    finalResultFileName = inputObj.finalResultFileName
    #PIK = inputObj.PIK
    lOfInputs = []   #for debugging purposes
    #lOfInputs += [CSrcFolderAddress, lOfCSrcFileAddress, generateMakeFile, rootFolder, AllInputScenariosInOneFile , AllInputFileOrDirectoryName, finalResultFileName, PIK ]
    bench_suit_name = inputObj.bench_suit_name; 
    #assert(len(lOfInputs) == 8) 
    
    
    
    
    energy = []
    error = []
    config = []
    inputFileNameList = []
    lOfAccurateValues = []
    
    
    rootFolder = inputObj.rootFolder 
    rootResultFolderName = rootFolder + "/" + settings_obj.generatedTextFolderName
    rootResultFolderName = rootFolder + "/" + settings_obj.generatedTextFolderName
    AllOperandsFolderName = rootResultFolderName + "/" + settings_obj.AllOperandsFolderName
    inputNumber = 0 
    nameOfAllOperandFilesList = getNameOfFilesInAFolder(AllOperandsFolderName)
    
    CSourceOutputForVariousSetUpFileName =  rootResultFolderName + "/" + settings_obj.rawResultFolderName + "/" + settings_obj.csourceOutputFileName + str(0) + ".txt" #where to collect C++ source results
    operatorSampleFileFullAddress = rootResultFolderName + "/"+ settings_obj.operatorSampleFileName
    executableName = "tool_exe" #src file to be analyzed
    executableInputList = [] 
    CBuildFolder = rootFolder + "/" + inputObj.CBuildFolderName
    AllOperandsFolderName = rootResultFolderName + "/" + settings_obj.AllOperandsFolderName
    

    if (AllInputScenariosInOneFile): #if a file
        print AllInputFileOrDirectoryName
        if not(os.path.isfile(AllInputFileOrDirectoryName)):
            print "All OperandsFile does not exist"
            exit();
    else: #checking for the directory
        if not(os.path.isdir(AllInputFileOrDirectoryName)):
            print "All OperandsDir does not exist"
            exit();
    
    #---------guide:::  generate make file or no
    if not((generateMakeFile == "YES") or (generateMakeFile == "NO")): 
        print generateMakeFile 
        print "generateMakeFile can only take YES or NO value (capital letters)"
        exit()
    lAllOpsInSrcFile = [] 
    for CSrcFileAddressItem in lOfCSrcFileAddress:
        lAllOpsInSrcFile += sourceFileParse(CSrcFileAddressItem, settings_obj)

    nameOfAllOperandFilesList = getNameOfFilesInAFolder(AllOperandsFolderName)
    allPossibleScenariosForEachOperator, limitedListIndecies, ignoreListIndecies, accurateSetUp = generateAllPossibleScenariosForEachOperator(rootResultFolderName, lAllOpsInSrcFile, settings_obj)


    for inputNumber,operandSampleFileName in enumerate(nameOfAllOperandFilesList):
        countSoFar = 0 
        #clearly state where the new results associated with the new input starts 
        CSourceOutputForVariousSetUpFileName =  rootResultFolderName + "/" + settings_obj.rawResultFolderName + "/" + settings_obj.csourceOutputFileName + str(0) + ".txt" #where to collect C++ source results
        # newOperand =  operandSet(get_operand_values(operandSampleFileName))
        accurateValues = []
        error.append([])
        energy.append( [])
        config.append( [])
        inputFileNameList.append([])
        mode = settings_obj.mode 
        operatorSampleFileFullAddress = rootResultFolderName + "/"+ settings_obj.operatorSampleFileName + str(0) + ".txt"
        
        #---------guide:::  getting accurate values associated with the CSource output
        #accurateSetUp,_,_= generateAccurateScenario(allPossibleScenariosForEachOperator,ignoreListIndecies)
        apxIndexSetUp = 0 #zero is associated with the accurate results (this is a contract that needs to be obeyed)
        # status, setUp = generateAPossibleApxScenarios(rootResultFolderName + "/" + settings_obj.AllPossibleApxOpScenarios, allPossibleApxScenarioursList , apxIndexSetUp, mode) 
        
        #---------guide:::  erasing the previuos content of the file
        CSourceOutputForVariousSetUpP = open(CSourceOutputForVariousSetUpFileName, "w").close()
        #---------guide:::  modify the operator sample file
        modifyOperatorSampleFile(operatorSampleFileFullAddress, accurateSetUp)
        #---------guide:::  run the CSrouce file with the new setUp(operators)
        make_run(executableName, executableInputList, rootResultFolderName, CSourceOutputForVariousSetUpFileName, CBuildFolder, operandSampleFileName, bench_suit_name, 0, settings_obj)
        #---------guide::: error
        accurateValues = extractCurrentValuesForOneInput(CSourceOutputForVariousSetUpFileName, inputObj, settings_obj)
        lOfAccurateValues.append(accurateValues)
        # lOfOperandSet.append(newOperand)
        #---------guide:::  make a apx set up and get values associated with it
     


    def specializedEval(normalize, possibly_worse_case_result_quality, settings_obj, individual):
        newPoint = points() 
        newPoint.set_dealing_with_pics(eval(inputObj.dealingWithPics))
        
        if (settings_obj.runMode == "parallel"): 
            exe_annex = multiprocessing.current_process()._identity[0] 
            print "proccess id: " 
        else:
            exe_annex = 0

        
        for operandIndex, operandSampleFileName in enumerate(nameOfAllOperandFilesList):
            energyValue = [getEnergy(individual)]
            
            if (settings_obj.runMode == "parallel"): 
                CSourceOutputForVariousSetUpFileName =  rootResultFolderName + "/" + settings_obj.rawResultFolderName + "/" + settings_obj.csourceOutputFileName + str(multiprocessing.current_process()._identity[0]) + ".txt" #where to collect C++ source results
                operatorSampleFileFullAddress = rootResultFolderName + "/"+ settings_obj.operatorSampleFileName + str(multiprocessing.current_process()._identity[0]) + ".txt"
            else: 
                CSourceOutputForVariousSetUpFileName =  rootResultFolderName + "/" + settings_obj.rawResultFolderName + "/" + settings_obj.csourceOutputFileName + str(0) + ".txt" #where to collect C++ source results
                operatorSampleFileFullAddress = rootResultFolderName + "/"+ settings_obj.operatorSampleFileName + str(0) + ".txt"
            
            open(CSourceOutputForVariousSetUpFileName, "w").close()
            modifyOperatorSampleFile(operatorSampleFileFullAddress, individual)
            make_run(executableName, executableInputList, rootResultFolderName, CSourceOutputForVariousSetUpFileName, CBuildFolder, operandSampleFileName, bench_suit_name, exe_annex, settings_obj)
            
            
            errantValues =  extractCurrentValuesForOneInput(CSourceOutputForVariousSetUpFileName, inputObj, settings_obj)
            errorValue = [calculateError( lOfAccurateValues[operandIndex], errantValues, settings_obj)]
                
            configValue = [individual]
            rawValues = [extractCurrentValuesForOneInput(CSourceOutputForVariousSetUpFileName, inputObj, settings_obj)]


            newPoint.append_raw_values(rawValues[0])  
            newPoint.append_error(errorValue[0])
            newPoint.set_energy(energyValue[0])
            newPoint.set_setUp(configValue[0])
            newPoint.append_lOf_operand(get_operand_values(operandSampleFileName))
            newPoint.append_accurate_values(lOfAccurateValues[operandIndex])
            newPoint.set_dealing_with_pics(eval(inputObj.dealingWithPics)) 
            newPoint.set_dealing_with_pics(eval(inputObj.dealingWithPics)) 
            newPoint.set_input_obj(inputObj)
            # newPoint.calculate_SNR()
            if (eval(inputObj.dealingWithPics)):
                newPoint.calculate_PSNR()
        if not(eval(inputObj.dealingWithPics)):
            newPoint.calculate_quality(True, possibly_worse_case_result_quality, settings_obj)
        
        return newPoint


    lOfParetoSetDirctions  = [] 
    # ---- get pointSet
    lOfPointSet= get_point_set(srcFile) 
    print "length of paretoSet is: " + str(len(lOfPointSet))
    
    #print "number of pareto set is " + str(len(lOfPointSet)) 

    for paretoSet in lOfPointSet:
        lOfParetoSetDirctions.append(paretoSet.get_direction())
    #print lOfParetoSetDirctions 
 
    # ---- making sure that the direction of all pareto_sets are the same
    # ---- turn the list to a set (dismiss the repetttive values)
    if (len(set(lOfParetoSetDirctions))) != 1:
        print "****ERROR something went wrong"
        print "all the pareto_sets need to have the same direction"
        print "it's also possible that you didn't set some of the pareto_sets' direction"
        print "here ist he lOfParetoSetDirctions" + str(lOfParetoSetDirctions) 
        exit()

    

    # lOfParetoPoints = lOfParetoSet[0].get_pareto_values()
    # generateGraph(map(lambda x: x.get_PSNR(), lOfParetoPoints), map(lambda x: x.get_energy(), lOfParetoPoints), "PSNR", "Energy", "*")

    
    
    orderedParetoSet = [] #considers the order that they are choped
    delimeterList = [] 
    for pointSetElm in lOfPointSet:
        delimeterList.append(range(pointSetElm.get_delimeter()[0], pointSetElm.get_delimeter()[1]))

    if len(set(list(itertools.chain.from_iterable(delimeterList)))) != len(list(itertools.chain.from_iterable(delimeterList))):
        print "configs can not overlap"
    
    # ---- sort so that we can permut properly
    sortedLOfParetoSet = sorted(lOfPointSet, key = lambda pointSetElm: pointSetElm.get_delimeter()[0]) 
    #l of all the portion of the pts's config in a perto set b/w the 2 delimter
    lOfParetoSetWithConfigChopped = [] 
    for pointSetElement in sortedLOfParetoSet: 
        pointSet = pointSetElement.get_points()
        configChopped = map(lambda x: x.get_setUp()[pointSetElement.get_delimeter()[0]:
            pointSetElement.get_delimeter()[1]], pointSet)
        lOfParetoSetWithConfigChopped.append(configChopped)

    
    permutedConfig = list(itertools.product(*lOfParetoSetWithConfigChopped))
    lOfNewSetUp = [] 
    for elm in permutedConfig: 
        mergedConfig = list(itertools.chain.from_iterable(elm)) 
        lOfNewSetUp.append(mergedConfig)
    newListOfPoints = []   
    
    
    possibly_worse_case_setup = generate_possibly_worse_case_setup(accurateSetUp, settings_obj)
    possibly_worse_case_result_point = specializedEval(False, 1, settings_obj, possibly_worse_case_setup[0])
    possibly_worse_case_result_energy = possibly_worse_case_result_point.get_energy()
    possibly_worse_case_result_quality = possibly_worse_case_result_point.get_quality()   
    def specializedEval_with_arg(setUp):
        return specializedEval(True, possibly_worse_case_result_quality, settings_obj, setUp)
    
    #--combining the points 
    if (settings_obj.runMode == "parallel"):
        pool = multiprocessing.Pool()
        newListOfPoints = pool.map(specializedEval_with_arg, lOfNewSetUp)
    elif (settings_obj.runMode == "serial"):
        newListOfPoints = map(specializedEval_with_arg, lOfNewSetUp)
    else: 
        print ("*******ERROR: this runMode not defined*****")
        sys.exit()
    
    #for element in lOfNewSetUp:
        #newListOfPoints.append(specializedEval(element))
    
    #---------------------------------
    #---------------------------------
    # lOfParetoPoints = pareto_frontier(newListOfPoints, maxX= True, maxY = False)
    # ---- adding the first blocks pareto points to the list
    # newListOfPoints += pointSet[0].get_points()
    lOfParetoPoints = pareto_frontier(newListOfPoints, settings_obj.maxX, settings_obj.maxY, settings_obj)
    finalResultFileFullAddress = rootResultFolderName + "/" + finalResultFileName
    

     #---all points of the combination 
    lOfQualityValue_after_combining_all_points = map(lambda x: x.get_quality(), newListOfPoints)
    lOfEnergy_after_combining_all_points = map(lambda x: x.get_energy(), newListOfPoints)
    
    #---pareto points of the combination 
    lOfQualityValue_after_combining_pareto_points = map(lambda x: x.get_quality(), lOfParetoPoints)
    lOfEnergy_after_combining_pareto_points = map(lambda x: x.get_energy(), lOfParetoPoints)

    #---pareto points for ref 
    lOfParetoPoints_ref = getPoints("pareto_of_heur_flattened") #getting the ref points
    lOfQualityValue_ref = map(lambda x: x.get_quality(), lOfParetoPoints_ref)
    lOfEnergyValue_ref = map(lambda x: x.get_energy(), lOfParetoPoints_ref)
    
    #---all points for s2
    lOfParetoPoints_s2 = getPoints("all_of_s2") #getting the ref points
    lOfQualityValue_s2 = map(lambda x: x.get_quality(), lOfParetoPoints_s2)
    lOfEnergyValue_s2 = map(lambda x: x.get_energy(), lOfParetoPoints_s2)

    
    #---all points for s3
    lOfParetoPoints_s3 = getPoints("all_of_s3") #getting the ref points
    lOfQualityValue_s3 = map(lambda x: x.get_quality(), lOfParetoPoints_s3)
    lOfEnergyValue_s3 = map(lambda x: x.get_energy(), lOfParetoPoints_s3)



    PIK = "all_of_combined" 
    with open(PIK, "wb") as f:
        for point in newListOfPoints: 
            pickle.dump(copy.deepcopy(point), f)


    
    PIK = "pareto_of_combined" 
    with open(PIK, "wb") as f:
        for point in lOfParetoPoints: 
            pickle.dump(copy.deepcopy(point), f)


#    if settings_obj.runToolChainGenerateGraph: 
#        generateGraph(lOfQualityValue_ref,lOfEnergyValue_ref, "quality", "Energy", "*") #flattened version
#        
#        generateGraph(lOfQualityValue_s2,lOfEnergyValue_s2, "quality", "Energy", "o")   #after s2
#        generateGraph(lOfQualityValue_s3,lOfEnergyValue_s3, "quality", "Energy", "+")   #after s3
#        # ---- combine
#        generateGraph(lOfQualityValue_after_combining_all_points,
#                lOfEnergy_after_combining_all_points, "quality", 
#                "Energy", "x")                                                          #simple permutation
#        
#        generateGraph(lOfQualityValue_after_combining_pareto_points,
#                lOfEnergy_after_combining_pareto_points, "quality", 
#                "Energy", "^")                                                          #pareto of(permutation)
#        
#        pylab.savefig(finalResultFileFullAddress[:-4]+".png") #saving the figure generated by generateGraph
#        
    
    

    # lOfParetoPoints = [] 
    # with open(PIK, "rb") as f:
        # while True: 
            # try: 
                # point = pickle.load(f)
                # print point 
                # lOfParetoPoints.append(point) 
                # # listOfPeople.append(copy.copy(person))# 
            # except Exception as ex:
                # if not (type(ex).__name__ == "EOFError"):
                    # print type(ex).__name__ 
                    # print ex.args
                    # print "something went wrong"
    #  pickled_results2           break
   #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ 
    # generateGraph(map(lambda x: x.get_PSNR(), lOfParetoPoints), map(lambda x: x.get_energy(), lOfParetoPoints), "PSNR", "Energy", "*")
    
    # plt.show() 
    

#def main():
#    inputFileName = "pareto_set_file.txt" #file containing paretoSets
#    point_combine(inputFileName)

if __name__ == "__main__":
    run_combine_pareto()
#if __name__ == "__main__":
#    main()
