from math import *
from reminder import *
import pylab
import os
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import sys
import matplotlib.pyplot as plt
import settings
from list_all_files_in_a_folder import *
import numpy
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D




import copy
import pylab
import operator
import input_list
import sys
import os
from plot_generation import *
import matplotlib.pyplot as plt
import run_task
import misc
import adjust
from scipy.spatial import distance
from src_parse_and_apx_op_space_gen import *
from modify_operator_sample_file import *
#from sample_operand_and_sweep_apx_space import *
from settings import *
from extract_result_properties import *
from plot_generation import *
import matplotlib.pyplot as plt
from find_position import *
from write_readable_output import *
from clean_up import *
from simulating_annealer import *
from misc import *
import datetime
from points_class import *
import pickle
from points_class import *
from reminder import *

def nearest_neighbors_2d(x, y) :
    #x, y = map(np.asarray, (x, y))
    #y = y.copy()
    y_idx = range(len(y))
    nearest_neighbor = np.empty((len(x),), dtype=np.intp)
    for j, xj in enumerate(x) :
        #idx = np.argmin(map(lambda xtemp, ytemp : np.linalg.norm(ytemp, xtemp), y , xj))
        dist = map(lambda ytemp: find_distance(xj, ytemp), y )
        idx = np.argmin(np.asarray(dist))
        nearest_neighbor[j] = y_idx[idx]

    return nearest_neighbor


def find_distance(x,y):
    return math.sqrt(((float(x[0]) - float(y[0]))**2 + (float(x[1]) - float(y[1]))**2))

def calc_distance_for_nearest_neighbors_2d(ref_values, tobe_compared_values):
    error = [] 
    #---turn the lists into dictionaries 
    if len(ref_values) < len(tobe_compared_values):
        ref1 = ref_values 
        ref2 = tobe_compared_values 
    else:
        ref2 = ref_values 
        ref1 = tobe_compared_values 

    #get the list of indecies of nearest neighbors
    indecies = nearest_neighbors_2d(ref2[:], ref1[:])
    #calculate error 
    for i in range(len(indecies)):
        error.append(find_distance(ref2[i], ref1[indecies[i]]))
    return error



#**--------------------**
#**--------------------**
#----disclaimers::: aMemberB needs to generalized for all type of optimizations
#**--------------------**




#--------------------**

def aMemberOfBStar(a, BPertoFront, radius1, radius2, maxX, maxY):
    if(not(maxX) and not(maxY)):
        for index1,element in enumerate(BPertoFront):
            if ((a[0] >= element[0] + radius1) 
                    and (a[1] >= element[1] + radius2)):
                return True
            if ((a[0] >= element[0]+ radius1) 
                    and (a[1] >= element[1] - radius2)):
                return True

            if ((a[0] >= element[0] - radius1) 
                    and (a[1] >= element[1] + radius2)):
                return True

            if ((a[0] >= element[0] - radius1) 
                    and (a[1] >= element[1] - radius2)):
                return True

    if(not(maxX) and maxY):
        for index1,element in enumerate(BPertoFront):
            if ((a[0] >= element[0]+ radius1) 
                    and (a[1] <= element[1] + radius2)):
                return True
            if ((a[0] >= element[0]+ radius1) 
                    and (a[1] <= element[1] - radius2)):
                return True

            if ((a[0] >= element[0] - radius1) 
                    and (a[1] <= element[1] + radius2)):
                return True

            if ((a[0] >= element[0] - radius1) 
                    and (a[1] <= element[1] - radius2)):
                return True
        
    if(maxX and not(maxY)):
        for index1,element in enumerate(BPertoFront):
            if ((a[0] <= element[0]+ radius1) 
                    and (a[1] >= element[1] + radius2)):
                return True
            if ((a[0] <= element[0]+ radius1) 
                    and (a[1] >= element[1] - radius2)):
                return True

            if ((a[0] <= element[0] - radius1) 
                    and (a[1] >= element[1] + radius2)):
                return True

            if ((a[0] <= element[0] - radius1) 
                    and (a[1] >= element[1] - radius2)):
                return True

    if(maxX and maxY):
        for index1,element in enumerate(BPertoFront):
            if ((a[0] <= element[0]+ radius1) 
                    and (a[1] <= element[1] + radius2)):
                return True
            if ((a[0] <= element[0]+ radius1) 
                    and (a[1] <= element[1] - radius2)):
                return True

            if ((a[0] <= element[0] - radius1) 
                    and (a[1] <= element[1] + radius2)):
                return True
            if ((a[0] <= element[0] - radius1) 
                    and (a[1] <= element[1] - radius2)):
                return True

        return False


    
    if ((a[0] <= element[0]+ radius1) 
            and (a[1] >= element[1] + radius2)):
        return True
    if ((a[0] <= element[0]+ radius1) 
            and (a[1] >= element[1] - radius2)):
        return True

    if ((a[0] <= element[0] - radius1) 
            and (a[1] >= element[1] + radius2)):
        return True

    if ((a[0] <= element[0] - radius1) 
            and (a[1] >= element[1] - radius2)):
        return True

    return False





