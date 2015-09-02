import math
from os.path import expanduser 
import settings 
import os
from db_misc import *
from db_create_table_python_IP import *
from db_retrieve_table_python_IP import *

def get_operand_values(sourceFileName):
    try:
        f = open(sourceFileName)
    except IOError:
        handleIOError(sourceFileName, "csource file")
        exit()
    else:
        with f:
            for line in f:
                operandValues = line.replace(',', ' ').replace('/',' ').replace(';', ' ').split(' ')
                if not(operandValues):
                    "*******Error *****"
                    print "file with the address" + str(sourceFileName) + " required for gettign the operand values's first is blank"
                    exit()
                break;
    return operandValues 

def handleIOError(fileAddress, filePurpose):
    print "file with the address of " + str(fileAddress) + " " + "for the purpose of " + str(filePurpose)  + " is not found"

def findTotalTime(timeBeforeFindingResults, timeAfterFindingResults):
    beforeDay = timeBeforeFindingResults.day
    beforeHour = timeBeforeFindingResults.hour
    beforeMinute = timeBeforeFindingResults.minute

    afterDay = timeAfterFindingResults.day
    afterHour = timeAfterFindingResults.hour
    afterMinute = timeAfterFindingResults.minute

    return (afterDay - beforeDay)*1440 + (afterHour - beforeHour)*60 + (afterMinute - beforeMinute)

def write_operands_info_for_max_boundary_determination():
     
    # ---- only change the following
    x = sympy.symbols('x[0]')
    
    operandOne = [23, 35]
    operandTwo = [12,17]
    deltaOperandOne = [3, x]
    deltaOperandTwo = [2,3]
    deltaOutput = [x, 5]
    
    
    # x = sympy.symbols('x[0] x[1] x[2] x[3] x[4] x[5] x[6] x[7] x[8] x[9]')
   #  operandOne = [x[0],x[1]]
    # operandTwo = [x[2],x[3]]
    # deltaOperandOne = [x[5], x[4]]
    # deltaOperandTwo = [x[6],x[7]]
   #  deltaOutput = [x[9], x[8]]
    # ---- only change above vars
    
    assert(len(operandOne) == len(operandTwo) == len(deltaOperandOne) == 
            len(deltaOperandTwo) == len(deltaOutput)), "all the inputs need to \
                    have he same length"

    dbFileName = "operands_info_for_max_boundary.db"
    tableName = "operands_info_for_max_boundary"
    propsName = ["operandOne", "operandTwo", "deltaOperandOne", "deltaOperandTwo", "deltaOutput"]
    # propsType = ["int"]*len(propsName) 
    #propsType = ["int"]*(len(propsName) - 1) + ["string"] 
    propsType = ["mix"]*(len(propsName)) 
    propList = [ operandOne,  operandTwo,  deltaOperandOne,  deltaOperandTwo,  deltaOutput]

    # ----body 
    propsTypeConverted = [convert_python_types_to_sqlite(argType) for argType in propsType]
    propsValuesConverted = [convert_python_values_to_sqlite_compatible_values(argType,value) for argType,value in zip(propsType,propList)]

    # ---- creating  
    createDB(dbFileName, tableName, propsName, propsTypeConverted, propsValuesConverted)
 
    
def read_operands_info_for_max_boundary_determination():
    
    dbFileName = "operands_info_for_max_boundary.db"
    tableName = "operands_info_for_max_boundary"
    propsName = ["operandOne", "operandTwo", "deltaOperandOne", "deltaOperandTwo", "deltaOutput"]
    
    x = sympy.symbols('x[0]')
    if not(isinstance(x,list)):
        x = [x]
    propsType = ["mix"]*(len(propsName)) 
    # propsType = ["int"]*(len(propsName) - 1) + ["string"] 
    props, propNames, _= retrieveDB(dbFileName , tableName)
    operandOne, operandTwo, deltaOperandOne, deltaOperandTwo, deltaOutput  = [impose_type(propsType[index], prop) for index,prop in enumerate(props)]
    
    
    operandOne =[eval(element) for element in operandOne]
    operandTwo = [eval(element) for element in operandTwo]
    deltaOperandOne = [eval(element) for element in deltaOperandOne]
    deltaOperandTwo = [eval(element) for element in deltaOperandTwo]
    deltaOutput = [eval(element) for element in deltaOutput]
    
    print operandOne 
    print operandTwo 
    print deltaOperandOne 
    print deltaOperandTwo 
    print deltaOutput 
    
    return operandOne, operandTwo, deltaOperandOne, deltaOperandTwo, deltaOutput, x

