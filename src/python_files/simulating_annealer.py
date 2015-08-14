import random
import math

from extract_result_properties import *
from modify_operator_sample_file import *
from src_parse_and_apx_op_space_gen import *
import copy
from misc import *
def getFirstTwo(myList):
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
    
    newNumberOfApxBits = random.choice(range(0,3, 1))
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







def make_move(operatorList, T):
    random.seed() 
    operatorIndex = chooseAnOperatorIndex(operatorList) #randomly choose an operator to modify
    operatorModified = modifyOperatorSubSetup(operatorList[operatorIndex], T) #randomly modify it (based on temperature)
    #modify the set up 
    newSetUp = copy.copy(operatorList)
    newSetUp[operatorIndex] = operatorModified
    return newSetUp, operatorModified, operatorIndex


def getEnergy(config):
    energy = calculateEnergy(map(getFirstTwo, config))
    return energy 


def naiveSimulatedAnnealing(initialSetUp, noiseRequirements, initialTemperature, stepSize, operatorSampleFileFullAddress,executableName, executableInputList, rootResultFolderName, CSourceOutputForVariousSetUpFileName, CBuildFolder, operandSampleFileName, accurateValues):
    
    progressionList = [] 
    annealerProgressionOutputFileP = open(settings.annealerProgressionOutputFileName, "a")
    annealerProgressionOutputFileP = open(settings.annealerProgressionOutputFileName, "a")
    
    percentageCompleted = 0 
    stepNumber = 0 
    temperature = initialTemperature 
    oldSetUp = initialSetUp
    bestSetUp = oldSetUp
   
    
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
    #---------guide::: noise
    bestSetUpNoise = extractNoiseForOneInput(CSourceOutputForVariousSetUpFileName , accurateValues)
    
    
   #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ 
   #---------guide:::  start the iterative process of simulated_annealing
   #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ 
    while temperature > 0:
        newSetUp, operatorModified, operatorModifiedIndex= make_move(bestSetUp, temperature)
        newEnergy = getEnergy(newSetUp) 
        #---------guide:::  erasing the previuos content of the file
        open(CSourceOutputForVariousSetUpFileName, "w").close()
        #---------guide::: run to get the noisek
        modifyOperatorSampleFile(operatorSampleFileFullAddress, newSetUp)
        #---------guide:::  run the csrouce file with the new setup(operators)
        make_run(executableName, executableInputList, rootResultFolderName, CSourceOutputForVariousSetUpFileName, CBuildFolder, operandSampleFileName)
        #---------guide::: noise
        newNoise = int(extractNoiseForOneInput(CSourceOutputForVariousSetUpFileName , accurateValues))
#        if len(newNoise) == 0:
#            sys.exit()
#        
       
        #---------guide:::  deciding whether the output associated with the new set up acceptable
        if (newNoise < int(noiseRequirements) and (newNoise > .85*int(noiseRequirements))):
            if(newEnergy < bestSetUpEnergy):
                print "found one better setup"
                print "old setUp: " + str(bestSetUp)
                print "old Energy " + str(bestSetUpEnergy)
                print "new setUp: " + str(newSetUp)
                print "new Energy " + str(newEnergy)
                print "new Noise " + str(newNoise)
                print "noiseRequirements: " + str(noiseRequirements) 
                #print "percentageCompleted: " + str(percentageCompleted) + " %"
                #---------guide:::  writing the output to a file
                annealerProgressionOutputFileP.write("************************************************************************\n")
                annealerProgressionOutputFileP.write("operatorModifiedIndex: " + "\\\\\\" + str(operatorModifiedIndex) + "////" +  "  operatorModified: " + str(operatorModified) +  "\n" )
                annealerProgressionOutputFileP.write("new setUp: " + str(newSetUp) + "\n")
                annealerProgressionOutputFileP.write("new Energy: " + str(newEnergy)+ "\n")
                annealerProgressionOutputFileP.write("new Noise: " + str(newNoise) + "\n")
                annealerProgressionOutputFileP.write("noiseRequirement: " + str(noiseRequirements) + "\n")
                #annealerProgressionOutputFileP.write("percentageCompleted: " + str(percentageCompleted) + " %" + "\n")
                progressionList.append(operatorModifiedIndex) 
                 
                
        
                bestSetUp = newSetUp
                bestSetUpEnergy = newEnergy
                bestSetUpNoise = newNoise

        temperature, percentageCompleted = updateNumberOfApxBitsTemperature(initialTemperature, stepSize*stepNumber)
        stepNumber += 1

    print "total number of iterations:", stepNumber
    if (int(bestSetUpNoise) > int(noiseRequirements)):
        print "*****************LOGIC ERROR**************" 
        print "the noise requirement was not satisfied"
        print "do one of the followings"
        print "change the stepSize"
        print "change the initial Setup"
        print "change the noise requirements"
        annealerProgressionOutputFileP.write("no config satisfied the Noise" + "\n")
        #exit()

    annealerProgressionOutputFileP.write("progression of the operator progressions based on index: " + str(progressionList))
    annealerProgressionOutputFileP.close()
    return [noiseRequirements,bestSetUp, bestSetUpNoise, bestSetUpEnergy]




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



