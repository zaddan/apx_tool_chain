#include <stdio.h>
#include <stdlib.h>
#include "globals.h"
extern hw_ac **myOp;   

int matmul_unfolded_1 (int A, int B) {
  int sum;
  int   i;
  int   j;
  int   k;
  int mulTemp; 
//------calculating element 0 and 0
sum = 0;
mulTemp = myOp[1]->calc(A, B); //AdditionOpIgnore
return mulTemp;
}
