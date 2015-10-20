import pickle
import copy
import pylab
import sys
import os
from plot_generation import *
import matplotlib.pyplot as plt

from inputs import *#this file contains all the inputs
from scipy.spatial import distance
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
import pickle
from points_class import *
from list_all_files_in_a_folder import *
from src_parse_and_apx_op_space_gen import *
#**--------------------**
#**--------------------**
#----disclaimers::: if dealingwith Pic and we are feeding couple of operands,
#----we need to collect their psnr in a list and get an avg. This should be done
#--- this requries adding a PSNR (or SNR) list to the points
#--- avgAccuratValue needs to be set
#**--------------------**
#--------------------**


def get_pareto_set(file1_name):     
    lOfParetoSet =[]
    with open(file1_name, "rb") as f:
        # pickle.load(f)
        while True: 
            try: 
                paretoSet = pickle.load(f)
                lOfParetoSet.append(paretoSet) 
                # listOfPeople.append(copy.copy(person))# 
            except Exception as ex:
                if not (type(ex).__name__ == "EOFError"):
                    print type(ex).__name__ 
                    print ex.args
                    print "something went wrong"
                break

    # lOfParetoPoints = pareto_frontier(lOfPoints, maxX= True, maxY = False)
    return lOfParetoSet


 

def pareto_combine(srcFile):
    inputObj = inputClass()
    inputObj.expandAddress()
    CSrcFolderAddress = inputObj.CSrcFolderAddress
    lOfCSrcFileAddress = inputObj.lOfCSrcFileAddress 
    generateMakeFile = inputObj.generateMakeFile
    rootFolder = inputObj.rootFolder 
    AllInputScenariosInOneFile = inputObj.AllInputScenariosInOneFile
    AllInputFileOrDirectoryName = inputObj.AllInputFileOrDirectoryName 
    finalResultFileName = inputObj.finalResultFileName
    PIK = inputObj.PIK
        
    
    energy = []
    error = []
    config = []
    inputFileNameList = []
    lOfAccurateValues = []
    
    
    rootFolder = inputObj.rootFolder 
    rootResultFolderName = rootFolder + "/" + settings.generatedTextFolderName
    rootResultFolderName = rootFolder + "/" + settings.generatedTextFolderName
    AllOperandsFolderName = rootResultFolderName + "/" + settings.AllOperandsFolderName
    inputNumber = 0 
    nameOfAllOperandFilesList = getNameOfFilesInAFolder(AllOperandsFolderName)
    
    CSourceOutputForVariousSetUpFileName =  rootResultFolderName + "/" + settings.rawResultFolderName + "/" + settings.csourceOutputFileName + str(inputNumber) + ".txt" #where to collect C++ source results
    operatorSampleFileFullAddress = rootResultFolderName + "/"+ settings.operatorSampleFileName
    executableName = "tool_exe" #src file to be analyzed
    executableInputList = [] 
    CBuildFolder = rootFolder + "/" + settings.CBuildFolderName
    AllOperandsFolderName = rootResultFolderName + "/" + settings.AllOperandsFolderName
    

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
        lAllOpsInSrcFile += sourceFileParse(CSrcFileAddressItem)

    nameOfAllOperandFilesList = getNameOfFilesInAFolder(AllOperandsFolderName)
    allPossibleScenariosForEachOperator = generateAllPossibleScenariosForEachOperator(rootResultFolderName, lAllOpsInSrcFile)


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
        accurateSetUp,_,_= generateAccurateScenario(allPossibleScenariosForEachOperator)
        apxIndexSetUp = 0 #zero is associated with the accurate results (this is a contract that needs to be obeyed)
        # status, setUp = generateAPossibleApxScenarios(rootResultFolderName + "/" + settings.AllPossibleApxOpScenarios, allPossibleApxScenarioursList , apxIndexSetUp, mode) 
        
        #---------guide:::  erasing the previuos content of the file
        CSourceOutputForVariousSetUpP = open(CSourceOutputForVariousSetUpFileName, "w").close()
        #---------guide:::  modify the operator sample file
        modifyOperatorSampleFile(operatorSampleFileFullAddress, accurateSetUp)
        #---------guide:::  run the CSrouce file with the new setUp(operators)
        make_run(executableName, executableInputList, rootResultFolderName, CSourceOutputForVariousSetUpFileName, CBuildFolder, operandSampleFileName)
        #---------guide::: error
        accurateValues = extractAccurateValues(CSourceOutputForVariousSetUpFileName)
        lOfAccurateValues.append(accurateValues)
        # lOfOperandSet.append(newOperand)
        #---------guide:::  make a apx set up and get values associated with it
     


    def specializedEval(individual):
        newPoint = points() 
        newPoint.set_dealing_with_pics(eval(inputObj.dealingWithPics))
        for operandIndex, operandSampleFileName in enumerate(nameOfAllOperandFilesList):
            print "here is the individual" 
            print individual 
            energyValue = [getEnergy(individual)]
            open(CSourceOutputForVariousSetUpFileName, "w").close()

            modifyOperatorSampleFile(operatorSampleFileFullAddress, individual)
            make_run(executableName, executableInputList, rootResultFolderName, CSourceOutputForVariousSetUpFileName, CBuildFolder, operandSampleFileName)
            errorValue = [extractErrorForOneInput(CSourceOutputForVariousSetUpFileName , lOfAccurateValues[operandIndex])]
            configValue = [individual]
            rawValues = [extractCurrentValuesForOneInput(CSourceOutputForVariousSetUpFileName)]


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
            newPoint.calculate_SNR()
        
        return newPoint


    lOfParetoSetDirctions  = [] 
    # ---- get paretoSet
    lOfParetoSet = get_pareto_set(srcFile) 
    print "number of pareto set is " + str(len(lOfParetoSet)) 
    for paretoSet in lOfParetoSet:
        lOfParetoSetDirctions.append(paretoSet.get_direction())
    print lOfParetoSetDirctions 
     
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
    for paretoSetElm in lOfParetoSet:
        delimeterList.append(range(paretoSetElm.get_delimeter()[0], paretoSetElm.get_delimeter()[1]))

    if len(set(list(itertools.chain.from_iterable(delimeterList)))) != len(list(itertools.chain.from_iterable(delimeterList))):
        print "configs can not overlap"
    
    # ---- sort so that we can permut properly
    sortedLOfParetoSet = sorted(lOfParetoSet, key = lambda paretoSetElm: paretoSetElm.get_delimeter()[0]) 
    #l of all the portion of the pts's config in a perto set b/w the 2 delimter
    lOfParetoSetWithConfigChopped = [] 
    for paretoSetElement in sortedLOfParetoSet: 
        paretoPoints = paretoSetElement.get_pareto_values()
        configChopped = map(lambda x: x.get_setUp()[paretoSetElement.get_delimeter()[0]:
            paretoSetElement.get_delimeter()[1]], paretoPoints)
        lOfParetoSetWithConfigChopped.append(configChopped)

    
    permutedConfig = list(itertools.product(*lOfParetoSetWithConfigChopped))
    lOfNewSetUp = [] 
    for elm in permutedConfig: 
        mergedConfig = list(itertools.chain.from_iterable(elm)) 
        lOfNewSetUp.append(mergedConfig)
    newListOfPoints = []   
    for element in lOfNewSetUp:
        newListOfPoints.append(specializedEval(element))
    

    
    # lOfParetoPoints = pareto_frontier(newListOfPoints, maxX= True, maxY = False)
    # ---- adding the first blocks pareto points to the list
    newListOfPoints += lOfParetoSet[0].get_pareto_values()
    lOfParetoPoints = pareto_frontier(newListOfPoints, maxX= True, maxY = False)
    lOfSNR = [] 
    lOfEnergy = [] 
    finalResultFileFullAddress = rootResultFolderName + "/" + finalResultFileName
    for point in lOfParetoPoints:
        # if point.get_SNR() != avgAccurateValue:
        if point.get_SNR() < 1000000:
            lOfSNR.append(point.get_SNR())
            lOfEnergy.append(point.get_energy())
    generateGraph(lOfSNR,lOfEnergy, "SNR", "Energy", "^")
    pylab.savefig(finalResultFileFullAddress[:-4]+".png") #saving the figure generated by generateGraph
    
    PIK = "pareto_curved_combined_pickled" 
    with open(PIK, "wb") as f:
       for point in lOfParetoPoints: 
           pickle.dump(copy.deepcopy(point), f)


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
    

def main():
    inputFileName = "pareto_set_file.txt" #file containing paretoSets
    pareto_combine(inputFileName)


if __name__ == "__main__":
    main()
