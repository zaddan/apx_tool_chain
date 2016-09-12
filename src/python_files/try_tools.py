from send_email import *
from tool_shed import run_a_tool
import os
from error import *
os.system("rm *.er") 
benchmark= "disparity"
#benchmark= "sift"
#benchmark= "localization"
#benchmark= "jpeg"

bench_suit_name= "sd-vbs"
#bench_suit_name= "my_micro_benchmark"

root_folder= "apx_tool_chain"

#heuristic_intensity1="small"
#heuristic_intensity2= "small"
#heuristic_intensity1="medium"
#heuristic_intensity2= "medium"
heuristic_intensity1="large"
heuristic_intensity2= "large"

tool_type = "various_inputs"
#heuristic_intensity1="xxxxl"
#heuristic_intensity2= "xxxxl"
try:
    run_a_tool(benchmark, bench_suit_name, root_folder, heuristic_intensity1, heuristic_intensity2,tool_type)
except TaskError as er:
    print "TASK ERROR OCCURED" 
    write_error(er)
except BenchMarkError as er:
    print "BENCHMARK ERROR OCCURED" 
    write_error(er)

#heuristic_intensity1="xl"
#heuristic_intensity2= "xl"
#try:
#    run_a_tool(benchmark, bench_suit_name, root_folder, heuristic_intensity1, heuristic_intensity2,tool_type)
#except TaskError as er:
#    print "TASK ERROR OCCURED" 
#    write_error(er)
#except BenchMarkError as er:
#    print "BENCHMARK ERROR OCCURED" 
#    write_error(er)
#
#


"""
try:
    run_a_tool(benchmark, bench_suit_name, root_folder, heuristic_intensity1, heuristic_intensity2,tool_type)
except TaskError as er:
    print "TASK ERROR OCCURED" 
    write_error(er)
except BenchMarkError as er:
    print "BENCHMARK ERROR OCCURED" 
    write_error(er)

"""
"""
#benchmark= "disparity"
#benchmark= "sift"
#benchmark= "localization"
benchmark= "disparity"

bench_suit_name= "sd-vbs"
#bench_suit_name= "my_micro_benchmark"

root_folder= "apx_tool_chain"

#heuristic_intensity1="small"
#heuristic_intensity2= "small"
#heuristic_intensity1="medium"
#heuristic_intensity2= "medium"
#heuristic_intensity1="large"
#heuristic_intensity2= "large"

tool_type = "various_inputs"
heuristic_intensity1="xxl"
heuristic_intensity2= "xxl"
run_a_tool(benchmark, bench_suit_name, root_folder, heuristic_intensity1, heuristic_intensity2,tool_type)

heuristic_intensity1="xxl"
heuristic_intensity2= "xxl"
tool_type = "s6"
run_a_tool(benchmark, bench_suit_name, root_folder, heuristic_intensity1, heuristic_intensity2,tool_type)
#
#

tool_type = "various_inpus"
heuristic_intensity1="xxxl"
heuristic_intensity2= "xxxl"
run_a_tool(benchmark, bench_suit_name, root_folder, heuristic_intensity1, heuristic_intensity2,tool_type)



heuristic_intensity1="xxxl"
heuristic_intensity2= "xxxl"
tool_type = "s6"
run_a_tool(benchmark, bench_suit_name, root_folder, heuristic_intensity1, heuristic_intensity2,tool_type)
#
#
"""




