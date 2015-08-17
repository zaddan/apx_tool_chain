import numpy as np
import sys
import math 
from scipy.optimize import curve_fit
from all_funcs import *
import all_funcs
import random


class degreeNPolyMultiVarClass:
    def __init__(self, maxDegree):
        self.maxDegree = maxDegree
        self.degree = 1 
   


## 
# @brief combination
# 
# @param n
# @param r
# 
# @return 
def nCr(n,r):
    assert(n>0), "n can not be less than zero"
    assert(r>0), "r can not be less than zero"
    assert(n - r>0), "n - r can not be less than zero"
    f = math.factorial
    return f(n) / f(r) / f(n-r)

#def polyThree(variableList, coeffList):
#    return coeffList[0]*pow(variableList[0],3) + coeffList[1]*pow(variableList[0],2) + coeffList[2]*pow(variableList[0],1) + coeffList[3]
#    
#def polyTwo(variableList, coeffList):
#    return coeffList[0]*pow(variableList[0],2) + coeffList[1]*pow(variableList[0],1) + coeffList[2]
# 
# 


def findCoefficients(xdataRaw, ydata, funcNumberOfCoeffDic, degreeNPolyMultiVarMaxDegree = 2, degreeNPolyMultiVarMinDegree = 1):
    funcCoeffDic = {} 
    for func in funcNumberOfCoeffDic:
        #-----------------  
        #---------guide:::  numberOfCoeff is necessary to pass to curvefit (if you want to pass 
        #-----------------  the coeff as a list. a tuple with this number of elements needs to be
        #-----------------  generated and passed as initial points to curve_fit. look at CoeffInitialPoint
        #-----------------  as reference
        #-----------------  
        if (func == degreeNPolyMultiVar):
            for degree in range(degreeNPolyMultiVarMinDegree, degreeNPolyMultiVarMaxDegree): 
                #degree = degreeNPolyMultiVarMaxDegree
    #            numberOfCoeff = funcNumberOfCoeffDic[func] #this is necessary to pass to the curve_fit
                numberOfVar = len(xdataRaw) 
                numberOfCoeff = nCr( degree + numberOfVar - 1, numberOfVar - 1)
                CoeffInitialPoint = tuple([0]*numberOfCoeff)
                extraArgAdded = [degree]*len(xdataRaw[0]) 
                xdata = [extraArgAdded] + xdataRaw
                popt, pcov = curve_fit(func, np.array(xdata),np.array(ydata), CoeffInitialPoint)
                funcCoeffDic[(func,degree)] =  popt

            
            
            #---------guide:::  generating an object that has control over the degree
            #-----------------  this degree is later used in the degreeOnePolyMultiVar function
#            degreeNPolyMultiVarObject = degreeNPolyMultiVarClass(degreeNPolyMultiVarMaxDegree)

#            for degree in range(1, degreeNPolyMultiVarObject.maxDegree):
#                    print degreeNPolyMultiVarObject.maxDegree 
#                    degreeNPolyMultiVarObject.degree = degree
#                    print degreeNPolyMultiVarObject.degree
#                    print xdata 
#                    sys.exit() 
#                    degreeNPolyMultiVarClass.degree = degree
#                    numberOfCoeff = funcNumberOfCoeffDic[func] #this is necessary to pass to the curve_fit
#                    CoeffInitialPoint = tuple([0]*numberOfCoeff)
#                    popt, pcov = curve_fit(func, np.array(xdata),np.array(ydata), CoeffInitialPoint)
#                    funcCoeffDic[func] =  popt
#
        
        else: 
            numberOfCoeff = funcNumberOfCoeffDic[func] #this is necessary to pass to the curve_fit
            CoeffInitialPoint = tuple([0]*numberOfCoeff)
            popt, pcov = curve_fit(func, np.array(xdataRaw),np.array(ydata), CoeffInitialPoint)
            funcCoeffDic[(func,0)] =  popt
    
    return funcCoeffDic
    
