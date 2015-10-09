import os
import sys
import copy
def sourceFileParse(inputFileName, dest1, matWidth, matHeight, numberOfMatToMultiply):
    unfoldedWriteP = open(dest1+".cpp", "w")                                                
    unfoldedTransformedWriteP =[]
    for i in range(numberOfMatToMultiply-1): 
        unfoldedTransformedWriteP.append(open(dest1+str(i)+".cpp", "w")                                                )
    counter = 0 
    try:                                                                        
        f = open(inputFileName)                                                
    except IOError:                                                             
        handleIOError(sourceFileName, "csource file" )                                               
        exit()                                                                  
    else:                                                                       
        with f:                                                                 
            for line in f:                                                      
                if ("start_generation" in line.split()):
                    for indexI  in range(matWidth):
                        i = indexI
                        for indexJ  in range(matWidth):
                            j=indexJ
                            unfoldedWriteP.write("//------calculating element " +str(i) + " and " +str(j)+ "\n")
                            
                            for z in range(numberOfMatToMultiply -1): 
                                unfoldedTransformedWriteP[z].write("//------calculating element " +str(i) + " and " +str(j)+ "\n")
                            
                            unfoldedWriteP.write("sum = 0;\n") 
                            for z in range(numberOfMatToMultiply -1): 
                                unfoldedTransformedWriteP[z].write("sum = 0;\n") 
                            for indexK in range(matHeight):
                                k=indexK
                                unfoldedWriteP.write("mulTemp = A[" + str(i)+"][" + str(k)+ "]*B["+ str(k)+ "][" + str(j) + "];\n")
                                for z in range(numberOfMatToMultiply -1): 
                                    unfoldedTransformedWriteP[z].write("mulTemp = myOp[" +str(counter) + "]->calc(A[" + str(i)+"][" + str(k)+ "],B["+ str(k)+ "][" + str(j) + "]); //MultiplicationOp\n")
                                
                                counter+=1 
                                unfoldedWriteP.write("sum = sum + mulTemp;\n")
                                for z in range(numberOfMatToMultiply -1): 
                                    unfoldedTransformedWriteP[z].write("sum = myOp["+str(counter)+"]->calc(sum, mulTemp); //AdditionOp\n")
                                counter+=1 
                            unfoldedWriteP.write("C[" + str(i) + "][" + str(j) + "] = sum;\n")
                            for z in range(numberOfMatToMultiply -1): 
                                unfoldedTransformedWriteP[z].write("C[" + str(i) + "][" + str(j) + "] = sum;\n")
                            
                
                elif ("//name" in line.split()):
                    unfoldedWriteP.write(line);
                    for z in range(numberOfMatToMultiply -1): 
                        print "******" 
                        newLine = line; 
                        newLineSplit = newLine.split() 
                        newLineSplit[1]=line.split()[1]+"_"+str(z)
                        unfoldedTransformedWriteP[z].write(' '.join(newLineSplit));
                else:
                   unfoldedWriteP.write(line);
                   for z in range(numberOfMatToMultiply -1): 
                       unfoldedTransformedWriteP[z].write(line);
def main():
    inputFileName = "mat_mul_for_parse.txt"
    dest1 = "mat_mul_unfolded_algo"
    matWidth = int(sys.argv[1])
    matHeight = int(sys.argv[2])
    numberOfMatToMultiply = int(sys.argv[3])
    sourceFileParse(inputFileName, dest1, matWidth, matHeight, numberOfMatToMultiply)
    
main()
