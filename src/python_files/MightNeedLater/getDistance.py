from math import *
import os.path

def sourceFileParse(sourceFileName):
    if not(os.path.isfile(sourceFileName)):
        print "the source file doesn't exist"
        exit();
    MV = [] 
    with open(sourceFileName) as f:
        for line in f:
            if len(line.split()) >3: 
                MV.append(sqrt(pow(int(line.split()[1]),2) + pow(int(line.split()[2]),2)))
    return MV

def getVecDif(vec1, vec2):
    diff = 0; 
    counter = 0; 
    for i in range(0, len(vec1)):
        diff += pow(vec1[i] - vec2[i],2)
        counter +=1
    return sqrt(diff)/counter


MVRef = sourceFileParse("test.txt");
filesToCompareWith = ["test2.txt", "test3.txt"]

fileVecDiff = {} 
for fileName in filesToCompareWith:
    MV= sourceFileParse(fileName);
    fileVecDiff[fileName]= getVecDif(MVRef, MV)
    
print fileVecDiff

