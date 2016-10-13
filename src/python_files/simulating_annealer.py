import random
import math
from points_class import *
from extract_result_properties import *
from modify_operator_sample_file import *
from src_parse_and_apx_op_space_gen import *
from extract_pareto_set_from_raw_material import *
import copy
from scipy.spatial import distance
from misc import *
from plot_generation import *
import pylab
def getFirstTwo(myList):
    if not(type(myList) == list):
        myList = myList.split(" ")
        myList2 = [int(myListElement) for myListElement in myList[1:]]
        myList = [myList[0]]+ myList2
    
    return (myList[0].replace("'", ""),int(myList[1]) - int(myList[2]))





def printToCommandPrompt(operatorModifiedIndex, oldSetUp, oldSetUpEnergy, oldSetUpNoise, newSetUp, newEnergy, newNoise, noiseRequirements, percentageCompleted):
    print "************************************************************************\n"
    print "noiseRequirement: " + str(noiseRequirements) 
    print "operatorModifiedIndex: " + "\\\\\\" + str(operatorModifiedIndex) + "////" +  "  operatorModified: " + str(oldSetUp[operatorModifiedIndex])
    print "old setUp: " + str(oldSetUp) 
    print "old setUpEnergy: " + str(oldSetUpEnergy) 
    print "oldSetUpNoise : " + str(oldSetUpNoise) 
    
    print "new setUp: " + str(newSetUp) 
    print "new Energy: " + str(newEnergy)
    print "new Noise: " + str(newNoise) 
    
    print "percentageCompleted: " + str(percentageCompleted) + "%"
    
    print "************************************************************************"

   

def printToProgressor(annealerProgressionOutputFileP, operatorModifiedIndex, oldSetUp, oldSetUpEnergy, oldSetUpNoise, newSetUp, newEnergy, newNoise, noiseRequirements, percentageCompleted):
    annealerProgressionOutputFileP.write("************************************************************************\n")
    annealerProgressionOutputFileP.write("noiseRequirement: " + str(noiseRequirements) + "\n")
    annealerProgressionOutputFileP.write("operatorModifiedIndex: " + "\\\\\\" + str(operatorModifiedIndex) + "////" +  "  operatorModified: " + str(oldSetUp[operatorModifiedIndex]) +  "\n" )
    annealerProgressionOutputFileP.write("old setUp: " + str(oldSetUp) + "\n")
    annealerProgressionOutputFileP.write("old setUpEnergy: " + str(oldSetUpEnergy) + "\n")
    annealerProgressionOutputFileP.write("oldSetUpNoise: " + str(oldSetUpNoise) + "\n")
    
    annealerProgressionOutputFileP.write("new setUp: " + str(newSetUp) + "\n")
    annealerProgressionOutputFileP.write("new Energy: " + str(newEnergy)+ "\n")
    annealerProgressionOutputFileP.write("new Noise: " + str(newNoise) + "\n")
    
    annealerProgressionOutputFileP.write("percentageCompleted: " + str(percentageCompleted) + " %" + "\n")
    
    annealerProgressionOutputFileP.write("************************************************************************\n")

def updateOperatorPickTemperature(T, k):
    if int(T-k) < 0:
        return 0
    else:
        return int(T - k)
    #return int(math.ceil(T - k))




def updateNumberOfApxBitsTemperature(T, k):
    #print "\n" 
    percentageCompleted = (100 - 100*float((T-k)/T)) 
    return (T - k, percentageCompleted) 
    #return int(math.ceil(T - k))

def get_neighbors(i, L):
    assert L > 1 and i >= 0 and i < L
    if i == 0:
        return [1]
    elif i == L - 1:
        return [L - 2]
    else:
        return [i - 1, i + 1]


def chooseAnOperatorIndex(operatorList):
    return random.choice(range(0, len(operatorList)))


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


