from math import *
import os.path

def sourceFileParse(sourceFileName):
    if not(os.path.isfile(sourceFileName)):
        print "the source file doesn't exist"
        exit();
    data = [] 
    with open(sourceFileName) as f:
        for line in f:
            if len(line.split()) >0: 
                if not(line.split() == "start" or line.split() == "end"): 
                    data.append(int(line.split() [0]))
    return data 

def getVecDif(vec1, vec2):
    diff = 0; 
    counter = 0; 
    for i in range(0, len(vec1)):
        diff += pow(vec1[i] - vec2[i],2)
        counter +=1
    return sqrt(diff)/counter




#refData= sourceFileParse("~/jpg_Dongwook/jpg_apx/quantization_results.test.txt");
#compareWidthData = sourceFileParse("~/jpg_Dongwook/jpg_apx/quantization2_results.test.txt");
refData= sourceFileParse("./test1.txt");
compareWidthData = sourceFileParse("./test2.txt");


print getVecDif(refData, compareWidthData);

