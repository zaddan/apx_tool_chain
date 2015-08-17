import numpy
import sys
import itertools
import copy
def polyThree(variableList, *Coeff):
    return Coeff[0]*pow(variableList[0],3) + Coeff[1]*pow(variableList[0],2) + Coeff[2]*pow(variableList[0],1) + Coeff[3] 
 
    
def polyTwo(variableList,*Coeff):
    return Coeff[0]*pow(variableList[0],2) + Coeff[1]*pow(variableList[0],1) + Coeff[2]
 
def multiVarFoo3(variableList,*Coeff):
    return Coeff[0]*variableList[0]*variableList[1]

def multiVarFoo2(variableList,*Coeff):
    return Coeff[0]*variableList[0] + variableList[1]
 

def degreeOnePolyMultiVar(variableList, *Coeff):
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
            result.append(degreeOnePolyMultiVar(element, *Coeff))
        return result 
    
    varibleListModifiedArray1D = numpy.array(variableModified)
    varibleListModifiedArray2D = varibleListModifiedArray1D.reshape((1,-1))
    varibleListModifiedMatrix  = numpy.mat(varibleListModifiedArray2D.T)

    CoeffArray1D = numpy.array(Coeff)
    CoeffArray2D= CoeffArray1D.reshape((1,-1))
    CoeffMatrix = numpy.mat(CoeffArray2D) 
    return (CoeffMatrix*varibleListModifiedMatrix).item(0,0)



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
            powerList.append(element)
   

    variableModifiedAlsoIncludedPower =[]
    for index in range(0,len(powerList)):
        variableModifiedAlsoIncludedPower.append([])
        for variableIndex in range(0, numberOfVar):
            variableModifiedAlsoIncludedPower[index]= numpy.float64(1)

    

    for index in range(0,len(powerList)):
        for variableIndex in range(1, numberOfVar + 1):
            variableModifiedAlsoIncludedPower[index] *= pow(numpy.float64(variableModified[variableIndex]), numpy.float64(powerList[index][variableIndex - 1]))
    
#    print "*****************" 
#    print "here is power list" + str(powerList)
#    print "variableModified" + str(variableModified)
#    print "modified include power" + str(variableModifiedAlsoIncludedPower) 
#    print "***************" 
    varibleListModifiedArray1D = numpy.array(variableModifiedAlsoIncludedPower)
    varibleListModifiedArray2D = varibleListModifiedArray1D.reshape((1,-1))
    varibleListModifiedMatrix  = numpy.mat(varibleListModifiedArray2D.T)

    CoeffArray1D = numpy.array(copy.copy(Coeff))
    CoeffArray2D= CoeffArray1D.reshape((1,-1))
    CoeffMatrix = numpy.mat(CoeffArray2D) 
#    print "coeffMatrix" + str(CoeffMatrix)
#    print "variblListModified Matrix" + str(varibleListModifiedMatrix)
#    print (CoeffMatrix*varibleListModifiedMatrix).item(0,0)

    return (CoeffMatrix*varibleListModifiedMatrix).item(0,0)



global funcNumberOfCoeffDic
funcNumberOfCoeffDic = {}
funcNumberOfCoeffDic[polyThree] = 4
funcNumberOfCoeffDic[polyTwo] = 3
funcNumberOfCoeffDic[multiVarFoo2] = 1
#funcNumberOfCoeffDic[degreeOnePolyMultiVar] = 2
#funcNumberOfCoeffDic[degreeNPolyMultiVar] = 3
funcNumberOfCoeffDic[multiVarFoo3] = 1
funcNumberOfCoeffDic[degreeNPolyMultiVar] = 2
