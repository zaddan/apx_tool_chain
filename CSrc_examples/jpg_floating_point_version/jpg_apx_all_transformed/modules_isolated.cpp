#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <iostream>

#include "savejpg.h"
#include "modules_isolated.h"
#include "globals.h"
using namespace std;
extern hw_ac **myOp;   


/** 
 * @brief This module implements the fdct
 * 
 * @param data :input data
 * @param fdtbl : 
 * @param datafloat: output
 * @param dataptr: I believe, this is only an intermediate variable
 */
void fdct(SBYTE *data,float *fdtbl, float *datafloat)
{
  float tmp0, tmp1, tmp2, tmp3, tmp4, tmp5, tmp6, tmp7;
  float tmp10, tmp11, tmp12, tmp13;
  float z1, z2, z3, z4, z5, z11, z13;
  //float datafloat[64];
  SBYTE ctr;
  BYTE i;
  float *dataptr; 
  for (i=0;i<64;i++) datafloat[i]=data[i];

  // Pass 1: process rows.
  dataptr=datafloat;
  for (ctr = 7; ctr >= 0; ctr--) {
    
    tmp0 = myOp[0]->calc(dataptr[0], dataptr[7]); //AdditionOp
    tmp7 = myOp[1]->calc(dataptr[0], -1*dataptr[7]); //AdditionOp
    tmp1 = myOp[2]->calc(dataptr[1], dataptr[6]); //AdditionOp
    tmp6 = myOp[3]->calc(dataptr[1], -1*dataptr[6]); //AdditionOp
    tmp2 = myOp[4]->calc(dataptr[2], dataptr[5]); //AdditionOp
    tmp5 = myOp[5]->calc(dataptr[2], -1*dataptr[5]); //AdditionOp
    tmp3 = myOp[6]->calc(dataptr[3], dataptr[4]); //AdditionOp
    tmp4 = myOp[7]->calc(dataptr[3], -1*dataptr[4]); //AdditionOp
    
    //Even part 
    tmp10 = myOp[8]->calc(tmp0 , tmp3); //AdditionOp
    tmp13 = myOp[9]->calc(tmp0 ,-1*tmp3); //AdditionOp
    tmp11 = myOp[10]->calc(tmp1 , tmp2); //AdditionOp
    tmp12 = myOp[11]->calc(tmp1 ,-1*tmp2); //AdditionOp

    dataptr[0] = myOp[12]->calc(tmp10 , tmp11);  //AdditionOp
    dataptr[4] = myOp[13]->calc(tmp10 ,-1*tmp11); //AdditionOp

    z1 = (tmp12 + tmp13) * ((float) 0.707106781); // c4
	dataptr[2] = myOp[14]->calc(tmp13 ,z1);	 //AdditionOp
    dataptr[6] = myOp[15]->calc(tmp13 ,-1*z1); //AdditionOp

    // Odd part
    tmp10 = myOp[16]->calc(tmp4 , tmp5); //AdditionOp
    tmp11 = myOp[17]->calc(tmp5 , tmp6); //AdditionOp
    tmp12 = myOp[18]->calc(tmp6 , tmp7); //AdditionOp

	// The rotator is modified from fig 4-8 to avoid extra negations
    z5 = (tmp10 - tmp12) * ((float) 0.382683433); // c6
    z2 = ((float) 0.541196100) * tmp10 + z5; // c2-c6
    z4 = ((float) 1.306562965) * tmp12 + z5; // c2+c6
    z3 = tmp11 * ((float) 0.707106781); // c4

    z11 = myOp[19]->calc(tmp7 , z3); //AdditionOp
    z13 = myOp[20]->calc(tmp7 , -1*z3); //AdditionOp

    dataptr[5] = myOp[21]->calc(z13 , z2); //AdditionOp
    dataptr[3] = myOp[22]->calc(z13 ,-1*z2); //AdditionOp
	dataptr[1] = myOp[23]->calc(z11 , z4); //AdditionOp
    dataptr[7] = myOp[24]->calc(z11 ,-1*z4); //AdditionOp

    dataptr += 8;		//advance pointer to next row
  }

  // Pass 2: process columns
  cout<<"wwwwwwwwwwwwwwwwww"<<endl;
  dataptr = datafloat;
  for (ctr = 7; ctr >= 0; ctr--) {
    tmp0 = myOp[25]->calc(dataptr[0] , dataptr[56]); //AdditionOp
    tmp7 = myOp[26]->calc(dataptr[0] ,-1*dataptr[56]); //AdditionOp
    tmp1 = myOp[27]->calc(dataptr[8] , dataptr[48]); //AdditionOp
    tmp6 = myOp[28]->calc(dataptr[8] ,-1*dataptr[48]); //AdditionOp
    tmp2 = myOp[29]->calc(dataptr[16] , dataptr[40]); //AdditionOp
    tmp5 = myOp[30]->calc(dataptr[16] ,-1*dataptr[40]); //AdditionOp
    tmp3 = myOp[31]->calc(dataptr[24] , dataptr[32]); //AdditionOp
    tmp4 = myOp[32]->calc(dataptr[24] ,-1*dataptr[32]); //AdditionOp

    //Even part/
    tmp10 = myOp[33]->calc(tmp0 , tmp3); //AdditionOp
    tmp13 = myOp[34]->calc(tmp0 ,-1*tmp3); //AdditionOp
    tmp11 = myOp[35]->calc(tmp1 , tmp2); //AdditionOp
    tmp12 = myOp[36]->calc(tmp1 ,-1*tmp2); //AdditionOp

    dataptr[0] = myOp[37]->calc(tmp10 , tmp11); //AdditionOp
    dataptr[32] = myOp[38]->calc(tmp10 , -1*tmp11); //AdditionOp

	z1 = (tmp12 + tmp13) * ((float) 0.707106781); // c4
    dataptr[16] = myOp[39]->calc(tmp13 , z1);  //AdditionOp
    dataptr[48] = myOp[40]->calc(tmp13 ,-1*z1); //AdditionOp
    
    // Odd part

    tmp10 = myOp[41]->calc(tmp4 , tmp5); //AdditionOp
    tmp11 = myOp[42]->calc(tmp5 , tmp6); //AdditionOp
    tmp12 = myOp[43]->calc(tmp6 , tmp7); //AdditionOp
    
    // The rotator is modified from fig 4-8 to avoid extra negations.
	z5 = (tmp10 - tmp12) * ((float) 0.382683433); // cu6
    z2 = ((float) 0.541196100) * tmp10 + z5; // c2-c6
    z4 = ((float) 1.306562965) * tmp12 + z5; // c2+c6
    z3 = tmp11 * ((float) 0.707106781); // c4

    z11 = myOp[44]->calc(tmp7 , z3);	 //AdditionOp
    z13 = myOp[45]->calc(tmp7 ,-1*z3); //AdditionOp
    dataptr[40] = myOp[46]->calc(z13 , z2);  //AdditionOp
	dataptr[24] = myOp[47]->calc(z13 , -1*z2); //AdditionOp
    dataptr[8] = myOp[48]->calc(z11,  z4); //AdditionOp
    dataptr[56] = myOp[49]->calc(z11, -1*z4); //AdditionOp

    dataptr++;			// advance pointer to next column
  }

}

  

