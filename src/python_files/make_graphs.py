import pickle
import copy
import sys
import os
from plot_generation import *
from compare_pareto_curves import getPoints
import multiprocessing

import matplotlib
#matplotlib.use('Agg') 

import pylab
import matplotlib.pyplot as plt
#plt.ioff()
from inputs import *#this file contains all the inputs
from scipy.spatial import distance
from src_parse_and_apx_op_space_gen import *
from modify_operator_sample_file import *
#from sample_operand_and_sweep_apx_space import *
import settings 
from extract_result_properties import *
from plot_generation import *
import matplotlib.pyplot as plt
from find_position import *
from write_readable_output import *
from clean_up import *
from simulating_annealer import *
from misc import *
from misc2 import *
import datetime
from points_class import *
import pickle
from points_class import *
from list_all_files_in_a_folder import *
from src_parse_and_apx_op_space_gen import *
from pareto_set_class import *


def get_quality_energy_values_directly(src_file, symbol, lOfPoints, points_to_graph, limit=False, lower_bound=-100, upper_bound=100):
    #only change here
#    for el in lOfPoints:
#        el.set_input_number(0)

    lOfInput_number =  map(lambda x: x.get_input_number(), lOfPoints) #this is used for
                                                                      #only s4 and can be 
                                                                      #commented OW
    
    lOfQualityVals = map(lambda x: x.get_quality(), lOfPoints)
    lOfEnergyVals = map(lambda x: x.get_energy(), lOfPoints)
    if (limit):
        result = filter(lambda x: x[0] > lower_bound and x[0] <upper_bound, zip(lOfQualityVals, lOfEnergyVals))
        lOfQualityVals = map(lambda x: x[0], result)
        lOfEnergyVals = map(lambda x: x[1], result)
    
    
    #here
    points_to_graph.append([lOfQualityVals, lOfEnergyVals, lOfInput_number, src_file])
#    points_to_graph.append([lOfQualityVals, lOfEnergyVals, symbol, src_file])


def get_quality_energy_values(src_file, symbol, points_to_graph, limit=False, lower_bound=-100, upper_bound=100):
    lOfPoints = getPoints(src_file)
    get_quality_energy_values_directly(src_file, symbol, lOfPoints, points_to_graph, limit, lower_bound, upper_bound)

    #only reads the files and generate a graph. This module is for convenience of