def write_operands_info_for_operator_characterization():
    home = expanduser("~")
    rootFolder =  home +"/" + "apx_tool_chain"
    rootResultFolderName = rootFolder + "/" + settings.generatedTextFolderName
    if not os.path.exists(rootResultFolderName):
        handleIOError(rootResultFolderName, "for writing the operands info for operator characterization")
        exit()
    
    
    dbFileFullAddress = rootFolder + "/" + settings.operandsInfoForOperatorCharacterizationName
    
     
    operandOneExactValueLowerBound = [21, 33]
    operandOneExactValueUpperBound = [25, 37]
    operandOneExactValueStep = [3, 3]
    maxInputOperandDeviationOne = [.2, .2]
    numberOfValuesBetweenExactAndDeviationOne = [2, 2]

    operandTwoExactValueLowerBound = [10, 14]
    operandTwoExactValueUpperBound = [14, 18]
    operandTwoExactValueStep = [3, 3]
    maxInputOperandDeviationTwo = [.2, .2]
    numberOfValuesBetweenExactAndDeviationTwo = [2, 2]
     
    tableName = "operandsInfo"
    propsName =  ["names","operandOneInfo" , "operandTwoInfo"]
    propsType = ["int"] +["listFloat"] + ["listFloat"] 
   
    
    names = range(len(operandOneExactValueLowerBound))
    operandOneInfo = [] 
    operandTwoInfo = [] 
    for index in range(len(operandOneExactValueLowerBound)):
        operandOneInfo.append([operandOneExactValueLowerBound[index],operandOneExactValueUpperBound[index],operandOneExactValueStep[index], maxInputOperandDeviationOne[index], numberOfValuesBetweenExactAndDeviationOne[index]])
        operandTwoInfo.append([operandTwoExactValueLowerBound[index],operandTwoExactValueUpperBound[index],operandTwoExactValueStep[index], maxInputOperandDeviationTwo[index], numberOfValuesBetweenExactAndDeviationTwo[index]])
    
    propList = [names, operandOneInfo, operandTwoInfo]
    
    # ---- body (copy paste the rest)
    propsTypeConverted = [convert_python_types_to_sqlite(argType) for argType in propsType]
    propsValuesConverted = [convert_python_values_to_sqlite_compatible_values(argType,value) for argType,value in zip(propsType, propList)] 
    createDB(dbFileFullAddress, tableName, propsName, propsTypeConverted,propsValuesConverted)


def retrieve_operands_info_for_operator_characterization():
     # ---- necessary inputs
    home = expanduser("~")
    rootFolder =  home +"/" + "apx_tool_chain"
    dbFileName = rootFolder + "/" + settings.operandsInfoForOperatorCharacterizationName
    tableName = "operandsInfo"
    
    # ---- get this from the module that calles createDB
    propsType = ["int"] +["listFloat"] + ["listFloat"] 
    
    # ---- body (copy past only the line bellow)
    props, propNames, propType = retrieveDB(dbFileName, tableName)
    # names, city, friends, age = [impose_type(propType[index + 1], prop) for index,prop in enumerate(props)]
    # ---- this line changes based on the properties
    names, operandsOneInfo, operandTwoInfo = [impose_type(propsType[index], prop) for index,prop in enumerate(props)]
    return operandsOneInfo, operandTwoInfo 


def findTotalTimeInSecond(timeBeforeFindingResults, timeAfterFindingResults):
    beforeDay = timeBeforeFindingResults.day
    beforeHour = timeBeforeFindingResults.hour
    beforeMinute = timeBeforeFindingResults.minute
    beforeSecond = timeBeforeFindingResults.second
    
    afterDay = timeAfterFindingResults.day
    afterHour = timeAfterFindingResults.hour
    afterMinute = timeAfterFindingResults.minute
    afterSecond = timeAfterFindingResults.second
    
    return (afterDay - beforeDay)*1440*60 + (afterHour - beforeHour)*60*60 + (afterMinute - beforeMinute)*60 + (afterSecond - beforeSecond)





def withinSomePercent(valOfInquiry, refVal, desiredMargin):
#    print "here is the refVal" + str(refVal)
#    print "valOfInquiry" + str(valOfInquiry)
    percentageError =  (math.fabs(refVal - valOfInquiry))/refVal
#    print percentageError
#    print (float(desiredMargin)/100)
#    print "done" 
    if percentageError < (float(desiredMargin)/100):
#        print "gotit" 
        return True
    else:
        return False



def getApxBit(setUp):
    return int(setUp[0].split()[2])
