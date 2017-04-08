import sys
import os
def parse_and_compare(src_addr):
    os.system("cp /home/polaris/behzad/behzad_local/verilog_files/apx_operators/int_ops_apx/build/functional/results.txt TRUNCATION.txt")
    # *** F:DN Parameters 
    operator = "mul"
    
    #*** F:DN Variables 
    #src__f__handle = open(src_addr, "r")

    # *** F:DN Body
    try:
        f = open(src_addr)
    except IOError:
        print "src_file" +src_addr+ "not found"
#        handleIOError(timing_per_cell__log__addr, "csource file")
        sys.exit()
    else:
        with f:
            for line in f:
                word_list =   line.strip().replace(',', ' ').replace(';', ' ').split(' ') 
                
                word_list = filter(lambda x: not(x==''), word_list) 
                input__1 = long(word_list[0])
                input__2 = long(word_list[1])
                if (operator == "mul"): 
                    if not(input__2 * input__1) == long(word_list[2]):
                        print "input__1:" + str(input__1)
                        print "input__2:" + str(input__2)
                        print "python result:" + str(input__2*input__1) 
                        print "verilog results:" + str(long(word_list[2]))
                        print "not all values are equal"
                        sys.exit()
                if (operator == "add"): 
                    if not(input__2 + input__1) == long(word_list[2]):
                        print "input__1:" + str(input__1)
                        print "input__2:" + str(input__2)
                        print "python result:" + str(input__2+input__1) 
                        print "verilog results:" + str(long(word_list[2]))
                        print "not all values are equal"
                        sys.exit()


    print "done with no errors for operator:" + str(operator) 
    print "*** F:AN note that this python module only works with accurate\
    multipliaction and addition. You also need to set the parameter inside"
parse_and_compare("TRUNCATION.txt")


