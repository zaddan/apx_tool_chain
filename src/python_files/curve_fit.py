import numpy as np
import sys
import math 
from scipy.optimize import curve_fit
from all_funcs import *
import all_funcs
import random
from joblib import Parallel, delayed  
import multiprocessing
from collections import defaultdict
from operator import *
from itertools import *
## 
# @brief finding combination
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


## 
# @brief running curve_fit. This function is intended for  parallelism is
# otherwise the functionality intented in this function could be unfolded
# 
# @param xdataRaw
# @param ydata
# @param degree: only applicable if the func is degreeNPolyMultiVar
# @param func
# 
# @return coefs of the func of concern
def run_curve_fit(xdataRaw, ydata, degree, func):
    
    numberOfVar = len(xdataRaw) 
    numberOfCoeff = nCr( degree + numberOfVar - 1, numberOfVar - 1)
    CoeffInitialPoint = tuple([0]*numberOfCoeff)
    extraArgAdded = [degree]*len(xdataRaw[0]) 
    xdata = [extraArgAdded] + xdataRaw
    
    popt, pcov = curve_fit(func, np.array(xdata),np.array(ydata), CoeffInitialPoint)
    
    return popt


## 
# @brief this module finds the coefficients for the func keys of the
# funcNumberOfCoeffDic dictionary, considering the x and y data
# 
# @param xdataRaw
# @param ydata
# @param funcNumberOfCoeffDic: a dic with the key,value of func,
#                                              numberOfFuncCoeff
# @param degreeNPolyMultiVarMaxDegree: the max Degree considerd for degreeNPoly
# @param degreeNPolyMultiVarMinDegree: the min Degree considered for degreeNPoly 
# 
# @return 
def findCoefficients(xdataRaw, ydata, funcNumberOfCoeffDic,
        degreeNPolyMultiVarMaxDegree = 2, degreeNPolyMultiVarMinDegree = 1):
    
    # ---- an attempt for parallelizing the implementation
    num_cores = multiprocessing.cpu_count()
    print("numCores = " + str(num_cores))
    funcCoeffDic = {} 
    
    # ---- an attempt for parallelizing the implementation
    for func in funcNumberOfCoeffDic:
        # ---- numberOfCoeff is necessary to pass to curvefit (if you want to pass 
        # the coeff as a list. a tuple with this number of elements needs to be
        # generated and passed as initial points to curve_fit. look at
        # CoeffInitialPoint as reference
        if (func == degreeNPolyMultiVar):
            result =  Parallel(n_jobs=num_cores)(delayed(run_curve_fit)(xdataRaw,ydata, degree, func) for degree in range(degreeNPolyMultiVarMinDegree, degreeNPolyMultiVarMaxDegree))
            for degree in range(degreeNPolyMultiVarMinDegree, degreeNPolyMultiVarMaxDegree):
                funcCoeffDic[(func,degree)] = result[degree - degreeNPolyMultiVarMinDegree]
        else: 
            numberOfCoeff = funcNumberOfCoeffDic[func] #this is necessary to pass to the curve_fit
            CoeffInitialPoint = tuple([0]*numberOfCoeff)
            popt, pcov = curve_fit(func, np.array(xdataRaw),np.array(ydata), CoeffInitialPoint)
            funcCoeffDic[(func,0)] =  popt
    
    return funcCoeffDic
    

def square(list): return [i ** 2 for i in list]


## 
# @brief this function uses the coeffs found previously (using the 
# inputTraning inputTraining) to implement the function on the inputTestdata
# The function with the least error (least deviation from the outputTestData
# wins
# 
# @param funcCoeffDic: (func:Coeff)
# @param inputTestDataRaw: 
# @param outputTestData:
# 
# @return 
def pickBestFit(funcCoeffDic, inputTestDataRaw, outputTestData, degreeNPolyMultiVarMaxDegree = 2, maximumAcceptableError = 1000):
    funcErrorListDic = defaultdict(list)
    funcErrorDic = {}
    inputReshaped = []
    
    # ---- go through all functions and find the list of error for each one. This
    # list contains the errors corresponding to each inputTestData
    for func in funcCoeffDic.keys():
        inputReshaped = []
        
        # ---- modify the input for degreeNPolyMultivar
        if (func[0] == degreeNPolyMultiVar):
            degree = func[1] 
            numberOfVar = len(inputTestDataRaw) 
            numberOfCoeff = nCr(degree + numberOfVar - 1, numberOfVar - 1)
            extraArgAdded = [degree]*len(inputTestDataRaw[0]) 
            
            inputTestData = [extraArgAdded] + inputTestDataRaw
        else:
            inputTestData = copy.copy(inputTestDataRaw)
       
        numberOfTestData =  len(inputTestData[0])
        numberOfVar = len(inputTestData) 
        inputReshaped = [[] for _ in range(numberOfTestData)]
        
        # ---- reshape the input for the sake of functions compatibility
        for testDataIndex in range(numberOfTestData):
            for varIndex in range(numberOfVar):
                inputReshaped[testDataIndex].append(inputTestData[varIndex][testDataIndex])

        # ---- find the list of errors associated with each func error
        for index,inputElement in enumerate(inputReshaped):
            funcErrorListDic[func].append(math.fabs(outputTestData[index] - func[0](inputElement, *funcCoeffDic[func])))
                
    # ---- generate the sqrt of all error for each function
    funcErrorDic = {key: math.sqrt(sum(square(value)))/len(value) for  key,value in
            funcErrorListDic.items()} 
   
    #---------guide:::  find the min error
    bestFittedFunc = min(funcErrorDic.items(), key=itemgetter(1))[0]
   
    #assert(funcErrorDic[bestFittedFunc] < maximumAcceptableError), str(funcErrorDic[bestFittedFunc])+ " is too big of an error to be acceptable. maximumAcceptableError is " + str(maximumAcceptableError)
    print bestFittedFunc 
    print funcCoeffDic[bestFittedFunc] 
    print funcErrorDic[bestFittedFunc] 
    sys.exit() 
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
def findBestFitFunction(inputTrainingData, outputTrainingData, inputTestData, outputTestData, funcNumberOfCoeffDic, degreeNPolyMultiVarMaxDegree, degreeNPolyMultiVarMinDegree, maximumAcceptableError):
    
    # ---- find coeffs for each function
    funcCoeffDic = findCoefficients(inputTrainingData, outputTrainingData, funcNumberOfCoeffDic, degreeNPolyMultiVarMaxDegree, degreeNPolyMultiVarMinDegree)
   
    # ---- find the best function that fits the data using the coeffs above and
    # testdata
    bestFittedFunc, funcErrorDic = pickBestFit(funcCoeffDic, inputTestData, outputTestData, degreeNPolyMultiVarMaxDegree, maximumAcceptableError)
    
    return bestFittedFunc,funcCoeffDic[bestFittedFunc] ,funcErrorDic






