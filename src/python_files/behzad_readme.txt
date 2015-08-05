##command line examples
python run_tool_chain.py ~/apx_tool_chain/src/CSrc/ ~/apx_tool_chain/src/CSrc/test.cpp  YES  ~/apx_tool_chain YES ~/apx_tool_chain/all_operands_scenarios.txt finalResult2.txt

python compare_results.py ~/apx_tool_chain/all_backups/backup_1/generated_text/finalResult2.txt ~/apx_tool_chain/all_backups/backup_0/generated_text/finalResult2.txt 0 4 0 4
