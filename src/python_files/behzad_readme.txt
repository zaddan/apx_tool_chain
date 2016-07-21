##command line examples
./test_bench_mark jpeg apx_tool_chain my_micro_benchmark

#Notes:
for now, make sure that the src file does not return 0, (because that's what I am using for error)
keep in mind that we should be really only using the upperBound values or low
ones. depending on whether the operator values will increase if the number of
apx bits increase.
This design only considers the bit truncation. In the case of other apx
techniques, the way we calculate operandInfoApxBitsLowerBoundDic which gets
it's vvalues from lowerBounderyDic needs to change.

TODO:
figure out the right power model
later, have the stepSize and initilTemperature as an inupt to the run_tool_chain
have the input of run_tool_chain to come from a file (instead of command line)

The way that I calculate PSNR is to first use the 0 apx bit to generate an image (we know
that this image is still noisy, since our operators can not deal with floating or fix points(I need to include the logic for this purpose), then I modify the operators and get PSNR)

===========
how to run properly
============
to run the entire flow:
    ./test_bench_mark $(benchmark_name) $(root_folder) $(bench_suit_name)

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
