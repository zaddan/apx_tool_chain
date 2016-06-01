import shutil
from scipy import optimize
from os.path import expanduser 
import itertools
import pylab
import sys
import os
import datetime
from collections import defaultdict 


from inputs import *
from src_parse_and_apx_op_space_gen import *
from modify_operator_sample_file import *
#from sample_operand_and_sweep_apx_space import *
import settings 
from extract_result_properties import *
from plot_generation import *
import matplotlib.pyplot as plt
from find_position import *
from write_readable_output import *
from clean_up import *
from simulating_annealer import *
from misc import *
from curve_fit import *
from db_create_table_python_IP import *
from db_retrieve_table_python_IP import *
from characterize_operators import *

class operator:
    def __init__(self, name):
        self.name = name
    
    def setFunctionType(self, func):
        self.funcType = func
    
    def getFunctionType(self):
        return self.funcType
   

    def setFunctionName(self, funcName):
        self.funcName = funcName 
    
    def getFunctionType(self):
        return self.funcName

    def setFunction(self, variables, *coeffs):
        assert not(self.funcType == None), "func type is not defined for this object"
        if (self.funcName == 'degreeNPolyMultiVar'):
            self.func = self.funcType(variables, *coeffs)[0]
        else:
            self.func = self.funcType(variables, *coeffs)
    
    def getFunction(self):
        return self.func
    
    def setUpperBound(self, upperBoundValue):
        self.upperBoundValue = upperBoundValue

    def setLowerBound(self, lowerBoundValue):
        self.lowerBoundValue = lowerBoundValue

    def getUpperBound(self):
        return self.upperBoundValue 

    def getLowerBound(self, lowerBoundValue):
        return self.lowerBoundValue 


