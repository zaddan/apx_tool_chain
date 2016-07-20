
import os
def write_benchmark_name(name):
    with open("benchmark_name.txt", "wb") as f:
        f.write(name)
 
def get_benchmark_name():
    sourceFileName = "benchmark_name.txt" 
    try:
        f = open(sourceFileName)
    except IOError:
        exit()
    else:
        with f:
            for line in f:
                benchmark_name= line.rstrip().replace(',', ' ').replace('/',' ').replace(';', ' ').split(' ')
    return benchmark_name[0]


