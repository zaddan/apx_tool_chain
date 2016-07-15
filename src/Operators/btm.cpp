#include <iostream>
#include <complex>
#include <vector>
#include "btm.h"
#include "fp_helpers.h"
#include "globals.h"
using namespace std;

btm::btm(void) {}

btm::btm(size_t Nt, size_t Nia, bool table_gen) {
    this->Nt = Nt;
    this->msb = Nia-1;
    this->lsb = 0;
    this->vbl = Nia;
    this->hbl = Nia;

    if (table_gen) tbl_gen();
}

btm::~btm(void) {}

size_t btm::get_hbl_bits(void) {
    return hbl;
}


size_t btm::get_vbl_bits(void) {
    return vbl;
}

float btm::calc(const float &number1, const int &number2) {
    float numOut = number2; 
    calc(number1, numOut);
} 

float btm::calc(const int &number1, const float &number2) {
    cout<<"=============insde other half float"<<endl; 
    float numOut = number1; 
    calc(numOut, number2);
} 


float btm::calc(const float &number1, const float &number2) {
    fpType num1;
    fpType num2;
    getFPComponents(number1, num1); //get the fp componenets
    getFPComponents(number2, num2); //get the fp components

    num1.Mantisa = ((num1.Mantisa)>> vbl) <<vbl;
    num2.Mantisa = ((num2.Mantisa)>> vbl) <<vbl;
    
    float num1_inverse_converted = convertFPCompToFP(num1);
    float num2_inverse_converted = convertFPCompToFP(num2);
    
    return num1_inverse_converted * num2_inverse_converted;
}


int btm::calc(const int &a, const int &b) {
    #ifdef VERBOSE 
    cout<<"=============in int version"<<endl; 
    #endif 
    // inaccurate part
    int weight = pow(2, vbl) - 1;
    int abs_a = (a<0) ? -a : a;
    int abs_b = (b<0) ? -b : b;
    int sign = (a<0 && b>0) || (a>0 && b<0) ? 1 : 0;
    //  int iap_a = weight&a;
//  int iap_b = weight&b;
//  int a_rnd = (((a >> vbl)&((int)(pow(2, Nt-vbl-1) - 1))) == ((int)pow(2, Nt-vbl-1) - 1)) ?
//              (a >> vbl) : (a >> vbl) + 1;
//  int b_rnd = (((b >> vbl)&((int)pow(2, Nt-vbl-1) - 1)) == ((int)pow(2, Nt-vbl-1) - 1)) ?
//              (b >> vbl) : (b >> vbl) + 1;
    //printf("SGLEE VBL: %d, %x, %x, %x\n", vbl, (b >> vbl), b_rnd, (int)(pow(2, Nt-vbl-1) - 1));
    //if (((b >> vbl)&((int)pow(2, Nt-vbl-1) - 1)) == ((int)pow(2, Nt-vbl-1) - 1)) cout << "SGLEE OVERFLOW" << endl;
    //if ((a >> vbl) == (pow(2, Nt) - 1)) cout << "SGLEE OVERFLOW" << endl;
//  int a_op = (iap_a >> (vbl - 1)) == 0x1 ? a_rnd : (a >> vbl);
//  int b_op = (iap_b >> (vbl - 1)) == 0x1 ? b_rnd : (b >> vbl);

#ifdef BT_RND
    int a_op = (abs_a >> (vbl - 1)) == 0x1 ? (abs_a >> vbl) + 1 : (abs_a >> vbl);
#else
    int a_op = (abs_a >> vbl);
#endif

#ifdef BT_RND
    int b_op = (abs_b >> (vbl - 1)) == 0x1 ? (abs_b >> vbl) + 1 : (abs_b >> vbl);
#else
    int b_op = (abs_b >> vbl);
#endif

    //printf("SGLEE VBL: %d, %d, %d\n", a_op, b_op, ((a_op)*(b_op)) << (2*vbl));
    int tmp = ((a_op)*(b_op)) << (2*vbl);
    // accurate part
    return (sign ? -tmp : tmp);
}