void quantization(float *fdtbl, SWORD *outdata, float *datafloat){
    // Quantize/descale the coefficients, and store into output array
    float temp;
    int i; 
    for (i = 0; i < 64; i++) {
        // Apply the quantization and scaling factor
        temp = myOp[50]->calc(datafloat[i], fdtbl[i]); //MultiplicationOp

        //Round to nearest integer.
        //Since C does not specify the direction of rounding for negative
        //quotients, we have to force the dividend positive for portability.
        //The maximum coefficient size is +-16K (for 12-bit data), so this
        //code should work for either 16-bit or 32-bit ints.

        outdata[i] = (SWORD) ((SWORD)(temp + 16384.5) - 16384);
    }
}



void huffmanCoding(SWORD *DC, bitstring *HTDC,bitstring *HTAC,bitstring EOB, bitstring M16zeroes){

    //zigzag reordered DU which will be Huffman coded
//
 //---------guide::: the next step after quantizatin is the coding stage, where we try to compress
 //the way that we send data over.
 //---------guide:::  the reordering is for the sake of Run-length Encoding, where the consecutive zeros
 //are mainly considered and coded. To increase the number of zeros, we use zig-zag reordering
 //zigzag reorder
 BYTE end0pos;
 BYTE nrzeroes;
 BYTE nrmarker;
 BYTE startpos;
 
 int i;
 SWORD Diff;
 for (i=0;i<=63;i++) DU[zigzag[i]]=DU_DCT[i];
 Diff=DU[0]-*DC;
 *DC=DU[0];
 
 //Huffman coding  (HTDC and HTAC)
 //Encode DC
 if (Diff==0) writebits(HTDC[0]); //Diff might be 0
 else {writebits(HTDC[category[Diff]]);
     writebits(bitcode[Diff]);
 }

 //Encode ACs
 for (end0pos=63;(end0pos>0)&&(DU[end0pos]==0);end0pos--) ;

 //end0pos = first element in reverse order !=0
 if (end0pos==0) {writebits(EOB);return;}

 i=1;
 while (i<=end0pos)
  {
   startpos=i;
   for (; (DU[i]==0)&&(i<=end0pos);i++) ;
   nrzeroes=i-startpos;
   if (nrzeroes>=16) {
      for (nrmarker=1;nrmarker<=nrzeroes/16;nrmarker++) writebits(M16zeroes);
      nrzeroes=nrzeroes%16;
		     }
   writebits(HTAC[nrzeroes*16+category[DU[i]]]);writebits(bitcode[DU[i]]);
   i++;
  }
 if (end0pos!=63) writebits(EOB);

}




