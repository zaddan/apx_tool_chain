//copy paste the following lines: start here
#include <fstream>
#include "Operators.h"
#include "operatorFile_parser.h"
#include "setSubType.h"
#include "operandFile_parser.h"
#include "globals.h"
#include "foo.h"
extern hw_ac **myOp;   
// end here

int foo(int a, int b){
    int c = myOp[2]->calc(a,b); //AdditionOp
    return c;
}
