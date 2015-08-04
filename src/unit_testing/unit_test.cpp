#include "operandFile_parser.h"
#include <vector>
#include <cstring>
#include <iostream>
using std::vector;
using std::string;
using namespace std;
enum status {SUCCESS, FAILURE}; 
vector<int> operandVar;
/** 
 * @brief this module is responsible for unit testing the inputParser
 * 
 * @return 
 */
int operandFileParserTest1(){
    string operandFile = "./../input_output_text_files/operandFile_parser_example.txt" ;
   
    int status = operandFileParser(operandFile, operandVar);
//    //defiing an array of MyOps 
    for (int i=0; i<operandVar.size(); i++) {
        cout<< "this is the " << i << "th value of the input " << operandVar[i] << endl;
    }
    
    cout<<"done"<<endl;     
    return 1;
}    
 



/** 
 * @brief contains all the unit tests
 * 
 * @return 
 */

int notmain() {//comment out when you want this to run as main
//int main() {
    operandFileParserTest1();
}