#graphing the info that I need. simply comment the points that you don't want
#to be graphed
#**--------------------**
#**--------------------**
#--------------------**
def main():
    assert(len(sys.argv) >= 2) 
    limit = False
    lower_bound = -100
    upper_bound = .001
    points_to_graph = [] 
    for arg in sys.argv[1:]:
        if (arg == "hierarchical"):
            get_quality_energy_values("all_of_s2.PIK", "+", points_to_graph, limit, lower_bound, upper_bound)
            get_quality_energy_values("all_of_s3.PIK", "1", points_to_graph, limit, lower_bound, upper_bound)
            get_quality_energy_values("pareto_of_all_of_s3.PIK", "+", points_to_graph, limit, lower_bound, upper_bound)
            get_quality_energy_values("pareto_of_all_of_s2.PIK", "+", points_to_graph, limit, lower_bound, upper_bound)
            get_quality_energy_values("all_of_combined.PIK", "x", points_to_graph, limit, lower_bound, upper_bound)
            get_quality_energy_values("pareto_of_combined.PIK", "o", points_to_graph, limit, lower_bound, upper_bound)
        
        if (arg == "ref"): #---ref all
            get_quality_energy_values("pareto_of_heur_flattened.PIK", "^", points_to_graph, limit, lower_bound, upper_bound) 
            get_quality_energy_values("all_of_flattened.PIK", "+", points_to_graph, limit, lower_bound, upper_bound) 
            get_quality_energy_values("pareto_of_all_of_flattened.PIK", "+", points_to_graph, limit, lower_bound, upper_bound)
        
        if(arg == "only_pareto"):
            get_quality_energy_values("pareto_of_all_of_s3.PIK", "+", points_to_graph, limit, lower_bound, upper_bound)
            get_quality_energy_values("pareto_of_all_of_s2.PIK", "+", points_to_graph, limit, lower_bound, upper_bound)
            get_quality_energy_values("pareto_of_heur_flattened.PIK", "^", points_to_graph, limit,  lower_bound, upper_bound) 
            get_quality_energy_values("pareto_of_all_of_flattened.PIK", "^", points_to_graph, limit, lower_bound, upper_bound) 
        if(arg == "s4" or arg == "s6"):
            get_quality_energy_values("all_of_s4.PIK", "*", points_to_graph, limit, lower_bound, upper_bound) 
        
        if(arg == "compare_pareto"):
            get_quality_energy_values("pareto_of_all_of_flattened.PIK", "^", points_to_graph, limit, lower_bound, upper_bound) 
            get_quality_energy_values("pareto_of_all_of_s4.PIK", "*", points_to_graph, limit, lower_bound, upper_bound) 
            get_quality_energy_values("pareto_of_combined.PIK", "o", points_to_graph, limit, lower_bound, upper_bound)
        
        if(arg == "all"): #--all graph
            get_quality_energy_values("all_of_s2.PIK", "+", points_to_graph, limit, lower_bound, upper_bound)
            get_quality_energy_values("all_of_s3.PIK", "1", points_to_graph, limit, lower_bound, upper_bound)
            get_quality_energy_values("pareto_of_all_of_s3.PIK", "+", points_to_graph, limit, lower_bound, upper_bound)
            get_quality_energy_values("pareto_of_all_of_s2.PIK", "+", points_to_graph, limit, lower_bound, upper_bound)
            get_quality_energy_values("all_of_combined.PIK", "x", points_to_graph, limit, lower_bound, upper_bound)
            get_quality_energy_values("pareto_of_combined.PIK", "o", points_to_graph, limit, lower_bound, upper_bound)
            get_quality_energy_values("pareto_of_heur_flattened.PIK", "^", points_to_graph, limit,  lower_bound, upper_bound) 
            get_quality_energy_values("all_of_flattened.PIK", "+", points_to_graph, limit, lower_bound, upper_bound) 
            get_quality_energy_values("pareto_of_all_of_flattened.PIK", "^", points_to_graph, limit, lower_bound, upper_bound)
        
        if (arg == "main_two"): 
            get_quality_energy_values("pareto_of_combined.PIK", "o", points_to_graph, limit, lower_bound, upper_bound)
            get_quality_energy_values("pareto_of_heur_flattened.PIK", "^", points_to_graph, limit, lower_bound, upper_bound) 

        if (arg == "s2"): #---stage 2 points
            get_quality_energy_values("all_of_s2.PIK", "+", points_to_graph, limit, lower_bound, upper_bound)
            get_quality_energy_values("pareto_of_all_of_s2.PIK", "o", points_to_graph, limit, lower_bound, upper_bound)
        
        if (arg == "s3"): #---stage 3 points
            get_quality_energy_values("all_of_s3.PIK", "1", points_to_graph, limit, lower_bound, upper_bound)
            get_quality_energy_values("pareto_of_all_of_s3.PIK", "o", points_to_graph, limit, lower_bound, upper_bound)
        
        if (arg == "combined_all"): #combined_all 
            get_quality_energy_values("all_of_combined.PIK", "x", points_to_graph, limit, lower_bound, upper_bound)
        
        if (arg == "combined_pareto"): #combined_pareto
            get_quality_energy_values("pareto_of_combined.PIK", "o", points_to_graph, limit, lower_bound, upper_bound)
        
        if (arg == "ref_pareto"): #---pareto points for ref 
            get_quality_energy_values("pareto_of_heur_flattened.PIK", "^", points_to_graph, limit, lower_bound, upper_bound) 
            get_quality_energy_values("pareto_of_all_of_flattened.PIK", "+", points_to_graph, limit, lower_bound, upper_bound) 
        
        if (arg == "ref_all"): #---ref all
            get_quality_energy_values("all_of_flattened.PIK", "+", points_to_graph, limit, lower_bound, upper_bound) 
         
    generateGraph_for_all(points_to_graph, "1/quality", "energy", get_benchmark_name()) 
    pylab.savefig("results.png") #saving the figure generated by generateGraph
    
    if (arg == "s4" or arg=="s6"):
        points_to_graph = [] 
        get_quality_energy_values("input_for_s4.PIK", "+", points_to_graph, limit, lower_bound, upper_bound)
        generateGraph_for_all(points_to_graph, "1/quality", "energy", get_benchmark_name()) 
        pylab.savefig("s4_inputs.png") #saving the figure generated by generateGraph
    if (arg=="s6"):
        points_to_graph = [] 
        get_quality_energy_values("all_of_combined.PIK", "+", points_to_graph, limit, lower_bound, upper_bound)
        generateGraph_for_all(points_to_graph, "1/quality", "energy", get_benchmark_name()) 
        pylab.savefig("s6_combined.png") #saving the figure generated by generateGraph
    
    if (arg=="clusters"):
        points_to_graph = [] 
        get_quality_energy_values("s2_output_acc.PIK", "+", points_to_graph, limit, lower_bound, upper_bound)
        generateGraph_for_all(points_to_graph, "1/quality", "energy", get_benchmark_name()) 
        pylab.savefig("s2_output_acc.png") #saving the figure generated by generateGraph
        points_to_graph = [] 
        get_quality_energy_values("cluster_rep.PIK", "+", points_to_graph, limit, lower_bound, upper_bound)
        generateGraph_for_all(points_to_graph, "1/quality", "energy", get_benchmark_name()) 
        pylab.savefig("cluster_rep.png") #saving the figure generated by generateGraph

if __name__ == "__main__":
    main()
