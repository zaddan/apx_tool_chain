import numpy
import sys
def polyThree(variableList, *Coeff):
    return Coeff[0]*pow(variableList[0],3) + Coeff[1]*pow(variableList[0],2) + Coeff[2]*pow(variableList[0],1) + Coeff[3] 
 
    
def polyTwo(variableList,*Coeff):
    return Coeff[0]*pow(variableList[0],2) + Coeff[1]*pow(variableList[0],1) + Coeff[2]
 
def multiVarFoo3(variableList,*Coeff):
    return Coeff[0]*variableList[0]*variableList[1]

def multiVarFoo2(variableList,*Coeff):
    return Coeff[0]*variableList[0] + variableList[1]
 

def degreeNPoly(variableList, *Coeff):
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
            result.append(degreeNPoly(element, *Coeff))
        return result 
    
    varibleListModifiedArray1D = numpy.array(variableModified)
    varibleListModifiedArray2D = varibleListModifiedArray1D.reshape((1,-1))
    varibleListModifiedMatrix  = numpy.mat(varibleListModifiedArray2D.T)

    CoeffArray1D = numpy.array(Coeff)
    CoeffArray2D= CoeffArray1D.reshape((1,-1))
    CoeffMatrix = numpy.mat(CoeffArray2D) 
    return (CoeffMatrix*varibleListModifiedMatrix).item(0,0)

global funcNumberOfCoeffDic
funcNumberOfCoeffDic = {}
funcNumberOfCoeffDic[polyThree] = 4
funcNumberOfCoeffDic[polyTwo] = 3
funcNumberOfCoeffDic[multiVarFoo2] = 1
funcNumberOfCoeffDic[degreeNPoly] = 3
funcNumberOfCoeffDic[multiVarFoo3] = 1
