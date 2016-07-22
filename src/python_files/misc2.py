import os
def write_benchmark_name(name):
    with open("config.txt", "wb") as f:
        f.write(name)
        f.write(" ")

def write_root_folder_name(name):
    with open("config.txt", "a") as f:
        f.write(name)
        f.write(" ")
def write_bench_suit_name(name):
    with open("config.txt", "a") as f:
        f.write(name)
        f.write(" ")

def write_heuristic_intensity(intensity):
    with open("config.txt", "a") as f:
        f.write(intensity) 



def get_benchmark_name():
    sourceFileName = "config.txt" 
    try:
        f = open(sourceFileName)
    except IOError:
        exit()
    else:
        with f:
            for line in f:
                benchmark_name= line.rstrip().replace(',', ' ').replace('/',' ').replace(';', ' ').split(' ')
    return benchmark_name[0]

def get_root_folder_name():
    sourceFileName = "config.txt" 
    try:
        f = open(sourceFileName)
    except IOError:
        exit()
    else:
        with f:
            for line in f:
                root_folder= line.rstrip().replace(',', ' ').replace('/',' ').replace(';', ' ').split(' ')
    return root_folder[1]

def get_bench_suit_name():
    sourceFileName = "config.txt" 
    try:
        f = open(sourceFileName)
    except IOError:
        exit()
    else:
        with f:
            for line in f:
                root_folder= line.rstrip().replace(',', ' ').replace('/',' ').replace(';', ' ').split(' ')
    return root_folder[2]


def get_heuristic_intensity():
    sourceFileName = "config.txt" 
    try:
        f = open(sourceFileName)
    except IOError:
        exit()
    else:
        with f:
            for line in f:
                root_folder= line.rstrip().replace(',', ' ').replace('/',' ').replace(';', ' ').split(' ')
    return root_folder[3]


