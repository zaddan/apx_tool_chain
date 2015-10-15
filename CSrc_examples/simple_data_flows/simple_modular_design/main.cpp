
#include <fstream>
#include <stdlib.h>
#include <stdio.h>
#include <iostream>
#include "globals.h"
#include "mat_mul_lib.h"
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
//  int** A;
//  int** B;
//  int** C;
//  int** D;
//  int** result1;
//  int** result2;
//  int** finalResult;
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
  printf("what\n"); 
  assign_global_variables(resultFolderName, operatorFileName);
/*  
  int debug = atoi(argv[4]);
  int matrixWidth = atoi(argv[5]);
  int matrixHeight = matrixWidth;
  //int matrixHeight= atoi(argv[6]);
  int matrixUpperBound = atoi(argv[6]);
  int randomSeed= atoi(argv[7]);
 */ 
  /* 
  create_matrix(&A, matrixWidth, matrixHeight, matrixUpperBound, randomSeed*2);
  create_matrix(&B, matrixHeight, matrixHeight, matrixUpperBound, randomSeed);
  create_matrix(&result1, matrixWidth, matrixHeight, matrixUpperBound, randomSeed);
  create_matrix(&C, matrixWidth, matrixHeight, matrixUpperBound, randomSeed*4);
  create_matrix(&D, matrixWidth, matrixHeight, matrixUpperBound, randomSeed*5);
  create_matrix(&result2, matrixWidth, matrixHeight, matrixUpperBound, randomSeed);
  create_matrix(&finalResult, matrixWidth, matrixHeight, matrixUpperBound, randomSeed);
  */ 
  // ---- printing the matrix if debug flag
    
// assume some initialization of A and B
  // think of this as a library where A and B are
  // inputs in row-major format, and C is an output
  // in row-major.
  int A = 1241;
  int B = 28721;
  int C = 72411; 
//  
//  int A = 12;
//  int B = 28;
//  int C = 72; 

  int result1;
  int result2; 
  result1 = matmul_unfolded_0(A, B);
  result2 = matmul_unfolded_1(C, result1);
  printf("ok\n");
  printf("%s\n",resultFileNameCompleteAddress.c_str());
  //matmul_unfolded_2(result1, result2, finalResult,matrixHeight, matrixWidth );
  
  /*if(debug) { */
      //printf("start^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n");
      //print_matrix(A,matrixHeight, matrixWidth);
      //print_matrix(B,matrixHeight, matrixWidth);
      //printf("-------------------------here is result1\n");
      //print_matrix(result1,matrixHeight, matrixWidth);
      //print_matrix(C,matrixHeight, matrixWidth);
      ////print_matrix(D,matrixHeight, matrixWidth);
      //printf("-------------------------here is result2\n");
      //print_matrix(result2,matrixHeight, matrixWidth);
    //[> 
      //printf("--------------------------------------------\n");
      ////printf("-------------------------here is finalResult\n");
      ////print_matrix(finalResult,matrixHeight, matrixWidth);
     //printf("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^end\n") ;
    //*/ 
     //} 
  
   resultFile<<"*****************start******"<<endl; 
   /*int x, y;*/
   //for (y = 0; y < matrixWidth; ++y) {
       //for (x = 0; x < matrixWidth; ++x) {
           //resultFile<<result2[y][x];
           //resultFile<<" ";
           ////printf("%f ", result[y * numOfCols+ x]);
       //}
   /*}*/
   resultFile<<result2; 
   resultFile<<endl;
   resultFile<<"*****************end******"<<endl; 
   resultFile.close();
   
   return 0;
}