def modifyOperatorSubSetup2(lOfAcceptableOperatorOptions):
#    print "hre is the op"
#    print operator
    
    newOperator = random.choice(lOfAcceptableOperatorOptions)
    return newOperator 
    # operatorType =  operator[0].replace("'", "")
    # totalNumberOfBits =  operator[1]
    # oldNumberOfApxBits = operator[2]
     
    
    # upperRadius = totalNumberOfBits - oldNumberOfApxBits
    # lowerRadius = oldNumberOfApxBits
   
    
    # upperBound = int(T*upperRadius)
    # lowerBound = int(T*lowerRadius)
    # randRange = range(-lowerBound, upperBound)
    
    # if len(randRange) == 0:
        # randRange = [0]
    
    # newNumberOfApxBits = random.choice(range(0,5, 1))
    # #newNumberOfApxBits = oldNumberOfApxBits + random.choice(randRange)
# #    print "here is the T" + str(T) 
# #    print "here is the upper " + str(upperRadius)
# #    print "here is the lower " + str(lowerRadius)
# #    print "upper bound " +str(upperBound)
# #    print "lower bound " +str(lowerBound)
# #    print "her is the newNumber " + str(newNumberOfApxBits) 
    # if newNumberOfApxBits < 0 or newNumberOfApxBits > 32:
        # newNumberOfApxBits = oldNumberOfApxBits
    # if operatorType == "btm":  
        # return ['btm' , operator[1] , newNumberOfApxBits]
    # elif operatorType == "bta":  
        # return ['bta' ,operator[1], newNumberOfApxBits, operator[3], operator[4]] 
    # else:
        # print "***************ERROR***************"
        # print "the operator type with the name of " + operatorType + "is not acceptable"
        # exit()

 

def modifyOperatorSubSetup(operator, T):
#    print "hre is the op"
#    print operator
    operatorType =  operator[0].replace("'", "")
    totalNumberOfBits =  operator[1]
    oldNumberOfApxBits = operator[2]
     
    upperRadius = totalNumberOfBits - oldNumberOfApxBits
    lowerRadius = oldNumberOfApxBits
   
    
    upperBound = int(T*upperRadius)
    lowerBound = int(T*lowerRadius)
    randRange = range(-lowerBound, upperBound)
    
    if len(randRange) == 0:
        randRange = [0]
    
    newNumberOfApxBits = random.choice(range(0,5, 1))
    #newNumberOfApxBits = oldNumberOfApxBits + random.choice(randRange)
#    print "here is the T" + str(T) 
#    print "here is the upper " + str(upperRadius)
#    print "here is the lower " + str(lowerRadius)
#    print "upper bound " +str(upperBound)
#    print "lower bound " +str(lowerBound)
#    print "her is the newNumber " + str(newNumberOfApxBits) 
    if newNumberOfApxBits < 0 or newNumberOfApxBits > 32:
        newNumberOfApxBits = oldNumberOfApxBits
    if operatorType == "btm":  
        return ['btm' , operator[1] , newNumberOfApxBits]
    elif operatorType == "bta":  
        return ['bta' ,operator[1], newNumberOfApxBits, operator[3], operator[4]] 
    else:
        print "***************ERROR***************"
        print "the operator type with the name of " + operatorType + "is not acceptable"
        exit()

    

def changeAllOperators(operatorList, numberOfApxBits):
    newSetUp = copy.copy(operatorList)
    for i in range(0, len(operatorList)):
        operatorIndex = i 
        operatorModified = modifyOperatorSubSetupExactly(operatorList[operatorIndex], numberOfApxBits) 
        newSetUp[operatorIndex] = operatorModified
    
    #modify the set up 
    return newSetUp







def make_move(tabuList, bestSetUp, T, maxNumberOfIteation, lOfAcceptableOperators):
    random.seed() 
    numberOfIteration = 0 
    while(True): 
        while(True): 
            operatorIndex = chooseAnOperatorIndex(bestSetUp) #randomly choose an operator to modify
            if (lOfAcceptableOperators[operatorIndex] > 1):
                break

        operatorModified = modifyOperatorSubSetup2(lOfAcceptableOperators[operatorIndex]) #randomly modify it (based on temperature)
        #modify the set up 
        newSetUp = copy.copy(bestSetUp)
        newSetUp[operatorIndex] = operatorModified
        if not(newSetUp in tabuList): 
            tabuList.append(newSetUp)
            break
        elif numberOfIteration > maxNumberOfIteation:
            break
        numberOfIteration +=1
    return newSetUp, operatorModified, operatorIndex


def getEnergy(config, settings_obj):
    energy = calculateEnergy(map(getFirstTwo, config), settings_obj)
    return energy 



