import numpy
import sys
import itertools
import copy
degreeNPolyMultiVarDivider = 100

def polyOneUnBallenced(variableList, *Coeff):
    return Coeff[0]*pow(variableList[0],1) + Coeff[1]*pow(variableList[1],5) + Coeff[2]*pow(variableList[2],1) + Coeff[3]*pow(variableList[3], 5)
def polyOne(variableList, *Coeff):
    return Coeff[0]*pow(variableList[0],1) + Coeff[1]*pow(variableList[1],1) + Coeff[2]*pow(variableList[2],1) + Coeff[3]*pow(variableList[3], 1) + Coeff[4]*pow(variableList[4], 1) + Coeff[5]
 
 
def polyThree(variableList, *Coeff):
    return Coeff[0]*pow(variableList[0],3) + Coeff[1]*pow(variableList[0],2) + Coeff[2]*pow(variableList[0],1) + Coeff[3] 
 
    
def polyTwo(variableList,*Coeff):
    return Coeff[0]*pow(variableList[0],2) + Coeff[1]*pow(variableList[0],1) + Coeff[2]
 
def multiVarFoo3(variableList,*Coeff):
    return Coeff[0]*variableList[0]*variableList[1]

def multiVarFoo2(variableList,*Coeff):
    return Coeff[0]*variableList[0] + variableList[1]
 

def degreeNPolyMultiVar(variableList, *Coeff):
    if not(isinstance(variableList,list)):
        variableModified = []
        for rowNumber in range(0,variableList.shape[1]):
            variableModified.append([])
        for colNumber in range(0,variableList.shape[1]):
            for rowNumber in range(0,variableList.shape[0]):
                variableModified[colNumber].append(variableList[rowNumber][colNumber])
    else:
        variableModified = variableList
    
    if not(isinstance(variableList,list)):
        result = [] 
        for element in variableModified:
            result.append(degreeNPolyMultiVar(element, *Coeff))
        return result 
    
    numberOfVar = len(variableModified) - 1
    degree = int(variableModified[0])
    #---------guide:::  list of all acceptable powers.
    #----------------- for example, if we are dealing with (x + y)^2
    #-----------------  this power list containst (2,0), (1,1) and (0,2)
    #-----------------  This depends on the degree and number of vars
    #---------guide:::  The reason that we get the iterators first 
    #----------------- is because itertools.product provide you with iterators
    powerListIterators = itertools.product(range(0,degree+1), repeat = numberOfVar) 
    #---------guide:::  contains the list of powers
    powerList = []
    for element in powerListIterators:
        if sum(element) == degree: 
            powerList.insert(0,element) 
            # powerList.append(element)
   

    variableModifiedAlsoIncludedPower =[]
    for index in range(0,len(powerList)):
        variableModifiedAlsoIncludedPower.append([])
        for variableIndex in range(0, numberOfVar):
            variableModifiedAlsoIncludedPower[index]= numpy.float64(1)

    
    # ---- values of variables are devided by a big value so they won't
    # overflow
    newVariableModified = [] 
    for element in variableModified:
        if  (isinstance(element, int) or isinstance(element, float)):
            newVariableModified.append(float(element)/degreeNPolyMultiVarDivider)
        else:
            newVariableModified.append(element)
    
    for index in range(0,len(powerList)):
        for variableIndex in range(1, numberOfVar + 1):
            variableModifiedAlsoIncludedPower[index] *= pow(newVariableModified[variableIndex], powerList[index][variableIndex - 1])

    return numpy.dot(Coeff, variableModifiedAlsoIncludedPower)



global funcNumberOfCoeffDic
funcNumberOfCoeffDic = {}
funcNumberOfCoeffDic[polyOne] = 6
funcNumberOfCoeffDic[polyOneUnBallenced] = 4
# funcNumberOfCoeffDi
# funcNumberOfCoeffDic[polyThree] = 4
# funcNumberOfCoeffDic[polyTwo] = 3
# funcNumberOfCoeffDic[multiVarFoo2] = 1
# funcNumberOfCoeffDic[multiVarFoo3] = 1
funcNumberOfCoeffDic[degreeNPolyMultiVar] = 2
