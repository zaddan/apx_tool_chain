#include <stdio.h>
#include <stdlib.h>
#include "globals.h"
extern hw_ac **myOp;   

void matmul_unfolded(int **A, int **B, int **C, int matHeight, int matWidth) {
  int sum;
  int   i;
  int   j;
  int   k;
  int mulTemp; 
  printf("%%%%%%%%%%%%%%%%%%%%%%%%%\n");  
//------calculating element 0 and 0
sum = 0;
mulTemp = A[0][0]*B[0][0];
sum = sum + mulTemp;
mulTemp = A[0][1]*B[1][0];
sum = sum + mulTemp;
C[0][0] = sum;
//------calculating element 0 and 1
sum = 0;
mulTemp = A[0][0]*B[0][1];
sum = sum + mulTemp;
mulTemp = A[0][1]*B[1][1];
sum = sum + mulTemp;
C[0][1] = sum;
//------calculating element 1 and 0
sum = 0;
mulTemp = A[1][0]*B[0][0];
sum = sum + mulTemp;
mulTemp = A[1][1]*B[1][0];
sum = sum + mulTemp;
C[1][0] = sum;
//------calculating element 1 and 1
sum = 0;
mulTemp = A[1][0]*B[0][1];
sum = sum + mulTemp;
mulTemp = A[1][1]*B[1][1];
sum = sum + mulTemp;
C[1][1] = sum;
}
