#include <fstream>
#include <cstring>
#include <math.h>
#include <stdio.h>
#include <fstream>
#include <iostream>
#include <vector>
#include <iomanip>
using namespace std;
int main() {

   int a = 0x44c00000 ;
//     int a = 0x49dcc000;
   int b = 0x45000000;
   //int b = 0x49d5d000  ;
  printf("%x\n", a);
    float a_fl;
    float b_fl;
    memcpy(&a_fl, &a, sizeof(int));
    memcpy(&b_fl, &b,sizeof(int));
    
   printf("num:%f  hex:%x\n", a_fl, *(unsigned int*)&a_fl);  
   //printf("%x\n", a_fl);
    float c = a_fl + b_fl; 
   printf("num:%f  hex:%x\n", c, *(unsigned int*)&c);  

}
