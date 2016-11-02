//copy paste the following lines: start here
#include <fstream>
#include "assert.h"
#include <math.h>
#include <bitset>
#include <iostream>
using namespace std;
/*
int set_bit(int &num, int bit_index, int bit_value){
    //cout <<"index"<< bit_index << " converted to "<< bitset<32>(bit_value) <<endl;
    int mask = 1 << bit_index;
    num = num & ~(mask); 
    num = num | (bit_value<<bit_index); 
}

int set_bits(int &num, int upper_bit_index, int lower_bit_index, int value){
    //cout <<"indecies"<< lower_bit_index << " to "<< upper_bit_index << "set to " << bitset<32>(value)<<endl;
    int mask = pow(2, upper_bit_index+1) - 1 - pow(2, lower_bit_index+1) - 1;
    num = num & ~(mask); 
    num = num | (value<<lower_bit_index);
}
//copy past the following lines: start here
int test_set_bit(int argc, char* argv[]){
    int a =  1234;
    cout<<"a intact:   "<<bitset<32>(a)<<endl;
    set_bits(a, 6, 1, 12);
    cout<<"a changed:  "<<bitset<32>(a)<<endl;

}    
*/