# ---- Note: the following comparison is only applicable if we max x and min uy
def compare_two_pareto_fronts(curve1FeatureValues, curve2FeatureValues):
    curve1FirstFeature = curve1FeatureValues[0]
    curve1SecondFeature = curve1FeatureValues[1]
    curve2FirstFeature = curve2FeatureValues[0]
    curve2SecondFeature = curve2FeatureValues[1]
    # ---- the following perameters measure how of one pareto front 
    # ---- is containted in the other one
    VAB = 0 #look at the link provided bellow for explanation of each one of these variables
    VBA = 0 
    
    # ---- measuing VA(e, Bstart) (look at the following link for explanation:
    """http://download.springer.com/static/pdf/261/art%253A10.1134%252FS0965542514090048.pdf?originUrl=http%3A%2F%2Flink.springer.com%2Farticle%2F10.1134%2FS0965542514090048&token2=exp=1443400700~acl=%2Fstatic%2Fpdf%2F261%2Fart%25253A10.1134%25252FS0965542514090048.pdf%3ForiginUrl%3Dhttp%253A%252F%252Flink.springer.com%252Farticle%252F10.1134%252FS0965542514090048*~hmac=40e9a4534e14b6e9417ab545187b351a08e93d556553602b922a6bacbcdc73c7"""
    
    radius1Max = 20 
    radius2Max = 100 
    radius1Step = 5 
    radius2Step = 10 
    
    
    radius1Range =  range(0, radius1Max, radius1Step)
    radius2Range =  range(0, radius2Max, radius2Step)
    myList = [radius1Range, radius2Range] 
    permutedRadius = itertools.product(*myList)
    VABDic = {} 
    VBADic = {} 
    for radiusPair in permutedRadius: 
        VAB = 0 #the high this number the weaker the paretoFront (A weaker than B, 1 is the maximum value)
        VBA = 0  #the high this number the weaker the paretoFront
        for index1,element1 in enumerate(zip(curve1FirstFeature, curve1SecondFeature)):
            if aMemberOfBStar(element1, zip(curve2FirstFeature, curve2SecondFeature), radiusPair[0], radiusPair[1], maxX, maxY):
                VAB +=1;
        VAB = float(VAB)/len(curve1FirstFeature)
        VABDic[radiusPair] = VAB; 
        for index1,element1 in enumerate(zip(curve2FirstFeature, curve2SecondFeature)):
            if aMemberOfBStar(element1, zip(curve1FirstFeature, curve1SecondFeature), radiusPair[0], radiusPair[1], maxX, maxY):
                VBA +=1
    
        VBA = float(VBA)/len(curve2FirstFeature)
        VBADic[radiusPair] = VBA; 

    
    VABRaidus0 = map(lambda x: x[0], VABDic.keys()) 
    VABRaidus1 = map(lambda x: x[1], VABDic.keys()) 
    VABRes =  map(lambda x: 1 - x, VABDic.values()) 
    
    VBARaidus0 = map(lambda x: x[0], VBADic.keys()) 
    VBARaidus1 = map(lambda x: x[1], VBADic.keys()) 
    VBARes =  map(lambda x: 1 - x, VBADic.values()) 
    
    
    print VABDic 
    print "****************" 
    print VBADic 
    generateGraph3D(VABRaidus0, VABRaidus1, VABRes, "rad0", "rad1", "paretoStrengh")
    generateGraph3D(VBARaidus0, VBARaidus1, VBARes, "rad0", "rad1", "paretoStrengh")
   
    #plt.show()
   #  symbolIndex = 0  
    # symbolsToChooseFrom = ['*', 'x', "o", "+", "*", "-", "^", "1", "2", "3", "4"] #symbols to draw the plots with
    # generateGraph(curve1FirstFeature, curve1SecondFeature,  "PSNR", "Energy", symbolsToChooseFrom[symbolIndex])
    # # plt.show() 
