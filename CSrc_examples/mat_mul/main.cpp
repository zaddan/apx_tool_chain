
#include <fstream>
#include <stdlib.h>
#include <stdio.h>
#include "mat_mul_lib.h"
#include <iostream>
#include "globals.h"

extern hw_ac **myOp;   
using namespace std;


//**--------------------**
//**--------------------**
//----disclaimers::: only works for square matrices
//**--------------------**
//--------------------**
// function to allocate a matrix on the heap
// creates an mXn matrix and returns the pointer.
//
// the matrices are in row-major order.

void create_matrix(int*** A, int matrixWidth, int matrixHeight, int upperBound, int randomSeed) {
  int **T = 0;
  int i;
  int j;
  int m = matrixHeight;
  int n = matrixWidth;
  srand(randomSeed);
  T = (int**)malloc( m*sizeof(int*));
  for (i=0; i<m; i++ ) {
     T[i] = (int*)malloc(n*sizeof(int));
  }
  for (i=0; i<m; i++) {
      // for each row of C
      for (j=0; j<n; j++) {
          T[i][j]= rand() % upperBound;
      }
  }
  *A = T;
}

void print_matrix(int **result, int numOfRows, int numOfCols) {
  int x, y;
  for (y = 0; y < numOfRows; ++y) {
    for (x = 0; x < numOfCols; ++x) {
        printf("%d ", result[y][x]);
        //printf("%f ", result[y * numOfCols+ x]);
    }
    printf("\n");
  }
  printf("\n");
}


int main(int argc, char *argv[]) {
  int** A;
  int** B;
  int** C;
  
  string resultFolderName; 
  string resultFileName; 
  string operatorFileName;
  //string operandFileName;
  
  if (argc < 4) {
      cout<< "provide the name of the file that you want the result to be written to"<<endl;
      cout<< "Example: resultFolderName.txt resultFile.txt operatorFile.txt"<<endl; 
      return 0; 
  }else{
      resultFolderName= argv[1]; 
      resultFileName = argv[2]; 
      operatorFileName = argv[3]; 
  }

  string resultFileNameCompleteAddress = resultFileName;
  ofstream resultFile;
  resultFile.open(resultFileNameCompleteAddress.c_str(), ios_base::app);
  assign_global_variables(resultFolderName, operatorFileName);
  
  int debug = atoi(argv[4]);
  int matrixWidth = atoi(argv[5]);
  int matrixHeight= atoi(argv[6]);
  int matrixUpperBound = atoi(argv[7]);
  int randomSeed= atoi(argv[8]);
  create_matrix(&A, matrixWidth, matrixHeight, matrixUpperBound, randomSeed*2);
  create_matrix(&B, matrixHeight, matrixHeight, matrixUpperBound, randomSeed);
  create_matrix(&C, matrixWidth, matrixHeight, matrixUpperBound, randomSeed);
  // ---- printing the matrix if debug flag
    
// assume some initialization of A and B
  // think of this as a library where A and B are
  // inputs in row-major format, and C is an output
  // in row-major.

  matmul_unfolded(A, B, C,matrixHeight, matrixWidth );
 
  if(debug) { 
      print_matrix(A,matrixHeight, matrixWidth);
      print_matrix(B,matrixHeight, matrixWidth);
      print_matrix(C,matrixHeight, matrixWidth);
  } 
  
   resultFile<<"*****************start******"<<endl; 
   int x, y;
   for (y = 0; y < matrixWidth; ++y) {
       for (x = 0; x < matrixWidth; ++x) {
           resultFile<<C[y][x];
           resultFile<<" ";
           //printf("%f ", result[y * numOfCols+ x]);
       }
   }
   resultFile<<endl;
   resultFile<<"*****************end******"<<endl; 
   resultFile.close();
   
   return 0;
}
