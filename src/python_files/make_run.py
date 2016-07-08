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
#change
# @file make_run.py
# @brief This file contains modules regarding  building and running the Module under test(the one that needs to be approximated)
# @author Behzad Boroujerdian
# @date 2015-07-01



from math import *
import os
import sys 
import make
import run 
import settings 

#def sourceFileParse(sourceFileName):
#    if not(os.path.isfile(sourceFileName)):
#        print sourceFileName 
#        print "the source file doesn't exist"
#        exit();
#    MV = [] 
#    with open(sourceFileName) as f:
#        for line in f:
#            if len(line.split()) >1: 
#                MV.append(sqrt(pow(int(line.split()[1]),2) + pow(int(line.split()[2]),2)))
#    return MV
#
def getVecDif(vec1, vec2):
    diff = 0; 
    counter = 0; 
    for i in range(0, len(vec1)):
        diff += pow(vec1[i] - vec2[i],2)
        counter +=1
    return sqrt(diff)/counter



## 
# @brief this is a helper module is for some behaviour testing. it parses a file and prints the lines in the file
# 
# @param srcFileName
# 
# @return 
def parseAndPrint(srcFileName):
    srcFilePtr = open(srcFileName, "r")
    for line in srcFilePtr:
        print line
    print "done"
    srcFilePtr.close()

 

## 
# @brief this module builds and runs one version of the src file (a version with one instance of the sample space)
# 
# @param CSrcFolder: what folder to get the C source file from
# @param executableName: what is the executable name
# @param executableInputList: what are the executable inputs
# @param resultFolderName: what folder to store the results
# @param resultFileName: what file to store the result to
# 
# @return no return
def make_run(executableName, executableInputList, resultFolderName, resultFileName, CBuildFolder, operandSampleFileName, bench_suit_name, process_id):
    if (bench_suit_name == "my_micro_benchmark"): 
        #validating the number of inputs
        #validating the existance of the dir, and making it other wise
        if not os.path.isdir(resultFolderName): 
            print "the folderName provided does not correspond to any existing folder. I will be making it"

            os.system("mkdir " + resultFolderName);
        
        if not os.path.isfile(operandSampleFileName):
            print "the operandSampleFileName:" + operandSampleFileName + " does not exist"
            exit()


        currentDir = os.getcwd() #getting the current directory
        #CBuildFolder = "./../../Debug" 
        os.chdir(CBuildFolder) #chaning the directory
        make.make()
        run.run(executableName, resultFolderName, resultFileName, settings.operatorSampleFileName, operandSampleFileName)
        os.chdir(currentDir) #chaning the directory
    elif (bench_suit_name == "sd-vbs"): 
        currentDir = os.getcwd() #getting the current directory
        os.chdir(CBuildFolder) #chaning the directory
        os.system("pwd"); 
        #os.system("gdb --args ./sift ~/behzad_local/sd-vbs/benchmarks/sift/data/sim");
        if (settings.runMode == "parallel"): 
            os.system("gmake c-run " + "exe_annex="+str(process_id))
        else:  
            os.system("gmake c-run " + "exe_annex="+str(0))
        os.chdir(currentDir) #chaning the directory

    
   


#    os.chdir(resultFolderName) #chaning the directory
#    resultFileP = open(resultFileName, "a")
#    resultFileP.close();
#    
    
    os.chdir(currentDir)
	

#os.system("make clean; make");
#os.system("./apx_tool_chain stefan_cif.yuv 352 288 300 8 32 1 1")
#os.chdir(pictureFolder)



#
#for op in opList:
#    for i in range (lowerBound, UpperBound):
#        #generate the All possible file  
#	    os.chdir("/home/polaris/behzad/MotionEstimationWithApproximation/AllPossibleInputs")
#	    input_to_generate = [op, 32, i, 0]
#	    #generateAll(input_to_generate, numOfOps)
#	    #build and run 
#	    os.chdir("/home/polaris/behzad/MotionEstimationWithApproximation/Debug/")
#	    os.system("make clean; make");
#	    os.system("./MotionEstimationWithApproximation stefan_cif.yuv 352 288 300 8 32 1 1")
#	    os.chdir(pictureFolder)
#	    #dump the file  
#	    newMV_file = "MVs_" + input_to_generate[0]+"_"+str(input_to_generate[2])+".vtxt" 
#	    filesToCompareList.append(newMV_file) 
#	    commandToRun =  "cp MVs.vtxt " + newMV_file
#	    os.system(commandToRun)
#	    fileName = newMV_file
#	    #dumping the vecdiff results  
#	    MV= sourceFileParse(fileName);
#	    fileVecDiff[fileName]= getVecDif(MVRef, MV)
#	    #resultFile = "vecDist.txt" 
#	    resultFileP = open(resultFile, "a")
#	    resultFileP.write(fileName + " " + str(fileVecDiff[fileName]) + "\n");
#	    resultFileP.close();
#
#for fileName in filesToCompareList:
#    MV= sourceFileParse(fileName);
#    fileVecDiff[fileName]= getVecDif(MVRef, MV)
#

#print fileVecDiff


#