def find_apx_bit_boundary():
    home = expanduser("~") 
    originalCSrcFileAddress = repo_root_address + "/apx_tool_chain/CSrc_examples/simple_dfg_2_operator.cpp"
    assert(os.path.isfile(originalCSrcFileAddress)), str(originalCSrcFileAddress) + " does not exist" 
    CSrcFolderAddress =  repo_root_address + "/apx_tool_chain/src/CSrc/"
    CSrcFileAddress = repo_root_address + "/apx_tool_chain/src/CSrc/test.cpp"
    # ---- copying because characterize_operators will modify the source file that it uses
    # ---- thus we keep the original file somewhere else and copy it over
    shutil.copy(originalCSrcFileAddress, CSrcFileAddress) 
    
    generateMakeFile = "YES"
    rootFolder  = repo_root_address +  "/apx_tool_chain"
    finalResultFileName =  "finalResult2.txt"
    
    lOfAcceptableModes = [ "all", "findLowUpBounery", "genOperandDicAndFindLowUpBounery", "genOperandDic"]
    moduleFunctionality = "all"
    # moduleFunctionality = "findLowUpBounery" 
    # moduleFunctionality = "genOperandDicAndFindLowUpBounery"
    # moduleFunctionality = "genOperandDic"
    moduleFunctionality = "FindBestFittedCurve"
    
    percentageOfDataUsedForTraining = .7
    workWithNegativeNumbers = False
    numberOfOperands = 2 
    signalToNoiseRatio = .1
    degreeNPolyMultiVarMinDegree = 1 
    degreeNPolyMultiVarMaxDegree = 3
    # ---- prepare inputs for operand generation and write in a table
    write_operands_info_for_operator_characterization()
    # ---- retrieve the infr from the table above
    listOfOperandOneGenValues, listOfOperandTwoGenValues = retrieve_operands_info_for_operator_characterization()
    operatorArchiveAddress = repo_root_address + "/apx_tool_chain/operator_archive"
    characterize_all_operators(CSrcFolderAddress, CSrcFileAddress, generateMakeFile,
            rootFolder, finalResultFileName, operatorArchiveAddress,  
            percentageOfDataUsedForTraining, workWithNegativeNumbers, 
            degreeNPolyMultiVarMinDegree, degreeNPolyMultiVarMaxDegree, signalToNoiseRatio,
            listOfOperandOneGenValues, listOfOperandTwoGenValues, moduleFunctionality)
    
    # # ---- retievig the data from the dbfile
    lOfFunc_degree_tuple = [] #contains the (func, degree) tuple
    props, propNames, _= retrieveDB("funcInfo.db" , "funcInfo")
    propsName = ["opNumber", "funcName", "funcCoeff"]
    propsType = ["int"] +["tuple"] + ["listFloat"] 
    lOfOpNumber, lOffuncName_degree_tuple, lOfFuncCoeff = [impose_type(propsType[index], prop) for index,prop in enumerate(props)]
    
    # ---- getting the operands
    write_operands_info_for_max_boundary_determination()
    operandOne, operandTwo, deltaOperandOne, deltaOperandTwo, deltaOutput, lOfSymbols = read_operands_info_for_max_boundary_determination()
    operatorInuptsTupleList = zip(operandOne, operandTwo, deltaOperandOne, deltaOperandTwo, deltaOutput)
    operatorInuptsListList = map(lambda x: list(x), operatorInuptsTupleList)
    operatorNumberOperatorInputDic = dict(zip(range(len(operatorInuptsListList)), operatorInuptsListList)) 
     
    print operatorInuptsListList
    
      
    # ---- setting up the func for each operator symbolically
    lOfOperatorObjects = []  
    for index, funcName_degree in enumerate(lOffuncName_degree_tuple):
        lOfOperatorObjects.append(operator(str(index)))
        coeff = lOfFuncCoeff[index] 
        funcName =  funcName_degree[0]
        degree = funcName_degree[1]
        funcType = eval(funcName)
        variables = operatorNumberOperatorInputDic[index]
        if (funcName == "degreeNPolyMultiVar"):
            variables.insert(0, degree) 
        lOfOperatorObjects[index].setFunctionType(funcType)
        lOfOperatorObjects[index].setFunctionName(funcName)
        lOfOperatorObjects[index].setFunction(variables, coeff)
        print lOfOperatorObjects[index].getFunction()
     
    for operatorObj in lOfOperatorObjects:
        print "here is the foo" 
        print operatorObj.getFunction()
    sys.exit() 
    funcToOptimize = 0 
    for operatorObj in lOfOperatorObjects:
        funcToOptimize += operatorObj.getFunction()
    
    print funcToOptimize
    print "partial derivative" 
    partialDerivateDic = {} 
    for symbolElement in lOfSymbols:
        partialDerivateDic[symbolElement] = funcToOptimize.diff(symbolElement)
    
    # ---- somehow find the values of symbolic elements
    for index, derivative in enumerate(partialDerivateDic):
        func = lambda x: partialDerivateDic[derivative].subs(lOfSymbols[index], x)
        sol = optimize.fsolve(func, [1]) 
    def findSymbolValues():
        lOfSymbolValues = []
        for index, derivative in enumerate(partialDerivateDic):
            func = lambda x: partialDerivateDic[derivative].subs(lOfSymbols[index], x)
            sol = optimize.fsolve(func, [1]) 
            lOfSymbolValues.append(sol) 
        return lOfSymbolValues 
    
    lOfSymbolValues = findSymbolValues() 
    print lOfSymbolValues
    lOfSymbolValues = [52.71]
    lOfSymbolValues = [-91.658]
    for operatorObj in lOfOperatorObjects:
        for value,symbol in zip(lOfSymbolValues, lOfSymbols):
            operatorObj.setUpperBound(operatorObj.getFunction().subs(symbol, value))

    for operatorObj in lOfOperatorObjects:
        print operatorObj.getUpperBound()
     

    # print funcToOptimize 
    
    # print "partial derivative" 
    # partialDerivateDic = {} 
    # for symbolElement in lOfSymbols:
        # partialDerivate[symbolElement] =  (funcToOptimize.diff(symbolElement))
    
    
     # for operatorNumber in operatorNumberOperatorInputDic:  
          
    #      operatorNumberOperatorInputDic[operatorNumber]
     # operandOne, operandTwo, deltaOperandOne, deltaOperandTwo, deltaOutput, lOfSymbols = 
    

    # for funcName_degree_tuple_string_tuple in lOffuncName_degree_string_tuple: 
        # lOfFunc_degree_tuple.append(tuple((eval(eval(funcName_degree_tuple_string_tuple)[0]), eval(funcName_degree_tuple_string_tuple)[1])))
    
    # print lOfFunc_degree_tuple


find_apx_bit_boundary()    
 
