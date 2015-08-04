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
    resultFile<<myOp[0]->calc(inputVar[0],inputVar[1])<<endl; //AdditionOp
    resultFile<<myOp[1]->calc(inputVar[2],inputVar[3])<<endl; //MultiplicationOp
    resultFile<<myOp[2]->calc(inputVar[4],inputVar[5])<<endl; //MultiplicationOp
    resultFile<<myOp[3]->calc(inputVar[0],inputVar[5])<<endl; //AdditionOp
    resultFile<<"*****************end******"<<endl; 
    resultFile.close();
    return 10;
}    
  





