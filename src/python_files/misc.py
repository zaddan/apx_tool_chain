import math
from os.path import expanduser 
import settings 
import os
from db_misc import *
from db_create_table_python_IP import *
from db_retrieve_table_python_IP import *

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



def write_operands_info_for_operator_characterization():
    home = expanduser("~")
    rootFolder =  home +"/" + "apx_tool_chain"
    rootResultFolderName = rootFolder + "/" + settings.generatedTextFolderName
    if not os.path.exists(rootResultFolderName):
        handleIOError(rootResultFolderName, "for writing the operands info for operator characterization")
        exit()
    dbFileName = rootFolder + "/" + settings.operandsInfoForOperatorCharacterizationName
    operandOneExactValueLowerBound = 13
    operandOneExactValueUpperBound = 20 
    operandOneExactValueStep = 3
    maxInputOperandDeviationOne = .2
    numberOfValuesBetweenExactAndDeviationOne = 2

    operandTwoExactValueLowerBound = 10 
    operandTwoExactValueUpperBound = 20 
    operandTwoExactValueStep = 3
    maxInputOperandDeviationTwo = .2
    numberOfValuesBetweenExactAndDeviationTwo = 5
     
    tableName = "operandsInfo"
    propsName =  ["names","operandOneInfo" , "operandTwoInfo"]
    propsType = ["int"] +["listFloat"] + ["listFloat"] 
    
    names = range(1)
    operandOneInfo = [[operandOneExactValueLowerBound,operandOneExactValueUpperBound,operandOneExactValueStep, maxInputOperandDeviationOne, numberOfValuesBetweenExactAndDeviationOne]]
    operandTwoInfo = [[operandTwoExactValueLowerBound,operandTwoExactValueUpperBound,operandTwoExactValueStep, maxInputOperandDeviationTwo, numberOfValuesBetweenExactAndDeviationTwo]]
    propList = [names, operandOneInfo, operandTwoInfo]
    
    # ---- body (copy paste the rest)
    propsTypeConverted = [convert_python_types_to_sqlite(argType) for argType in propsType]
    for index, argType in enumerate(propsType):
        if "list" in argType:
            propList[index] = [' '.join(map(str, element)) for element in propList[index]] 
    createDB(dbFileName, tableName, propsName, propsTypeConverted,propList)


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
