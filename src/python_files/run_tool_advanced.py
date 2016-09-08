from send_email import *
from test_benchmark import *
from test_benchmark_4_input_dep import *



def run_a_tool(benchmark, bench_suit_name, root_folder, heuristic_intensity1, heuristic_intensity2,tool_type):
    subject = "starting a run"
    body = "start the test_benchmark with benchmark: " + benchmark + " heuristic_intensity1:" + heuristic_intensity1 + " heuristic_intensity2:" + heuristic_intensity2 + " tool_type:" + tool_type
    send_email("behzadboro@gmail.com", "+1mastermind+", "behzadboro@gmail.com", subject, body)

    if(tool_type == "s6"):
        run_test_bench_mark(benchmark, root_folder, bench_suit_name,  heuristic_intensity1, heuristic_intensity2)
    if (tool_type == "multiple_inputs"):
        run_test_bench_mark_4_input_dep(benchmark, root_folder, bench_suit_name,  heuristic_intensity1, heuristic_intensity2)

    config_addr = open("config.txt", "w")
    config_addr.write("test_benchmark with benchmark: " + benchmark + " heuristic_intensity1:" + heuristic_intensity1 + " heuristic_intensity2:" + heuristic_intensity2 + " tool_type:" + tool_type)
    config_addr.close() 
    os.system("python make_backup.py " + benchmark + "  "  + tool_type)

    subject = "ending a run"
    body = "end the test_benchmark with benchmark: " + benchmark + " heuristic_intensity1:" + heuristic_intensity1 + " heuristic_intensity2:" + heuristic_intensity2 + " tool_type:" + tool_type
    send_email("behzadboro@gmail.com", "+1mastermind+", "behzadboro@gmail.com", subject, body)


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

tool_type = "multiple_inputs"
heuristic_intensity1="xl"
heuristic_intensity2= "xl"
run_a_tool(benchmark, bench_suit_name, root_folder, heuristic_intensity1, heuristic_intensity2,tool_type)

heuristic_intensity1="xl"
heuristic_intensity2= "xl"
tool_type = "s6"
run_a_tool(benchmark, bench_suit_name, root_folder, heuristic_intensity1, heuristic_intensity2,tool_type)
#
#

tool_type = "multiple_inputs"
heuristic_intensity1="xxl"
heuristic_intensity2= "xxl"
run_a_tool(benchmark, bench_suit_name, root_folder, heuristic_intensity1, heuristic_intensity2,tool_type)



heuristic_intensity1="xxl"
heuristic_intensity2= "xxl"
tool_type = "s6"
run_a_tool(benchmark, bench_suit_name, root_folder, heuristic_intensity1, heuristic_intensity2,tool_type)
#
#


