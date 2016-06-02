#include <stdio.h>
#include <stdlib.h>
#include "globals.h"
extern hw_ac **myOp;   

int matmul_unfolded_1 (int A[4]) {
 //------calculating element 0 and 0
 int c= myOp[3]->calc(A[0], A[1]); //AdditionOp
 int d= myOp[4]->calc(A[2], A[3]); //AdditionOp
 int e= myOp[5]->calc(c, d); //AdditionOp
 return e;
}

float matmul_unfolded_1 (float A[4]) {
 //------calculating element 0 and 0
 float c= myOp[3]->calc(A[0], A[1]); //AdditionOp
 float d= myOp[4]->calc(A[2], A[3]); //AdditionOp
 float e= myOp[5]->calc(c, d); //AdditionOp
 return e;
}