def pickInitialSetUpIndexForSimmulatedAnnelaing(initialSetUp, noiseRequirements, operatorSampleFileFullAddress,executableName, executableInputList, rootResultFolderName, CSourceOutputForVariousSetUpFileName, CBuildFolder, operandSampleFileName, accurateValues):
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ 
    #---------guide:::  variables
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ 
    bestSetUp = initialSetUp  #setting the bestSetUp to initialSetup


    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ 
    #---------guide:::  get information regarding the initial Setup
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ 
    #---------guide:::  modify the operator sample file
    modifyOperatorSampleFile(operatorSampleFileFullAddress, initialSetUp)
    #---------guide:::  run the csrouce file with the new setup(operators)
    make_run(executableName, executableInputList, rootResultFolderName, CSourceOutputForVariousSetUpFileName, CBuildFolder, operandSampleFileName)
    #---------guide::: get the noise
    bestSetUpNoise = extractNoiseForOneInput(CSourceOutputForVariousSetUpFileName , accurateValues)


    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ 
    #---------guide:::  start the iterative process of simulated_annealing
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ 
    for i in range(0, 32, 1): 
        newSetUp = changeAllOperators(bestSetUp, i)
        #---------guide::: run to get the noise
        modifyOperatorSampleFile(operatorSampleFileFullAddress, newSetUp)
        #os.system("cp " + operatorSampleFileFullAddress + " " +  "bul"+ "_" + str(numberOfTries) )
        #if (numberOfTries > 4):
        #    sys.exit()
        
        
        #---------guide:::  run the csrouce file with the new setup(operators)
        make_run(executableName, executableInputList, rootResultFolderName, CSourceOutputForVariousSetUpFileName, CBuildFolder, operandSampleFileName)
        #os.system("cp " + CSourceOutputForVariousSetUpFileName + " " +"res" + "_" + str(numberOfTries))
        
        #---------guide::: noise
        newNoise = int(extractNoiseForOneInput(CSourceOutputForVariousSetUpFileName , accurateValues))
            
        #---------guide:::  deciding whether the output associated with the new set up acceptable
        oldSetUp = bestSetUp 
        oldSetUpNoise = bestSetUpNoise
        
        #---------guide::: the following 3 criterian needs to be satisfied
        #1. make sure new noise satisfies the requirement
        if (newNoise < int(noiseRequirements)):
            bestSetUp = newSetUp
            bestSetUpNoise = newNoise
    
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ 
    return bestSetUp




