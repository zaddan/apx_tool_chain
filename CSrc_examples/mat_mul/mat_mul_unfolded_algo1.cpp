#include <stdio.h>
#include <stdlib.h>
#include "globals.h"
extern hw_ac **myOp;   

void matmul_unfolded_1 (int **A, int **B, int **C, int matHeight, int matWidth) { //name  int sum;
  int   i;
  int   j;
  int   k;
  int mulTemp; 
  printf("%%%%%%%%%%%%%%%%%%%%%%%%%\n");  
//------calculating element 0 and 0
sum = 0;
mulTemp = myOp[0]->calc(A[0][0],B[0][0]); //MultiplicationOp
sum = myOp[1]->calc(sum, mulTemp); //AdditionOp
mulTemp = myOp[2]->calc(A[0][1],B[1][0]); //MultiplicationOp
sum = myOp[3]->calc(sum, mulTemp); //AdditionOp
mulTemp = myOp[4]->calc(A[0][2],B[2][0]); //MultiplicationOp
sum = myOp[5]->calc(sum, mulTemp); //AdditionOp
C[0][0] = sum;
//------calculating element 0 and 1
sum = 0;
mulTemp = myOp[6]->calc(A[0][0],B[0][1]); //MultiplicationOp
sum = myOp[7]->calc(sum, mulTemp); //AdditionOp
mulTemp = myOp[8]->calc(A[0][1],B[1][1]); //MultiplicationOp
sum = myOp[9]->calc(sum, mulTemp); //AdditionOp
mulTemp = myOp[10]->calc(A[0][2],B[2][1]); //MultiplicationOp
sum = myOp[11]->calc(sum, mulTemp); //AdditionOp
C[0][1] = sum;
//------calculating element 0 and 2
sum = 0;
mulTemp = myOp[12]->calc(A[0][0],B[0][2]); //MultiplicationOp
sum = myOp[13]->calc(sum, mulTemp); //AdditionOp
mulTemp = myOp[14]->calc(A[0][1],B[1][2]); //MultiplicationOp
sum = myOp[15]->calc(sum, mulTemp); //AdditionOp
mulTemp = myOp[16]->calc(A[0][2],B[2][2]); //MultiplicationOp
sum = myOp[17]->calc(sum, mulTemp); //AdditionOp
C[0][2] = sum;
//------calculating element 1 and 0
sum = 0;
mulTemp = myOp[18]->calc(A[1][0],B[0][0]); //MultiplicationOp
sum = myOp[19]->calc(sum, mulTemp); //AdditionOp
mulTemp = myOp[20]->calc(A[1][1],B[1][0]); //MultiplicationOp
sum = myOp[21]->calc(sum, mulTemp); //AdditionOp
mulTemp = myOp[22]->calc(A[1][2],B[2][0]); //MultiplicationOp
sum = myOp[23]->calc(sum, mulTemp); //AdditionOp
C[1][0] = sum;
//------calculating element 1 and 1
sum = 0;
mulTemp = myOp[24]->calc(A[1][0],B[0][1]); //MultiplicationOp
sum = myOp[25]->calc(sum, mulTemp); //AdditionOp
mulTemp = myOp[26]->calc(A[1][1],B[1][1]); //MultiplicationOp
sum = myOp[27]->calc(sum, mulTemp); //AdditionOp
mulTemp = myOp[28]->calc(A[1][2],B[2][1]); //MultiplicationOp
sum = myOp[29]->calc(sum, mulTemp); //AdditionOp
C[1][1] = sum;
//------calculating element 1 and 2
sum = 0;
mulTemp = myOp[30]->calc(A[1][0],B[0][2]); //MultiplicationOp
sum = myOp[31]->calc(sum, mulTemp); //AdditionOp
mulTemp = myOp[32]->calc(A[1][1],B[1][2]); //MultiplicationOp
sum = myOp[33]->calc(sum, mulTemp); //AdditionOp
mulTemp = myOp[34]->calc(A[1][2],B[2][2]); //MultiplicationOp
sum = myOp[35]->calc(sum, mulTemp); //AdditionOp
C[1][2] = sum;
//------calculating element 2 and 0
sum = 0;
mulTemp = myOp[36]->calc(A[2][0],B[0][0]); //MultiplicationOp
sum = myOp[37]->calc(sum, mulTemp); //AdditionOp
mulTemp = myOp[38]->calc(A[2][1],B[1][0]); //MultiplicationOp
sum = myOp[39]->calc(sum, mulTemp); //AdditionOp
mulTemp = myOp[40]->calc(A[2][2],B[2][0]); //MultiplicationOp
sum = myOp[41]->calc(sum, mulTemp); //AdditionOp
C[2][0] = sum;
//------calculating element 2 and 1
sum = 0;
mulTemp = myOp[42]->calc(A[2][0],B[0][1]); //MultiplicationOp
sum = myOp[43]->calc(sum, mulTemp); //AdditionOp
mulTemp = myOp[44]->calc(A[2][1],B[1][1]); //MultiplicationOp
sum = myOp[45]->calc(sum, mulTemp); //AdditionOp
mulTemp = myOp[46]->calc(A[2][2],B[2][1]); //MultiplicationOp
sum = myOp[47]->calc(sum, mulTemp); //AdditionOp
C[2][1] = sum;
//------calculating element 2 and 2
sum = 0;
mulTemp = myOp[48]->calc(A[2][0],B[0][2]); //MultiplicationOp
sum = myOp[49]->calc(sum, mulTemp); //AdditionOp
mulTemp = myOp[50]->calc(A[2][1],B[1][2]); //MultiplicationOp
sum = myOp[51]->calc(sum, mulTemp); //AdditionOp
mulTemp = myOp[52]->calc(A[2][2],B[2][2]); //MultiplicationOp
sum = myOp[53]->calc(sum, mulTemp); //AdditionOp
C[2][2] = sum;
}
