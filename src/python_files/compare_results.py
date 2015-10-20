from math import *
import os
import sys
import matplotlib.pyplot as plt
import settings
from list_all_files_in_a_folder import *
import numpy
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import numpy as np

def getSetUpNumFromText(myList):
    return myList[1]


def getNoiseFromText(myList):
    return myList[-2]

def getEnergyFromText(myList):
    return myList[-1]


def getAllOpsFromText(myList):
    return myList[2:-2]


def getSetUpNumFromlist(myList):
    return myList[0]


def getNoiseFromlist(myList):
    return myList[-2]

def getEnergyFromlist(myList):
    return myList[-1]


def getOpsFromlist(myList):
    return myList[1]






def getSomeOpsFromText(myList, startIndex, endIndex):
    if endIndex > (len(myList) - 1):
        print "*********************ERROR*************"
        print "index is not acceptable. Check it"
        exit()
    if( startIndex >= endIndex) :
        print "*********************ERROR*************"
        print "start index can not be equal or bigger than endIndex"
        exit()
    if( startIndex < 0):
        print "*********************ERROR*************"
        print "start index can not be less than zero"
        exit()
    

    return myList[startIndex:endIndex+1]

def extractRequiredInfo(sourceFileName, startingOpNum, endingOpNum):
    inputFileDic = {} 
    #whether the file exist or no 
    if not(os.path.isfile(sourceFileName)):
        print "source file with the name " + sourceFileName + "doesn't exist"
        exit();
    noise = [] 
    setup = 0 #the specific setup(same configuration but different type of operators) 

    with open(sourceFileName) as f:
        for line in f:
            if len(line.split()) >0: 
                stripedLine =  line.rstrip().replace(';', ' ').replace('(', ' ').replace(')', ' ').replace(']', ' ').replace('[',  ' ').replace("'", ' ').replace("\n", ' ').split(',') #find the lines with key word and write it to another file
                for word in stripedLine:
                    if ("inputFile" in word):
                        fileName = line.rstrip().replace(';', ' ').replace('(', ' ').replace(')', ' ').replace(']', ' ').replace('[',  ' ').replace("'", ' ').replace("\n", ' ').split(' ')[5] #find the lines with key word and write it to another file
                        Ops = [] #contain information regarding an inputFile Operators
                        inputFileDic[fileName] = [] #contain info regarding an inputFile energy, noise and ops

                    if "paretoResult" in word:
                        energy = getEnergyFromText(stripedLine)
                        noise = getNoiseFromText(stripedLine)
                        setUpNumber = getSetUpNumFromText(stripedLine) 
                        Ops = getSomeOpsFromText(getAllOpsFromText(stripedLine), startingOpNum,endingOpNum)
                        inputFileDic[fileName].append((setUpNumber, Ops, noise, energy))
                        break 


    return inputFileDic 


def getRidOfLeadingAndTailingSpaces(myListElement):
    return myListElement.replace("''",'').rstrip().lstrip()


def compareResults(sourceFile1Name, sourceFile2Name, startingOpNumforFile1, endingOpNumForFile1, startingOpNumforFile2, endingOpNumForFile2):
    #---------guide:::  get the information from the source files
    inputFile1Dic = extractRequiredInfo(sourceFile1Name, int(startingOpNumforFile1), int(endingOpNumForFile1))
    inputFile2Dic = extractRequiredInfo(sourceFile2Name, int(startingOpNumforFile2), int(endingOpNumForFile2))
    #---------guide:::  compare them
    for key in inputFile1Dic.keys():
        if not(key in inputFile2Dic.keys()):
            print "*********************ERROR*****************" 
            print "input should be the same for both of the files"
            exit()

    foundEqual = False #this variable indicates whether a pareto point has been found in both results
    for key in inputFile1Dic.keys():
        file1Values = inputFile1Dic[key] #pareto points for one input
        file2Values = inputFile2Dic[key] #pareto points for one input
        for paretoPointNumberAssWithFile1 in range(0,len(file1Values),1):
            for paretoPointNumberAssWithFile2 in range(0,len(file2Values),1):
                if (map(getRidOfLeadingAndTailingSpaces, getOpsFromlist(file1Values[paretoPointNumberAssWithFile1])) == map(getRidOfLeadingAndTailingSpaces, getOpsFromlist(file2Values[paretoPointNumberAssWithFile2]))):
                    foundEqual = True 
                    break
            if not(foundEqual): 
	            print "------------------------------" 
	            print "this is the pareto point found in " + sourceFile1Name + " but not found in" + sourceFile2Name 
	            print getOpsFromlist(file1Values[paretoPointNumberAssWithFile1])
	#	        print "this is the pareto point associated with the second file" 
	#	        print getOpsFromlist(file2Values[paretoPointNumberAssWithFile1])
	            print "------------------------------" 
            foundEqual = False 
    return inputFile1Dic, inputFile2Dic

    
def compareResultsTest():
    sourceFile1Name = "/home/polaris/behzad/apx_tool_chain/input_output_text_files/final_results1.txt"
    sourceFile2Name = "/home/polaris/behzad/apx_tool_chain/input_output_text_files/final_results2.txt"
    inputFile1Dic,inputFIle2Dic = compareResults(sourceFile1Name, sourceFile2Name, 0, 2, 0,1)
    
#    for key in inputFile1Dic.keys():
#        print key 
#        for paretoPoint in inputFile1Dic[key]:
#            print getOpsFromlist(paretoPoint) 

#compareResultsTest()
def main():
    if len(sys.argv) < 7:
        print "***ERROR***"
        print "the number of inputs provided are not consistant with the need of this file"
        print "inputs with the following type and order are necessary" 
        print "1.sourceFile1Name"
        print  "2.sourceFile2Name"
        print "3.startingOpNumforFile1" 
        print"4.endingOpNumForFile1" 
        print "5.startingOpNumforFile2" 
        print"6.endingOpNumForFile2"
        exit()

    #-----acquaring the inputs
    sourceFile1Name = sys.argv[1]
    sourceFile2Name = sys.argv[2]
    startingOpNumforFile1 = sys.argv[3]
    endingOpNumForFile1 =  sys.argv[4]
    startingOpNumforFile2 =  sys.argv[5]
    endingOpNumForFile2 =   sys.argv[6]
    inputFile1Dic,inputFIle2Dic = compareResults(sourceFile1Name, sourceFile2Name,startingOpNumforFile1, endingOpNumForFile1, startingOpNumforFile2, endingOpNumForFile2)
    inputFile1Dic,inputFIle2Dic = compareResults(sourceFile2Name, sourceFile1Name,startingOpNumforFile2, endingOpNumForFile2, startingOpNumforFile1, endingOpNumForFile1)

main()
/home/polaris/behzad/apx_tool_chain/all_input_scenarios.txt
YES
/home/polaris/behzad/apx_tool_chain/src/CSrc/
pickled_results
False
finalResult.txt
YES
['/home/polaris/behzad/apx_tool_chain/src/CSrc/mat_mul_unfolded_algo0.cpp', '/home/polaris/behzad/apx_tool_chain/src/CSrc/mat_mul_unfolded_algo1.cpp']
/home/polaris/behzad/apx_tool_chain/inputPics/roki_noisy.jpg
/home/polaris/behzad/apx_tool_chain/inputPics/roki.jpg
/home/polaris/behzad/apx_tool_chain
