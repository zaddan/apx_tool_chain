##command line examples

*********
*********
python run_tool_chain.py ~/apx_tool_chain/src/CSrc/ ~/apx_tool_chain/src/CSrc/test.cpp  YES  ~/apx_tool_chain YES ~/apx_tool_chain/all_operands_scenarios.txt finalResult2.txt
*********
*********

*********
*********
python compare_results.py ~/apx_tool_chain/all_backups/backup_1/generated_text/finalResult2.txt ~/apx_tool_chain/all_backups/backup_0/generated_text/finalResult2.txt 0 4 0 4
*********
*********


#Notes:
for now, make sure that the src file does not return 0, (because that's what I am using for error)
keep in mind that we should be really only using the upperBound values or low
ones. depending on whether the operator values will increase if the number of
apx bits increase.
This design only considers the bit truncation. In the case of other apx
techniques, the way we calculate operandInfoApxBitsLowerBoundDic which gets
it's vvalues from lowerBounderyDic needs to change.

#things to do 
at this time, if the number of input variables not the same as the ones provided in the operand, it does not error out

noiseRequirement is set up to be a percentage of the accurate values



TODO:
figure out the right power model
later, have the stepSize and initilTemperature as an inupt to the run_tool_chain
have the input of run_tool_chain to come from a file (instead of command line)

in the annealer, introduce a tabu list(which indicates which nodes where visited)
and avoid revisiting those nodes again
The way that I calculate PSNR is to first use the 0 apx bit to generate an image (we know
that this image is still noisy, since our operators can not deal with floating or fix points(I need to include the logic for this purpose), then I modify the operators and get PSNR)

I dont think non dominant sorting is working properly
I had to add dealingWithPic Attribute to the points, because if we are dealing with pictures, instead of calculating the SNR at the output level using python, we internally do it in the C function,
thus the output value read from the output file is actually SNR (as opposed to the output value of the DFG). later on try to merge the two. 


compare_two_pareto_fronts function is only valid if we max x and min y (change later)
