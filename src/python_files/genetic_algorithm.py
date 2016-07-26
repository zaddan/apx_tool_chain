import random
import sys
import copy
import math
import numpy
import settings 
from deap import algorithms
from points_class import *
from deap import base
from deap import creator
from deap import tools
from simulating_annealer import *
from inputs import *
#**--------------------**
#**--------------------**
#----disclaimers::: if dealingwith Pic and we are feeding couple of operands,
#----we need to collect their psnr in a list and get an avg. This should be done
#--- this requries adding a PSNR (or SNR) list to the points
#**--------------------**
#--------------------**

def return_conf(config):
    number = 0 
    allConfsLenght = len(config) 
    while True:
        if (number >= allConfsLenght):
            return
        
        yield config[number][2]
        number += 1


def evalOneMax(individual):
    return sum(individual),

# def specializedMutate(individual):
    # individual[1] = int(random.gauss(16 , 5.2))
    # individual[0] = int(random.gauss(16 , 5.2))
    # return individual, 

def modifyOperatorSubSetupExactly(operator, numberOfApxBits):
    operatorType =  operator[0].replace("'", "")
     
    if operatorType == "btm":  
        return ['btm' , operator[1] , numberOfApxBits]
    elif operatorType == "bta":  
        return ['bta' ,operator[1], numberOfApxBits, operator[3], operator[4]] 
    else:
        print "***************ERROR***************"
        print "the operator type with the name of " + operatorType + "is not acceptable"
        exit()

def specializedMutate(ignoreIndexList, setUp):
    newSetUp = copy.copy(setUp)
    operatorToChooseIndex = random.choice(range(0, len(setUp)))
    # numberOfApxBits = int(random.gauss(10 , 5.2))
    numberOfApxBits = int(random.choice(range(settings.apxLowBound, settings.apxUpBound)))
    newSetUp[operatorToChooseIndex] = numberOfApxBits 
#    if operatorToChooseIndex in ignoreIndexList:
#        return newSetUp,
#    operatorModified = modifyOperatorSubSetupExactly(setUp[operatorToChooseIndex], numberOfApxBits) 
#    newSetUp[operatorToChooseIndex] = operatorModified
    return newSetUp,
    

def generate_possibly_worse_case_setup(accurateSetUp):
    population = [] 
    newSetUp = copy.copy(accurateSetUp)
    for index, element in enumerate(newSetUp): 
        # operatorToChooseIndex = random.choice(range(0, len(accurateSetUp)))
        # numberOfApxBits = int(random.gauss(10 , 4))
        numberOfApxBits = settings.worseCase
        
        operatorModified = modifyOperatorSubSetupExactly(accurateSetUp[index], numberOfApxBits) 
        newSetUp[index] = operatorModified
    population.append(copy.deepcopy(newSetUp)) 
    return population
 

def generateInitialPopulation(accurateSetUp, numberOfIndividualsToStartWith,inputObj, ignoreIndexList, limitedListValues, limitedListIndecies):
    population = [] 
    population.append(accurateSetUp) 
    for count in range(numberOfIndividualsToStartWith - 1):
        newSetUp = copy.copy(accurateSetUp)
        for index, element in enumerate(newSetUp): 
            if (index in ignoreIndexList):
                continue
            # operatorToChooseIndex = random.choice(range(0, len(accurateSetUp)))
            # numberOfApxBits = int(random.gauss(10 , 4))
            if (index in limitedListIndecies):
                numberOfApxBits = int(random.choice(limitedListValues[index]))
            else: 
                numberOfApxBits = int(random.choice(range(settings.apxLowBound, settings.apxUpBound)))
            
            operatorModified = modifyOperatorSubSetupExactly(accurateSetUp[index], numberOfApxBits) 
            newSetUp[index] = operatorModified
        population.append(copy.deepcopy(newSetUp)) 
    return population
 

def doNothing(individual):
    return individual,


