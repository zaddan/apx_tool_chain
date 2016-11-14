import pickle
import copy
import sys
import os
from plot_generation import *
from compare_pareto_curves import getPoints
import multiprocessing
from reminder import *

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
        if (arg == "various_inputs"):
#            points_to_graph = [] 
#            get_quality_energy_values("various_inputs.PIK", "+", points_to_graph, limit, lower_bound, upper_bound)
#            generateGraph_for_all(points_to_graph, "1/quality", "energy", get_benchmark_name(), "optimal setUp for various prime inputs for ", "various_inputs") 
            """ 
            points_to_graph = [] 
            
            get_quality_energy_values("various_inputs_same_setUp.PIK", "+", points_to_graph, limit, lower_bound, upper_bound)
            generateGraph_for_all(points_to_graph, "1/quality", "energy", get_benchmark_name(), "One input optimal setUp imposed on others for ", "various_inputs_same_setUp") 
            #pylab.savefig("various_inputs_same_setUp.png") #saving the figure generated by generateGraph
            points_to_graph = [] 
            get_quality_energy_values("pickled_results_all_points.PIK", "+", points_to_graph, limit, lower_bound, upper_bound)
            generateGraph_for_all(points_to_graph, "1/quality", "energy", get_benchmark_name(), "all input", "all_points_tried") 
            #pylab.savefig("all_points_tried.png") #saving the figure generated by generateGraph
            exit()
            """

        #--- all results 
        
        get_quality_energy_values("pickled_results_all_points.PIK", "+", points_to_graph, limit, lower_bound, upper_bound)
        generateGraph_for_all_simplified(points_to_graph, "1/quality", "energy", get_benchmark_name(), "","", "E_vs_Q_all_points", "E_vs_Q") 
        #--- various inputs 
        points_to_graph = [] 
        points_to_graph_2 = [] 
        get_quality_energy_values("various_inputs.PIK", "+", points_to_graph, limit, lower_bound, upper_bound)
        generateGraph_for_all_simplified(points_to_graph, "1/quality", "energy", get_benchmark_name(), "", "", "same_Q_vs_input", "same_Q_vs_input") 
        generateGraph_for_all_simplified(points_to_graph, "1/quality", "energy", get_benchmark_name(), "", "", "E_vs_Q", "E_vs_Q") 
        
        #--- imposed on various inputs
        points_to_graph = [] 
        get_quality_energy_values("various_inputs_same_setUp.PIK", "+", points_to_graph, limit, lower_bound, upper_bound)
        
        generateGraph_for_all_simplified(points_to_graph, "1/quality", "energy", get_benchmark_name(), "", "" , "E_vs_Q_imposed", "E_vs_Q") 
        generateGraph_for_all_simplified(points_to_graph, "1/quality", "energy", get_benchmark_name(), "", "", "Q_vs_mean_imposed", "same_E_vs_input") 
        generateGraph_for_all_simplified(points_to_graph, "1/quality", "energy", get_benchmark_name(), "", "" , "Qstd_vs_E_imposed", "Qstd_vs_E_imposed") 

        reminder(True, "make sure to creat a file with universal name that holds the imposed values so we  can sample", "URGENT") 
        points_to_graph_3 =[] 
        
        #get_quality_energy_values("various_inputs_avg_setUp.PIK", "+", points_to_graph_3, limit, lower_bound, upper_bound)
        get_quality_energy_values("imposed_setUp.PIK", "+", points_to_graph_3, limit, lower_bound, upper_bound)
        print points_to_graph_3
        #get_quality_energy_values("various_inputs_worse_case_setUp.PIK", "+", points_to_graph_3, limit, lower_bound, upper_bound)
        generateGraph_for_all_simplified(points_to_graph, "1/quality", "energy", get_benchmark_name(), "", "" , "Qmean_normalized_to_Q_promissed", "Qmean_normalized_to_Q_promissed", False, False, "one", points_to_graph_3) 
        generateGraph_for_all_simplified(points_to_graph, "1/quality", "energy", get_benchmark_name(), "", "" , "Q_satisfaction_success_rate", "Q_satisfaction_success_rate", False, False, "one", points_to_graph_3) 
        #--- various inputs imposed vs regular 
        points_to_graph = [] 
        get_quality_energy_values("various_inputs_same_setUp.PIK", "+", points_to_graph, limit, lower_bound, upper_bound)
        ax, fig = generateGraph_for_all_simplified(points_to_graph, "1/quality", "energy", get_benchmark_name(), "", "", "E_vs_Q_imposed_vs_optimal", "E_vs_Q", True) #-- post pone saving
        
        points_to_graph = [] 
        get_quality_energy_values("various_inputs.PIK", "+", points_to_graph, limit, lower_bound, upper_bound)
        generateGraph_for_all_simplified(points_to_graph, "1/quality", "energy", get_benchmark_name(), ax, fig, "E_vs_Q_impose_vs_optimal", "E_vs_Q", False, True) 

        
        #--- various inputs E vs Q adjusted
        points_to_graph = [] 
        get_quality_energy_values("various_inputs.PIK", "+", points_to_graph, limit, lower_bound, upper_bound)
        ax,fig =generateGraph_for_all_simplified(points_to_graph, "1/quality", "energy", get_benchmark_name(), "", "", "E_vs_Q_adjusted", "E_vs_Q_adjusted")
        
        
        #--- (E vs Q adjusted) and vs (E vs Q adjusted imposed)
        points_to_graph = [] 
        get_quality_energy_values("various_inputs_same_setUp.PIK", "+", points_to_graph, limit, lower_bound, upper_bound)
        ax,fig =generateGraph_for_all_simplified(points_to_graph, "1/quality", "energy", get_benchmark_name(), "", "", "E_vs_Q_adjusted_vs_imposed", "E_vs_Q_adjusted", True)
        points_to_graph = [] 
        get_quality_energy_values("various_inputs.PIK", "+", points_to_graph, limit, lower_bound, upper_bound)
        fig = generateGraph_for_all_simplified(points_to_graph, "1/quality", "energy", get_benchmark_name(), ax, fig, "E_vs_Q_adjusted_vs_imposed", "E_vs_Q_adjusted", False, True) #-- post pone saving
        

        sys.exit()
        if (arg == "various_inputs_alter"):
            for index in range(6): 
                generateGraph_for_all_alternative(points_to_graph, points_to_graph_2, "1/quality", "energy", get_benchmark_name(), index, "One input optimal setUp imposed on others for ") 
                pylab.savefig("cmp_ideal_vs_imposed_for_input"+str(index)+".png") #saving the figure generated by generateGraph
            """ 
            points_to_graph = [] 
            get_quality_energy_values("pickled_results_all_points.PIK", "+", points_to_graph, limit, lower_bound, upper_bound)
            generateGraph_for_all(points_to_graph, "1/quality", "energy", get_benchmark_name()) 
            pylab.savefig("all_points_tried.png") #saving the figure generated by generateGraph
            """ 
            exit()
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
