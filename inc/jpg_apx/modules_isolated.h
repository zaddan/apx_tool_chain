#ifndef FDCT_H
#define FDCT_H 
#include "savejpg.h"

void fdct(SBYTE *data,float *fdtbl, float *datafloat);
void quantization(float *fdtbl,SWORD *outdata, float *datafloat);
void huffmanCoding(SWORD *DC, bitstring *HTDC,bitstring *HTAC,bitstring EOB, bitstring M16zeroes);

#endif //FDCT_H

