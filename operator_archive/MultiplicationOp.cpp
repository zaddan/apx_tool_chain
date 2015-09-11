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
using namespace std;

vector<vector<string> > OpTypeVec;
enum status {SUCCESS, FAILURE}; 
hw_ac **myOp;   

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

    
    string OpListFile = resultFolderName;
    OpListFile += "/";
    OpListFile += operatorFileName;
    
    //    
//    //getting the operators 
    int status = operatorFileParser(OpListFile, OpTypeVec);
    //defiing an array of MyOps 
    myOp = new hw_ac*[OpTypeVec.size()];
    //instantiating the array elements to the values of OpTypeVec 
    //note: OpTypeVec is populated with the parsed values in the OpListFile 
    for (int i = 0; i<OpTypeVec.size(); i++) {
        int status = setOpSubTypeAndInputs(&myOp[i], OpTypeVec[i]);
        if (status == FAILURE) {
            printf("this type is not acceptable \n"); 
            return 1;// 0;
        }
    }
    
    
    //getting the operand values  
    string operandListFileName;
    
    operandListFileName = operandFileName;
    //operandListFileName += "operandFile_parser_example.txt";
    vector<int> inputVar;
    status = operandFileParser(operandListFileName, inputVar);
    
    string resultFileNameCompleteAddress = resultFileName;
    cout<< resultFileName;

    ofstream resultFile;
    resultFile.open(resultFileNameCompleteAddress.c_str(), ios_base::app);
    
    
   
    resultFile<<"*****************start******"<<endl; 
    //resultFile<<inputVar.size();
    int a = myOp[0]->calc(inputVar[0],inputVar[1]); //MultiplicationOp
    int numberOfOperandsNecessary = 2; 
    if (numberOfOperandsNecessary != inputVar.size()){
        cout << "the number of operands do not match what is necesary in the source file"<<endl;
        cout << "here is the number of operands provided: " << inputVar.size() <<endl;
        cout << "here is the number of Operands necessary: " << numberOfOperandsNecessary <<endl;
        exit(0); 
    }
    //writing the result 
    resultFile<< a <<endl;
    //resultFile<< b <<endl;
    //resultFile<< d <<endl;
    resultFile<<"*****************end******"<<endl; 
    
    
    resultFile.close();
    return 10;
}    
  





