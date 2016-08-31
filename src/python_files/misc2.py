import os
#def reduce_ideal_setUp_list(previous_ideal_setUp_list, previous_ideal_setUp_output_list):
def reduce_ideal_setUp_list(previous_ideal_setUp_list):
    #return previous_ideal_setUp_list[:len(previous_ideal_setUp_list)/2]
    print "length is of previous_ideal_setUp_list: " + str(previous_ideal_setUp_list)
    return previous_ideal_setUp_list[:1]



def update_unique(point, output_list, unique_point_list):
    exist = True
    try:
        index_value = output_list.index(point.get_raw_values())
    except Exception as ex:
        if (type(ex).__name__ == "ValueError"):
            exist = False
        elif not(type(ex).__name__ == "ValueError"):
            print "there shouldn't be other kind of errors for update_unique"  
            exit()
        
#    print "before" 
#    print point.get_raw_values() 
#    print "after"

    if not(exist):
        output_list.append(point.get_raw_values())
        unique_point_list.append(point)
    else:
        print "no addition to unique points"
        if (point.get_energy() < unique_point_list[index_value].get_energy()):
            unique_point_list[index_value] = point
                



def clean_doubles(lOfpoints):
    result = [] 
    for el in lOfpoints:
        add = True 
        for el2 in result:
            if el.get_energy() == el2.get_energy() and el.get_quality() == el2.get_quality():
                add = False
                break
        if (add):
            result.append(el)
    return result

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

def write_get_UTC(UTC):
    with open("config.txt", "a") as f:
        f.write(UTC)
        f.write(" ")

def write_write_UTC(w_UTC):
    with open("config.txt", "a") as f:
        f.write(w_UTC)
        f.write(" ")

def write_adjust_NGEN(NGEN):
    with open("config.txt", "a") as f:
        f.write(NGEN)
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

def get_UTC_or_no():
    sourceFileName = "config.txt" 
    try:
        f = open(sourceFileName)
    except IOError:
        exit()
    else:
        with f:
            for line in f:
                UTC = line.rstrip().replace(',', ' ').replace('/',' ').replace(';', ' ').split(' ')
    if(UTC[3] == "True"):
        return True
    elif(UTC[3] == "False"):
        return False
    else:
        print "***ERRR this get_UTC value is not acceptable"
        exit()

def get_write_UTC_or_no():
    sourceFileName = "config.txt" 
    try:
        f = open(sourceFileName)
    except IOError:
        exit()
    else:
        with f:
            for line in f:
                UTC = line.rstrip().replace(',', ' ').replace('/',' ').replace(';', ' ').split(' ')
    if(UTC[4] == "True"):
        return True
    elif(UTC[4] == "False"):
        return False
    else:
        print "***ERRR this write_UTC value is not acceptable"
        exit()

def get_adjust_NGEN_or_no():
    sourceFileName = "config.txt" 
    try:
        f = open(sourceFileName)
    except IOError:
        exit()
    else:
        with f:
            for line in f:
                UTC = line.rstrip().replace(',', ' ').replace('/',' ').replace(';', ' ').split(' ')
    if(UTC[5] == "True"):
        return True
    elif(UTC[5] == "False"):
        return False
    else:
        print "***ERRR this adjust_UTC value is not acceptable"
        exit()


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
    return root_folder[6]


