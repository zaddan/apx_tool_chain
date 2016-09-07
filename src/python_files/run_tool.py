from send_email import *
#benchmark= "disparity"
#benchmark= "sift"
#benchmark= "localization"
benchmark= "jpeg"

#bench_suit_name= "sd-vbs"
bench_suit_name= "my_micro_benchmark"

root_folder= "apx_tool_chain"

#heuristic_intensity1="small"
#heuristic_intensity2= "small"
#heuristic_intensity1="medium"
#heuristic_intensity2= "medium"
heuristic_intensity1="large"
heuristic_intensity2= "large"
#




from test_benchmark import *
from test_benchmark_4_input_dep import *

#--send an email to signal start of a run
subject = "starting a run"
body = "start the test_benchmark"
send_email("behzadboro@gmail.com", "+1mastermind+", "behzadboro@gmail.com", subject, body)

#run_test_bench_mark(benchmark, root_folder, bench_suit_name,  heuristic_intensity1, heuristic_intensity2)
run_test_bench_mark_4_input_dep(benchmark, root_folder, bench_suit_name,  heuristic_intensity1, heuristic_intensity2)

#--send an email to signal end of a run
subject = "ending a run"
body = "end the test_benchmark"
send_email("behzadboro@gmail.com", "+1mastermind+", "behzadboro@gmail.com", subject, body)
