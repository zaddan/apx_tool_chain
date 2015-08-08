import random
import math
from extract_result_properties import *
from modify_operator_sample_file import *
from src_parse_and_apx_op_space_gen import *

def getFirstTwo(myList):
    return (myList[0].replace("'", ""),int(myList[1]) - int(myList[2]))


def update_temperature(T, k):
    return T - k 
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
    newNumberOfApxBits = oldNumberOfApxBits + random.choice(range(-lowerBound, upperBound))
#    print "here is the T" + str(T) 
#    print "here is the upper " + str(upperRadius)
#    print "here is the lower " + str(lowerRadius)
#    print "upper bound " +str(upperBound)
#    print "lower bound " +str(lowerBound)
#    print "her is the newNumber " + str(newNumberOfApxBits) 
    if newNumberOfApxBits < 0 or newNumberOfApxBits > 32:
        print "#####################" 
        newNumberOfApxBits = oldNumberOfApxBits
    if operatorType == "btm":  
        return ['btm' , operator[1] , newNumberOfApxBits]
    elif operatorType == "bta":  
        return ['bta' ,operator[1], newNumberOfApxBits, operator[3], operator[4]] 
    else:
        print "***************ERROR***************"
        print "the operator type with the name of " + operatorType + "is not acceptable"

    



def make_move(operatorList, T):
    operatorIndex = chooseAnOperatorIndex(operatorList) #randomly choose an operator to modify
    operatorModified = modifyOperatorSubSetup(operatorList[operatorIndex], T) #randomly modify it (based on temperature)
    #modify the set up 
    newSetUp = operatorList
    newSetUp[operatorIndex] = operatorModified
    return newSetUp


def getEnergy(config):
    energy = calculateEnergy(map(getFirstTwo, config))
    return energy 


def simulatedAnnealing(initialSetUp, noiseRequirements, initialTemperature, stepSize, operatorSampleFileFullAddress,executableName, executableInputList, rootResultFolderName, CSourceOutputForVariousSetUpFileName, CBuildFolder, operandSampleFileName, accurateValues):
    
            
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
        print "temperature is "+  str(temperature )
        newSetUp = make_move(bestSetUp, temperature)
        newEnergy = getEnergy(newSetUp) 
        #---------guide:::  erasing the previuos content of the file
        open(CSourceOutputForVariousSetUpFileName, "w").close()
        #---------guide::: run to get the noisek
        modifyOperatorSampleFile(operatorSampleFileFullAddress, newSetUp)
        #---------guide:::  run the csrouce file with the new setup(operators)
        make_run(executableName, executableInputList, rootResultFolderName, CSourceOutputForVariousSetUpFileName, CBuildFolder, operandSampleFileName)
        #---------guide::: noise
        newNoise = extractNoiseForOneInput(CSourceOutputForVariousSetUpFileName , accurateValues)
#        if len(newNoise) == 0:
#            sys.exit()
#        
       
        #---------guide:::  deciding whether the output associated with the new set up acceptable
        print "newNoise is : " +str(newNoise) + "\n"
        if (newNoise < noiseRequirements):
            if(newEnergy < bestSetUpEnergy):
                bestSetup = newSetUp
                bestSetUpEnergy = newEnergy
                bestSetUpNoise = newNoise

        temperature = update_temperature(initialTemperature, stepSize*stepNumber)
        stepNumber += 1

    print "total number of iterations:", stepNumber
    if (int(bestSetUpNoise) > int(noiseRequirements)):
        print "*****************LOGIC ERROR**************" 
        print "the noise requirement was not satisfied"
        print "do one of the followings"
        print "change the stepSize"
        print "change the initial Setup"
        print "change the noise requirements"
        exit()

    return bestSetUp, bestSetUpNoise, bestSetUpEnergy



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
