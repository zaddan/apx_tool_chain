import random
import math
from extract_result_properties import *


def getFirstTwo(myList):
    return (myList[0].replace("'", ""),int(myList[1]) - int(myList[2]))


def update_temperature(T, k):
    return int(T - k)

def get_neighbors(i, L):
    assert L > 1 and i >= 0 and i < L
    if i == 0:
        return [1]
    elif i == L - 1:
        return [L - 2]
    else:
        return [i - 1, i + 1]


def chooseAnOperatorIndex(operatorList):
    return random.choice(range(0, operatorList))

def chooseOperatorSubType(operator, T):
    operatorType =  operator.replace("'", "").split()[0]
    oldNumberOfApxBits =  operator.replace("'", "").split()[1]
    print "here is the operator Type: " + operatorType
    newNumberOfApxBits = oldNumberOfApxBits - random.choice(range(-T, T))
    if newNumberOfApxBits < 0 or newNumberOfApxBits > 32:
        newNumberOfApxBits = oldNumberOfApxBits
    
    if operatorType == "btm":  
        return "'" + operatorType + " " + newNumberOfApxBits +"'"
    elif operatorType == "bta":  
        return "'" + operatorType + " " + newNumberOfApxBits + operator.replace("'", "").split()[2] + " " + operator.replace("'", "").split()[3] + "'" 
    else:
        print "***************ERROR***************"
        print "the operator type with the name of " + operatorType + "is not acceptable"

    



def make_move(oldSetUp, T):
    operatorIndex = chooseAnOperatorIndex(operatorList) #randomly choose an operator to modify
    operatorModified = chooseOperatorSubType(operatorList[operatorIndex], T) #randomly modify it (based on temperature)
    #modify the set up 
    newSetUp =  oldSetUp 
    newSetUp[operatorIndex] = operatorModified
    
    return newSetUp 


def getEnergy(config):
    print config 
    energy = calculateEnergy(map(getFirstTwo, config))
    return energy 


def simulated_annealing(initialSetup, noiseRequirements, initialTemprature, stepSize, stepNumber):
    temperature = initialTemprature 
    oldSetup = initialSetup
    bestSetUp = oldSetUp

    while temperature > 0:
        newSetUp = make_move(bestSetUp, temperature)
        newEnergy = getEnergy(newSetUp) 
        bestSetUpEnergy = getEnergy(bestSetUpEnergy) 
        
        
        newNoise = getNoise(newSetUp)
        if (newNoise < noiseRequirements):
            if(newEnergy < bestSetUpEnergy):
                bestSetUp = newSetUp
        
        temperature = update_temperature(temperature, stepSize*stepNumber)
        stepNumber += 1

    print "total number Of Iterations:", stepNumber
    return bestSetup



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