def square(list):
        return [i ** 2 for i in list]


## 
# @brief this module is use to generate the list of functions that 
#        is later used to pick the best function from
# 
# @return 
#def funcGenerator(maxDegreeN = 2):
#    funcNumberOfCoeffDic = {} 
#    funcNumberOfCoeffDic = copy.copy(all_funcs.funcNumberOfCoeffDic)
#    
#    for degree in range(0, len(maxDegreeN)):
#




def pickBestFit(funcCoeffDic, inputTestDataRaw, outputTestData, degreeNPolyMultiVarMaxDegree = 2):
    funcErrorListDic = {}
    funcErrorDic = {}
    
    #---------guide::: go through all functions and find the list of error for each one. This list contains the errors corresponding to each inputTestData
    for func in funcCoeffDic.keys():
        if (func[0] == degreeNPolyMultiVar):
            degree = func[1] 
            numberOfVar = len(inputTestDataRaw) 
            numberOfCoeff = nCr(degree + numberOfVar - 1, numberOfVar - 1)
            extraArgAdded = [degree]*len(inputTestDataRaw[0]) 
            
            inputTestData = [extraArgAdded] + inputTestDataRaw
        else:
            inputTestData = copy.copy(inputTestDataRaw)
       
        
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
                funcErrorListDic[func].append(math.fabs(outputTestData[index] - func[0](funcInput, *funcCoeffDic[func])))
            else:
                funcErrorListDic[func] = [(math.fabs(outputTestData[index] - func[0](funcInput, *funcCoeffDic[func])))]
    
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

   #assert(bestFittedFunc == foo), "something went wrong because the best fitted function was found to be foo. Note: foo is a dummy function"
        
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
def findBestFitFunction(inputTrainingData, outputTrainingData, inputTestData, outputTestData, funcNumberOfCoeffDic, degreeNPolyMultiVarMaxDegree, degreeNPolyMultiVarMinDegree):
    #---------guide:::  find the coeffs for all the functions
    funcCoeffDic = findCoefficients(inputTrainingData, outputTrainingData, funcNumberOfCoeffDic, degreeNPolyMultiVarMaxDegree, degreeNPolyMultiVarMinDegree)
    #---------guide:::  find the bestFittedFunc
    bestFittedFunc, funcErrorDic = pickBestFit(funcCoeffDic, inputTestData, outputTestData, degreeNPolyMultiVarMaxDegree)
