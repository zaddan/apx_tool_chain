void matmul(int **A, int **B, int **C, int matHeight, int matWidth) {
    int sum;
    int   i;
    int   j;
    int   k;
    int mulTemp; 
    for (i=0; i<matHeight; i++) {
        // for each row of C
        for (j=0; j<matWidth; j++) {
            // for each column of C
            sum = 0.0f; // temporary value
            for (k=0; k<matHeight; k++) {
                sum += A[i][k]*B[k][j]; 
                C[i][j] = sum;
            }
        }
    }
}
