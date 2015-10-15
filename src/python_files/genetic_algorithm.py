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
        
        yield config[number]
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
    if operatorToChooseIndex in ignoreIndexList:
        return newSetUp,
    operatorModified = modifyOperatorSubSetupExactly(setUp[operatorToChooseIndex], numberOfApxBits) 
    newSetUp[operatorToChooseIndex] = operatorModified
    return newSetUp,
    

def generateInitialPopulation(accurateSetUp, numberOfIndividualsToStartWith,inputObj, ignoreIndexList):
    population = [] 
    population.append(accurateSetUp) 
    for count in range(numberOfIndividualsToStartWith - 1):
        newSetUp = copy.copy(accurateSetUp)
        for index, element in enumerate(newSetUp): 
            if (index in ignoreIndexList):
                continue
            # operatorToChooseIndex = random.choice(range(0, len(accurateSetUp)))
            # numberOfApxBits = int(random.gauss(10 , 4))
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

   

def run_spea2(NGEN, MU, LAMBDA, CXPB, MUTPB, population, 
        CSourceOutputForVariousSetUpFileName, operatorSampleFileFullAddress, 
        executableName, executableInputList, rootResultFolderName, 
        CBuildFolder, operandSampleFileName, lOfAccurateValues, toolbox, nameOfAllOperandFilesList, inputObj, ignoreIndexList):
     
    def specializedEval(individual):
        newPoint = points() 
        newPoint.set_dealing_with_pics(eval(inputObj.dealingWithPics))
        for operandIndex, operandSampleFileName in enumerate(nameOfAllOperandFilesList):
            energyValue = [getEnergy(individual)]
            open(CSourceOutputForVariousSetUpFileName, "w").close()
             
            modifyOperatorSampleFile(operatorSampleFileFullAddress, individual)
            make_run(executableName, executableInputList, rootResultFolderName, CSourceOutputForVariousSetUpFileName, CBuildFolder, operandSampleFileName)
            print "here is the accurate" + str(lOfAccurateValues) 
            errorValue = [extractErrorForOneInput(CSourceOutputForVariousSetUpFileName , lOfAccurateValues[operandIndex])]
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
            newPoint.calculate_SNR()
        # if (inputObj.dealingWithPics):
        #     newPoint.calculate_PSNR()
        # print "here is the snr " + str(newPoint.get_SNR())
        # sys.exit() 
        if eval(inputObj.dealingWithPics):
            return (newPoint.get_energy(), newPoint.get_PSNR())
        else:
            return (newPoint.get_energy(), newPoint.get_SNR())

       
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    a = [1,2] 
    b = [1,2] 
    toolbox.register("evaluate", specializedEval)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", specializedMutate, ignoreIndexList) 
    toolbox.register("select", tools.selSPEA2)

    # population = eaMuPlusLambda_redefined(population, toolbox, MU, LAMBDA, CXPB, MUTPB, NGEN)
    algorithms.eaMuPlusLambda(population, toolbox, MU, LAMBDA, CXPB, MUTPB, NGEN, stats)
    # nonDominatedSort = tools.sortNondominated(population, len(population))
    # print nonDominatedSort 
    return population