#    for func in funcErrorDic:
#        print func
#        print funcErrorDic[func]
#     
#    sys.exit()
    return bestFittedFunc,funcCoeffDic[bestFittedFunc] ,funcErrorDic


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------guide::: testing
def testBestFittedFunc():
    #---------guide:::  only applicable to degreeNPolyMultiVar
    foo = degreeNPolyMultiVar
    degree = 5 
    maxDegree = 7 
    minDegree = 4 
    numberOfVar = 4 
    inputTrainingLowerBound = 100
    inputTrainingUpperBound = 320
    
    inputTestLowerBound = 10 
    inputTestUpperBound = 200
    coeffLowerBound = 5
    coeffUpperBound = 21
    #----------------- 
    

    #----------------- 
    #---------guide:::  things to change for testing different functions
    #----------------- 
    #coeff = [10,14,13,25] 
    #coeff = [1,14,25] 
    #coeff = [9, 8, 12] 
    #coeff = [9, 8, 12] 
    
    #foo = polyThree 
    #foo = multiVarFoo2
    #foo = degreeOnePolyMultiVar
   
    
    #inputTrainingData = [range(0,10)]
    #inputTrainingData = [[2,4,5,6], [4,5,6,7]]
    #inputTrainingData = [[2,4,5,6], [4,5,6,7], [3,4,2,7]]
    #inputTrainingDataRaw = [[2,4,5,6,11, 12,7], [4,5,6,7,10,14,11]]
            

    #inputTestData = [range(200, 400, 2)]
    #inputTestData = [range(200, 400, 2), range(300, 500,2)]
    #inputTestData = [range(200, 400, 2), range(300, 500,2), range(600,800,2)]
    
    #inputTestDataRaw = [range(200, 400, 2), range(300, 500,2)]
        
    maxNumberOfReqCoeff = nCr(maxDegree + numberOfVar - 1, numberOfVar-1)
    inputTestDataLength = random.randrange(maxNumberOfReqCoeff, maxNumberOfReqCoeff+ 1)
    inputTrainingDataLength = random.randrange(maxNumberOfReqCoeff, maxNumberOfReqCoeff+ 1)
    coeff = [] 
    numberOfReqCoeff = nCr(degree + numberOfVar - 1, numberOfVar-1)
    for i in range(0, numberOfReqCoeff):
        coeff.append(random.randrange(coeffLowerBound, coeffUpperBound))
    print "coeff is " + str(coeff)
    #coeff = [ 8, 12, 15,5,8] 
    inputTrainingDataRaw =[] 
    for varNumber in range(0, numberOfVar):
        inputTrainingDataRaw.append([])

    #coeff = [ 8, 12, 15,5,8] 
    for i in range(0, inputTrainingDataLength):
        for varNumber in range(0, numberOfVar):
            inputTrainingDataRaw[varNumber].append(random.randrange(inputTrainingLowerBound, inputTrainingUpperBound)/float(inputTrainingUpperBound))
   
    inputTestDataRaw =[] 
    for varNumber in range(0, numberOfVar):
        inputTestDataRaw.append([])
    
    for i in range(0, inputTestDataLength):
        for varNumber in range(0, numberOfVar):
            inputTestDataRaw[varNumber].append(numpy.float64(random.randrange(inputTestLowerBound, inputTestUpperBound))/inputTestUpperBound)
   
    #-----------------  
    #-----------------  
    
         
    #----------------- 
    #---------guide::: this check makes sure to adjust the number of input for 
    #----------------  degreeNPolyMultiVar. The input to degreeNPolyMultiVar is not 
    #-----------------  just the regular input. You need to also include the degree
    #-----------------  for example if the regular input is [[4,5,6], [1,6,7]]
    #-----------------  the modified input (if the degree is 5) looks like [[5,5,5], [4,5,6],[1,6,7]
    #-----------------  thus we add the degeree as the first elemnet of the list 
    #----------------- 
    if (foo == degreeNPolyMultiVar):
            numberOfVar = len(inputTrainingDataRaw) 
            numberOfCoeff = nCr( degree + numberOfVar - 1, numberOfVar - 1)
            extraArgAddedTraning = [degree]*len(inputTrainingDataRaw[0]) 
            inputTrainingData =  [extraArgAddedTraning] + inputTrainingDataRaw 
            extraArgAddedTest = [degree]*len(inputTestDataRaw[0]) 
            inputTestData =  [extraArgAddedTest] + inputTestDataRaw
    else:
        inputTrainingData = inputTrainingDataRaw
        inputTestData = inputTestDataRaw
    
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
        outputTestData.append(numpy.float64(foo(inputTestingReshaped[index], *coeff)))
   
    bestFittedFunc, funcCoeff, funcErrorDic = findBestFitFunction(inputTrainingDataRaw, outputTrainingData, inputTestDataRaw, outputTestData, all_funcs.funcNumberOfCoeffDic,maxDegree, minDegree)
    
    # print funcError 
    print "the function that we used: " + str(foo.__name__) +","+ str(degree)
    print "the coeff that we started with:" + str(coeff) 
    print str(bestFittedFunc[0].__name__) + ","+str(bestFittedFunc[1])
    print funcCoeff

test = True
if (test): 
    testBestFittedFunc()