def compare_adjusted(points_collected, points_collected_imposed):
    fig, ax = plt.subplots()

    symbolsToChooseFrom = ['*', 'x', "o", "+","^", '1', '2', "3"] 
    color =['g', 'y', 'r', 'm']
    
    """ 
    limit = False
    lower_bound = -100
    upper_bound = .001

    get_quality_energy_values("various_inputs.PIK", "+", points_collected, limit, lower_bound, upper_bound)
    """ 
    lOf_run_input_list = input_list.lOf_run_input_list
    number_of_inputs_used = len(lOf_run_input_list)
    input_results = map(list, [[]]*number_of_inputs_used) 
    base_dir = "/home/local/bulkhead/behzad/usr/local/apx_tool_chain/inputPics/"
    counter = 0
    energy_list_to_be_drawn = []
    setup_list_to_be_drawn = [] 
    quality_list_to_be_drawn = []
    std_list_to_be_drawn = []
    image_list_to_be_drawn = [] 
    z_vals = [] 

    mR =0 
    mG =0
    mB =0
    for val in points_collected:
        input_results = map(list, [[]]*number_of_inputs_used) 
        zipped = zip(*val[:-1])  
        for el in zipped:
            input_results[el[2]].append(el)
        for index,res in enumerate(input_results):
            """ 
            if (counter > 50 ):
                break
            """ 
            print counter 
            if len(res) > 0:
                image_addr =  base_dir+lOf_run_input_list[index][0] + ".ppm"
                #mR, mG, mB, stdR, stdG, stdB = cluster_images.calc_image_mean_std(image_addr)
                mR +=1 
                mG +=1
                mB +=1
                stdB = 0
                stdR = 0
                stdG = 0

                if (int(np.mean([mR,mG,mB]))) in z_vals:
                    continue
                el = map(lambda x: list(x), zip(*res))
                quality_values_shifted = map(lambda x: x+1, el[0]) 
                
                #--- sort based on the quality
                Q = quality_values_shifted
                E = el[1]
                SetUps =  el[2]
                E_index_sorted = sorted(enumerate(E), key=lambda x: x[1])
                index_of_E_sorted = map(lambda y: y[0], E_index_sorted)
                Q_sorted = [Q[i] for i in index_of_E_sorted]
                E_sorted = [E[i] for i in index_of_E_sorted]
                SetUp_sorted = [SetUps[i] for i in index_of_E_sorted]
                quality_list_to_be_drawn.append(Q_sorted)
                energy_list_to_be_drawn.append(E_sorted)
                setup_list_to_be_drawn.append(SetUp_sorted)
                std_list_to_be_drawn.append([int(np.mean([mR,mG,mB]))]*len(E_sorted))
                image_list_to_be_drawn.append([lOf_run_input_list[index][0]]*len(E_sorted))
                z_vals.append( int(np.mean([mR,mG,mB])))
                counter +=1
        
        reminder(True,"the following lines which creates a new image every len(symbolsToChooseFrom) should be commented if we use any flag but various_inputs")
        
        
        #--sorting the data. This is necessary for wire frame 
        zvals_index_sorted = sorted(enumerate(z_vals), key=lambda x: x[1])
        index_of_zvals_sorted = map(lambda y: y[0], zvals_index_sorted)
        quality_list_sorted_based_on_z = [quality_list_to_be_drawn[i] for i in index_of_zvals_sorted]                
        std_list_sorted_based_on_z = [std_list_to_be_drawn[i] for i in index_of_zvals_sorted]                
        energy_list_sorted_based_on_z = [energy_list_to_be_drawn[i] for i in index_of_zvals_sorted]                
        
        image_list_sorted_based_on_z = [image_list_to_be_drawn[i] for i in index_of_zvals_sorted]                
        
        SetUp_list_sorted_based_on_z = [setup_list_to_be_drawn[i] for i in index_of_zvals_sorted]                
    Qs_ref, Es_ref, stds_ref, QSs_ref = adjust.adjust_vals_2(quality_list_sorted_based_on_z, energy_list_sorted_based_on_z, std_list_sorted_based_on_z)
    
    
    lOf_run_input_list = input_list.lOf_run_input_list
    number_of_inputs_used = len(lOf_run_input_list)
    input_results = map(list, [[]]*number_of_inputs_used) 
    base_dir = "/home/local/bulkhead/behzad/usr/local/apx_tool_chain/inputPics/"
    counter = 0
    energy_list_to_be_drawn = []
    setup_list_to_be_drawn = [] 
    quality_list_to_be_drawn = []
    std_list_to_be_drawn = []
    image_list_to_be_drawn = [] 
    z_vals = [] 

    mR =0 
    mG =0
    mB =0

    for val in points_collected_imposed:
        input_results = map(list, [[]]*number_of_inputs_used) 
        zipped = zip(*val[:-1])  
        for el in zipped:
            input_results[el[2]].append(el)
        for index,res in enumerate(input_results):
            """ 
            if (counter > 50 ):
                break
            """ 
            print counter 
            if len(res) > 0:
                mR +=1 
                mG +=1
                mB +=1
                stdB = 0
                stdR = 0
                stdG = 0

                image_addr =  base_dir+lOf_run_input_list[index][0] + ".ppm"
                #mR, mG, mB, stdR, stdG, stdB = cluster_images.calc_image_mean_std(image_addr)
                if (int(np.mean([mR,mG,mB]))) in z_vals:
                    continue
                el = map(lambda x: list(x), zip(*res))
                quality_values_shifted = map(lambda x: x+1, el[0]) 
                
                #--- sort based on the quality
                Q = quality_values_shifted
                E = el[1]
                SetUps =  el[2]
                E_index_sorted = sorted(enumerate(E), key=lambda x: x[1])
                index_of_E_sorted = map(lambda y: y[0], E_index_sorted)
                Q_sorted = [Q[i] for i in index_of_E_sorted]
                E_sorted = [E[i] for i in index_of_E_sorted]
                SetUp_sorted = [SetUps[i] for i in index_of_E_sorted]
                quality_list_to_be_drawn.append(Q_sorted)
                energy_list_to_be_drawn.append(E_sorted)
                setup_list_to_be_drawn.append(SetUp_sorted)
                std_list_to_be_drawn.append([int(np.mean([mR,mG,mB]))]*len(E_sorted))
                image_list_to_be_drawn.append([lOf_run_input_list[index][0]]*len(E_sorted))
                z_vals.append( int(np.mean([mR,mG,mB])))
                counter +=1
        
        reminder(True,"the following lines which creates a new image every len(symbolsToChooseFrom) should be commented if we use any flag but various_inputs")
        
        
        #--sorting the data. This is necessary for wire frame 
        zvals_index_sorted = sorted(enumerate(z_vals), key=lambda x: x[1])
        index_of_zvals_sorted = map(lambda y: y[0], zvals_index_sorted)
        quality_list_sorted_based_on_z = [quality_list_to_be_drawn[i] for i in index_of_zvals_sorted]                
        std_list_sorted_based_on_z = [std_list_to_be_drawn[i] for i in index_of_zvals_sorted]                
        energy_list_sorted_based_on_z = [energy_list_to_be_drawn[i] for i in index_of_zvals_sorted]                
        
        image_list_sorted_based_on_z = [image_list_to_be_drawn[i] for i in index_of_zvals_sorted]                
        
        SetUp_list_sorted_based_on_z = [setup_list_to_be_drawn[i] for i in index_of_zvals_sorted]                
    Qs_imposed, Es_imposed, stds_imposed, QSs_imposed = adjust.adjust_vals_2(quality_list_sorted_based_on_z, energy_list_sorted_based_on_z, std_list_sorted_based_on_z)
        
    
    Es_diff = []
    for input_index in range(len(Es_imposed)):
