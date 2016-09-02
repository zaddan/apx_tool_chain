benchmark= "disparity"
root_folder= "apx_tool_chain"
bench_suit_name= "sd-vbs"
#UTC= False
#write_UTC=$5
#adjust_NGEN=$6
heuristic_intensity1="large"
heuristic_intensity2= "large"
from test_bench_mark import *


run_test_bench_mark(benchmark, root_folder, bench_suit_name, False, True, True, heuristic_intensity1, heuristic_intensity2)