def improvedSimulatedAnnealing2(initialSetUp, noiseRequirement, numberOfApxBitsInitialTemperature, numberOfApxBitsStepSize, operatorPickInitialTemperature, operatorPickStepSize,
        operatorSampleFileFullAddress,executableName, executableInputList, rootResultFolderName, CSourceOutputForVariousSetUpFileName, CBuildFolder, operandSampleFileName, accurateValues,
        noiseRequirementPosition, totalNumberOfNoiseRequirements, lOfAcceptableOperators):
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ 
    #---------guide:::  variables
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ 
    progressionList = []  #this list helps us understand the progression of the oeprators that were swapped
    annealerProgressionOutputFileP = open(rootResultFolderName + "/" + settings.annealerProgressionOutputFileName, "a") #this file contains the informatino about the progression of the operators that were swapped
    percentageCompleted = 0  #what percentage of the iterations are completed (this is hard to calculate sometimes) as the number of iterations can vary dynamically (not always linearly)
    stepNumber = 0 #is used in modifying the temperature
    numberOfApxBitsTemperature = numberOfApxBitsInitialTemperature #one of the temperatures
    operatorPickTemperature = operatorPickInitialTemperature #one of the temperatues
    bestSetUp = initialSetUp  #setting the bestSetUp to initialSetup
    numberOfTries = 0 #indicates the number of times that we have try a new set of operator to acquire a better result. (note that this is not the number of time that we have been succesfully changed the operators)
    numberOfSuccessfulTries = 0 #number of tries that our operator substituion resulted in a better set of oprators (satisifes some constaint and took us closer to the final result)

    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ 
    #---------guide:::  get information regarding the initial Setup
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ 
    bestSetUpEnergy = getEnergy(initialSetUp) 
    #---------guide:::  erasing the previuos content of the file
    open(CSourceOutputForVariousSetUpFileName, "w").close()
    #---------guide:::  modify the operator sample file
    modifyOperatorSampleFile(operatorSampleFileFullAddress, initialSetUp)
    #---------guide:::  run the csrouce file with the new setup(operators)
    make_run(executableName, executableInputList, rootResultFolderName, CSourceOutputForVariousSetUpFileName, CBuildFolder, operandSampleFileName)
    #---------guide::: get the noise
    bestSetUpNoise = extractNoiseForOneInput(CSourceOutputForVariousSetUpFileName , accurateValues)

    newPoint = points()
    newPoint.set_noise(bestSetUpNoise)
    newPoint.set_energy(bestSetUpEnergy)
    newPoint.set_setUp(bestSetUp)
    newPoint.set_setUp_number(0)
    lOfParetoPoints = [newPoint]
    
    
    bestParetoPoint = newPoint
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ 
    #---------guide:::  start the iterative process of simulated_annealing
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ 
    tabuList = []  
    maxNumberOfIteation = 100 
    otherPoints = []  
    lOfPoints = []  
    while numberOfApxBitsTemperature > 0:
        foundBetter = False 
        for i in range(0, operatorPickTemperature, 1): 
            numberOfTries += 1 
            newSetUp, operatorModified, operatorModifiedIndex= make_move(tabuList,bestSetUp, numberOfApxBitsTemperature, maxNumberOfIteation, lOfAcceptableOperators)
            newEnergy = getEnergy(newSetUp) 
            
            open(CSourceOutputForVariousSetUpFileName, "w").close()
            modifyOperatorSampleFile(operatorSampleFileFullAddress, newSetUp)
            make_run(executableName, executableInputList, rootResultFolderName, CSourceOutputForVariousSetUpFileName, CBuildFolder, operandSampleFileName)
            newNoise = int(extractNoiseForOneInput(CSourceOutputForVariousSetUpFileName , accurateValues))
                
            oldSetUp = bestSetUp 
            oldSetUpEnergy =  bestSetUpEnergy
            oldSetUpNoise = bestSetUpNoise
            
            newPoint = points()
            newPoint.set_noise(newNoise)
            newPoint.set_energy(newEnergy)
            newPoint.set_setUp(newSetUp)
            newPoint.set_setUp_number(0)
            if (newNoise <= int(noiseRequirement)):
                lOfPoints.append(copy.deepcopy(newPoint))
                otherPoints.append(newPoint) 
                # lOfParetoPoints.append(copy.deepcopy(newPoint))
                lOfParetoPoints = pareto_frontier(lOfPoints, maxX= False, maxY = False)
                print "*****" 
                for element in lOfParetoPoints:
                    print "here is the list of pareto Points"
                    print element.get_noise()
                
                print "done with the list" 
                print "*****" 
                bestParetoPoint =  max(lOfParetoPoints, key= lambda x: x.get_noise())
                alpha = .3 
                lOfPointsSorted = sorted(lOfPoints, key=lambda x:
                        distance.euclidean((alpha*x.get_energy(), (1-alpha)*x.get_noise()),
                            (alpha*bestParetoPoint.get_energy(), (1 - alpha)*noiseRequirement)))
                bestPoint =  lOfPointsSorted[0]
                bestSetUp = bestPoint.get_setUp() 
                bestSetUpNoise = bestPoint.get_noise()
                bestSetUpEnergy = bestPoint.get_energy()

                printToProgressor(annealerProgressionOutputFileP, operatorModifiedIndex, oldSetUp, oldSetUpEnergy, oldSetUpNoise, newSetUp, newEnergy, newNoise, noiseRequirement, percentageCompleted) 
                if (bestSetUp == newPoint.get_setUp()): 
                    print "here we go" 
                    foundBetter = True 
                    numberOfSuccessfulTries += 1
                   
        if (foundBetter):
            annealerProgressionOutputFileP.write("&&&&&&&&&&&&&&&&&&&&&&&&&&&")
            printToProgressor(annealerProgressionOutputFileP, operatorModifiedIndex, oldSetUp, oldSetUpEnergy, oldSetUpNoise, newSetUp, newEnergy, newNoise, noiseRequirement, percentageCompleted) 
            annealerProgressionOutputFileP.write("&&&&&&&&&&&&&&&&&&&&&&&&&&&")
            progressionList.append(operatorModifiedIndex) 
        
        #---- updating the temperature
        numberOfApxBitsTemperature, percentageCompleted = updateNumberOfApxBitsTemperature(numberOfApxBitsInitialTemperature, numberOfApxBitsStepSize*stepNumber)
        print "percentage completed: " + str(percentageCompleted) + " for " + str(noiseRequirementPosition) + " out of " + str(totalNumberOfNoiseRequirements) + " noiseRequirement"
        stepNumber += 1
        #operatorPickTemperature = updateOperatorPickTemperature(operatorPickInitialTemperature, operatorPickStepSize*stepNumber)
        operatorPickTemperature = int(numberOfApxBitsTemperature*operatorPickInitialTemperature)
        #-----------------  
    


    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ 
    #---------guide::: final outputing and closing file ptrs
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ 
    print "total number of iterations:", stepNumber
    if (numberOfSuccessfulTries == 0):
        annealerProgressionOutputFileP.write("no config satisfied the Noie" + "\n")
    annealerProgressionOutputFileP.write("progression of the operator progressions based on index: " + str(progressionList))
    annealerProgressionOutputFileP.close()
    

    
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ 
    #---------guide::: return
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ 
    # resultPoint = points()
    # resultPoint.set_noise(bestSetUpNoise)
    # resultPoint.set_energy(bestSetUpEnergy)
    # resultPoint.set_setUp(bestSetUp)
    # resultPoint.set_setUp_number(0)
    bestParetoPoint.set_setUp_number(0)
    energyDistance = distance.euclidean((bestPoint.get_energy()), (bestParetoPoint.get_energy()))
    
    # if energyDistance < .05*bestParetoPoint.get_energy():
        # resultPoint = bestPoint
    # else:
        # resultPoint = bestParetoPoint

    resultPoint = bestParetoPoint
    
    # finalResultFileFullAddress = rootResultFolderName + "/" + "finalResult_demo.txt" 
    # os.system("rm " + finalResultFileFullAddress[:-4]+".png")
    # generateGraph(map(lambda x: x.get_noise(),otherPoints), map(lambda x: x.get_energy(),otherPoints),"Noise", "Energy", 'yx') 
    # generateGraph(map(lambda x: x.get_noise(),[resultPoint]), map(lambda x: x.get_energy(),[resultPoint]),"Noise", "Energy", 'bo')
    # generateGraph(map(lambda x: x.get_noise(),[bestPoint]), map(lambda x: x.get_energy(),[bestPoint]),"Noise", "Energy", 'ro')
    
    # pylab.savefig(finalResultFileFullAddress[:-4]+".png") #saving the figure generated by generateGraph
    #         #
    return resultPoint,otherPoints, noiseRequirement,[noiseRequirement,bestSetUp, bestSetUpNoise, bestSetUpEnergy], numberOfTries, numberOfSuccessfulTries