#        Es_diff_el = [] 
#        for el in range(len(Es_imposed[input_index])):
#            Es_diff_el.append(Es_imposed[input_index][el] - Es_ref[input_index][el])
         
        #Es_diff.append(Es_diff_el) 
        Es_diff.append(map(operator.sub, Es_imposed[input_index], Es_ref[input_index]))
     
    line_style = '-'
    plt.xlabel("Quality")
    plt.ylabel("Energy")
    second_axis = Es_diff; 
    third_axis = std_list_sorted_based_on_z; 
    third_axis_name = "input" 
    n_lines = len(std_list_sorted_based_on_z)
    colors = gen_color_spec.gen_color(n_lines+1, 'seismic') 
    for x in range(len(third_axis)):
        my_label =  third_axis_name +": " + str(int(third_axis[x][0]))
        #if (int(third_axis[x][0]) == 151): 
        ax.plot(QSs_imposed, Es_diff[x], marker = symbolsToChooseFrom[x%len(symbolsToChooseFrom)], c= colors[x], label=my_label, linestyle=line_style)
#
    #   

    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width*.8 ,  box.height])
    # Put a legend to the right of the current axis (note: prop changes the fontsize)
    ax.legend(loc='center left', bbox_to_anchor=(1, .9), prop={'size':6})
    graph_title = "Ediff_vs_Q"
    name  = graph_title
    benchmark_name = "jpeg" 
    plt.title(graph_title + str(benchmark_name) + " benchmark")
    pylab.savefig(name+str(counter)+".png") #saving the figure generated by generateGraph
     
    
    Es_diff_avg_per_quality = [] 
    for x in range(len(QSs_imposed)):
        Es_diff_avg_per_quality.append(numpy.mean(map(lambda y: y[x], Es_diff)))
        #if (int(third_axis[x][0]) == 151): 
     
    my_label =  "AVG"
    ax.plot(QSs_imposed, Es_diff_avg_per_quality, marker = symbolsToChooseFrom[x%len(symbolsToChooseFrom)], c= colors[n_lines], label=my_label, linestyle=line_style)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width*.8 ,  box.height])
    # Put a legend to the right of the current axis (note: prop changes the fontsize)
    ax.legend(loc='center left', bbox_to_anchor=(1, .9), prop={'size':6})
    graph_title = "Ediff_avg_vs_Q"
    name  = graph_title
    benchmark_name = "jpeg" 
    plt.title(graph_title + str(benchmark_name) + " benchmark")
    pylab.savefig(name+str(counter)+".png") #saving the figure generated by generateGraph
    
    #plt.close()
    fig, ax = plt.subplots()
    print "avg of ES_diff" + str(numpy.mean(map(lambda x: numpy.mean(x), Es_diff)))

    """
    if(mode == ":
        Es_ref = [Es[0]]*len(stds)
    print "QS is : " + str(QSs) 
    l_diff_avged = []  
    l_diff = []  
    for input_index, input in enumerate(stds):
        #print "Es for mean:"  + str(stds[input_index][0]) + " " + str(Es[input_index])
        l_diff.append(map(operator.sub, Es[input_index], Es_ref[index]))
    print l_diff
    
    for diffs in l_diff:
        l_diff_avged.append(numpy.mean(diffs))
    print l_diff_avged
    
    l_diff_normalized = [] 
    for diffs in l_diff:
        l_diff_normalized.append(map(operator.div, diffs, Es[0]))

    print l_diff_normalized
    print "avg difference of E between PFs normalized to ref curve Evalues: " + str(numpy.mean(l_diff_normalized))
    """



