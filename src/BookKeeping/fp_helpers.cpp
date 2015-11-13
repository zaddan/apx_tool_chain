#include<iostream>
#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include "fp_helpers.h"
using namespace std;

unsigned getNumberOfDigits (long unsigned i)
{
    return i > 0 ? (int) log2 ((double) i) + 1 : 1;
}

void getFPComponents(float number, fpType &num){
 unsigned int* ptr = (unsigned int*)&number;
 num.Sign = *ptr>> 31;
 num.Exp = *ptr& 0x7f800000;
 num.Exp >>= MANTISA_WIDTH;
 num.Mantisa = *ptr& 0x007fffff;
}

float convertFPCompToFP(fpType num){
    float result = 0;
    int expSoFar = num.Exp - bias; //what exp to use at the moment
    int decodedMantisaWithExtraOne = (1 <<MANTISA_WIDTH) + num.Mantisa;//decode mantisa with Extra one
    int mask = 1 << MANTISA_WIDTH;
    int shftRightAmt = MANTISA_WIDTH;
    while(1)  {
        result += ((decodedMantisaWithExtraOne & mask) >>  shftRightAmt)* pow(2, expSoFar );
        mask = mask >> 1; 
        shftRightAmt -= 1;
        expSoFar -=1;
        if (mask == 0) {
            break;
        }
    }

    if (num.Sign) {
        result = -1*result;
    }
    return result;
}

void normalizeMul(fpType &resultNum){ 
    int numOfDig = getNumberOfDigits (resultNum.Mantisa);
    if (numOfDig > MANTISA_WIDTH + 1) {
        resultNum.Mantisa = resultNum.Mantisa >> (numOfDig - (MANTISA_WIDTH + 1));
        resultNum.Exp= resultNum.Exp + (numOfDig - (2*MANTISA_WIDTH + 1));
    }else{
        ; //do nothing
    }
}

void normalizeAdd(fpType &resultNum){ 
    int numOfDig = getNumberOfDigits (resultNum.Mantisa);
    if (numOfDig > MANTISA_WIDTH + 1) {
        resultNum.Mantisa = resultNum.Mantisa >> (numOfDig - (MANTISA_WIDTH + 1));
        resultNum.Exp= resultNum.Exp + (numOfDig - (MANTISA_WIDTH + 1));
    }else{
        ; //do nothing
    }
}

