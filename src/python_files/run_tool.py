#benchmark= "disparity"
#benchmark= "sift"
#benchmark= "localization"
benchmark= "jpeg"

#bench_suit_name= "sd-vbs"
bench_suit_name= "my_micro_benchmark"

root_folder= "apx_tool_chain"

#heuristic_intensity1="small"
#heuristic_intensity2= "small"
heuristic_intensity1="medium"
heuristic_intensity2= "medium"
#heuristic_intensity1="large"
#heuristic_intensity2= "large"
#




from test_benchmark import *
from test_benchmark_4_input_dep import *


run_test_bench_mark(benchmark, root_folder, bench_suit_name,  heuristic_intensity1, heuristic_intensity2)
#run_test_bench_mark_4_input_dep(benchmark, root_folder, bench_suit_name,  heuristic_intensity1, heuristic_intensity2)
