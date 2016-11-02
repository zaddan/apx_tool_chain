//copy paste the following lines: start here
#include <fstream>
#include "assert.h"
#include "Operators.h"
#include "operatorFile_parser.h"
#include "setSubType.h"
#include "operandFile_parser.h"
#include "globals.h"
#include <math.h>
#include "foo.h"
#include <stdio.h>
#include <fstream>
#include <iostream>
#include <vector>
#include <iomanip>
using namespace std;
extern hw_ac **myOp;   
//end here


void test_1(void) {
int in1 = 0;
    show_binary(in1);
    set_bits(in1, 4,1, 15);
    show_binary(in1);
    set_bit(in1, 1,0);
    show_binary(in1);
    set_bit(in1, 0,1);
    show_binary(in1);
    
    cout<<get_bits(in1,2,0)<<endl;
    cout<<get_bits(in1,7,3)<<endl;
    cout<<get_bit(in1,5)<<endl;
    cout<<get_bit(in1,6)<<endl;
    set_bit(in1,6,1);
    cout<<get_bit(in1,6)<<endl;
    show_binary(in1);
    set_bit(in1, 5, 0);
    show_binary(in1);
    set_bit(in1, 6, 0);
    show_binary(in1);
    set_bit(in1, 6, 1);
    show_binary(in1);
    cout<<get_bits(in1,6,5)<<endl;
    show_hex(in1);

    float in3 = 20.1;
    show_binary(in3);
    set_bits(in3, 5,4, 3);
    show_binary(in3);
    set_bit(in3, 1,1);
    show_binary(in3);
    cout<<get_bits(in3,2,0)<<endl;
    cout<<get_bits(in3,7,4)<<endl;
    
    set_bit(in3,7,0);
    show_binary(in3);
    
    cout<<get_bit(in3,5)<<endl;
    cout<<get_bit(in3,7)<<endl;
    cout<<get_bits(in3,10,5)<<endl;
    
    show_hex(in3);
    int sign;
}

//copy past the following lines: start here
int main(int argc, char* argv[]){
    string resultFolderName; 
    string resultFileName; 
    string operatorFileName;
    if (argc < 4) {
        cout<< "provide the name of the file that you want the result to be written to"<<endl;
        cout<< "Example: resultFolderName.txt resultFile.txt operatorFile.txt"<<endl; 
        return 0; 
    }else{
        resultFolderName= argv[1]; 
        resultFileName = argv[2]; 
        operatorFileName = argv[3]; 
    }
    
    std::setprecision(11); 
    assign_global_variables(resultFolderName, operatorFileName);
    string resultFileNameCompleteAddress = resultFileName;
    ofstream resultFile;
    //resultFile.setprecision(11);
    //resultFile.open(resultFileNameCompleteAddress.c_str(), ios_base::app);
#ifdef BT_RND    
    resultFile.open("BT_RND_c.txt", ios_base::out);
#else
    resultFile.open("TRUNCATION_c.txt", ios_base::out);
#endif    


//    float in1 = pow(2, 23) - 1;//2.75;
//    float in2 = 20.1;

    
    float data_element;
    unsigned int data_element_mem_holder; 
    unsigned int in1_mem_holder; 
    unsigned int in2_mem_holder; 
    unsigned int overAllOutput_mem_holder; 
    vector <float> data; 
    ifstream fin;
#ifdef BT_RND
    fin.open("BT_RND.txt",ios::in);    // open file
#else
    fin.open("TRUNCATION.txt",ios::in);    // open file
#endif     
    assert (!fin.fail( ));     
    while (!fin.eof( ))      //if not at end of file, continue reading numbers
    {
        fin>>hex>>data_element_mem_holder ; 
        memcpy(&data_element, &data_element_mem_holder, sizeof(data_element));
        data.push_back(data_element);
    }
    fin.close( );       //close file
    float in1;
    float in2;
    for (int i = 0; i < (data.size())/3; i++) {
        in1 = data[3*i] ;
        in2 = data[3*i + 1];

        float overAllOutput = myOp[0]->calc(in1, in2);  //MultiplicationOp
        //cout<<i <<":"<<overAllOutput<<endl; 
        //exit(0);
        //--- we need to set the precision properly o.w, the values dumped i the file would be rounded up or down :/ 
        //resultFile<<std::setprecision(7 + log10(int(abs(in1))))<<in1 << " " <<std::setprecision(7 + log10(int(abs(in2)+1))) <<in2 << " " << setprecision(7 +  log10(int(abs(overAllOutput)+1)))<<overAllOutput <<endl;
        //resultFile<<std::setprecision(20 )<<in1 << " " <<std::setprecision(20) <<in2 << " " << setprecision(20 )<<overAllOutput <<endl;
        
        
        memcpy(&in1_mem_holder, &in1, sizeof(in1));
        memcpy(&in2_mem_holder, &in2, sizeof(in2));
        memcpy(&overAllOutput_mem_holder, &overAllOutput, sizeof(overAllOutput));
        //resultFile<<in1 << " " <<in2 << " " << overAllOutput <<endl;
        resultFile<<hex<<in1_mem_holder << " " <<in2_mem_holder << " " << overAllOutput_mem_holder <<endl;
    } 

    resultFile.close();
     
    //test_1();
    
    /*
     
    int LO = -10000;
    int HI= 10000;
    int number_of_inputs = 10000000; 
    for (int i = 0 ;i < number_of_inputs; i++) {
        float in1= LO + static_cast <float> (rand()) /( static_cast <float> (RAND_MAX/(HI-LO)));
        float in2= LO + static_cast <float> (rand()) /( static_cast <float> (RAND_MAX/(HI-LO)));
        float result = myOp[0]->calc(in1, in2);
        //cout <<"apx version:" <<result<<" acc:" << in1 + in2<<endl;
        //cout<<in1<<endl;
        //cout<<in2<<endl;
        //cout <<result<<endl;
//        show_hex(in1);
//        show_hex(in2);
        //cout <<in1 + in2<<endl;
        //show_hex(in1+in2);
//        show_hex(result);
//        show_hex(in1 * in2);
        assert(result == (in1 * in2));
    }
    */
    return 0;
    }    

