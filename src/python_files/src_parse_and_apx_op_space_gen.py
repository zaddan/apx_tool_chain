 
# Copyright (C) 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
# 
## 

# @file   src_sweep_and_apx_op_space_gen.py 
# @brief this file contains modules for sweeping the src file and generating all the possible aproximate versions of the operations found (this operations
# need to be flagged before running this file)
# Note: make sure to change OpTypOpKind list according to the types and versions that you want
# Note: to run this file, make sure you provide it with a src file
# @author Behzad Boroujerdian
# @date 2015-06-30



import itertools
import sys
from GenOpSpace import GenOpSpace
import os.path
import settings
from misc import * 
import linecache
#CSrcDir = "../MotionEstimation/"
#CSrcDir = "./"
#global variables


#sourceFileName = CSrcDir + "all_ops_test.cpp"
#sourceFileName = CSrcDir + "test.txt"



## 
# @brief subtracting a string from another (a from b)
# 
# @param a
# @param b
# 
# @return 
def subtract(a, b):                              
    return "".join(a.rsplit(b))

## 
# @brief parses the source file (the one that needs to be approximated) and find all the ops that are approximatable
# 
# @param sourceFileName: the file whoose ops need to be replaced with apx one
# @param lAllOpsInSrcFile: list of all the ops within the src file which can be replaced with the apx version
# 
# @return no return, infact, lAllOpsInSrcFile is where we store the output
def sourceFileParse(sourceFileName):
    lAllOpsInSrcFile = [] 
    # if not(os.path.isfile(sourceFileName)):
        # print "the source file doesn't exist"
        # exit();
    try:
        f = open(sourceFileName)
    except IOError:
        handleIOError(sourceFileName, "csource file")
        exit()
    else:
        with f:
            count = 0
            for line in f:
                for words in line.replace(',', ' ').replace('/',' ').replace(';', ' ').split(' '): #find the lines with key word and write it to another file
                    if words.strip() in settings.lAccurateOpFlags:
                        lAllOpsInSrcFile.append(words.strip())
                    if "Ignore" in words.strip() and subtract(words.strip(), "Ignore") in settings.lAccurateOpFlags: #if ignore is part of the words, that means you can ignore that operator, but still add it
                        lAllOpsInSrcFile.append(words.strip())
                    if "Limited" in words.strip() and subtract(words.strip(), "Ignore") in settings.lAccurateOpFlags: #if ignore is part of the words, that means you can ignore that operator, but still add it
                        count +=1; 
    return lAllOpsInSrcFile
def generateLimited(opIndexSelected, opTypeOpKind):
    for index, opVersion in enumerate(opTypeOpKind):
        if index in opIndexSelected:
            result.append(opVersion)

    print results 
    return results

def getOpIndexSelected(srcFile, opIndex):
    result =[]
    line = linecache.getline(srcFile, opIndex).split()
    result = map(lambda x: float(x), line) 
    return result
  
     

def generateAllPossibleScenariosForEachOperator(outputFile, lAllOpsInSrcFile):
    allPossibleScenariosForEachOperator = []
    allPossibleScenariosForEachOperator = [] 
    opIndexSelectedFile = settings.opIndexSelectedFile 
    limitedListIndecies = [] 
    ignoreListIndecies = [] 
    accurateConfig = [] 
    for opIndex,element in enumerate(lAllOpsInSrcFile):
        if "Ignore" in element:
            allPossibleScenariosForEachOperator.append([settings.OpTypeOpKind[subtract(element,"Ignore")][0]])
            ignoreListIndecies.append(opIndex)
            accurateConfig.append(settings.OpTypeOpKind[subtract(element,"Ignore")][0])
        elif "Limited" in element:
            limitedListIndecies.append(opIndex)
            accurateConfig.append(settings.OpTypeOpKind[subtract(element,"Limited")][0])
            # opIndexSelected = getOpIndexSelected(opIndex,opIndexSelectedFile) 
        #     allPossibleScenariosForEachOperator.append(generateLimited(opIndexSelected,settings.OpTypeOpKind[subtract(element,"Limited")))
        else:
            allPossibleScenariosForEachOperator.append(copy.deepcopy(settings.OpTypeOpKind[element]))
            accurateConfig.append(settings.OpTypeOpKind[element][0])
    return allPossibleScenariosForEachOperator, limitedListIndecies, ignoreListIndecies, accurateConfig 

def turnAListOfTuplesToAListOfLists(listOfTuples):
    resultList = [] 
    for element in [listOfTuples][0]:
        resultList.append(element); 
    
    return resultList



def generateWorkingList(ignoreIndexList, allPossibleScenariosForEachOperator):
    accurateScenario = []  
    #ignoreIndexList = []
    workingList =[] 
    count1 = 0;
    count2 = 0;
    for index,operator in enumerate(allPossibleScenariosForEachOperator):
        if not(index in ignoreIndexList):
            workingList.append(index) 
            count2+=1
        # accurateScenario.append(operator[0])
        #settings.OpTypeOpKind[subtract(element,"Ignore")][0]
        #    ignoreListIndecies.append(opIndex)

        #accurateScenario.append(operator[0])
    return workingList 
    #return accurateScenario, workingList
#
def generateAllPossibleApxScenariousList(allPossibleScenariosForEachOperator):
    permutedList = list(itertools.product(*allPossibleScenariosForEachOperator))
    listOfAllPossibleApxScenarious = map(turnAListOfTuplesToAListOfLists, permutedList)
    return listOfAllPossibleApxScenarious
## 
# @brief generate a possible apx scenario
# 
# @param outputFile: where to write the result. The result 
# @param lAllOpsInSrcFile: list of ops that can be aproximated
# 
# @return  no return. outputFile is where all the results are written into
def generateAPossibleApxScenarios(outputFile, allPossibleApxScenarioursList, permListIndex, mode ):
    setUp = allPossibleApxScenarioursList[permListIndex]
    #writing the result to an output file
    #this step is introduce to clear the content of the file left from that last run
    if (len(allPossibleApxScenarioursList) == (permListIndex + 1)):
        status = "done" 
    else:
        status = "undone" 

    return status, setUp 
#    outputFileP = open(outputFile, "w")
#    outputFileP.close()
#    outputFileP = open(outputFile, "w")
#    for element in setUp:
#        outputFileP.write("************start*******\n");
#        print  
#        for value in element:
#             
#            outputFileP.write(str(value).replace('[', '').replace(']', '').replace(',', '').replace("'", ''));
#            outputFileP.write("\n")
#        outputFileP.write("************end*******\n");
#    outputFileP.close()
#    if (len(allPossibleApxScenarioursList) == (permListIndex + 1)):
#        return "done"
#    else:
#        return "notDone"
#




## 
# @brief this module parse the src and sweep the apx space of the all the accurate ops in the src
# 
# @param sourceFileName: the source to be parsed
# 
# @return 
#def src_parse_and_apx_op_space_gen(outputFolder, sourceFileName):
#    #print lAllOpsInSrcFile
#    #generate different permutations, using the lAllOpsInSrcFile generated in the previous stage 
#    return generateAPossibleApxScenarios(outputFolder + "/" + settings.AllPossibleApxOpScenarios, lAllOpsInSrcFile)
#
