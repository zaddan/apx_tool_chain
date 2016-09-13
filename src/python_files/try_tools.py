from send_email import *
from tool_shed import run_a_tool
import os
from error import *
import traceback
import logging

os.system("rm *.er") 

LOG_FILENAME = exception_dump_file
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
logger = logging.getLogger(__name__)

#heuristic_intensity1="small"
#heuristic_intensity2= "small"
#heuristic_intensity1="medium"
#heuristic_intensity2= "medium"
#heuristic_intensity1="large"
#heuristic_intensity2= "large"
#heuristic_intensity1="xxl"
#heuristic_intensity2= "xxl"



send_email_activate = True
benchmark= "disparity"
#benchmark= "sift"
#benchmark= "localization"
#benchmark= "jpeg"
bench_suit_name= "sd-vbs"
#bench_suit_name= "my_micro_benchmark"
root_folder= "apx_tool_chain"
tool_type = "various_inputs"
heuristic_intensity1="xxxl"
heuristic_intensity2= "xxxl"
try:
    run_a_tool(benchmark, bench_suit_name, root_folder, heuristic_intensity1, heuristic_intensity2,tool_type)
except TaskError as er:
    print "TASK ERROR OCCURED" 
    write_error(er)
    subject = "TASK ERROR" 
    body = "error in the test_benchmark with benchmark: " + benchmark + " heuristic_intensity1:" + heuristic_intensity1 + " heuristic_intensity2:" + heuristic_intensity2 + " tool_type:" + tool_type
    send_email("behzadboro@gmail.com", "+1mastermind+", "behzadboro@gmail.com", subject, body, send_email_activate)
    exit()
except BenchMarkError as er:
    print "BENCHMARK ERROR OCCURED" 
    write_error(er)
    subject = "BENCHMARK ERROR" 
    body = "error in the test_benchmark with benchmark: " + benchmark + " heuristic_intensity1:" + heuristic_intensity1 + " heuristic_intensity2:" + heuristic_intensity2 + " tool_type:" + tool_type
    send_email("behzadboro@gmail.com", "+1mastermind+", "behzadboro@gmail.com", subject, body, send_email_activate)
    exit()
except Exception as ex:
    traceback.print_exc()
    logger.exception(error)
    subject = "ERROR" 
    body = "error in the test_benchmark with benchmark: " + benchmark + " heuristic_intensity1:" + heuristic_intensity1 + " heuristic_intensity2:" + heuristic_intensity2 + " tool_type:" + tool_type
    send_email("behzadboro@gmail.com", "+1mastermind+", "behzadboro@gmail.com", subject, body, send_email_activate)
    exit()


send_email_activate = True
#benchmark= "disparity"
#benchmark= "sift"
#benchmark= "localization"
benchmark= "jpeg"
#bench_suit_name= "sd-vbs"
bench_suit_name= "my_micro_benchmark"
root_folder= "apx_tool_chain"
tool_type = "various_inputs"
heuristic_intensity1="xxxl"
heuristic_intensity2= "xxxl"
try:
    run_a_tool(benchmark, bench_suit_name, root_folder, heuristic_intensity1, heuristic_intensity2,tool_type)
except TaskError as er:
    print "TASK ERROR OCCURED" 
    write_error(er)
    subject = "TASK ERROR" 
    body = "error in the test_benchmark with benchmark: " + benchmark + " heuristic_intensity1:" + heuristic_intensity1 + " heuristic_intensity2:" + heuristic_intensity2 + " tool_type:" + tool_type
    send_email("behzadboro@gmail.com", "+1mastermind+", "behzadboro@gmail.com", subject, body, send_email_activate)
    exit()
except BenchMarkError as er:
    print "BENCHMARK ERROR OCCURED" 
    write_error(er)
    subject = "BENCHMARK ERROR" 
    body = "error in the test_benchmark with benchmark: " + benchmark + " heuristic_intensity1:" + heuristic_intensity1 + " heuristic_intensity2:" + heuristic_intensity2 + " tool_type:" + tool_type
    send_email("behzadboro@gmail.com", "+1mastermind+", "behzadboro@gmail.com", subject, body, send_email_activate)
    exit()
except Exception as ex:
    traceback.print_exc()
    logger.exception(error)
    subject = "ERROR" 
    body = "error in the test_benchmark with benchmark: " + benchmark + " heuristic_intensity1:" + heuristic_intensity1 + " heuristic_intensity2:" + heuristic_intensity2 + " tool_type:" + tool_type
    send_email("behzadboro@gmail.com", "+1mastermind+", "behzadboro@gmail.com", subject, body, send_email_activate)
    exit()




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




