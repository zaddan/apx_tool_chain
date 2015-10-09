#include <stdlib.h>
#include <stdio.h>
#include "mat_mul_lib.h"
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
  srand(randomSeed);
  int **T = 0;
  int i;
  int j;
  int m = matrixHeight;
  int n = matrixWidth;
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

int find_diff(int **goldenResult, int **resultToCompare, int numOfRows, int numOfCols){
    int x, y;
    for (y = 0; y < numOfRows; ++y) {
        for (x = 0; x < numOfCols; ++x) {
            if (goldenResult[y][x] != resultToCompare[y][x]){
                return 1;
            }
        }
    }
    return 0;
}
int main(int argc, char *argv[]) {
  int** A;
  int** B;
  int** goldenResult;
  int** resultToCompare;
  int debug = atoi(argv[1]);
  int matrixWidth = atoi(argv[2]);
  int matrixHeight= atoi(argv[3]);
  int matrixUpperBound = atoi(argv[4]);
  int randomSeed= atoi(argv[5]);
  create_matrix(&A, matrixWidth, matrixHeight, matrixUpperBound, 2*randomSeed);
  create_matrix(&B, matrixHeight, matrixHeight, matrixUpperBound, randomSeed);
  create_matrix(&goldenResult, matrixWidth, matrixHeight, matrixUpperBound, randomSeed);
  create_matrix(&resultToCompare, matrixWidth, matrixHeight, matrixUpperBound, randomSeed);
  // ---- printing the matrix if debug flag
    
// assume some initialization of A and B
  // think of this as a library where A and B are
  // inputs in row-major format, and C is an output
  // in row-major.

  matmul(A, B, goldenResult,matrixHeight, matrixWidth );
  matmul_unfolded(A, B, resultToCompare,matrixHeight, matrixWidth );
  
  int diff; //weather ther is a dif between golden and current
  diff = find_diff(goldenResult, resultToCompare, matrixHeight, matrixWidth);
  if (debug) {  
      print_matrix(A,matrixHeight, matrixWidth);
      print_matrix(B,matrixHeight, matrixWidth);
      printf("**golden results\n"); 
      print_matrix(goldenResult,matrixHeight, matrixWidth);
      printf("**result to Compare\n"); 
      print_matrix(resultToCompare,matrixHeight, matrixWidth);
  }
  
   
  return diff;
}
