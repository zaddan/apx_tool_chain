#include <stdio.h>
#include <stdlib.h>
#include "globals.h"
extern hw_ac **myOp;   

int matmul_unfolded_1 (int A[4]) {
 //------calculating element 0 and 0
 int c= myOp[3]->calc(A[0], -1*A[1]); //AdditionOpIgnore
 int d= myOp[4]->calc(A[2], -1*A[3]); //AdditionOpIgnore
 int e= myOp[5]->calc(c, d); //AdditionOpIgnore
 return e;
}
