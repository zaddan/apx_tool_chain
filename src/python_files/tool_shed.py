from send_email import *
from test_benchmark import *
from test_benchmark_4_input_dep import *
import time

def run_a_tool(benchmark, bench_suit_name, root_folder, heuristic_intensity1, heuristic_intensity2,tool_type):
    start_time = time.time() 
    subject = "starting a run"
    body = "start the test_benchmark with benchmark: " + benchmark + " heuristic_intensity1:" + heuristic_intensity1 + " heuristic_intensity2:" + heuristic_intensity2 + " tool_type:" + tool_type
#     send_email("behzadboro@gmail.com", "+1mastermind+", "behzadboro@gmail.com", subject, body)

    if(tool_type == "s6"):
        run_test_bench_mark(benchmark, root_folder, bench_suit_name,  heuristic_intensity1, heuristic_intensity2)
    if (tool_type == "various_inputs"):
        run_test_bench_mark_4_input_dep(benchmark, root_folder, bench_suit_name,  heuristic_intensity1, heuristic_intensity2)

    end_time = time.time() 
    config_addr = open("config.txt", "w")
    config_addr.write("benchmark: " + benchmark + "\n") 
    config_addr.write("heuristic_intensity1:" + heuristic_intensity1 + " heuristic_intensity2:" + heuristic_intensity2 + "\n")
    config_addr.write("tool_type: " + tool_type + "\n")
    run_time_duration =  (end_time - start_time)/60
    config_addr.write("run duration(minutes): " + str(run_time_duration))
    config_addr.close() 
    #os.system("python make_backup.py " + benchmark + "  "  + tool_type)

    subject = "ending a run"
    body = "end the test_benchmark with benchmark: " + benchmark + " heuristic_intensity1:" + heuristic_intensity1 + " heuristic_intensity2:" + heuristic_intensity2 + " tool_type:" + tool_type + "run time duration:" + str(run_time_duration)
    send_email("behzadboro@gmail.com", "+1mastermind+", "behzadboro@gmail.com", subject, body)