#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------guide::: testing
def main():
    #---------guide:::  only applicable to degreeNPolyMultiVar
    foo = degreeNPolyMultiVar
    
    degree = 4
    maxDegree = 5 
    minDegree = 2
    
    numberOfVar = 5 # make sure that this variable is set properly 
    inputTrainingLowerBound = 10
    inputTrainingUpperBound = 100 
    
    inputTestLowerBound = 80 
    inputTestUpperBound = 120 
    
    coeffLowerBound = 5
    coeffUpperBound = 21
    #----------------- 
    
    
    maxNumberOfReqCoeff = nCr(maxDegree + numberOfVar - 1, numberOfVar-1)
    inputTestDataLength = random.randrange(maxNumberOfReqCoeff, maxNumberOfReqCoeff+ 1)
    inputTrainingDataLength = random.randrange(maxNumberOfReqCoeff, maxNumberOfReqCoeff+ 1)
    numberOfReqCoeff = nCr(degree + numberOfVar - 1, numberOfVar-1)
    
    # ---- sets coeffs
    coeff = [random.randrange(coeffLowerBound, coeffUpperBound) for i in range(numberOfReqCoeff)]
    print "coeff is " + str(coeff)
    
    # ---- set training data
    inputTrainingDataRaw = [[] for _ in range(numberOfVar)]
    for i in range(0, inputTrainingDataLength):
        for varNumber in range(0, numberOfVar):
             #inputTrainingDataRaw[varNumber].append(random.randrange(inputTrainingLowerBound, inputTrainingUpperBound)/float(inputTrainingUpperBound))
             inputTrainingDataRaw[varNumber].append(random.randrange(inputTrainingLowerBound, inputTrainingUpperBound))
    
    # ---- set test data
    inputTestDataRaw =[] 
    inputTestDataRaw = [[] for _ in range(numberOfVar)]
    for i in range(0, inputTestDataLength):
        for varNumber in range(0, numberOfVar):
            inputTestDataRaw[varNumber].append(numpy.float64(random.randrange(inputTestLowerBound, inputTestUpperBound)))
   
         
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
    
    #---------guide:::  the input and output training data should also be given. In this case we are genrating it for functionality verification
    
    #---------guide:::  reshape the training data. This is necessary since 
    #-----------------  the format that curve_fit accept data is odd. 
    inputTrainingReshaped = []
    inputTrainingReshaped = [[] for _ in range(inputTrainingDataLength)]
    
    for index in range(0, len(inputTrainingData[0])):
        for inputNumber in range(0, len(inputTrainingData)):
            inputTrainingReshaped[index].append(inputTrainingData[inputNumber][index])
    
    outputTrainingData = [] 
    for index in range(0, len(inputTrainingReshaped)):
        outputTrainingData.append(foo(inputTrainingReshaped[index], *coeff))

    
    inputTestingReshaped = []
    for inputNumber in range(0, len(inputTestData[0])):
        inputTestingReshaped.append([])
    
    for index in range(0, len(inputTestData[0])):
        for inputNumber in range(0, len(inputTestData)):
            inputTestingReshaped[index].append(inputTestData[inputNumber][index])
    
    outputTestData = [] 
    for index in range(0, len(inputTestData[0])):
        outputTestData.append(numpy.float64(foo(inputTestingReshaped[index], *coeff)))
   
    
    maximumAcceptableError = .1*numpy.float64(sum(outputTestData)/len(outputTestData))
    print "maximumAcceptableError : " + str(maximumAcceptableError )
    
    bestFittedFunc, funcCoeff, funcErrorDic = findBestFitFunction(inputTrainingDataRaw, outputTrainingData, inputTestDataRaw, outputTestData, all_funcs.funcNumberOfCoeffDic,maxDegree, minDegree, maximumAcceptableError)
    
    # print funcError 
    print "the function that we used: " + str(foo.__name__) +", "+ str(degree)
    print "the coeff that we started with:" + str(coeff) 
    print funcErrorDic 
    print str(bestFittedFunc[0].__name__) + ", "+str(bestFittedFunc[1])
    print funcCoeff
    return bestFittedFunc, funcCoeffDic, funcErrorListDic


# test = True
test = False
if (test): 
    main()