unsigned int btm::calc(const unsigned int &a, const unsigned int &b) {
    #ifdef VERBOSE 
    cout<<"=============in unsigned int version"<<endl; 
    #endif 
    // inaccurate part
    unsigned int weight = pow(2, vbl) - 1;
    unsigned int abs_a =  a;
    unsigned int abs_b =  b;

#ifdef BT_RND
    unsigned int a_op = (abs_a >> (vbl - 1)) == 0x1 ? (abs_a >> vbl) + 1 : (abs_a >> vbl);
#else
    unsigned int a_op = (abs_a >> vbl);
#endif

#ifdef BT_RND
    unsigned int b_op = (abs_b >> (vbl - 1)) == 0x1 ? (abs_b >> vbl) + 1 : (abs_b >> vbl);
#else
    unsigned int b_op = (abs_b >> vbl);
#endif

    //prunsigned intf("SGLEE VBL: %d, %d, %d\n", a_op, b_op, ((a_op)*(b_op)) << (2*vbl));
    unsigned int tmp = ((a_op)*(b_op)) << (2*vbl);
    // accurate part
    return tmp;
}

int btm::calc(const unsigned int &a_unsigned, const int &b) {
    #ifdef VERBOSE 
    cout<<"=============in half usigned int version"<<endl; 
    #endif 
    int a = (int) a_unsigned ;
    // inaccurate part
    int weight = pow(2, vbl) - 1;
    int abs_a =  a;
    int abs_b =  b;

#ifdef BT_RND
    int a_op = (abs_a >> (vbl - 1)) == 0x1 ? (abs_a >> vbl) + 1 : (abs_a >> vbl);
#else
    int a_op = (abs_a >> vbl);
#endif

#ifdef BT_RND
    int b_op = (abs_b >> (vbl - 1)) == 0x1 ? (abs_b >> vbl) + 1 : (abs_b >> vbl);
#else
    int b_op = (abs_b >> vbl);
#endif

    //printf("SGLEE VBL: %d, %d, %d\n", a_op, b_op, ((a_op)*(b_op)) << (2*vbl));
    int tmp = ((a_op)*(b_op)) << (2*vbl);
    // accurate part
    return tmp;
}

int btm::calc(const int &a, const unsigned int &b_unsigned) {
    #ifdef VERBOSE 
    cout<<"=============in half usigned int version"<<endl; 
    #endif 
    int b = (int) b_unsigned;
    // inaccurate part
    int weight = pow(2, vbl) - 1;
    int abs_a =  a;
    int abs_b =  b;

#ifdef BT_RND
    int a_op = (abs_a >> (vbl - 1)) == 0x1 ? (abs_a >> vbl) + 1 : (abs_a >> vbl);
#else
    int a_op = (abs_a >> vbl);
#endif

#ifdef BT_RND
    int b_op = (abs_b >> (vbl - 1)) == 0x1 ? (abs_b >> vbl) + 1 : (abs_b >> vbl);
#else
    int b_op = (abs_b >> vbl);
#endif

    //printf("SGLEE VBL: %d, %d, %d\n", a_op, b_op, ((a_op)*(b_op)) << (2*vbl));
    int tmp = ((a_op)*(b_op)) << (2*vbl);
    // accurate part
    return tmp;
}




int btm::calc_ref(const int &a, const int &b) {
    return a*b;
}

void btm::tbl_gen() {
    int i, j;
    int i_w, j_w;
    for (i = 0; i < pow(2, msb - lsb + 1); i++) {
        for (int j = 0; j < pow(2, msb - lsb + 1); j++) {
            if (!(i == 0 && j == 0)) {
                err_tbl.push_back(make_pair(make_pair((0x80000000 | i), (0x80000000 | j)), make_pair(make_pair(j, i), i*j)));
            }
        }
    }
}
