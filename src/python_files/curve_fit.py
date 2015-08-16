import numpy as np
import sys
import math 
from scipy.optimize import curve_fit
from all_funcs import *
import all_funcs
#def polyThree(variableList, coeffList):
#    return coeffList[0]*pow(variableList[0],3) + coeffList[1]*pow(variableList[0],2) + coeffList[2]*pow(variableList[0],1) + coeffList[3]
#    
#def polyTwo(variableList, coeffList):
#    return coeffList[0]*pow(variableList[0],2) + coeffList[1]*pow(variableList[0],1) + coeffList[2]
# 
# 



def findCoefficients(xdata, ydata, funcNumberOfCoeffDic):
    funcCoeffDic = {} 
    for func in funcNumberOfCoeffDic:
        #-----------------  
        #---------guide:::  numberOfCoeff is necessary to pass to curvefit (if you want to pass 
        #-----------------  the coeff as a list. a tuple with this number of elements needs to be
        #-----------------  generated and passed as initial points to curve_fit. look at CoeffInitialPoint
        #-----------------  as reference
        #-----------------  
        numberOfCoeff = funcNumberOfCoeffDic[func] #this is necessary to pass to the curve_fit
        CoeffInitialPoint = tuple([0]*numberOfCoeff)
        popt, pcov = curve_fit(func, np.array(xdata),np.array(ydata), CoeffInitialPoint)
        funcCoeffDic[func] =  popt
    
    return funcCoeffDic
    
def square(list):
        return [i ** 2 for i in list]





def pickBestFit(funcCoeffDic, inputTestData, outputTestData):
    funcErrorListDic = {}
    funcErrorDic = {}
    
    #---------guide::: go through all functions and find the list of error for each one. This list contains the errors corresponding to each inputTestData
    for func in funcCoeffDic.keys():
        
        inputReshaped = []
        for inputNumber in range(0, len(inputTestData[0])):
            inputReshaped.append([])
        
        for index in range(0, len(inputTestData[0])):
            for inputNumber in range(0, len(inputTestData)):
                inputReshaped[index].append(inputTestData[inputNumber][index])

        for index in range(0,len(inputReshaped)):
            #---------guide:::  reshaping the input acceptable for func
#            for inputNumber in range(0, len(inputTestData)): 
#                funcInput.append(inputTestData[inputNumber][index])
#           
            funcInput = inputReshaped[index]
            if func in funcErrorListDic: 
                funcErrorListDic[func].append(math.fabs(outputTestData[index] - func(funcInput, *funcCoeffDic[func])))
            else:
                funcErrorListDic[func] = [(math.fabs(outputTestData[index] - func(funcInput, *funcCoeffDic[func])))]
    
    #---------guide::: use sqrt of sum of squre of all error in the error list for each function to calculate the error
    for func in funcCoeffDic.keys(): 
        funcErrorDic[func] = math.sqrt(sum(square(funcErrorListDic[func])))
    
    #---------guide:::  foo is only defined to initialize bestFittedFunc
    def foo():
        return 0
    
    bestFittedFunc = foo 
    minimumError = 10000
    
    #---------guide:::  find the min error
    for func in funcErrorDic:
        if funcErrorDic[func] <= minimumError:
            minimumError = funcErrorDic[func]
            bestFittedFunc = func


    return bestFittedFunc, funcErrorDic



## 
# @brief this function finds the best fitted function for set of inputs
# 
# @param inputTrainingData: to find the coeffs with. This should be a list of lists. meaning,
#                           if we only have one input, for example the funcs of interests are f(x)
#                           looking, then the input should be something like [[2,4,5,6], [4,5,6,7]]
#                           if the func is multivariable, for example f(x, y), then we will have:
#                           [[2,4,5,6], [4,5,6,7]] where the [2,4,5,6] are the list of input for x 
#                           and [4,5,6,7] is for y

# @param outputTrainingData: to find the coeffs with
# @param inputTestData: to test the found coeffs of the funcs and deduce the best fit
# @param outputTestData: to test the found coeffs of the funcs and deduce the best fit
# 
# @return 
def findBestFitFunction(inputTrainingData, outputTrainingData, inputTestData, outputTestData, funcNumberOfCoeffDic):
    #---------guide:::  find the coeffs for all the functions
    funcCoeffDic = findCoefficients(inputTrainingData, outputTrainingData, funcNumberOfCoeffDic)
   
    #---------guide:::  find the bestFittedFunc
    bestFittedFunc, funcErrorDic = pickBestFit(funcCoeffDic, inputTestData, outputTestData)
  
    return bestFittedFunc,funcCoeffDic[bestFittedFunc] ,funcErrorDic


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------guide::: testing
def testBestFittedFunc():
    #----------------- 
    #---------guide:::  things to change for testing different functions
    #----------------- 
    #coeff = [10,14,13,25] 
    #coeff = [1,14,25] 
    coeff = [9] 
    #foo = polyThree 
    foo = multiVarFoo2
    
    #inputTrainingData = [range(0,10)]
    inputTrainingData = [[2,4,5,6], [4,5,6,7]]
    
    #inputTestData = [range(200, 400, 2)]
    inputTestData = [range(200, 400, 2), range(300, 500,2)]
    #-----------------  
    #-----------------  
    
    
    
    outputTrainingData = [] 
    #---------guide:::  the input and output training data should also be given. In this case we are genrating it for functionality verification
    
    #---------guide:::  reshape the training data. This is necessary since 
    #-----------------  the format that curve_fit accept data is odd. 
    inputTrainingReshaped = []
    for inputNumber in range(0, len(inputTrainingData[0])):
        inputTrainingReshaped.append([])
    
    for index in range(0, len(inputTrainingData[0])):
        for inputNumber in range(0, len(inputTrainingData)):
            inputTrainingReshaped[index].append(inputTrainingData[inputNumber][index])
    
    for index in range(0, len(inputTrainingReshaped)):
        outputTrainingData.append(foo(inputTrainingReshaped[index], *coeff))
        #---------guide:::  the input and output test data should also be given. In this case we are genrating it for functionality verification
    outputTestData = [] 
   
    
    #---------guide:::  reshape the test data. This is necessary since 
    #-----------------  the format that curve_fit accept data is odd. 
    inputTestingReshaped = []
    for inputNumber in range(0, len(inputTestData[0])):
        inputTestingReshaped.append([])
    
    for index in range(0, len(inputTestData[0])):
        for inputNumber in range(0, len(inputTestData)):
            inputTestingReshaped[index].append(inputTestData[inputNumber][index])

    for index in range(0, len(inputTestData[0])):
        outputTestData.append(foo(inputTestingReshaped[index], *coeff))
   
    
    bestFittedFunc, funcCoeff, funcErrorDic = findBestFitFunction(inputTrainingData, outputTrainingData, inputTestData, outputTestData, all_funcs.funcNumberOfCoeffDic)
    
    # print funcError 
    print bestFittedFunc.__name__
    print funcCoeff

test = False
if (test): 
    testBestFittedFunc()
