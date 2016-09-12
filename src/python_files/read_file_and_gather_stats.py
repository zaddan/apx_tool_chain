import os
import sys
import numpy
#---only works if all the lines have the same length
def get_columns(srcFileName):
    on_first_line = True 


    #--- make sure that all the lines are of the same length
    with  open(srcFileName, "r") as srcFilePtr:
        for line in srcFilePtr:
            words_in_line = line.rstrip().replace(',', ' ').replace('/',' ').replace(';', ' ').split(' ') 
            if not(on_first_line):
                if not(previous_line_length == len(words_in_line)):
                    print "number of words in different lines are different"
                    exit()
            on_first_line = False
            previous_line_length = len(words_in_line)


    #---generate a l_of_columns (of empty elements)
    l_of_columns = map(list, [[]]*previous_line_length)


    #----gather columns
    with  open(srcFileName, "r") as srcFilePtr:
        for line in srcFilePtr:
            counter = 0
            for words in line.rstrip().replace(',', ' ').replace('/',' ').replace(';', ' ').split(' '): 
                l_of_columns[counter].append(words) 
                counter +=1
        srcFilePtr.close()


    return l_of_columns

def gather_stats(input_list):
    result = [] 
    for el in input_list:
        el_mean = numpy.mean(map(lambda x: int(x), el), axis=0) 
        el_std = numpy.std(map(lambda x: int(x), el), axis=0) 
        result.append([el_mean,el_std])
    
    return result


input_list = get_columns("ok.txt")
print gather_stats(input_list)

