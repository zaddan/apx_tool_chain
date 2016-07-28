##command line examples
./test_bench_mark jpeg apx_tool_chain my_micro_benchmark
#=============================
#Notes:
#=============================
assert(not(error_mode == "image") or not(test_error)) #can not have error_mode be image
                                                      #and test_error being true
for now, make sure that the src file does not return 0, (because that's what I am using for error)
keep in mind that we should be really only using the upperBound values or low
ones. depending on whether the operator values will increase if the number of
apx bits increase.


worse_case_scenrio elements are set to 1 for sift since we get a segfault
for this scenario (b/c the author of the c file didn't consider a corner case),
hence if the run falls in this corner case (where frames are never defined), we set a flag
that alarms the script_sift to allocate and populate the frames variable (with infinity 
and 1(as the last element). This way, the quality calculated is infinity
for other cases (besides the worse_case_scenario config), we adopt the same strategy
to avoid the segfault. By setting the quality to infinity (thes set up is not selected in the
hueristic searchs)




This design only considers the bit truncation. In the case of other apx
techniques, the way we calculate operandInfoApxBitsLowerBoundDic which gets
it's vvalues from lowerBounderyDic needs to change.
#=============================
TODO:
#=============================
include other heuristic search:
    flatten: 
        try other deap search (with run_tool)
            if want to try ES, we need to change the individual so that it is a list of numbers,
                so the mutation can take place
        
        make some search
        accodomate the possibility of having different runs run with different search
    partial:
        try other deap search (with run_tool
        make some search

quantification of the difference b/w two flatten and partial methods

include the pareto front of the lOfAllTriedPoints


figure out the right power model



The way that I calculate PSNR is to first use the 0 apx bit to generate an image (we know
that this image is still noisy, since our operators can not deal with floating or fix points(I need to include the logic for this purpose), then I modify the operators and get PSNR)

#=============================
how/where to set up the parameters
#=============================
parameters are set up in two different part:
    settings.py
    passed as cmd to test_benchmark (note that if we want to run_too_chain.py
                                     we need to set config.txt manually)

all_inputs_scenarios need to be set properly according to the benchmark of intereset.
    if sd-vbs benchmarks used, no need to worry about this file (all_inputs_scenarios)

===========
how to run properly
============
to run the entire flow:
    ./test_bench_mark $(benchmark_name) $(root_folder) $(bench_suit_name) $(heuristic_intenity1) $(heuristic_intenity2)

to run just run_tool_chain.py (to generates the result for only one task assignment)
    1.populuate config.txt with proper values
    2.python run_tool_chain.py 
    

Notes:
the lOfCSrcFileAddress list needs to be filled the same order that the myOps are ordered

----
some files format
----
config.txt format:
benchmark_name root_Folder_name bench_suit_name

all_input for jpeg:
    ~/apx_b/inputPics/roki_320_240.ppm ~/apx_b/inputPics/roki_noisy.jpg 320 240 0 10 
