from termcolor import colored
import os
#for integers
#for truncation
#os.system("make");
#os.system("cp ~/behzad_local/verilog_files/apx_operators/int_ops_apx/TRUNCATION.txt .")
#os.system("./simple . out ../operator_sample.txt")
#os.system("python get_elements_and_compare_truncation.py")

#for rounding
#os.system("make");
#os.system("cp ~/behzad_local/verilog_files/apx_operators/int_ops_apx/BT_RND.txt .")
#os.system("./simple . out ../operator_sample.txt")
#os.system("python get_elements_and_compare_rnd.py")


#for floating
#for truncation
os.chdir("../../build/")
os.system("make");
#
os.chdir("../src/PySrc")
os.system("cp ~/behzad_local/verilog_files/apx_operators/float_ops_apx/TRUNCATION.txt .")
os.system("../../build/simple . out ../../operator_sample.txt")
os.system("python get_elements_and_compare_truncation.py")
#

#for rounding
#os.chdir("../../build/")
#os.system("make");
#os.chdir("../src/PySrc")
#os.system("cp ~/behzad_local/verilog_files/apx_operators/float_ops_apx/BT_RND.txt .")
#os.system("../../build/simple . out ../..//operator_sample.txt")
#os.system("python get_elements_and_compare_rnd.py")
print colored("test passed", 'green');