#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------guide::: testing
# myList = [['btm', 32, 0], ['bta', 32, 0, 0, 0], ['btm', 32, 0], ['bta', 32, 0, 0, 0], ['btm', 32, 4]]
# print getEnergy(myList)

#def isminima_local(p, A):
#    return all(A[p] < A[i] for i in get_neighbors(p, len(A)))
#
#def func(x):
#    return math.sin((2 * math.pi / LIMIT) * x) + 0.001 * random.random()
#
#def initialize(L):
#    return map(func, xrange(0, L))
#
#def main():
#    A = initialize(LIMIT)
#
#    local_minima = []
#    for i in xrange(0, LIMIT):
#        if(isminima_local(i, A)):
#            local_minima.append([i, A[i]])
#
#    x = 0
#    y = A[x]
#    for xi, yi in enumerate(A):
#        if yi < y:
#            x = xi
#            y = yi
#    global_minumum = x
#
#    print "number of local minima: %d" % (len(local_minima))
#    print "global minimum @%d = %0.3f" % (global_minumum, A[global_minumum])
#
#    x, x_best, x0 = simulated_annealing(A)
#    print "Solution is @%d = %0.3f" % (x, A[x])
#    print "Best solution is @%d = %0.3f" % (x_best, A[x_best])
#    print "Start solution is @%d = %0.3f" % (x0, A[x0])
#

#main()
