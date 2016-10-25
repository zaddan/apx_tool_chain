from reminder import *
import os
import pickle
import copy
import pylab
import sys
import random
import numpy as np
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans

from extract_pareto_set_from_raw_material import *
def get_imposing_setups(imposed_setUp_file):
    l_imposing_setUp = [] 
    l_promised_quality = []  
    all_points = getPoints(imposed_setUp_file)
    for el in all_points:
        l_imposing_setUp.append(el)
        l_promised_quality.append(el.get_quality())
    return l_imposing_setUp, l_promised_quality


def write_points(lOfPoints, file_addr):
    with open(file_addr, "wb") as f:
        for point in lOfPoints:
            pickle.dump(copy.deepcopy(point), f)

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
                        print "something went wrongsss"
                    break
                finally:
                    print "was insed the read_pickled_points"


def cluster_input(lOfPoints, settings_obj):
    clustered_input = [[] for i in range(settings_obj.n_clusters)]
    #[[]]*settings_obj.n_clusters
    data = [] 
    for el in lOfPoints:
        data.append([el.get_energy(), el.get_quality()])
    myKMeans = KMeans(k=settings_obj.n_clusters, init='k-means++', n_init=4, max_iter=300, tol=0.0001, precompute_distances='auto', verbose=0, random_state=None, copy_x=True, n_jobs=1)
    data_fitted = myKMeans.fit(data)
    labels = data_fitted.labels_
    
    #---creat a list of clusters with each element of the list containing all the points belonging to that cluster 
    for index,el in enumerate(lOfPoints):
        clustered_input[labels[index]].append(el)
    
    return clustered_input
def pick_rep_from_each_cluster(clustered_input):
    rep_list = [] 
    num = 0 
    
    for clstr in  clustered_input:
        print "---cluster:" + str(num) 
        for pt in clstr:
            print str(pt.get_quality())  + " " + str(pt.get_energy())
        num +=1 
    
    for cluster in clustered_input:
       rep_list.append(random.choice(cluster))

    return rep_list

#def reduce_ideal_setUp_list(previous_ideal_setUp_list, previous_ideal_setUp_output_list):
def reduce_ideal_setUp_list(previous_ideal_setUp_list, settings_obj):
    #return previous_ideal_setUp_list[:len(previous_ideal_setUp_list)/2]
    print "length is of previous_ideal_setUp_list: " + str(previous_ideal_setUp_list)
    result = [] 
    
    mode = "random"
    if (mode == "random"):
        for x in  range(0, settings_obj.num_of_cluster):
            result += [random.choice(previous_ideal_setUp_list)]
    elif(mode == "range"):
        result = previous_ideal_setUp_list[:settings_obj.num_of_cluster]
    else:
        print "this mode is not defined for reduction"
        exit()
    return result



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
                break
    return benchmark_name[1]

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

def is_accurate_design(lOfSetUps):
    for el in lOfSetUps:
        if not(el == 0):
            return False
    print "it is accurate" + str(lOfSetUps )
    return True


def normalized_quality(lOfQualityVals, lOfInput_number, lOfAccurate_PSNR) :
    lOfQualityVals_normalized = []
    for index,input_num in enumerate(lOfInput_number):
        lOfQualityVals_normalized.append(lOfQualityVals[index]/lOfAccurate_PSNR[input_num])
    return lOfQualityVals_normalized

def get_quality_energy_values_directly(src_file, symbol, lOfPoints, points_to_graph, limit=False, lower_bound=-100, upper_bound=100):
 
     
    reminder(True,"the following needs to be uncommented if we want to show s6 results")
    #only change here
#    for el in lOfPoints:
#        el.set_input_number(0)

    lOfInput_number =  map(lambda x: x.get_input_number(), lOfPoints) #this is used for
                                                                      #only s4 and can be 
                                                                      #commented OW
    
    lOfQualityVals = map(lambda x: x.get_quality(), lOfPoints)
    lOfEnergyVals = map(lambda x: x.get_energy(), lOfPoints)
    lOfSetUps = map(lambda x: x.get_raw_setUp(), lOfPoints)
    if (limit):
        result = filter(lambda x: x[0] > lower_bound and x[0] <upper_bound, zip(lOfQualityVals, lOfEnergyVals))
        lOfQualityVals = map(lambda x: x[0], result)
        lOfEnergyVals = map(lambda x: x[1], result)
    
    
    
    reminder(True, "The normalization shouldn't been done for other quality metrics that already consider the accurate desing in their quality calculations")
    reminder(True, "normalization needs to be done automatically");
    reminder(True, "normalization of energy also needs to be automated") 
    print "before normialization" + str(lOfQualityVals) 
    #lOfAccurate_PSNR = [41.14, 39.67, 43.35, 40.34, 39.67, 41.14, 43.35]
    lOfAccurate_PSNR = [1,1, 1,1,1,1,1]
    lOfQualityVals_normalized = normalized_quality(lOfQualityVals, lOfInput_number,lOfAccurate_PSNR) 
    accurate_design_energy  = 516918
    lOfEnergyVals_normalized = map(lambda x: float(x)/float(accurate_design_energy), lOfEnergyVals)
    lOfQualityVals = lOfQualityVals_normalized 
    lOfEnergyVals= lOfEnergyVals_normalized
    
    #here
    points_to_graph.append([lOfQualityVals, lOfEnergyVals, lOfInput_number, lOfSetUps, src_file])

     
    pts = points_to_graph[0] #am not using scenario where points_to_graph is more than oneelement deep 
    
    
    """ 
    l_accurate_design_PSNR = []
    for index,_ in enumerate(pts[0]):
        lOfSetUps =  pts[3][index]
        if is_accurate_design(lOfSetUps):
            l_accurate_design_PSNR.append(lOfQualityVals[index])

    print l_accurate_design_PSNR  
    sys.exit()
    """  

#    points_to_graph.append([lOfQualityVals, lOfEnergyVals, symbol, src_file])
def getPoints(file1_name):     
    lOfPoints =[]
    with open(file1_name, "rb") as f:
        # pickle.load(f)
        while True: 
            try: 
                point = pickle.load(f)
                lOfPoints.append(point) 
                # listOfPeople.append(copy.copy(person))# 
            except Exception as ex:
                if not (type(ex).__name__ == "EOFError"):
                    print type(ex).__name__ 
                    print ex.args
                    print "something went wrongss"
                break



    return lOfPoints




def get_quality_energy_values(src_file, symbol, points_to_graph, limit=False, lower_bound=-100, upper_bound=100):
    lOfPoints = getPoints(src_file)
    get_quality_energy_values_directly(src_file, symbol, lOfPoints, points_to_graph, limit, lower_bound, upper_bound)


