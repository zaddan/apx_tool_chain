##command line examples
python run_tool_chain.py ~/apx_tool_chain/src/CSrc/ ~/apx_tool_chain/src/CSrc/test.cpp  YES  ~/apx_tool_chain YES ~/apx_tool_chain/all_operands_scenarios.txt finalResult2.txt

python compare_results.py ~/apx_tool_chain/all_backups/backup_1/generated_text/finalResult2.txt ~/apx_tool_chain/all_backups/backup_0/generated_text/finalResult2.txt 0 4 0 4

#Notes:
for now, make sure that the src file does not return 0, (because that's what I am using for error)
#things to do 
at this time, if the number of input variables not the same as the ones provided in the operand, it does not error out


later, have the stepSize and initilTemperature as an inupt to the run_tool_chain

have the input of run_tool_chain to come from a file (instead of command line)
