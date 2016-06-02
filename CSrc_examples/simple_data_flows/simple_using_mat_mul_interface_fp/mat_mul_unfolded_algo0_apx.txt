#include <stdio.h>
#include <stdlib.h>
#include "globals.h"
extern hw_ac **myOp;   

int matmul_unfolded_0 (int A[4]) {
 //------calculating element 0 and 0
 int c= myOp[0]->calc(A[0], A[1]); //AdditionOp
 int d= myOp[1]->calc(A[2], A[3]); //AdditionOp
 int e= myOp[2]->calc(c, d); //AdditionOp
 return e;
}
