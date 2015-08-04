from math import *
import os
def generateAll(input, numOfOps):
    outputFile = "sample_op_list.txt" 
    outputFileP = open(outputFile, "w")
    for i in range(0, numOfOps):
        if input[2] > 0:
            msb = input[2] - 1
        else:
            msb = 0
        outputFileP.write(input[0] + " " + str(input[1]) + " " + str(input[2]) + " " + str(msb) + " " + str(input[3]) + "\n")
     
    outputFileP.close()



def sourceFileParse(sourceFileName):
    if not(os.path.isfile(sourceFileName)):
        print sourceFileName 
        print "the source file doesn't exist"
        exit();
    MV = [] 
    with open(sourceFileName) as f:
        for line in f:
            if len(line.split()) >1: 
                MV.append(sqrt(pow(int(line.split()[1]),2) + pow(int(line.split()[2]),2)))
    return MV

def getVecDif(vec1, vec2):
    diff = 0; 
    counter = 0; 
    for i in range(0, len(vec1)):
        diff += pow(vec1[i] - vec2[i],2)
        counter +=1
    return sqrt(diff)/counter



#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------#--------------------------------------------------------------------------------------------------------------------------------------------------------
#---------guide::: main
lowerBound =6;
UpperBound = 8;
pictureFolder ="/home/polaris/behzad/MotionEstimationWithApproximation/Debug/1stefan_cif.yuv"
numOfOps = 30 
MVRef = sourceFileParse(pictureFolder + "/MVs_accurate.vtxt");
fileVecDiff = {} 
filesToCompareList = []

#deleting the reulst file
resultFile = "vecDist.txt" 
os.chdir(pictureFolder);
os.system("rm " + resultFile);
resultFileP = open(resultFile, "w")
resultFileP.close();
#opList = ["eta1", "eta2", "loa"]
opList = ["eta1", "loa"]
#opList = ["eta2"]
for op in opList:
    for i in range (lowerBound, UpperBound):
        #generate the All possible file  
	    os.chdir("/home/polaris/behzad/MotionEstimationWithApproximation/AllPossibleInputs")
	    input_to_generate = [op, 32, i, 0]
	    generateAll(input_to_generate, numOfOps)
	    #build and run 
	    os.chdir("/home/polaris/behzad/MotionEstimationWithApproximation/Debug/")
	    os.system("make clean; make");
	    os.system("./MotionEstimationWithApproximation stefan_cif.yuv 352 288 300 8 32 1 1")
	    os.chdir(pictureFolder)
	    #dump the file  
	    newMV_file = "MVs_" + input_to_generate[0]+"_"+str(input_to_generate[2])+".vtxt" 
	    filesToCompareList.append(newMV_file) 
	    commandToRun =  "cp MVs.vtxt " + newMV_file
	    os.system(commandToRun)
	    fileName = newMV_file
	    #dumping the vecdiff results  
	    MV= sourceFileParse(fileName);
	    fileVecDiff[fileName]= getVecDif(MVRef, MV)
	    #resultFile = "vecDist.txt" 
	    resultFileP = open(resultFile, "a")
	    resultFileP.write(fileName + " " + str(fileVecDiff[fileName]) + "\n");
	    resultFileP.close();

#for fileName in filesToCompareList:
#    MV= sourceFileParse(fileName);
#    fileVecDiff[fileName]= getVecDif(MVRef, MV)
#

#print fileVecDiff


#
