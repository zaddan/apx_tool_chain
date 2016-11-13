#include "Operators.h"
#include "operatorFile_parser.h"
#include "setSubType.h"
#include "operandFile_parser.h"
#include <bitset>
#include <assert.h>
#include <typeinfo>
//#define VERBOSE
#define BT_RND
#define APX


void assign_global_variables(string, string);
extern hw_ac **myOp; 

/*
void set_bit(int &num, int bit_index, int bit_value);
void set_bit(long &num, int bit_index, int bit_value);
//void set_bits(long &num, int upper_bit_index, int lower_bit_index, long value);
//-----------------------------------------------------------------
int get_bit(int num, int bit_index);
int get_bits(int num, int upper_bit_index, int lower_bit_index);
long get_bit(long num, int bit_index);
long get_bits(long num, int upper_bit_index, int lower_bit_index);
*/

#ifndef GLOBLAS_H
#define GLOBALS_H
template <class T>
void show_binary(T num) {
    cout<<"num:" <<num<<" bin:"<<bitset<sizeof(T)*8>(*(long unsigned int*)(&num))<<endl;
}


template <class T>
void show_hex(T num) {
    if (typeid(T) == typeid(float)) {
       printf("num:%f  hex:%x\n", num, *(unsigned int*)&num);  
    }else if (typeid(T)  == typeid(double)){
       printf("num:%f hex:%x\n", num, *(unsigned long*)&num);  
    }else{
        cout<<"num:"<<num << " hex:"<<std::hex<<num<<endl;
    }
}


template <class T1, class T2>
void set_bits(T1 &num, int upper_bit_index, int lower_bit_index, T2 value){
    //cout <<"indecies"<< lower_bit_index << " to "<< upper_bit_index << "set to " << bitset<32>(value)<<endl;
    assert(upper_bit_index> lower_bit_index); 
    int mask = ((1<<(upper_bit_index - lower_bit_index + 1)) - 1)<<(lower_bit_index);
    value = ((1<<(upper_bit_index - lower_bit_index + 1)) -1) & value; //make sure that value doesn't go over
                                               // the number of bits it's allowed to
    
//    cout <<"mask is: ";
//    show_hex(mask);
    //show_hex(mask);

    int thirty_two_bit_mem_holder;
    long sixty_four_mem_holder;
    
    if (sizeof(T1) == sizeof(int)){
        memcpy(&thirty_two_bit_mem_holder, &num, sizeof(thirty_two_bit_mem_holder));
        thirty_two_bit_mem_holder = thirty_two_bit_mem_holder & ~(mask); 
        thirty_two_bit_mem_holder = thirty_two_bit_mem_holder | (value<<lower_bit_index);
        memcpy(&num, &thirty_two_bit_mem_holder, sizeof(thirty_two_bit_mem_holder));
    }else{
        memcpy(&sixty_four_mem_holder, &num, sizeof(sixty_four_mem_holder));
        sixty_four_mem_holder = sixty_four_mem_holder & ~(mask); 
        sixty_four_mem_holder = sixty_four_mem_holder | (value<<lower_bit_index);
        memcpy(&num, &sixty_four_mem_holder, sizeof(sixty_four_mem_holder));
    }
}

template <class T>
void set_bit(T &num, int bit_index, int value){
    int mask = 1<<bit_index;
    
    int thirty_two_bit_mem_holder;
    long sixty_four_mem_holder;
    
    if (sizeof(T) == sizeof(int)){
        memcpy(&thirty_two_bit_mem_holder, &num, sizeof(thirty_two_bit_mem_holder));
        thirty_two_bit_mem_holder = thirty_two_bit_mem_holder & ~(mask); 
        thirty_two_bit_mem_holder = thirty_two_bit_mem_holder | (value<<bit_index);
        memcpy(&num, &thirty_two_bit_mem_holder, sizeof(thirty_two_bit_mem_holder));
    }else{
        memcpy(&sixty_four_mem_holder, &num, sizeof(sixty_four_mem_holder));
        sixty_four_mem_holder = sixty_four_mem_holder & ~(mask); 
        sixty_four_mem_holder = sixty_four_mem_holder | (value<<bit_index);
        memcpy(&num, &sixty_four_mem_holder, sizeof(sixty_four_mem_holder));
    }



}
template <class T>
int get_bits(T num, int upper_bit_index, 
        int lower_bit_index){
    assert(upper_bit_index - lower_bit_index <= 31);  //make sure that doubles are not allowed
    //cout <<"indecies"<< lower_bit_index << " to "<< upper_bit_index << "set to " << bitset<32>(value)<<endl;
    assert(upper_bit_index>= lower_bit_index); 
    int mask = (1<<(upper_bit_index+1)) - (1<<(lower_bit_index));
    int thirty_two_bit_mem_holder;
     
    long sixty_four_mem_holder;
    long sixty_four_mem_holder_shifted ;
    if (sizeof(T) == sizeof(int)){
        memcpy(&thirty_two_bit_mem_holder, &num, sizeof(thirty_two_bit_mem_holder));
        return ((thirty_two_bit_mem_holder & mask)>>lower_bit_index);
    }else{
        memcpy(&sixty_four_mem_holder, &num, sizeof(sixty_four_mem_holder));
        sixty_four_mem_holder_shifted =  (sixty_four_mem_holder& mask)>>lower_bit_index;
        memcpy(&thirty_two_bit_mem_holder, &sixty_four_mem_holder_shifted, sizeof(int));
        return thirty_two_bit_mem_holder;
    }
}

template <class T>
int get_bit(T num, int bit_index){
   return get_bits(num, bit_index, bit_index);
}
#endif
//extern vector<int> inputVar;

