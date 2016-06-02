/*!
  \file dct.cpp
  DCT transform from JPEG example.
!*/
//#include "jpegEncoder.h"
#include <stdio.h>
#include <fstream>
#include <stdlib.h>
#include <sstream>
#include <assert.h>
//#include "globals.h"
#include <iostream>
using namespace std;


/*
#define c1d4 362L
#define c1d8 473L
#define c3d8 196L
#define c1d16 502L
#define c3d16 426L
#define c5d16 284L
#define c7d16 100L
*/

extern ofstream dct_io_log;
int c1d4= 362;
int c1d8= 473;
int c3d8= 196;
int c1d16= 502;
int c3d16= 426;
int c5d16= 284;
int c7d16= 100;

int LS(int r, int s) {
    return ((r) << (s));
}


int RS(int r, int s) {
    return ((r) >> (s));       
}


int MSCALE(int r) {
    return ((r) >> (9));       
}

int CLIP(int tmp)
{
   int tval=tmp;
   tval = (((tval < 0) ? (tval - 4) : (tval + 4)) / 8);
   if (tval < -1023)
   {
     tval = -1023;
   }
   else if (tval > 1023)
   {
     tval = 1023;
   }
	 return tval;
}


extern int dct_invocation;
ofstream dct_out_file;
ifstream dct_in_file("dct_in.txt");
void dct(
	bool dcten, 
	char inqueue[64], 
	int outqueue[64], 
	bool&qen)
{
 
   if (dct_invocation == 0) {
        dct_io_log.open("dct_io.log",std::fstream::out | std::fstream::binary);
        dct_io_log << "iter: " <<dct_invocation << "-------"<<endl;
        dct_io_log <<"*****IO ARE******"<<endl;
        dct_io_log<< "dct_en: "<<dcten<<endl; 
        dct_io_log << "inqueue: "<<endl;
        for (int i=0; i< 64; i++) {
            //dct_io_log<< (char)inqueue[i]<< " "; 
            dct_io_log<< (char)inqueue[i]; 
        }
        dct_io_log<<endl; 
    }
    /* 
    if (dct_invocation == 0) {
     dct_out_file.open("dct_input.txt",std::fstream::out | std::fstream::binary);
     dct_out_file << "iter: " <<dct_invocation << "-------"<<endl;
     dct_out_file << "inqueue: "<<endl;
     for (int i=0; i< 64; i++) {
         dct_out_file<< inqueue[i] + " "; 
     }
    dct_out_file<<endl; 
 }
 
  */ 
        //cout<<"dct has been incovated for " << dct_invocation <<endl;
//#pragma HLS function_instantiate variable=color

  int i;// aptr;
  int a0,  a1,  a2,  a3;
  int b0,  b1,  b2,  b3;
  int tb0,  tb1,  ta0, ta1,  ta2,  ta3;
  int c0,  c1,  c2,  c3;
  int v0,  v1,  v2,  v3,  v4,  v5,  v6,  v7;
  //yuv_t in_block[64];
  int tmp[64];
	qen=dcten;
  if(dcten==false) return;
  for (i = 0; i < 8; i++)
  {

	//#pragma HLS PIPELINE
    //aptr = i;
    v0 = inqueue[i*8+0];
    v1 = inqueue[i*8+1];
    v2 = inqueue[i*8+2];
    v3 = inqueue[i*8+3];
    v4 = inqueue[i*8+4];
    v5 = inqueue[i*8+5];
    v6 = inqueue[i*8+6];
    v7 = inqueue[i*8+7];
    a0 = LS((v0+ v7),  2); //AdditionOp     
    //cout<< "a0: "<< a0<<endl; 
    
    c3 = LS((v0 + -1*v7),  2);//AdditionOp
    a1 = LS((v1 + v6),  2);//AdditionOp 
    c2 = LS((v1 +  -1*v6),  2);//AdditionOp
    a2 = LS((v2 + v5),  2);//AdditionOp 
    c1 = LS((v2 + -1*v5),  2);//AdditionOp
    a3 = LS((v3 + v4),  2);//AdditionOp 
    c0 = LS((v3 + -1*v4),  2);//AdditionOp
    b0 = a0 + a3; //AdditionOp
    b1 = a1 +  a2;//AdditionOp
    b2 = a1 + -1*a2;//AdditionOp
    b3 = a0 + -1*a3;//AdditionOp
    int b0b1Add1 = b0 + b1; //AdditionOp
    tmp[i] = MSCALE(c1d4 * (b0b1Add1));//MultiplicationOp
    int b0b1Sub1 = b0 + -1*b1; //AdditionOp
    tmp[i + 32] = MSCALE(c1d4 * (b0b1Sub1)); //MultiplicationOp
   

    int c3d8b2Mul = c3d8 * b2;//MultiplicationOp
    int c1d8b3Mul = c1d8 *  b3;//MultiplicationOp
    int c3d8b3Mul = c3d8 *  b3;//MultiplicationOp
    int c1d8b2Mul = c1d8 * b2;//MultiplicationOp
    
    tmp[i + 16] = MSCALE(c3d8b2Mul+ c1d8b3Mul);//AdditionOp
    tmp[i + 48] = MSCALE(c3d8b3Mul + -1*(c1d8b2Mul)); //AdditionOp
    
    int c2c1Temp =  c2 + -1*c1; //AdditionOp
    b0 = MSCALE(c1d4 *c2c1Temp);//MultiplicationOp
    int c2c1Temp2 =  c2 +  c1;//AdditionOp
    
    
    
    b1 = MSCALE(c1d4 * (c2c1Temp2));
    a0 = c0 + b0;
    a1 = c0 - b0;
    a2 = c3 - b1;
    a3 = c3 + b1;
    int c7d16a0Mul =  c7d16 * a0;
    int c1d16a3Mul = c1d16 * a3;
    int c3d16a2Mul =  c3d16 * a2;
    int c5d16a1Mul =  c5d16 * a1;
    int c5d16a2Mul =  c5d16 * a2;
    int c3d16a1Mul =  c3d16 * a1;
    int c7d16a3Mul =  c7d16 * a3;
    int c1d16a0Mul =  c1d16 * a0;
    tmp[i + 8] = MSCALE((c7d16a0Mul) + (c1d16a3Mul));
    tmp[i + 24] = MSCALE((c3d16a2Mul) - (c5d16a1Mul));
    tmp[i + 40] = MSCALE((c3d16a1Mul) + (c5d16a2Mul));
    tmp[i + 56] = MSCALE((c7d16a3Mul) - (c1d16a0Mul));
  }
  for (i = 0; i < 8; i++)
  {

	//#pragma HLS PIPELINE
    //aptr = LS(i,  3);
    v0 = tmp[i*8+0];// aptr++;
    v1 = tmp[i*8+1]; //aptr++;
    v2 = tmp[i*8+2]; //aptr++;
    v3 = tmp[i*8+3]; //aptr++;
    v4 = tmp[i*8+4];// aptr++;
    v5 = tmp[i*8+5]; //aptr++;
    v6 = tmp[i*8+6]; //aptr++;
    v7 = tmp[i*8+7];
    c3 = RS((v0 + -1*v7),  1);  //AdditionOp
    a0 = RS((v0 +  v7),  1);//AdditionOp
    c2 = RS((v1 + -1*v6),  1); //AdditionOp
    a1 = RS((v1 +  v6),  1);//AdditionOp
    c1 = RS((v2 + -1*v5),  1); //AdditionOp
    a2 = RS((v2 +  v5),  1);//AdditionOp
    c0 = RS((v3 + -1*v4),  1); //AdditionOp
    a3 = RS((v3 + v4),  1);//AdditionOp
    b0 = a0 + a3;//AdditionOp 
    b1 = a1 + a2;//AdditionOp
    b2 = a1 + -1*a2;//AdditionOp
    b3 = a0 + -1* a3;//AdditionOp
    int c1c2Sub = c2 + -1*c1; //AdditionOp
    int c1c2Add= c2 + c1; //AdditionOp
    tb0 = MSCALE(c1d4 *  (c1c2Sub)); //MultiplicationOp
    tb1 = MSCALE(c1d4 * (c1c2Add)); //MultiplicationOp
    ta0 = c0 + tb0; //AdditionOp
    ta1 = c0 + -1*tb0; //AdditionOp
    ta2 = c3 + -1*tb1; //AdditionOp
    ta3 = c3 +  tb1; //AdditionOp

    int b0b1Add = b0 +  b1;  //AdditionOp
    int b0b1Sub = b0 + -1*b1; //AdditionOp 
    int c3d8b2Mul = c3d8 * b2;//MultiplicationOp
    int c1d8b3Mul = c1d8 *  b3;//MultiplicationOp
    int c3d8b3Mul = c3d8 *  b3;//MultiplicationOp
    int c1d8b2Mul = c1d8 * b2;//MultiplicationOp
    
    
    outqueue[i*8] 		=CLIP(MSCALE(c1d4 * (b0b1Add)));
    outqueue[i*8 + 4] =CLIP(MSCALE(c1d4 * (b0b1Sub)));
    outqueue[i*8 + 2] =CLIP(MSCALE((c3d8b2Mul) + (c1d8b3Mul)));
    outqueue[i*8 + 6] =CLIP(MSCALE((c3d8b3Mul) - (c1d8b2Mul)));
    outqueue[i*8 + 1] =CLIP(MSCALE((c7d16 * ta0) + (c1d16 * ta3)));
    outqueue[i*8 + 3] =CLIP(MSCALE((c3d16 * ta2) - (c5d16 * ta1)));
    outqueue[i*8 + 5] =CLIP(MSCALE((c3d16 * ta1) + (c5d16 * ta2)));
    outqueue[i*8 + 7] =CLIP(MSCALE((c7d16 * ta3) - (c1d16 * ta0)));
	
  }
  
  /* 
  if (dct_invocation == 0){ 
      dct_out_file.open("dct_out.txt",std::fstream::out | std::fstream::binary);
      dct_out_file << "outqueue: "<<endl;
      for (int i=0; i< 64; i++) {
          dct_out_file<< outqueue[i]<<" "<<endl;; 
      }
      dct_out_file<<"qen "<<qen<<endl;
      dct_out_file.close(); 
  }
  */ 
  if (dct_invocation == 0){ 
      dct_io_log << "outqueue: "<<endl;
      for (int i=0; i< 64; i++) {
          dct_io_log<< (int)outqueue[i]<<" "; 
      }
      
      dct_io_log<<endl<<"qen: "<<qen<<endl; 
      dct_io_log.close(); 
  }
  
  
  dct_invocation++;  
}


