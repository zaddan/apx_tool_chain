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
from error import *
from run_task import *
import os
from settings import * 
from inputs import *
from combine_paretos import *
from compare_pareto_curves import *
from make_graphs import *
import image_list
def run_test_bench_mark_4_input_dep(benchmark, root_folder, bench_suit_name, heuristic_intensity1, heuristic_intensity2):
    #removing all the previous files
    print "---------starting stage 0"
    #os.system("rm *.PIK") 
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
        #lOf_run_input_list = [["1.bmp", "2.bmp"], ["3.bmp", "4.bmp"], ["5.bmp","6.bmp" ]]
        lOf_run_input_list = [["room_1.bmp", "room_2.bmp"], ["papers_1.bmp", "papers_2.bmp"], ["odd_1.bmp", "odd_2.bmp"], ["baby1_1.bmp", "baby1_2.bmp"], ["plastic_1.bmp", "plastic_2.bmp"], ["rocks1_1.bmp", "rocks1_2.bmp"]]
        #lOf_run_input_list = [["room_1.bmp", "room_2.bmp"], ["baby1_1.bmp", "baby1_2.bmp"]]
        try: 
            optimal_setUps_for_various_inputs, lOflOfAllPointsTried =  apply_heuristic_on_task_with_multiple_prime_input(settings_obj, inputObj, lOf_run_input_list)
        except BenchMarkError as er:
            write_error(er)
            raise ToolError 
        
        optimal_setUps_for_various_inputs_flattened = list(itertools.chain(*optimal_setUps_for_various_inputs))
        write_points(optimal_setUps_for_various_inputs_flattened, "various_inputs.PIK") 
        
        lOflOfAllPointsTried_flattened = list(itertools.chain(*lOflOfAllPointsTried))
        write_points(lOflOfAllPointsTried_flattened, "pickled_results_all_points.PIK")
        
        #----apply first input's optimal setUp for various inputs
        lOfmyPoints = [] 
        for iteration, input_ in enumerate(lOf_run_input_list): 
            inputObj.settings_obj.runMode = "serial" 
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
        #lOf_run_input_list = [["west_1"], ["stop_1"], ["moreboxes_1"], ["tree_1"]]
        #lOf_run_input_list = [["flowerpots_1"], ["aloe_1"]]
        #, ["monopoly_1"], ["baby1_1"], ["plastic_1"], ["rocks1_1"]]
        lOf_run_input_list = image_list.lOf_run_input_list
        
        
        inputObj.quality_calc_mode = "individual" 
        """
        optimal_setUps_for_various_inputs,lOflOfAllPointsTried =  apply_heuristic_on_task_with_multiple_prime_input(settings_obj, inputObj, lOf_run_input_list)
        optimal_setUps_for_various_inputs_flattened = list(itertools.chain(*optimal_setUps_for_various_inputs))
        write_points(optimal_setUps_for_various_inputs_flattened, "various_inputs.PIK") 
        
        lOflOfAllPointsTried_flattened = list(itertools.chain(*lOflOfAllPointsTried))
        write_points(lOflOfAllPointsTried_flattened, "pickled_results_all_points.PIK")
        #----apply first input's optimal setUp for various inputs
         
        #--- get the input with most number of set up founds
        #--- this is done mainly for evaluating the dependency of input and quality
        #--- we pick the input with the most number of setup b/c it give us the most
        #--- number of points
        input_n_setUps = [len(i) for i in optimal_setUps_for_various_inputs]
        input_n_setUps_index_sorted = sorted(enumerate(input_n_setUps), key=lambda x: x[1])
        index_of_n_setUps_sorted = map(lambda y: y[0], input_n_setUps_index_sorted)
        max_n_setUps = index_of_n_setUps_sorted[-1] 
        imposer_input_number = 0  
        l_imposing_setUp = optimal_setUps_for_various_inputs[imposer_input_number]
        
        #---- removing and creating image_dirs for further comparison
        optimal_image_dir = "optimal_image_dump"
        imposed_image_dir = "imposed_image_dump" 
        os.system("rm -r " + optimal_image_dir)
        os.system("mkdir " + optimal_image_dir)
        os.system("rm -r " + imposed_image_dir)
        os.system("mkdir " + imposed_image_dir)
        
        #--- separating each inupts optimal setUp 
        all_points = getPoints("various_inputs.PIK")
        each_input_optimal_setup = map(list, [[]]*len(lOf_run_input_list))
        for el in all_points:
            each_input_optimal_setup[el.get_input_number()].append(el)

        #--- making images for all the optimal setups
        lOfmyPoints = [] 
        for iteration, input_ in enumerate(lOf_run_input_list): 
            inputObj.settings_obj.runMode = "serial" 
            inputObj.set_run_input(input_) 
            lOfSetUps = each_input_optimal_setup[iteration] 
            for el in lOfSetUps:
                #print "here is the setUp: " + str(el.get_raw_setUp() )
                myPoint = run_task_with_one_set_up_and_collect_info(settings_obj, inputObj,el.get_raw_setUp())
                myPoint.set_input_number(iteration) 
                myPoint_quality = myPoint.get_quality() 
                os.system("cp ~/apx_b/inputPics/" + input_[0]+"_noisy.ppm " + optimal_image_dir + "/"+input_[0]+"^^"+str(round(float(myPoint_quality),3))+"_quality^^noisy.ppm")
                lOfmyPoints.append(myPoint)       
        reminder(True, "delete the following line. just there to see if previous setUP corret. no need to rewirte various_inputs.PIK") 
        write_points(lOfmyPoints, "various_inputs.PIK") 
        """
        #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ 
        #--- setting up an imposer mode, and getting the setups associated with it
        #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ 
        imposing_mode =  "specific_input"
        #imposing_mode =  "avg_setUp"
        #imposing_mode =  "worst_case_setUp"
        lOfmyPoints = [] 
        if (imposing_mode == "avg_setUp") :
            imposed_setUp_file =  "various_inputs_avg_setUp.PIK"
            inputObj.quality_calc_mode = "avg" 
            optimal_setUps_for_various_inputs,lOflOfAllPointsTried =  apply_heuristic_on_task_with_multiple_prime_input(settings_obj, inputObj, lOf_run_input_list)
            optimal_setUps_for_various_inputs_flattened = list(itertools.chain(*optimal_setUps_for_various_inputs))
            write_points(optimal_setUps_for_various_inputs_flattened, imposed_setUp_file) 
        elif (imposing_mode ==  "worst_case_setUp"):
            imposed_setUp_file =  "various_inputs_worse_case_setUp.PIK"
            inputObj.quality_calc_mode = "worst_case" 
            optimal_setUps_for_various_inputs,lOflOfAllPointsTried =  apply_heuristic_on_task_with_multiple_prime_input(settings_obj, inputObj, lOf_run_input_list)
            optimal_setUps_for_various_inputs_flattened = list(itertools.chain(*optimal_setUps_for_various_inputs))
            write_points(optimal_setUps_for_various_inputs_flattened, imposed_setUp_file) 
        elif (imposing_mode == "specific_input"):
            inputObj.quality_calc_mode = "individual" 
            imposer_input_number = 2
            print "the image to use as an imposer: " + str(lOf_run_input_list[imposer_input_number])
            imposed_setUp_file =  "one_input_imposed_setUp_points.PIK"
            all_points = getPoints("various_inputs.PIK")
            for el in all_points:
                if el.get_input_number() == imposer_input_number:
                    lOfmyPoints.append(el) 
            write_points(lOfmyPoints, imposed_setUp_file) 
        else:
            print "this imposing_mode is not defined"
            sys.exit()
        l_imposing_setUp, l_promised_quality = get_imposing_setups(imposed_setUp_file)
        
        
        write_points(lOfmyPoints, "imposed_setUp.PIK") 
        #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ 
        #--- applying the imposed setUps on all images, and also recording the images
        #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ 
        lOfmyPoints = [] 
        for iteration, input_ in enumerate(lOf_run_input_list): 
            inputObj.settings_obj.runMode = "serial" 
            inputObj.set_run_input(input_) 
            for imposed_setUp_index, el in enumerate(l_imposing_setUp):
                print "here is the setUp: " + str(el.get_raw_setUp() )
                myPoint = run_task_with_one_set_up_and_collect_info(settings_obj, inputObj,el.get_raw_setUp())
                myPoint.set_input_number(iteration) 
                myPoint_quality = myPoint.get_quality() 