def run_compare_pareto_curves(settings_obj):
    #settings_obj = settingsClass()
    PIK1 = "pareto_of_heur_flattened.PIK"
    PIK2 = "pareto_of_combined.PIK" 
     
    lOfParetoPoints1 = getPoints(PIK1)
    lOfParetoPoints2 = getPoints(PIK2)
    # ---- creating the curves
    curve1FeatureValues =[]
    curve2FeatureValues =[]
    dealingWithPic = lOfParetoPoints1[0].get_dealing_with_pics()
    
    if(dealingWithPic): 
        curve1FeatureValues.append(map(lambda x: x.get_PSNR(), lOfParetoPoints1))
        curve2FeatureValues.append(map(lambda x: x.get_PSNR(), lOfParetoPoints2))
    else:
        curve1FeatureValues.append(map(lambda x: x.get_quality(), lOfParetoPoints1))
        
        curve2FeatureValues.append(map(lambda x: x.get_quality(), lOfParetoPoints2))
    
    curve1FeatureValues.append(map(lambda x: x.get_energy(), lOfParetoPoints1))
    curve2FeatureValues.append(map(lambda x: x.get_energy(), lOfParetoPoints2))
     
    # ---- comparing the two curves
    if (settings_obj.pareto_comparison_mode == "comparison_of_nearest_neighbours"):
        refZipped = zip(curve1FeatureValues[0], curve1FeatureValues[1])
        tobeComparedZipped = zip(curve2FeatureValues[0], curve2FeatureValues[1])
        print "the mean distance between the two curve is:" 
        print np.mean(calc_distance_for_nearest_neighbors_2d(refZipped, tobeComparedZipped))
    if (settings_obj.pareto_comparison_mode == "subsumption_comparison"):
        compare_two_pareto_fronts(curve1FeatureValues, curve2FeatureValues)
    
    # generateGraph(map(lambda x: x.get_PSNR(), lOfParetoPoints1), map(lambda x: x.get_energy(), lOfParetoPoints1), "PSNR", "Energy", symbolsToChooseFrom[symbolIndex])
    # # compare_two_pareto_fronts(PIK1, PIK2)
    # plt.show() 

if __name__ == "__main__":
    limit = False
    lower_bound = -100
    upper_bound = .05
    print "diff accoross images" 
    points_collected = [] 
    points_collected_imposed = [] 
    get_quality_energy_values("various_inputs.PIK", "+", points_collected, limit, lower_bound, upper_bound)
    get_quality_energy_values("various_inputs_same_setUp.PIK", "+", points_collected_imposed, limit, lower_bound, upper_bound)
    compare_adjusted(points_collected, points_collected_imposed) 
    
    """
    points_collected = [] 
    print "diff accross images once imposed" 
    get_quality_energy_values("various_inputs_same_setUp.PIK", "+", points_collected, limit, lower_bound, upper_bound)
    compare_adjusted(points_collected)
    """


#    run_compare_pareto_curves() 
