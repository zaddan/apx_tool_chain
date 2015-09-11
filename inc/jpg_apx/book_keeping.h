#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <iostream>
#include <fstream>
using namespace std;

//overloading of the same function
void writeOutput(string outputFileName, float *output, int outputLength, string openningStatement, string closingStatment); 
 
void writeOutput(string outputFileName, float output, string openningStatement, string closingStatment);

void writeOutput(string outputFileName, short int *output, int outputLength, 
        string openningStatement, string closingStatment);



void rmOutputFile(string outputFileName);
