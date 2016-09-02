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


def run_test_bench_mark(benchmark, root_folder, bench_suit_name, heuristic_intensity1, heuristic_intensity2):
    #removing all the previous files
    print "---------starting stage 0"
    os.system("rm pareto_of_heur_flattened")
    os.system("rm pareto_set_file.txt")
    os.system("rm ref.png")
    os.system("rm combine.png")
    os.system("rm pickled_results_pareto")
    os.system("rm pareto_of_combined")
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
        
        unique_point_list, lOfAllPointsTried, lOfPoints_out_of_heuristic, pointSet, input_Point_list, accurateSetUp = run_task_and_collect_points(settings_obj, inputObj)
        write_results(unique_point_list, lOfAllPointsTried, lOfPoints_out_of_heuristic, pointSet, input_Point_list, stage_number, inputObj, settings_obj)
        
        os.system("cp pickled_results_pareto pareto_of_heur_flattened");
        os.system("cp pickled_results_all_points all_of_flattned")
        os.system("cp pickled_results_pareto_of_all pareto_of_all_of_flattened")
        os.system("rm pareto_set_file.txt")
        os.system("cp ../../generated_text/finalResult.png ref.png")
        print "done with the stage 1: flattening and apx of all files"
        #---- starting stage 2(apx some files)
        stage_number = 2
        print "\n\n---------starting stage 2"
        settings_obj = settingsClass(benchmark, root_folder, bench_suit_name, heuristic_intensity2)
        settings_obj.outputMode = "uniform"
        settings_obj.error_mode= "corresponding_elements"

        inputObj.set_lOfSetUps([])
        inputObj.is_primary_input = True

        os.chdir("/home/local/bulkhead/behzad/usr/local/sd-vbs/benchmarks/disparity/src/c/")
        os.system("cp computeSAD_acc.txt computeSAD.c")
        os.system("cp finalSAD_acc.txt finalSAD.c")
        os.system("cp integralImage2D2D_acc.txt integralImage2D2D.c")

        os.system("cp computeSAD_apx.txt computeSAD.c")
        os.system("cp integralImage2D2D_apx.txt integralImage2D2D.c")

        os.chdir("/home/polaris/behzad/behzad_local/" + root_folder + "/src/python_files/")
        
        unique_point_list, lOfAllPointsTried, lOfPoints_out_of_heuristic_2, pointSet, input_Point_list, accurateSetUp = run_task_and_collect_points(settings_obj, inputObj)
        write_results(unique_point_list, lOfAllPointsTried, lOfPoints_out_of_heuristic_2, pointSet, input_Point_list, stage_number, inputObj, settings_obj)
        
        append_results(pointSet, settings_obj)
        
        os.system("rm ../../generated_text/finalResult.png ")
        os.system("rm pickled_results_pareto")
        os.system("cp pickled_results_all_points all_of_s2")
        os.system("cp pickled_results_pareto_of_all pareto_of_all_of_s2")
        print "done with the stage 2: apx of some files"
       

        # ---- starting stage 3(apx some files)
        print ""
        print ""
        print "---------starting stage 3"
        stage_number = 3 
        settings_obj = settingsClass(benchmark, root_folder, bench_suit_name, heuristic_intensity2)
        settings_obj.outputMode = "uniform"
        settings_obj.error_mode= "corresponding_elements"
        inputObj.set_lOfSetUps([accurateSetUp])
        inputObj.is_primary_input = False
        os.chdir("/home/local/bulkhead/behzad/usr/local/sd-vbs/benchmarks/disparity/src/c/")
        os.system("cp computeSAD_acc.txt computeSAD.c")
        os.system("cp finalSAD_acc.txt finalSAD.c")
        os.system("cp integralImage2D2D_acc.txt integralImage2D2D.c")

        os.system("cp finalSAD_apx.txt finalSAD.c")

        os.chdir("/home/polaris/behzad/behzad_local/"+root_folder+"/src/python_files/")
        unique_point_list, lOfAllPointsTried, lOfPoints_out_of_heuristic, pointSet, input_Point_list, accurateSetUp = run_task_and_collect_points(settings_obj, inputObj)
        write_results(unique_point_list, lOfAllPointsTried, lOfPoints_out_of_heuristic, pointSet, input_Point_list, stage_number, inputObj, settings_obj)
        append_results(pointSet, settings_obj)
        
        os.system("rm ../../generated_text/finalResult.png ")
        os.system("rm pickled_results_pareto")
        os.system("cp pickled_results_all_points all_of_s3")
        os.system("cp pickled_results_pareto_of_all pareto_of_all_of_s3")
        print "done with the stage 3: apx of some files"

        # ---- starting stage 4(apx some files, using UTC)
        print "\n\n---------starting stage 4"
        stage_number = 4
        #unique_point_list, lOf_UTC_PF, pareto_frontier_of_lOfPoints_out_of_heuristic, lOfAllPointsTried, pareto_frontier_of_lOfAllPointsTried, pointSet, input_Point_list = read_results()
        settings_obj = settingsClass(benchmark, root_folder, bench_suit_name, heuristic_intensity2)
        settings_obj.outputMode = "uniform"
        settings_obj.error_mode= "corresponding_elements"
        inputObj.is_primary_input = False
        inputObj.set_lOfSetUps(reduce_ideal_setUp_list(map(lambda x: x.get_setUp(), lOfPoints_out_of_heuristic_2)))
        
        #python run_write_config.py $benchmark $root_folder $bench_suit_name "True" "False" "False" $heuristic_intensity2
        os.chdir("/home/local/bulkhead/behzad/usr/local/sd-vbs/benchmarks/disparity/src/c/")
        os.system("cp computeSAD_acc.txt computeSAD.c")
        os.system("cp finalSAD_acc.txt finalSAD.c")
        os.system("cp integralImage2D2D_acc.txt integralImage2D2D.c")

        os.system("cp finalSAD_apx.txt finalSAD.c")

        os.chdir("/home/polaris/behzad/behzad_local/"+root_folder+"/src/python_files/")
        
        unique_point_list, lOfAllPointsTried, lOfPoints_out_of_heuristic, pointSet, input_Point_list, accurateSetUp = run_task_and_collect_points(settings_obj, inputObj)
        write_results(unique_point_list, lOfAllPointsTried, lOfPoints_out_of_heuristic, pointSet, input_Point_list, stage_number, inputObj, settings_obj)

        os.system("rm ../../generated_text/finalResult.png ")
        os.system("rm pickled_results_pareto")
        os.system("cp pickled_results_all_points all_of_s4")
        os.system("cp pickled_results_pareto_of_all pareto_of_all_of_s4")
        print "done with the stage 4: apx of some files"


        #---- starting stage 5(combine and compare)
        print "\n\n---------starting stage 5"
        stage_number = 5
        os.chdir("/home/local/bulkhead/behzad/usr/local/sd-vbs/benchmarks/disparity/src/c/")
        #returning all the files to approximate version (so we can get the accurate result)
        os.chdir("/home/local/bulkhead/behzad/usr/local/sd-vbs/benchmarks/disparity/src/c/")
        os.system("cp computeSAD_apx.txt computeSAD.c")
        os.system("cp finalSAD_apx.txt finalSAD.c")
        os.system("cp integralImage2D2D_apx.txt integralImage2D2D.c")

        os.chdir("/home/polaris/behzad/behzad_local/" +root_folder+"/src/python_files/")
       
        run_combine_pareto(settings_obj)
        #python combine_paretos.py
        run_compare_pareto_curves(settings_obj)
        #python compare_pareto_curves.py >> compare_results.txt
        os.system("cp ../../generated_text/finalResult.png combine.png")
        print "done with stage 5:combining the paretos and comparing"

    if (benchmark == "sift"):
        print "first make sure that the error_mode is correct, then get rid of the sys.exit()"
        sys.exit() 
        settings_obj = settingsClass(benchmark, root_folder, bench_suit_name,heuristic_intensity1)
        settings_obj.outputMode = "non-uniform"
        settings_obj.error_mode= "corresponding_elements"
        inputObj = inputClass(settings_obj)

        print "\n\n---------starting stage 1"
        stage_number = 1 
        os.chdir("/home/local/bulkhead/behzad/usr/local/sd-vbs/benchmarks/sift/src/c/")
        os.system("cp imsmooth_apx.txt imsmooth.c")
        os.system("cp diffss_apx.txt diffss.c")
        
        os.chdir("/home/polaris/behzad/behzad_local/"+ root_folder +"/src/python_files/")
        
        unique_point_list, lOfAllPointsTried, lOfPoints_out_of_heuristic, pointSet, input_Point_list, accurateSetUp = run_task_and_collect_points(settings_obj, inputObj)
        write_results(unique_point_list, lOfAllPointsTried, lOfPoints_out_of_heuristic, pointSet, input_Point_list, stage_number, inputObj, settings_obj)
        
        os.system("cp pickled_results_pareto pareto_of_heur_flattened");
        os.system("cp pickled_results_all_points all_of_flattned")
        os.system("cp pickled_results_pareto_of_all pareto_of_all_of_flattened")
        os.system("rm pareto_set_file.txt")
        os.system("cp ../../generated_text/finalResult.png ref.png")
        print "done with the stage 1: flattening and apx of all files"
        #---- starting stage 2(apx some files)
        stage_number = 2
        print "\n\n---------starting stage 2"
        settings_obj = settingsClass(benchmark, root_folder, bench_suit_name, heuristic_intensity2)
        settings_obj.outputMode = "non-uniform"
        settings_obj.error_mode= "corresponding_elements"
        inputObj.set_lOfSetUps([])
        inputObj.is_primary_input = True

        os.chdir("/home/local/bulkhead/behzad/usr/local/sd-vbs/benchmarks/sift/src/c/")
        os.system("cp imsmooth_acc.txt imsmooth.c")
        os.system("cp diffss_acc.txt diffss.c")
        os.system("cp imsmooth_apx.txt imsmooth.c")

        os.chdir("/home/polaris/behzad/behzad_local/" + root_folder + "/src/python_files/")
        
        unique_point_list, lOfAllPointsTried, lOfPoints_out_of_heuristic_2, pointSet, input_Point_list, accurateSetUp = run_task_and_collect_points(settings_obj, inputObj)
        write_results(unique_point_list, lOfAllPointsTried, lOfPoints_out_of_heuristic_2, pointSet, input_Point_list, stage_number, inputObj, settings_obj)
        
        append_results(pointSet, settings_obj)
        
        os.system("rm ../../generated_text/finalResult.png ")
        os.system("rm pickled_results_pareto")
        os.system("cp pickled_results_all_points all_of_s2")
        os.system("cp pickled_results_pareto_of_all pareto_of_all_of_s2")
        print "done with the stage 2: apx of some files"
       

        # ---- starting stage 3(apx some files)
        print ""
        print ""
        print "---------starting stage 3"
        stage_number = 3 
        settings_obj = settingsClass(benchmark, root_folder, bench_suit_name, heuristic_intensity2)
        settings_obj.outputMode = "non-uniform"
        settings_obj.error_mode= "corresponding_elements"

        inputObj.set_lOfSetUps([accurateSetUp])
        inputObj.is_primary_input = False
        os.chdir("/home/local/bulkhead/behzad/usr/local/sd-vbs/benchmarks/sift/src/c/")
        
        os.system("cp imsmooth_acc.txt imsmooth.c")
        os.system("cp diffss_acc.txt diffss.c")

        os.system("cp diffss_apx.txt diffss.c")

        os.chdir("/home/polaris/behzad/behzad_local/"+root_folder+"/src/python_files/")
        unique_point_list, lOfAllPointsTried, lOfPoints_out_of_heuristic, pointSet, input_Point_list, accurateSetUp = run_task_and_collect_points(settings_obj, inputObj)
        write_results(unique_point_list, lOfAllPointsTried, lOfPoints_out_of_heuristic, pointSet, input_Point_list, stage_number, inputObj, settings_obj)
        append_results(pointSet, settings_obj)
        
        os.system("rm ../../generated_text/finalResult.png ")
        os.system("rm pickled_results_pareto")
        os.system("cp pickled_results_all_points all_of_s3")
        os.system("cp pickled_results_pareto_of_all pareto_of_all_of_s3")
        print "done with the stage 3: apx of some files"

        # ---- starting stage 4(apx some files, using UTC)
        print "\n\n---------starting stage 4"
        stage_number = 4
        #unique_point_list, lOf_UTC_PF, pareto_frontier_of_lOfPoints_out_of_heuristic, lOfAllPointsTried, pareto_frontier_of_lOfAllPointsTried, pointSet, input_Point_list = read_results()
        settings_obj = settingsClass(benchmark, root_folder, bench_suit_name, heuristic_intensity2)
        settings_obj.outputMode = "non-uniform"
        settings_obj.error_mode= "corresponding_elements"
        inputObj.is_primary_input = False
        inputObj.set_lOfSetUps(reduce_ideal_setUp_list(map(lambda x: x.get_setUp(), lOfPoints_out_of_heuristic_2)))
        
        #python run_write_config.py $benchmark $root_folder $bench_suit_name "True" "False" "False" $heuristic_intensity2
        os.chdir("/home/local/bulkhead/behzad/usr/local/sd-vbs/benchmarks/sift/src/c/")
        
        os.system("cp imsmooth_acc.txt imsmooth.c")
        os.system("cp diffss_acc.txt diffss.c")
        os.system("cp diffss_apx.txt diffss.c")
        os.chdir("/home/polaris/behzad/behzad_local/"+root_folder+"/src/python_files/")
        
        unique_point_list, lOfAllPointsTried, lOfPoints_out_of_heuristic, pointSet, input_Point_list, accurateSetUp = run_task_and_collect_points(settings_obj, inputObj)
        write_results(unique_point_list, lOfAllPointsTried, lOfPoints_out_of_heuristic, pointSet, input_Point_list, stage_number, inputObj, settings_obj)

        os.system("rm ../../generated_text/finalResult.png ")
        os.system("rm pickled_results_pareto")
        os.system("cp pickled_results_all_points all_of_s4")
        os.system("cp pickled_results_pareto_of_all pareto_of_all_of_s4")
        print "done with the stage 4: apx of some files"


        #---- starting stage 5(combine and compare)
        print "\n\n---------starting stage 5"
        stage_number = 5
        os.chdir("/home/local/bulkhead/behzad/usr/local/sd-vbs/benchmarks/sift/src/c/")
        #returning all the files to approximate version (so we can get the accurate result)
        os.chdir("/home/local/bulkhead/behzad/usr/local/sd-vbs/benchmarks/sift/src/c/")
       
        os.system("cp imsmooth_apx.txt imsmooth.c")
        os.system("cp diffss_apx.txt diffss.c")
        
        os.chdir("/home/polaris/behzad/behzad_local/" +root_folder+"/src/python_files/")
       
        run_combine_pareto(settings_obj)
        #python combine_paretos.py
        run_compare_pareto_curves(settings_obj)
        #python compare_pareto_curves.py >> compare_results.txt
        os.system("cp ../../generated_text/finalResult.png combine.png")
        print "done with stage 5:combining the paretos and comparing"
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
        
        unique_point_list, lOfAllPointsTried, lOfPoints_out_of_heuristic, pointSet, input_Point_list, accurateSetUp = run_task_and_collect_points(settings_obj, inputObj)
        write_results(unique_point_list, lOfAllPointsTried, lOfPoints_out_of_heuristic, pointSet, input_Point_list, stage_number, inputObj, settings_obj)
        
        os.system("cp pickled_results_pareto pareto_of_heur_flattened");
        os.system("cp pickled_results_all_points all_of_flattned")
        os.system("cp pickled_results_pareto_of_all pareto_of_all_of_flattened")
        os.system("rm pareto_set_file.txt")
        os.system("cp ../../generated_text/finalResult.png ref.png")
        print "done with the stage 1: flattening and apx of all files"
        exit() 
        #---- starting stage 2(apx some files)
        stage_number = 2
        print "\n\n---------starting stage 2"
        settings_obj = settingsClass(benchmark, root_folder, bench_suit_name, heuristic_intensity2)
        settings_obj.outputMode = "non-uniform"
        settings_obj.error_mode= "corresponding_elements"
        inputObj.set_lOfSetUps([])
        inputObj.is_primary_input = True

        os.chdir("/home/local/bulkhead/behzad/usr/local/sd-vbs/benchmarks/localization/src/c/")
        
        os.system("cp fMtimes_mod_acc.txt fMtimes_mod.c")
        os.system("cp script_localization_acc.txt script_localization.c")
                
        os.chdir("/home/polaris/behzad/behzad_local/" + root_folder + "/src/python_files/")
        
        unique_point_list, lOfAllPointsTried, lOfPoints_out_of_heuristic_2, pointSet, input_Point_list, accurateSetUp = run_task_and_collect_points(settings_obj, inputObj)
        write_results(unique_point_list, lOfAllPointsTried, lOfPoints_out_of_heuristic_2, pointSet, input_Point_list, stage_number, inputObj, settings_obj)
        
        append_results(pointSet, settings_obj)
        
        os.system("rm ../../generated_text/finalResult.png ")
        os.system("rm pickled_results_pareto")
        os.system("cp pickled_results_all_points all_of_s2")
        os.system("cp pickled_results_pareto_of_all pareto_of_all_of_s2")
        print "done with the stage 2: apx of some files"
       

        # ---- starting stage 3(apx some files)
        print ""
        print ""
        print "---------starting stage 3"
        stage_number = 3 
        settings_obj = settingsClass(benchmark, root_folder, bench_suit_name, heuristic_intensity2)
        settings_obj.outputMode = "non-uniform"
        settings_obj.error_mode= "corresponding_elements"
        inputObj.set_lOfSetUps([accurateSetUp])
        inputObj.is_primary_input = False
        os.chdir("/home/local/bulkhead/behzad/usr/local/sd-vbs/benchmarks/localization/src/c/")
        
        os.system("cp eul2quat_acc.txt eul2quat.c")
        os.system("cp quatMul_acc.txt quatMul.c")
        os.system("cp fTimes_mod_acc.txt fTimes_mod.c")
        os.system("cp fMtimes_mod_apx.txt fMtimes_mod.c")
        os.system("cp script_localization_apx.txt script_localization.c")

        os.chdir("/home/polaris/behzad/behzad_local/"+root_folder+"/src/python_files/")
        unique_point_list, lOfAllPointsTried, lOfPoints_out_of_heuristic, pointSet, input_Point_list, accurateSetUp = run_task_and_collect_points(settings_obj, inputObj)
        write_results(unique_point_list, lOfAllPointsTried, lOfPoints_out_of_heuristic, pointSet, input_Point_list, stage_number, inputObj, settings_obj)
        append_results(pointSet, settings_obj)
        
        os.system("rm ../../generated_text/finalResult.png ")
        os.system("rm pickled_results_pareto")
        os.system("cp pickled_results_all_points all_of_s3")
        os.system("cp pickled_results_pareto_of_all pareto_of_all_of_s3")
        print "done with the stage 3: apx of some files"

        # ---- starting stage 4(apx some files, using UTC)
        print "\n\n---------starting stage 4"
        stage_number = 4
        settings_obj = settingsClass(benchmark, root_folder, bench_suit_name, heuristic_intensity2)
        settings_obj.outputMode = "non-uniform"
        settings_obj.error_mode= "corresponding_elements"
        inputObj.is_primary_input = False
        inputObj.set_lOfSetUps(reduce_ideal_setUp_list(map(lambda x: x.get_setUp(), lOfPoints_out_of_heuristic_2)))
        
        os.chdir("/home/local/bulkhead/behzad/usr/local/sd-vbs/benchmarks/localization/src/c/")
        
        os.system("cp eul2quat_acc.txt eul2quat.c")
        os.system("cp quatMul_acc.txt quatMul.c")
        os.system("cp fTimes_mod_acc.txt fTimes_mod.c")
        os.system("cp fMtimes_mod_apx.txt fMtimes_mod.c")
        os.system("cp script_localization_apx.txt script_localization.c")

        os.chdir("/home/polaris/behzad/behzad_local/"+root_folder+"/src/python_files/")
        
        unique_point_list, lOfAllPointsTried, lOfPoints_out_of_heuristic, pointSet, input_Point_list, accurateSetUp = run_task_and_collect_points(settings_obj, inputObj)
        write_results(unique_point_list, lOfAllPointsTried, lOfPoints_out_of_heuristic, pointSet, input_Point_list, stage_number, inputObj, settings_obj)

        os.system("rm ../../generated_text/finalResult.png ")
        os.system("rm pickled_results_pareto")
        os.system("cp pickled_results_all_points all_of_s4")
        os.system("cp pickled_results_pareto_of_all pareto_of_all_of_s4")
        print "done with the stage 4: apx of some files"


        #---- starting stage 5(combine and compare)
        print "\n\n---------starting stage 5"
        stage_number = 5
        os.chdir("/home/local/bulkhead/behzad/usr/local/sd-vbs/benchmarks/localization/src/c/")
        #returning all the files to approximate version (so we can get the accurate result)
        os.chdir("/home/local/bulkhead/behzad/usr/local/sd-vbs/benchmarks/localization/src/c/")
       
        
        os.system("cp eul2quat_apx.txt eul2quat.c")
        os.system("cp quatMul_apx.txt quatMul.c")
        os.system("cp fTimes_mod_apx.txt fTimes_mod.c")
        os.system("cp fMtimes_mod_apx.txt fMtimes_mod.c")
        os.system("cp script_localization_apx.txt script_localization.c")

        os.chdir("/home/polaris/behzad/behzad_local/" +root_folder+"/src/python_files/")
       
        run_combine_pareto(settings_obj)
        #python combine_paretos.py
        run_compare_pareto_curves(settings_obj)
        #python compare_pareto_curves.py >> compare_results.txt
        os.system("cp ../../generated_text/finalResult.png combine.png")
        print "done with stage 5:combining the paretos and comparing"

    if (benchmark == "jpeg"):
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
        
        unique_point_list, lOfAllPointsTried, lOfPoints_out_of_heuristic, pointSet, input_Point_list, accurateSetUp = run_task_and_collect_points(settings_obj, inputObj)
        write_results(unique_point_list, lOfAllPointsTried, lOfPoints_out_of_heuristic, pointSet, input_Point_list, stage_number, inputObj, settings_obj)
        
        os.system("cp pickled_results_pareto pareto_of_heur_flattened");
        os.system("cp pickled_results_all_points all_of_flattned")
        os.system("cp pickled_results_pareto_of_all pareto_of_all_of_flattened")
        os.system("rm pareto_set_file.txt")
        os.system("cp ../../generated_text/finalResult.png ref.png")
        print "done with the stage 1: flattening and apx of all files"
        #---- starting stage 2(apx some files)
        stage_number = 2
        print "\n\n---------starting stage 2"
        settings_obj = settingsClass(benchmark, root_folder, bench_suit_name, heuristic_intensity2)
        settings_obj.outputMode = "uniform"
        settings_obj.error_mode= "image"
        inputObj.set_lOfSetUps([])
        inputObj.is_primary_input = True

        os.chdir("/home/polaris/behzad/behzad_local/" + root_folder + "/src/CSrc/")
        
        os.system("cp dct_acc.txt dct.cpp")
        os.system("cp quant_acc.txt quant.cpp")
        os.system("cp dct_apx.txt dct.cpp")
       
        os.chdir("/home/polaris/behzad/behzad_local/" + root_folder + "/src/python_files/")
        
        unique_point_list, lOfAllPointsTried, lOfPoints_out_of_heuristic_2, pointSet, input_Point_list, accurateSetUp = run_task_and_collect_points(settings_obj, inputObj)
        write_results(unique_point_list, lOfAllPointsTried, lOfPoints_out_of_heuristic_2, pointSet, input_Point_list, stage_number, inputObj, settings_obj)
        
        append_results(pointSet, settings_obj)
        
        os.system("rm ../../generated_text/finalResult.png ")
        os.system("rm pickled_results_pareto")
        os.system("cp pickled_results_all_points all_of_s2")
        os.system("cp pickled_results_pareto_of_all pareto_of_all_of_s2")
        print "done with the stage 2: apx of some files"
       

        # ---- starting stage 3(apx some files)
        print ""
        print ""
        print "---------starting stage 3"
        stage_number = 3 
        settings_obj = settingsClass(benchmark, root_folder, bench_suit_name, heuristic_intensity2)
        settings_obj.outputMode = "uniform"
        settings_obj.error_mode= "image"
        inputObj.set_lOfSetUps([accurateSetUp])
        inputObj.is_primary_input = False
        
        os.chdir("/home/polaris/behzad/behzad_local/" + root_folder + "/src/CSrc/")
        
        os.system("cp dct_acc.txt dct.cpp")
        os.system("cp quant_acc.txt quant.cpp")
        os.system("cp quant_apx.txt quant.cpp")

        os.chdir("/home/polaris/behzad/behzad_local/"+root_folder+"/src/python_files/")
        unique_point_list, lOfAllPointsTried, lOfPoints_out_of_heuristic, pointSet, input_Point_list, accurateSetUp = run_task_and_collect_points(settings_obj, inputObj)
        write_results(unique_point_list, lOfAllPointsTried, lOfPoints_out_of_heuristic, pointSet, input_Point_list, stage_number, inputObj, settings_obj)
        append_results(pointSet, settings_obj)
        
        os.system("rm ../../generated_text/finalResult.png ")
        os.system("rm pickled_results_pareto")
        os.system("cp pickled_results_all_points all_of_s3")
        os.system("cp pickled_results_pareto_of_all pareto_of_all_of_s3")
        print "done with the stage 3: apx of some files"

        # ---- starting stage 4(apx some files, using UTC)
        print "\n\n---------starting stage 4"
        stage_number = 4
        #unique_point_list, lOf_UTC_PF, pareto_frontier_of_lOfPoints_out_of_heuristic, lOfAllPointsTried, pareto_frontier_of_lOfAllPointsTried, pointSet, input_Point_list = read_results()
         
        settings_obj = settingsClass(benchmark, root_folder, bench_suit_name, heuristic_intensity2)
        settings_obj.outputMode = "uniform"
        settings_obj.error_mode= "image"
        inputObj.is_primary_input = False
        inputObj.set_lOfSetUps(reduce_ideal_setUp_list(map(lambda x: x.get_setUp(), lOfPoints_out_of_heuristic_2)))
        

        os.chdir("/home/polaris/behzad/behzad_local/" + root_folder + "/src/CSrc/")
        
        os.system("cp dct_acc.txt dct.cpp")
        os.system("cp quant_acc.txt quant.cpp")
        os.system("cp quant_apx.txt quant.cpp")

        os.chdir("/home/polaris/behzad/behzad_local/"+root_folder+"/src/python_files/")
        
        unique_point_list, lOfAllPointsTried, lOfPoints_out_of_heuristic, pointSet, input_Point_list, accurateSetUp = run_task_and_collect_points(settings_obj, inputObj)
        write_results(unique_point_list, lOfAllPointsTried, lOfPoints_out_of_heuristic, pointSet, input_Point_list, stage_number, inputObj, settings_obj)

        os.system("rm ../../generated_text/finalResult.png ")
        os.system("rm pickled_results_pareto")
        os.system("cp pickled_results_all_points all_of_s4")
        os.system("cp pickled_results_pareto_of_all pareto_of_all_of_s4")
        print "done with the stage 4: apx of some files"


        #---- starting stage 5(combine and compare)
        print "\n\n---------starting stage 5"
        stage_number = 5
        os.chdir("/home/polaris/behzad/behzad_local/" + root_folder + "/src/CSrc/")
        
        os.system("cp dct_apx.txt dct.cpp")
        os.system("cp quant_apx.txt quant.cpp")

        os.chdir("/home/polaris/behzad/behzad_local/" +root_folder+"/src/python_files/")
       
        run_combine_pareto(settings_obj)
        #python combine_paretos.py
        run_compare_pareto_curves(settings_obj)
        #python compare_pareto_curves.py >> compare_results.txt
        os.system("cp ../../generated_text/finalResult.png combine.png")
        print "done with stage 5:combining the paretos and comparing"



#if __name__ == "__main__":
#    main() 
#python send_email.py "ending_a_run" "done with test_benchmark"