def improvedSimulatedAnnealing(initialSetUp, noiseRequirements, numberOfApxBitsInitialTemperature, numberOfApxBitsStepSize, operatorPickInitialTemperature, operatorPickStepSize, operatorSampleFileFullAddress,executableName, executableInputList, rootResultFolderName, CSourceOutputForVariousSetUpFileName, CBuildFolder, operandSampleFileName, accurateValues, noiseRequirementsPosition, totalNumberOfNoiseRequirements):
    
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



    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ 
    #---------guide:::  start the iterative process of simulated_annealing
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ 
    while numberOfApxBitsTemperature > 0:
        #---------guide::: if we found a better set of operators, output in the command prompt and also to a file
        #-----------------  
        foundBetter = False 
        for i in range(0, operatorPickTemperature, 1): 
            numberOfTries += 1 
            newSetUp, operatorModified, operatorModifiedIndex= make_move(bestSetUp, numberOfApxBitsTemperature)
            newEnergy = getEnergy(newSetUp) 
            
            #---------guide:::  erasing the previuos content of the file
            open(CSourceOutputForVariousSetUpFileName, "w").close()
            
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
            oldSetUpEnergy =  bestSetUpEnergy
            oldSetUpNoise = bestSetUpNoise
            #---------guide::: the following 3 criterian needs to be satisfied
            #1. make sure new noise satisfies the requirement
            #2. if new new is closer to the requirement than oldnoise or if it falls within a certain margin
            #3. if energy of the new set up is smaller than the energy of the old set up of falls within a certain margin
            if (newNoise < int(noiseRequirements)):
                if withinSomePercent(math.fabs(newNoise - int(noiseRequirements)), math.fabs(bestSetUpNoise - int(noiseRequirements)),settings.annealersAcceptableImprovementOnNoiseMarginePercentage) or (math.fabs(newNoise - int(noiseRequirements)) < math.fabs(bestSetUpNoise - int(noiseRequirements))):
                    if(withinSomePercent(newEnergy, bestSetUpEnergy, settings.annealersAcceptableEnergyMarginePercentage)) or (newEnergy < bestSetUpEnergy):
#                        print "new noise diff: " + str(math.fabs(newNoise - int(noiseRequirements)))
#                        print "old noise diff:" + str(math.fabs(bestSetUpNoise - int(noiseRequirements)))
                        
#                        printToCommandPrompt(operatorModifiedIndex, oldSetUp, oldSetUpEnergy, oldSetUpNoise, newSetUp, newEnergy, newNoise, noiseRequirements, percentageCompleted) 
#                        sys.exit() 
                        bestSetUp = newSetUp
                        bestSetUpEnergy = newEnergy
                        bestSetUpNoise = newNoise
                        
                        
                        printToProgressor(annealerProgressionOutputFileP, operatorModifiedIndex, oldSetUp, oldSetUpEnergy, oldSetUpNoise, newSetUp, newEnergy, newNoise, noiseRequirements, percentageCompleted) 
                        foundBetter = True 

                        numberOfSuccessfulTries += 1
                   
            #printToCommandPrompt(operatorModifiedIndex, oldSetUp, oldSetUpEnergy, oldSetUpNoise, newSetUp, newEnergy, newNoise, noiseRequirements, percentageCompleted) 
        #-----------------  
        
        #-----------------  
        #---------guide::: if we found a better set of operators, output in the command prompt and also to a file
        #-----------------  
        if (foundBetter):
             
            printToCommandPrompt(operatorModifiedIndex, oldSetUp, oldSetUpEnergy, oldSetUpNoise, newSetUp, newEnergy, newNoise, noiseRequirements, percentageCompleted) 
            annealerProgressionOutputFileP.write("&&&&&&&&&&&&&&&&&&&&&&&&&&&")
            printToProgressor(annealerProgressionOutputFileP, operatorModifiedIndex, oldSetUp, oldSetUpEnergy, oldSetUpNoise, newSetUp, newEnergy, newNoise, noiseRequirements, percentageCompleted) 
            annealerProgressionOutputFileP.write("&&&&&&&&&&&&&&&&&&&&&&&&&&&")
            progressionList.append(operatorModifiedIndex) 
        #-----------------  
        
        #-----------------  
        #---------guide::: updating the temperature
        #-----------------  
        numberOfApxBitsTemperature, percentageCompleted = updateNumberOfApxBitsTemperature(numberOfApxBitsInitialTemperature, numberOfApxBitsStepSize*stepNumber)
        print "percentage completed: " + str(percentageCompleted) + " for " + str(noiseRequirementsPosition) + " out of " + str(totalNumberOfNoiseRequirements) + " noiseRequirements"
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
    return [noiseRequirements,bestSetUp, bestSetUpNoise, bestSetUpEnergy], numberOfTries, numberOfSuccessfulTries


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------guide::: testing
myList = [['btm', 32, 0], ['bta', 32, 0, 0, 0], ['btm', 32, 0], ['bta', 32, 0, 0, 0], ['btm', 32, 4]]
print getEnergy(myList)

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
