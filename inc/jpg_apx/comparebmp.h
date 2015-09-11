#ifndef COMPAREBMP_H
#define COMPAREBMP_H

#include "savejpg.h"

#define  Y1(R,G,B) ((BYTE)( (YRtab1[(R)]+YGtab1[(G)]+YBtab1[(B)])>>16 ) - 128)
#define Cb1(R,G,B) ((BYTE)( (CbRtab1[(R)]+CbGtab1[(G)]+CbBtab1[(B)])>>16 ) )
#define Cr1(R,G,B) ((BYTE)( (CrRtab1[(R)]+CrGtab1[(G)]+CrBtab1[(B)])>>16 ) )

void init_all1();

void precalculate_YCbCr_tables1();

void exitmessage2(char *error_message);

void load_bitmap1(char *bitmap_name, WORD *Ximage_original, WORD *Yimage_original);

void load_bitmap2(char *bitmap_name, WORD *Ximage_original, WORD *Yimage_original);

void load_data_units_from_RGB_buffer_cmp(WORD xpos,WORD ypos);

double main_compare();

double comparebmp(char *BmpFile, char *BmpFile_ref);

#endif 
