from termcolor import colored
import itertools
import struct
import sys
import os
import math
import binascii

NAB = 12 
op = "addition"
#op = "mul"
mode = "truncation"
#mode = "rounding"

verilog_results = []
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
diff = []
for index in range(len(verilog_results_flattened)/2):
    #bigger_input_string = verilog_results_flattened[2*index]
    acc_val_string = verilog_results_flattened[2*index + 0]
    apx_val_string = verilog_results_flattened[2*index + 1]
    
    """ 
    print abs(int(acc_val_string, 16) - int(apx_val_string, 16))
    print 2*(pow(2, NAB) - 1)
    """ 
    
    print "line" + str(index) + ":" + hex(abs(int(acc_val_string, 16) - int(apx_val_string, 16)))
    """ 
    if mode == "truncation": 
        if (op == "addition"): 
            print hex(2*(pow(2, NAB) - 1))
            assert(abs(int(acc_val_string, 16) - int(apx_val_string, 16)) <= 2*(pow(2, NAB)-1))
        elif (op == "mul"):
            print hex((pow(2, NAB) - 1)*(pow(2, NAB) - 1))
            assert(abs(int(acc_val_string, 16) - int(apx_val_string, 16)) <= (pow(2, NAB)-1)*(pow(2, NAB)-1))
    elif mode == "rounding":
        if (op == "addition"): 
            print hex(2*(pow(2, NAB) - 2))
            assert(abs(int(acc_val_string, 16) - int(apx_val_string, 16)) <= 2*(pow(2, NAB)-2))
        elif (op == "mul"):
            print hex(pow((pow(2, NAB) - 2),2))
            assert(abs(int(acc_val_string, 16) - int(apx_val_string, 16)) <= ((pow(2, NAB)-2) * (pow(2, NAB)-2)))

print colored("test passed", 'green');
    """
    acc_val_float = struct.unpack('!f', acc_val_string.decode('hex'))[0]
    apx_val_float = struct.unpack('!f', apx_val_string.decode('hex'))[0]
    """ 
    bigger_input_float = struct.unpack('!f', bigger_input_string.decode('hex'))[0]
    bigger_input_binary = binascii.unhexlify(bigger_input_string) 

    bigger_input_binary_string= (bin(int(bigger_input_string, 16))[2:]).zfill(32)

    #print bigger_input_binary_string 
    exp_string = ''.join(list(bigger_input_binary_string)[1:9])
    exp  = int(exp_string, 2) - 127
    """
    
    
    #this needs to be set manually according to the input values
    #our inputs have the same exponent, this is b/c I am not sure how to
    #model the error if they have different exp values (this is due to the mantisa
    #shifting that occurs
    exp = 20
    #--value taken away from an operand
    #--note that there in one of the cases, due to rounding we add one to mantisa,
    #need to account for that hence:
    suppression_amount_add =  ((pow(2, NAB)+1)*pow(2, -23)) #number of apx bits,
    #it is technically num of apx bits - 1, but there are scenarios that am gets 
    #incremented for rounding
    suppression_amount_mul =  ((pow(2, NAB)+1)*pow(2, -23)) #twice
    #as many bits. think of the following scenario
    #0xfff * 0xfff (where 4 bits trucated) => that can reach to 8 bits
    if (op == "addition") :
        allowed_diff = pow(2, exp+1)*(suppression_amount_add)
    elif (op == "mul"):
        allowed_diff = pow(2, 2*(exp)+1)*(suppression_amount_mul)
    
    #print "bigger number" + str(bigger_input_float )
    print "allowed_diff " + str(allowed_diff) 
    print "actual_diff" + str(acc_val_float - apx_val_float) 
    print "acc_val_float" + str(acc_val_float) 
    
    print "actual value" + str(acc_val_string)
    print "truncated value" + str(apx_val_string)
    print "sample number:" + str(index)
    print "---------------"
    #print "bigger number" + str(bigger_input_float) 
    assert(acc_val_float - apx_val_float <= allowed_diff)
