Note: for now the executable name is pre set in the run_tool_chain.py to tool_exe for both run_tool_chain.py and run_unit_test.py. If we want to change this, we also have to change the CMakeLists.txt (add_executable tool_exe, and have CMake to get a command line arg and I dont know how)

to run the program, you only need to run run_tool_chain.py
to configure the program, you need to modify the setting.py

the energy of multipliers are considered to be 31 times the adder since they do 31 additions (besides addition, they do other things too, but this is a very simplistic versions)

Note: to learn how to run various files look at the command_line_example.txt located in the src/python_files/
