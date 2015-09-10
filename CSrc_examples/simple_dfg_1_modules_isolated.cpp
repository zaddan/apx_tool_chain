/**
* @file RecME.cpp
* @author Muhammad Usman Karim Khan
* Group: Prof. Joerg Henkel at Chair for Embedded Systems (CES), KIT
* @brief This file contains the computational adaptation for both number
* of threads and the frequency of the cores.
*/

#include <fstream>

#include "Operators.h"
#include "Utilities.h"
#include "operatorFile_parser.h"
#include "setSubType.h"
#include "operandFile_parser.h"
#include "globals.h"
using namespace std;
extern hw_ac **myOp;   
extern vector<int> inputVar;

int foo(int a){
    int b = myOp[0]->calc(a,inputVar[2]); //AdditionOp
    return b;
}
//int notMain(){ //uncomment when you want to run the run_unit_tests
int main(int argc, char* argv[]){
    string resultFolderName; 
    string resultFileName; 
    string operatorFileName;
    string operandFileName;
    if (argc != 5) {
        cout<< "provide the name of the file that you want the result to be written to"<<endl;
        cout<< "Example: resultFolderName.txt resultFile.txt operatorFile.txt"<<endl; 
        return 0; 
    }else{
        resultFolderName= argv[1]; 
        resultFileName = argv[2]; 
        operatorFileName = argv[3]; 
        operandFileName = argv[4]; 
    }

    assign_global_variables(resultFolderName, operatorFileName, operandFileName);
    string resultFileNameCompleteAddress = resultFileName;
    ofstream resultFile;
    resultFile.open(resultFileNameCompleteAddress.c_str(), ios_base::app);
    
   
    resultFile<<"*****************start******"<<endl; 
    //resultFile<<inputVar.size();
    int a = myOp[1]->calc(inputVar[0],inputVar[1]); //MultiplicationOp
    int b = foo(a); 
    int d = myOp[2]->calc(b,inputVar[3]); //MultiplicationOp
    int c = myOp[3]->calc(inputVar[4],inputVar[5]); //AdditionOp
    int e = myOp[4]->calc(c,d); //MultiplicationOp
    
    int numberOfOperandsNecessary = 6; 
    if (numberOfOperandsNecessary != inputVar.size()){
        cout << "the number of operands do not match what is necesary in the source file"<<endl;
        cout << "here is the number of operands provided: " << inputVar.size() <<endl;
        cout << "here is the number of Operands necessary: " << numberOfOperandsNecessary <<endl;
        exit(0); 
    }
    //writing the result 
    resultFile<< e <<endl;
    //resultFile<< b <<endl;
    //resultFile<< d <<endl;
    resultFile<<"*****************end******"<<endl; 
    
    
    resultFile.close();
    return 10;
}    
  





