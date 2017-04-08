from termcolor import colored
import os

operand_type = "integers"
#operand_type = "floating"
mode  = "truncation"
#mode = "rounding"


#--- for integers
if (operand_type == "integers"):
    #--- for truncation
    if (mode == "truncation"): 
        os.chdir("../../build/")
        os.system("make");
        os.chdir("../src/PySrc")
        os.system("cp ~/behzad_local/verilog_files/apx_operators/int_ops_apx/build/functional/results.txt TRUNCATION.txt")
        os.system("../../build/simple . out ../../operator_sample.txt")
        os.system("python get_elements_and_compare_truncation.py")

    #--- for rounding
    if (mode == "rounding"):
        os.chdir("../../build/")
        os.system("make");
        os.chdir("../src/PySrc")
        os.system("cp ~/behzad_local/verilog_files/apx_operators/int_ops_apx/BT_RND.txt .")
        os.system("../../build/simple . out ../../operator_sample.txt")
        os.system("python get_elements_and_compare_rnd.py")

#--- for floating points
if (operand_type == "floating"):
    #--- for truncation
    if (mode == "truncation"): 
        os.chdir("../../build/")
        os.system("make");
        os.chdir("../src/PySrc")
        os.system("cp ~/behzad_local/verilog_files/apx_operators/float_ops_apx/TRUNCATION.txt .")
        os.system("../../build/simple . out ../../operator_sample.txt")
        os.system("python get_elements_and_compare_truncation.py")

    #--- for rounding
    if( mode == "rounding"):
        os.chdir("../../build/")
        os.system("make");
        os.chdir("../src/PySrc")
        os.system("cp ~/behzad_local/verilog_files/apx_operators/float_ops_apx/BT_RND.txt .")
        os.system("../../build/simple . out ../..//operator_sample.txt")
        os.system("python get_elements_and_compare_rnd.py")



print colored("if nothing has printed then test has passed. also 800000 and 000000 are simply two different versions of zero and c and verilog might disagree but we can ignore", 'blue');

