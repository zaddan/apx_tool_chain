import os
import pickle
import copy
import pylab
import sys
from extract_pareto_set_from_raw_material import *

def write_results(unique_point_list, lOfAllPointsTried,lOfPoints_out_of_heuristic, pointSet, input_Point_list, stage_number,
        inputObj, settings_obj):
        with open(inputObj.PIK_pareto, "wb") as f:
            pareto_frontier_of_lOfPoints_out_of_heuristic = pareto_frontier(lOfPoints_out_of_heuristic, settings_obj.maxX, settings_obj.maxY, settings_obj)
            points_to_dump = pareto_frontier_of_lOfPoints_out_of_heuristic
            for point in points_to_dump:
                pickle.dump(copy.deepcopy(point), f)
        with open(inputObj.PIK_all_points, "wb") as f:
            points_to_dump = lOfAllPointsTried
            for point in points_to_dump:
                pickle.dump(copy.deepcopy(point), f)
        with open(inputObj.PIK_pareto_of_all, "wb") as f:
            pareto_frontier_of_lOfAllPointsTried = pareto_frontier(lOfAllPointsTried, settings_obj.maxX, settings_obj.maxY, settings_obj)
            points_to_dump = pareto_frontier_of_lOfAllPointsTried 
            for point in points_to_dump:
                pickle.dump(copy.deepcopy(point), f)

        with open(inputObj.input_for_s4_file, "w") as f:
            for el in input_Point_list:
                pickle.dump(el, f)   

def append_results(pointSet, settings_obj):
        with open(settings_obj.lOfParetoSetFileName, "a") as f:
            pickle.dump(copy.deepcopy(pointSet), f)



def read_pickled_points(file_addr):
    with open(file_addr, "rb") as f:
            while True: 
                try: 
                    point = pickle.load(f)
                    ideal_pts.append(point) 
                    # listOfPeople.append(copy.copy(person))# 
                except Exception as ex:
                    if not (type(ex).__name__ == "EOFError"):
                        print type(ex).__name__ 
                        print ex.args
                        print "something went wrong"
                    break


#def reduce_ideal_setUp_list(previous_ideal_setUp_list, previous_ideal_setUp_output_list):
def reduce_ideal_setUp_list(previous_ideal_setUp_list):
    #return previous_ideal_setUp_list[:len(previous_ideal_setUp_list)/2]
    print "length is of previous_ideal_setUp_list: " + str(previous_ideal_setUp_list)
    return previous_ideal_setUp_list[:4]



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