#                 os.system("cp ~/apx_b/inputPics/" + input_[0]+"_noisy.ppm " + imposed_image_dir + "/"+input_[0]+"^^"+str(round(l_promised_quality[imposed_setUp_index],3))+"_VS_"+str(round(float(myPoint_quality),3))+"_quality^^noisy.ppm")
                lOfmyPoints.append(myPoint)
         
        write_points(lOfmyPoints, "various_inputs_same_setUp.PIK") 
        
    if (benchmark == "localization"):
        settings_obj = settingsClass(benchmark, root_folder, bench_suit_name,heuristic_intensity1)
        settings_obj.outputMode = "non-uniform"
        settings_obj.error_mode= "corresponding_elements"
        inputObj = inputClass(settings_obj)
        
        print "\n\n---------starting stage 1"
        stage_number = 1 
        os.chdir("/home/local/bulkhead/behzad/usr/local/sd-vbs/benchmarks/localization/src/c/")
        
        os.system("cp eul2quat_apx.txt eul2quat.c")
        os.system("cp quatMul_apx.txt quatMul.c")
        os.system("cp fTimes_mod_apx.txt fTimes_mod.c")
        os.system("cp fMtimes_mod_apx.txt fMtimes_mod.c")
        os.system("cp script_localization_apx.txt script_localization.c")
        
        os.chdir("/home/polaris/behzad/behzad_local/"+ root_folder +"/src/python_files/")
        
        #---- get optimal setUps for various inputs 
        #lOf_run_input_list = [["1.bmp", "2.bmp"], ["3.bmp", "4.bmp"], ["5.bmp","6.bmp" ]]
        lOf_run_input_list = [["1.txt", "GARBAGE"], ["3.txt", "GARBAGE"], ["4.txt", "GARBAGE"], ["5.txt", "GARBAGE"],["6.txt", "GARBAGE"], ["1.txt", "GARBAGE"]]
        #, ["2.txt", "GARBAGE"]]
        #, ["3.txt", "GARBARGE"], ["4.txt", "GARBAGE"], ["5.txt", "GARGABGE"], ["6.txt", "GARBAGE"]]
        try: 
            optimal_setUps_for_various_inputs,lOflOfAllPointsTried =  apply_heuristic_on_task_with_multiple_prime_input(settings_obj, inputObj, lOf_run_input_list)
        except BenchMarkError as er:
            write_error(er)
            raise ToolError 
        
        optimal_setUps_for_various_inputs_flattened = list(itertools.chain(*optimal_setUps_for_various_inputs))
        write_points(optimal_setUps_for_various_inputs_flattened, "various_inputs.PIK") 
        
        lOflOfAllPointsTried_flattened = list(itertools.chain(*lOflOfAllPointsTried))
        write_points(lOflOfAllPointsTried_flattened, "pickled_results_all_points.PIK")
        #----apply first input's optimal setUp for various inputs
        lOfmyPoints = [] 
        for iteration, input_ in enumerate(lOf_run_input_list): 
            inputObj.settings_obj.runMode = "serial" 
            inputObj.set_run_input(input_) 
            for el in optimal_setUps_for_various_inputs[0]: 
                myPoint = run_task_with_one_set_up_and_collect_info(settings_obj, inputObj,el.get_raw_setUp())
                myPoint.set_input_number(iteration) 
                lOfmyPoints.append(myPoint)
        write_points(lOfmyPoints, "various_inputs_same_setUp.PIK") 




#if __name__ == "__main__":
#    main() 
#python send_email.py "ending_a_run" "done with test_benchmark"