# ---- redefinging the eaMulPlusLambda to have a better understanding
# ---- and control over it
def eaMuPlusLambda_redefined(population, toolbox, MU, LAMBDA, CXPB, MUTPB, NGEN):
    for i in range(NGEN):
        # ----determine the offspring and evaluate the fitness,w
        offspring = algorithms.varOr(population, toolbox, LAMBDA, CXPB, MUTPB)
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        
        # ---- evaluate fitness values for the population
        invalid_ind = [ind for ind in population if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        
        population = toolbox.select(offspring + population, MU) 

    return population

   
"""
def run_spea2(NGEN, MU, LAMBDA, CXPB, MUTPB, population, 
        CSourceOutputForVariousSetUpFileName, operatorSampleFileFullAddress, 
        executableName, executableInputList, rootResultFolderName, 
        CBuildFolder, operandSampleFileName, lOfAccurateValues, toolbox, nameOfAllOperandFilesList, inputObj, ignoreIndexList):
     
    def specializedEval(individual):
        print "started specialized Eval" 
        sys.stdout.flush() 
        newPoint = points() 
        newPoint.set_dealing_with_pics(eval(inputObj.dealingWithPics))
        for operandIndex, operandSampleFileName in enumerate(nameOfAllOperandFilesList):
            print "operandblah blah" + str(operandIndex) 
            energyValue = [getEnergy(individual)]
            open(CSourceOutputForVariousSetUpFileName, "w").close()
             
            modifyOperatorSampleFile(operatorSampleFileFullAddress, individual)
            if not(errorTest): #if errorTest generate acc.txt and apx.txt which contain accurate and apx values
                make_run(executableName, executableInputList, rootResultFolderName, CSourceOutputForVariousSetUpFileName, CBuildFolder, operandSampleFileName, inputObj.bench_suit_name)
            # print "here is the accurate" + str(lOfAccurateValues) 
            
            if (errorTest):
                newPath = "/home/local/bulkhead/behzad/usr/local/apx_tool_chain/src/python_files/scratch/apx.txt"
                print "error values are " 
                print errorValue 
                sys.exit() #temporary    errorValue = [extractErrorForOneInput(newPath, lOfAccurateValues[operandIndex])]
            else:
                errantValues =  extractCurrentValuesForOneInput(CSourceOutputForVariousSetUpFileName)
                errorValue = [calculateError(lOfAccurateValues[operandIndex],errantValues, error_mode)]

           
            configValue = [individual]
            rawValues = [extractCurrentValuesForOneInput(CSourceOutputForVariousSetUpFileName)]
            # print "where" 
            # print errorValue 
            newPoint.append_raw_values(rawValues[0])  
            newPoint.append_error(errorValue[0])
            newPoint.set_energy(energyValue[0])
            newPoint.set_setUp(configValue[0])
            newPoint.append_lOf_operand(get_operand_values(operandSampleFileName))
            newPoint.append_accurate_values(lOfAccurateValues[operandIndex])
            newPoint.set_dealing_with_pics(eval(inputObj.dealingWithPics)) 
            newPoint.set_dealing_with_pics(eval(inputObj.dealingWithPics)) 
            newPoint.set_input_obj(inputObj)
            if (eval(inputObj.dealingWithPics)):
                newPoint.calculate_PSNR()
        

         
        # print "here is the config " + str(newPoint.get_setUp())
        if not(eval(inputObj.dealingWithPics)):
            newPoint.calculate_quality()
            print "errors" 
            print newPoint.get_lOfError()
            print "here is my quality values"
            print newPoint.get_quality()
        # if (inputObj.dealingWithPics):
        #     newPoint.calculate_PSNR()
        if eval(inputObj.dealingWithPics):
            return (newPoint.get_energy(), newPoint.get_PSNR())
        else:
            return (newPoint.get_energy(), newPoint.get_quality())

       
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    a = [1,2] 
    b = [1,2] 
    #pool = multiprocessing.Pool() 
    #toolbox.register("map", pool.map) 

    toolbox.register("evaluate", specializedEval)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", specializedMutate, ignoreIndexList) 
    toolbox.register("select", tools.selSPEA2)

    # population = eaMuPlusLambda_redefined(population, toolbox, MU, LAMBDA, CXPB, MUTPB, NGEN)
    algorithms.eaMuPlusLambda(population, toolbox, MU, LAMBDA, CXPB, MUTPB, NGEN, stats)
    # nonDominatedSort = tools.sortNondominated(population, len(population))
    # print nonDominatedSort 
    print "end specialized Eval" 
    sys.stdout.flush() 
    return population
"""
def specializedEval(normalize,possibly_worse_case_result_quality,  mold, ignoreListIndecies, accurateSetUp, inputObj, nameOfAllOperandFilesList, rootResultFolderName,executableName,
        executableInputList, CBuildFolder, operandSampleFileName, lOfAccurateValues, allPointsTried, individual):
        exe_annex = 0
        if (runMode == "parallel"): 
            if(multiprocessing.current_process()._identity == ()):
                exe_annex = 0
            else:
                exe_annex = multiprocessing.current_process()._identity[0] 
            print "proccess id: " 

        #print "-----end" 
        #print multiprocessing.current_process()
        #--- zeroing out the ignoreList 
        for x in ignoreListIndecies:
            mold[x][2] = 0

        newSetUp = modifyMold(accurateSetUp, individual) 
        sys.stdout.flush() 
        newPoint = points() 
        newPoint.set_dealing_with_pics(eval(inputObj.dealingWithPics))
        for operandIndex, operandSampleFileName in enumerate(nameOfAllOperandFilesList):
            energyValue = [getEnergy(newSetUp)]

            if (runMode == "parallel"): 
                CSourceOutputForVariousSetUpFileName =  rootResultFolderName + "/" + settings.rawResultFolderName + "/" + settings.csourceOutputFileName + str(exe_annex) + ".txt" #where to collect C++ source results
                operatorSampleFileFullAddress = rootResultFolderName + "/"+ settings.operatorSampleFileName + str(exe_annex) + ".txt"
            else: 
                CSourceOutputForVariousSetUpFileName =  rootResultFolderName + "/" + settings.rawResultFolderName + "/" + settings.csourceOutputFileName + str(0) + ".txt" #where to collect C++ source results
                operatorSampleFileFullAddress = rootResultFolderName + "/"+ settings.operatorSampleFileName + str(0) + ".txt"

            open(CSourceOutputForVariousSetUpFileName, "w").close()

            modifyOperatorSampleFile(operatorSampleFileFullAddress, newSetUp)


            if not(errorTest): #if errorTest generate acc.txt and apx.txt which contain accurate and apx values
                make_run(executableName, executableInputList, rootResultFolderName, CSourceOutputForVariousSetUpFileName, CBuildFolder, operandSampleFileName, inputObj.bench_suit_name,exe_annex) 
            # print "here is the accurate" + str(lOfAccurateValues) 
            if (errorTest):
                newPath = "/home/local/bulkhead/behzad/usr/local/apx_tool_chain/src/python_files/scratch/apx.txt"
                if(errorTest):
                    print "Acurate Vals:"
                    print lOfAccurateValues
                    errantValues =  extractCurrentValuesForOneInput(newPath)
                    print "errant Vals:" 
                    print errantValues
                    errorValue = [calculateError( lOfAccurateValues[operandIndex],errantValues)]

                    print "error Vals:"
                    print errorValue 
                    print "------" 
            else:
                errantValues =  extractCurrentValuesForOneInput(CSourceOutputForVariousSetUpFileName)
                errorValue = [calculateError(lOfAccurateValues[operandIndex], errantValues)]
                if (settings.DEBUG):
                    print "Acurate Vals:" + str(lOfAccurateValues)
                    print "errant Vals:" +str(errantValues)
                    print "error Vals:" + str(errorValue)

            configValue = [newSetUp]
            rawValues = [extractCurrentValuesForOneInput(CSourceOutputForVariousSetUpFileName)]
            #print errorValue
            # print "where" 
            # print errorValue 
            newPoint.append_raw_values(rawValues[0])  
            newPoint.append_error(errorValue[0])
            newPoint.set_energy(energyValue[0])
            newPoint.set_setUp(configValue[0])
            newPoint.append_lOf_operand(get_operand_values(operandSampleFileName))
            newPoint.append_accurate_values(lOfAccurateValues[operandIndex])
            newPoint.set_dealing_with_pics(eval(inputObj.dealingWithPics)) 
            newPoint.set_dealing_with_pics(eval(inputObj.dealingWithPics)) 
            newPoint.set_input_obj(inputObj)
            if (eval(inputObj.dealingWithPics)):
                newPoint.calculate_PSNR()



        # print "here is the config " + str(newPoint.get_setUp())
        if not(eval(inputObj.dealingWithPics)):
            newPoint.calculate_quality(normalize, possibly_worse_case_result_quality)
            if (settings.DEBUG):
                print "quality is: " + str(newPoint.get_quality())
            if (errorTest):
                print "quality is" 
                print newPoint.get_quality()
                sys.exit()
            #print "here is my quality values"
            #print newPoint.get_quality()
        if eval(inputObj.dealingWithPics):
            allPointsTried.append(newPoint)
            return (newPoint.get_energy(), newPoint.get_PSNR())
        else:
            allPointsTried.append(newPoint)
            return (newPoint.get_energy(), newPoint.get_quality())







def run_spea2(population, 
        CSourceOutputForVariousSetUpFileName, operatorSampleFileFullAddress, 
        executableName, executableInputList, rootResultFolderName, 
        CBuildFolder, operandSampleFileName, lOfAccurateValues, nameOfAllOperandFilesList, inputObj, ignoreListIndecies, possibly_worse_case_result_quality,accurateSetUp, allConfs):
    
    
    allPointsTried = []
    if (settings.maxX):
            x_direction = 1
    else:
        x_direction = -1

    if (settings.maxY):
        y_direction = 1
    else:
        y_direction = -1


    
    
    NGEN = settings.NGEN
    MU = settings.MU#number of indi for the next gen
    LAMBDA = settings.LAMBDA#number of children
    CXPB = settings.CXPB 
    MUTPB = settings.MUTPB
    creator.create("FitnessMin", base.Fitness, weights=(x_direction, y_direction))
    creator.create("Individual", list, fitness=creator.FitnessMin)
    toolbox = base.Toolbox()
    
    # generating the initial population
    
    
    
    # Operator registering
    toolbox.register("individual", tools.initRepeat, creator.Individual)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    toolbox.register("evaluate", specializedEval, True, possibly_worse_case_result_quality, accurateSetUp, ignoreListIndecies, accurateSetUp, inputObj, nameOfAllOperandFilesList, rootResultFolderName,
            executableName, executableInputList, CBuildFolder, operandSampleFileName, lOfAccurateValues, allPointsTried)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", specializedMutate, ignoreListIndecies)
    toolbox.register("select", tools.selSPEA2)
    if (runMode == "parallel"): 
        #the_lock = multiprocessing.Lock() 
        #pool = multiprocessing.Pool() 
        toolbox.register("map", pool.map)
        allPointsTried = [] #since deap is not compatible with multiprocessor
                            #library (when it comes to sharing a list accross
                            #processes), we set allPointsTried to empty to 
                            #avoid any unwanted consequences

    #--run the genetic algo
    print("\n......running genetic algo\n")
    for index in range(len(allConfs)):
            myGenerator = return_conf(allConfs[index])
            population.append(toolbox.individual(lambda: next(myGenerator), len(allConfs[index])))

    
    algorithms.eaMuPlusLambda(population, toolbox, MU, LAMBDA, CXPB, MUTPB, NGEN, stats)
    return allPointsTried, population

