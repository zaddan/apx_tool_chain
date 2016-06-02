#include <stdio.h>
#include <stdlib.h>
#include "globals.h"
extern hw_ac **myOp;   

int matmul_unfolded_0 (int a[4]) {
 //------calculating element 0 and 0
 int c= myOp[0]->calc((int)a[0], a[1]); //AdditionOp
 int d= myOp[1]->calc(a[2], a[3]); //AdditionOp
 int e= myOp[2]->calc(c, d); //AdditionOp
 return e;
}

float matmul_unfolded_0 (float a[4]) {
 //------calculating element 0 and 0
 float c= myOp[0]->calc(a[0], a[1]); //AdditionOp
 //float d= myOp[1]->calc(a[2], a[3]); //AdditionOp
 float d= myOp[1]->calc(a[2], a[3]); //AdditionOp
 float e= myOp[2]->calc(c, d); //AdditionOp
 return e;
}


