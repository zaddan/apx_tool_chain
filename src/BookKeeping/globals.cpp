#include <fstream>
#include "globals.h"
#include "Operators.h"
#include "operatorFile_parser.h"
#include "setSubType.h"
#include "operandFile_parser.h"
#include <math.h>
#include <iostream>
#include <bitset>
using namespace std;

hw_ac **myOp;   
long double energy_value;

vector<int> mul_long_long_energy_counters {0, 0, 0, 0, 0, 0,  0,0,0, 0 ,0 ,0 ,0 ,0 , 0, 0,0,0,0,0,0,0};
vector<int> mul_long_int_energy_counters  {0, 0, 0, 0, 0, 0,  0,0,0, 0 ,0 ,0 ,0 ,0 , 0, 0,0,0,0,0,0,0};
vector<int> mul_int_int_energy_counters {0, 0, 0, 0, 0, 0,  0,0,0, 0 ,0 ,0 ,0 ,0 , 0, 0,0,0,0,0,0,0};
vector<int> mul_float_float_energy_counters {0, 0, 0, 0, 0, 0,  0,0,0, 0 ,0 ,0 ,0 ,0 , 0, 0,0,0,0,0,0};

vector<int> add_long_long_energy_counters {0, 0, 0, 0, 0, 0,  0,0,0, 0 ,0 ,0 ,0 ,0 , 0, 0,0,0,0,0,0,0};
vector<int> add_long_int_energy_counters  {0, 0, 0, 0, 0, 0,  0,0,0, 0 ,0 ,0 ,0 ,0 , 0, 0,0,0,0,0,0};
vector<int> add_int_int_energy_counters {0, 0, 0, 0, 0, 0,  0,0,0, 0 ,0 ,0 ,0 ,0 , 0, 0,0,0,0,0,0};
vector<int> add_float_float_energy_counters {0, 0, 0, 0, 0, 0,  0,0,0, 0 ,0 ,0 ,0 ,0 , 0, 0,0,0,0,0,0};
/*
void set_bit(int &num, int bit_index, int bit_value){
    //cout <<"index"<< bit_index << " converted to "<< bitset<32>(bit_value) <<endl;
    int mask = 1 << bit_index;
    num = num & ~(mask); 
    num = num | (bit_value<<bit_index); 
}

int get_bit(int num, int bit_index){
    //cout <<"index"<< bit_index << " converted to "<< bitset<32>(bit_value) <<endl;
    int mask = 1 << bit_index;
    return num & (mask); 
}

int get_bits(int num, int upper_bit_index, int lower_bit_index){
    //cout <<"indecies"<< lower_bit_index << " to "<< upper_bit_index << "set to " << bitset<32>(value)<<endl;
    int result; 
    int mask = pow(2, upper_bit_index+1) - 1 - pow(2, lower_bit_index+1) - 1;
    return num & mask ;
}


long get_bit(long num, int bit_index){
    //cout <<"index"<< bit_index << " converted to "<< bitset<32>(bit_value) <<endl;
    long mask = 1 << bit_index;
    return num & (mask); 
}

//-----------------------------------------------------------------
long get_bits(long num, int upper_bit_index, int lower_bit_index){
    //cout <<"indecies"<< lower_bit_index << " to "<< upper_bit_index << "set to " << bitset<32>(value)<<endl;
    long mask = pow(2, upper_bit_index+1) - 1 - pow(2, lower_bit_index+1) - 1;
    return num & mask ;
}

*/
//vector<int> inputVar;
//void assign_global_variables(string resultFolderName, string operatorFileName, string operandFileName){


void assign_global_variables(string resultFolderName, string operatorFileName){
    energy_value = 0.0; 
    vector<vector<string> > OpTypeVec;
    enum status {SUCCESS, FAILURE}; 
    string OpListFile = resultFolderName;
    OpListFile += "/";
    OpListFile += operatorFileName;


    int status = operatorFileParser(OpListFile, OpTypeVec);
    printf("the OpTypeVec size%d\n", OpTypeVec.size()); 
    cout<<std::flush; 
    myOp = new hw_ac*[OpTypeVec.size()];
    for (int i = 0; i<OpTypeVec.size(); i++) {
        int status = setOpSubTypeAndInputs(&myOp[i], OpTypeVec[i]);
        if (status == FAILURE) {
            printf("this type is not acceptable \n"); 
            exit(1);// 0;
        }
    }

    //status = operandFileParser(operandFileName, inputVar);
    /*if (status == FAILURE){*/
        //cout <<"could not find the operandfile" << endl;
    /*}*/
}
