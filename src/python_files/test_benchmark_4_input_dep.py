#python send_email.py "starting a run" "start the test_benchmark"
#echo "======================"
#echo "REMINDERS"
#echo "======================"
#echo "reminder: the command line argument order is the following"
#echo "benchmark_name, root_folder,benchsuit_name"
#echo 
#echo 
#
#benchmark=$1
#root_folder=$2
#bench_suit_name=$3
#UTC=$4
#write_UTC=$5
#adjust_NGEN=$6
#heuristic_intensity1=$7
#heuristic_intensity2=$8
#echo "======================"
#echo "testing the $benchmark benchmark and dumping the results in $root_folder" 
#echo "======================"
#echo 
#echo
#
from run_task import *
import os
from settings import * 
from inputs import *
from combine_paretos import *
from compare_pareto_curves import *
from make_graphs import *

def run_test_bench_mark_4_input_dep(benchmark, root_folder, bench_suit_name, heuristic_intensity1, heuristic_intensity2):
    #removing all the previous files
    print "---------starting stage 0"
    os.system("rm *.PIK") 
    os.system("rm *.png") 
#    os.system("rm pareto_of_heur_flattened.PIK")
#    os.system("rm pareto_set_file.PIK")
#    os.system("rm ref.png")
#    os.system("rm combine.png")
#    os.system("rm pickled_results_pareto.PIK")
#    os.system("rm pareto_of_combined.PIK")
    print "done with the stage 0, removing all the files"

    ## ---- starting stage 1(apx all files, flattened version)
    if (benchmark == "disparity"):
        settings_obj = settingsClass(benchmark, root_folder, bench_suit_name,heuristic_intensity1)
        settings_obj.outputMode = "uniform"
        settings_obj.error_mode= "corresponding_elements"
        
        inputObj = inputClass(settings_obj)
        print "\n\n---------starting stage 1"
        stage_number = 1 
        os.chdir("/home/local/bulkhead/behzad/usr/local/sd-vbs/benchmarks/disparity/src/c/")
        os.system("cp computeSAD_apx.txt computeSAD.c")
        os.system("cp finalSAD_apx.txt finalSAD.c")
        os.system("cp integralImage2D2D_apx.txt integralImage2D2D.c")

        os.chdir("/home/polaris/behzad/behzad_local/"+ root_folder +"/src/python_files/")
        
         
        #---- get optimal setUps for various inputs 
        lOf_run_input_list = [["1.bmp", "2.bmp"], ["3.bmp", "4.bmp"]]
        optimal_setUps_for_various_inputs =  apply_heuristic_on_task_with_multiple_prime_input(settings_obj, inputObj, lOf_run_input_list)
        optimal_setUps_for_various_inputs_flattened = list(itertools.chain(*optimal_setUps_for_various_inputs))
        write_points(optimal_setUps_for_various_inputs_flattened, "various_inputs.PIK") 
        
        #----apply first input's optimal setUp for various inputs
        lOfmyPoints = [] 
        for iteration, input_ in enumerate(lOf_run_input_list): 
            inputObj.set_run_input(input_) 
            for el in optimal_setUps_for_various_inputs[0]: 
                myPoint = run_task_with_one_set_up_and_collect_info(settings_obj, inputObj,el.get_raw_setUp())
                myPoint.set_input_number(iteration) 
                lOfmyPoints.append(myPoint)
        
        write_points(lOfmyPoints, "various_inputs_same_setUp.PIK") 

    if (benchmark == "jpeg"):
        #run_input_list= ["1.bmp", "2.bmp"]
        settings_obj = settingsClass(benchmark, root_folder, bench_suit_name,heuristic_intensity1)
        settings_obj.outputMode = "uniform"
        settings_obj.error_mode = "image"
        inputObj = inputClass(settings_obj)
        print "\n\n---------starting stage 1"
        stage_number = 1 
        
        os.chdir("/home/polaris/behzad/behzad_local/" + root_folder + "/src/CSrc/")
        
        os.system("cp dct_apx.txt dct.cpp")
        os.system("cp quant_apx.txt quant.cpp")

        os.chdir("/home/polaris/behzad/behzad_local/"+ root_folder +"/src/python_files/")
        
        
        #---- get optimal setUps for various inputs 
        lOf_run_input_list = [["west_1"], ["stop_1"], ["moreboxes_1"], ["tree_1"]]
        optimal_setUps_for_various_inputs =  apply_heuristic_on_task_with_multiple_prime_input(settings_obj, inputObj, lOf_run_input_list)
         
        optimal_setUps_for_various_inputs_flattened = list(itertools.chain(*optimal_setUps_for_various_inputs))
        write_points(optimal_setUps_for_various_inputs_flattened, "various_inputs.PIK") 
        
        #----apply first input's optimal setUp for various inputs
        lOfmyPoints = [] 
        for iteration, input_ in enumerate(lOf_run_input_list): 
            inputObj.set_run_input(input_) 
            for el in optimal_setUps_for_various_inputs[0]: 
                myPoint = run_task_with_one_set_up_and_collect_info(settings_obj, inputObj,el.get_raw_setUp())
                myPoint.set_input_number(iteration) 
                lOfmyPoints.append(myPoint)
        
        write_points(lOfmyPoints, "various_inputs_same_setUp.PIK") 
        

#if __name__ == "__main__":
#    main() 
#python send_email.py "ending_a_run" "done with test_benchmark"
