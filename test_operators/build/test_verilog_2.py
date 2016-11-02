from termcolor import colored
import itertools
import struct
import sys
import os
import math
import binascii


#----------------------------------------------------
#---- parameters
#----------------------------------------------------
DEBUG = True#--- print 
NAB   = 10#--- num of appx bits, needs to be set according to NAB in
         #--- in the test_apx_float_* file
#-- addition or multiplication
#op    = "addition"
op = "mul"
#---- truncation or rounding
#mode  = "truncation"
mode = "rounding"
exp   = 10 #exp associated with the largest of the number used within the set
failed = 0 #how many time we fail to fall within meet the error boundary
counter =0 #number of tests run


#----------------------------------------------------
#--- variables
#----------------------------------------------------
verilog_results = []
l_diff = []

#----------------------------------------------------
#--- body
#----------------------------------------------------
if(mode == "truncation"):
    os.system("cp ~/behzad_local/verilog_files/apx_operators/float_ops_apx/TRUNCATION_acc_vs_apx.txt .")
    with  open("TRUNCATION_acc_vs_apx.txt") as f:
        for line in f:
            verilog_results.append(line.split()) 
if (mode == "rounding"):
    os.system("cp ~/behzad_local/verilog_files/apx_operators/float_ops_apx/BT_RND_acc_vs_apx.txt .")
    with  open("BT_RND_acc_vs_apx.txt") as f:
        for line in f:
            verilog_results.append(line.split()) 
verilog_results_flattened = list(itertools.chain(*verilog_results))


#----------------------------------------------------
#--- iterate and get error
#----------------------------------------------------
for index in range(len(verilog_results_flattened)/4):
    #--- read the file  
    acc_val_string = verilog_results_flattened[4*index + 2]
    apx_val_string = verilog_results_flattened[4*index + 3]
    in1 = verilog_results_flattened[4*index + 0]
    in2 = verilog_results_flattened[4*index + 1]
    in1_f = struct.unpack('!f', in1.decode('hex'))[0]
    in2_f = struct.unpack('!f', in2.decode('hex'))[0]
    acc_val_float = struct.unpack('!f', acc_val_string.decode('hex'))[0]
    apx_val_float = struct.unpack('!f', apx_val_string.decode('hex'))[0]
    
    #--- calc the suppression amounts, the amounts by which approximation
    #--- effects the mantisa
    smallest_unit =  pow(2, -23)
    if (mode == "truncation"):
        mantisa_suppression_add = (pow(2, NAB+1))
        mantisa_suppression_mul =  (pow(2, NAB+1))
        if (op == "addition") :
            largest_number = 2*pow(2, exp+1) 
            allowed_diff = pow(2, exp+1)   * mantisa_suppression_add *smallest_unit
        elif (op == "mul"):
            largest_number = pow(pow(2, exp+1),2)
            allowed_diff = (pow(2,2*exp+2))* mantisa_suppression_mul *smallest_unit
    elif (mode == "rounding"):
        mantisa_suppression_add = (pow(2, NAB)) #both can be added one
        mantisa_suppression_mul =  (pow(2, NAB))
        if (op == "addition") :
            largest_number = 2*pow(2, exp+1) 
            allowed_diff = pow(2, exp+1)* mantisa_suppression_add *smallest_unit
        elif (op == "mul"):
            largest_number = pow(pow(2, exp+1),2)
            allowed_diff = (pow(2,2*exp+2))* mantisa_suppression_mul *smallest_unit


    #--- set allowd_diff based on the operation (op) 
    diff =  abs(acc_val_float - apx_val_float)
    #---- print values  
    if(DEBUG): 
        if(diff > abs(allowed_diff)):
            print "---------------"
            print "allowed_diff:   " + str(allowed_diff) 
            print "actual_diff:    " + str(acc_val_float - apx_val_float) 
            print "in1:            " + str(in1)
            print "in2             " + str(in2)  
            print "actual value:   " + str(acc_val_string)
            print "truncated value:" + str(apx_val_string)
        assert(abs(acc_val_float - apx_val_float) < abs(allowed_diff))
    
    #--- calc failure rate 
    if(diff > abs(allowed_diff)):
        l_diff.append(diff) 
        failed +=1;
    counter +=1;


#--- output to the screen
print "%-20s %-10s" %("NAB", NAB)
print "%-20s %-10s" %("largest number", largest_number)
print "%-20s %-10s" %("allowed diff", allowed_diff)
print "%-20s %-10s" %("failed", failed)
print "%-20s %-10s" %("counter", counter)
print "%-20s %-10s" %("failure rate", str(float(failed)/float(counter)))
print "%-20s %-10s" %("list of difs", str(l_diff))
#print colored("test_passed", "green");
