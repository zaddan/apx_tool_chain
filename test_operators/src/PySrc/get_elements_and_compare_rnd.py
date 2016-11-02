import itertools
c_results =[]
verilog_results = []
with  open("BT_RND.txt") as f:
    for line in f:
        verilog_results.append(line.split()) 

with  open("BT_RND_c.txt") as f:
    for line in f:
        c_results.append(line.split()) 

c_results_flattened = list(itertools.chain(*c_results))
verilog_results_flattened = list(itertools.chain(*verilog_results))
for index in range(len(verilog_results_flattened)):
    if not(verilog_results_flattened[index] == c_results_flattened[index]):
        print "------------" 
        print "%-20s %-10s" %("input1: ", verilog_results_flattened[index-2])
        print "%-20s %-10s" %("input2: ", verilog_results_flattened[index-1])
        
        print "%-20s %-10s" %("verilog_results: ", verilog_results_flattened[index])
        
        print "%-20s %-10s" %("c_results: ", c_results_flattened[index])
    
