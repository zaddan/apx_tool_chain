from math import *
from reminder import *
import operator
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
import numpy as np
from matplotlib import cm
plt.ioff()
import input_list
from extract_result_properties import *
from extract_pareto_set_from_raw_material import *
import cluster_images 
import gen_color_spec 
import adjust
#def generateParetoGraph(energy, noise, graphType = "2d")
#    symbolsToChooseFrom = ['*', 'x', "o", "+", "*", "-", "^"]
#    if (graphType == "3d"): 
#	    #preparing the inputs for generating the graph
#	    noiseArray = numpy.asarray(noise)
#	    energyArray = numpy.asarray((energy*len(noise))).reshape(noiseArray.shape)
#	    
#	    inputSetupNumber = [] 
#	    inputSetUpNumberDistance = 10  
#	    for i in range(0, len(noise)*inputSetUpNumberDistance, inputSetUpNumberDistance):
#	        inputSetupNumber.append([i]*len(energy))
#	    
#	    inputSetupNumberArray = numpy.asarray(inputSetupNumber)
#	    
#	    #drawing the graph 
#	    X = noiseArray
#	    Y = energyArray
#	    Z = inputSetupNumberArray
#	    fig = plt.figure()
#	    ax = fig.add_subplot(111, projection ='3d', )
#	    ax.scatter(X,Y,Z)
#	    ax.set_xlabel('Noise')
#	    ax.set_ylabel('Energy')
#	    ax.set_zlabel('inputNumber')
#    elif(graphType == "2d"):
#        print noise 
#        print len(noise) 
#        for i in range(0, len(noise), 1):
#            #---------guide:::  generating the pareto set
#            paretoNoise = []  #cleaning the previous values if exist
#            paretoEnergy = [] #cleaning the previous values if exist         
#            paretoNoise, paretoEnergy = pareto_frontier(noise[i], energy, maxX= False, maxY = False)
#            #---------guide::: plotting the pareto curve
#            plt.plot(paretoNoise, paretoEnergy, symbolsToChooseFrom[i%len(symbolsToChooseFrom)])
#            plt.ylabel('Energy')
#            plt.xlabel('Noise')
#
#    plt.show()



## 
# @brief simply drawing a graph
# 
# @param x
# @param y
# @param xName
# @param yName
# @param symbol
# 
# @return 

#-- adjusting the values so they can be drawn and easily compared with one another


def generateGraph(x, y, xName, yName, symbol):
    fig, ax = plt.plots()
    ax.plot(x, y, symbol, label="ok")
    #plt.yscale('log')
    plt.xscale('log')
    plt.ylabel(yName)
    plt.xlabel(xName)
  # Now add the legend with some customizations.
    legend = ax.legend(loc='upper center', shadow=True)

    # The frame is matplotlib.patches.Rectangle instance surrounding the legend.
    frame = legend.get_frame()
    frame.set_facecolor('0.90')

    # Set the fontsize
    for label in legend.get_texts():
        label.set_fontsize('large')

    for label in legend.get_lines():
        label.set_linewidth(1.5)  # the legend line width  
        
    
    #plt.show()

def generateGraph_for_all_alternative(valueList, valueList_2, xName, yName, benchmark_name, input_number, graph_title="pareto comparison for"):
    fig, ax = plt.subplots()
    #plt.yscale('log')
    plt.xscale('log')
    plt.ylabel(yName)
    plt.xlabel(xName)
    
    symbolsToChooseFrom = ['*', 'x', "o", "+","^"] #symbols to draw the plots with
    symbolsToChooseFrom += ['1', '2', "3"] #symbols to draw the plots with
    
    #color =['r','y', 'g', 'b', 'w']
    color =['b','g', 'r', 'c', 'm', 'y', 'k', 'w']
    number_of_inputs_used = 25 
    
    #lOf_run_input_list = [["flowerpots_1"], ["aloe_1"], ["monopoly_1"], ["baby1_1"], ["plastic_1"], ["rocks1_1"]]
    lOf_run_input_list = [["room_1.bmp", "room_2.bmp"], ["papers_1.bmp", "papers_2.bmp"], ["odd_1.bmp", "odd_2.bmp"], ["baby1_1.bmp", "baby1_2.bmp"], ["plastic_1.bmp", "plastic_2.bmp"], ["rocks1_1.bmp", "rocks1_2.bmp"]]
    #= [[] for i in range(settings_obj.n_clusters)]
    
    input_results = map(list, [[]]*number_of_inputs_used) 
    counter = 0
    for val in valueList:
        input_results = map(list, [[]]*number_of_inputs_used) 
        zipped = zip(*val[:-1])  
        for el in zipped:
            if (el[2] == input_number):
                input_results[el[2]].append(el)
        for index,res in enumerate(input_results):
            if len(res) > 0:
                el = map(lambda x: list(x), zip(*res))
                quality_values_shifted = map(lambda x: x+1, el[0]) 
                #ax.plot(quality_values_shifted, el[1], symbolsToChooseFrom[counter%len(symbolsToChooseFrom)]+color[counter/len(symbolsToChooseFrom)], label=val[3]) 
                
                
                reminder(True,"this label generation requires lOf_run_input_list which needs to be copied over manually")
                #---un comment(from here) the next line whenever you want to provide the resuls t professor, 
                #-- this requires manually updating lOf_run_input_list (by copying it from test_bench_mark_4.._)
                my_label =  lOf_run_input_list[index][0]
                ax.plot(quality_values_shifted, el[1], 3, symbolsToChooseFrom[input_number]+color[0], label=my_label)
                # to here
                
                #--uncomment if you want to use regular labels 
                #ax.plot(quality_values_shifted, el[1], symbolsToChooseFrom[counter%len(symbolsToChooseFrom)]+color[counter%len(symbolsToChooseFrom)], label=val[3])
                
                counter +=1
    #---comment up to here if not using proviing s4 point
    #--uncomment the following two lines to return back to without s4 inut consideration
#    for el in valueList: 
#        quality_values_shifted = map(lambda x: x+1, el[0]) 
#        ax.plot(quality_values_shifted, el[1], el[2], label=el[3])
#
    
    
    input_results = map(list, [[]]*number_of_inputs_used) 
    counter = 0
    for val in valueList_2:
        input_results = map(list, [[]]*number_of_inputs_used) 
        zipped = zip(*val[:-1])  
        for el in zipped:
            if (el[2] == input_number):
                input_results[el[2]].append(el)
        for index,res in enumerate(input_results):
            if len(res) > 0:
                el = map(lambda x: list(x), zip(*res))
                quality_values_shifted = map(lambda x: x+1, el[0]) 
                #ax.plot(quality_values_shifted, el[1], symbolsToChooseFrom[counter%len(symbolsToChooseFrom)]+color[counter/len(symbolsToChooseFrom)], label=val[3]) 
                
                #--here 
                #---un comment the next line whenever you want to provide the resuls t professor, 
                #-- this requires manually updating lOf_run_input_list (by copying it from test_bench_mark_4.._)
                my_label =  lOf_run_input_list[index][0]
                ax.plot(quality_values_shifted, el[1], symbolsToChooseFrom[input_number]+color[1], label=my_label)
                #ax.plot(quality_values_shifted, el[1], symbolsToChooseFrom[counter%len(symbolsToChooseFrom)]+color[counter%len(symbolsToChooseFrom)], label=val[3])
                
                counter +=1

    # ---- moving the legend outside of the graph (look bellow for placing inside)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.85, box.height])
    # Put a legend to the right of the current axis (note: prop changes the fontsize)
    ax.legend(loc='center left', bbox_to_anchor=(1, .9), prop={'size':8})
    plt.title(graph_title + str(benchmark_name) + " benchmark")
    # ---- the following was commented cause it will place the lgend inside the graph
#    legend = ax.legend(loc='upper right', shadow=True)
#
#    # The frame is matplotlib.patches.Rectangle instance surrounding the legend.
#    frame = legend.get_frame()
#    frame.set_facecolor('0.90')
#
#    # Set the fontsize
#    for label in legend.get_texts():
#        label.set_fontsize('small')
#
#    for label in legend.get_lines():
#        label.set_linewidth(1.5)  # the legend line width  
#        

def finish_up_making_graph(ax, name, graph_title, benchmark_name, counter=0): 
            #--- wrapping up making the graph 
            box = ax.get_position()
            ax.set_position([box.x0, box.y0, box.width*.8 ,  box.height])
            # Put a legend to the right of the current axis (note: prop changes the fontsize)
            ax.legend(loc='center left', bbox_to_anchor=(1, .9), prop={'size':6})
            plt.title(graph_title + str(benchmark_name) + " benchmark")
            pylab.savefig(name+str(counter)+".png") #saving the figure generated by generateGraph
             
            #plt.close()
            fig, ax = plt.subplots()
            #plt.yscale('log')
#            plt.xscale('log')
#            plt.ylabel(yName)
#            plt.xlabel(xName)



def sort_values(valueList):
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



    for val in valueList:
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
                # the following line is commented to incorperate applications
                # that are not images, b/c the following line is only applicable
                # for images
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
                
                print "mean of image : " + (lOf_run_input_list[index][0]) + " is: " +  str(np.mean([mR,mG,mB]))
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
        print quality_list_sorted_based_on_z
        print std_list_sorted_based_on_z
        print energy_list_sorted_based_on_z
        
        return quality_list_sorted_based_on_z, std_list_sorted_based_on_z,energy_list_sorted_based_on_z            
    return [],[],[]        
        
        
 



def generateGraph_for_all_simplified(valueList,xlabel, ylabel, benchmark_name, ax, fig,  graph_title="pareto comparison for", name = "various_inputs", post_pone_saving_graph = False, use_prev_ax_fig = False, n_graphs="one", valueList_promised=[]):
    
    name_counter = 0 
    #fig = plt.figure(figsize=plt.figaspect(0.5)) 
    #--- sanity check 
    if not(use_prev_ax_fig):
        fig, ax = plt.subplots()


    """ 
    if (graph_type == "Q_E_product"):
        plt.ylabel("Q_E_product")
        plt.xlabel("mean")
    else: 
        #plt.xscale('log')
        plt.xlabel("mean")
        plt.ylabel("Energy")
#            plt.ylabel(yName)
#            plt.xlabel(xName)
    """
    #here
    #----comment if not proving th s4 pont
    symbolsToChooseFrom = ['*', 'x', "o", "+","^", '1', '2', "3"] 
    color =['g', 'y', 'r', 'm']
    quality_list_sorted_based_on_z, std_list_sorted_based_on_z, energy_list_sorted_based_on_z = sort_values(valueList)
    quality_list_promised_sorted_based_on_z, std_list_promised_sorted_based_on_z, energy_list_promised_sorted_based_on_z = sort_values(valueList_promised)


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

    for val in valueList:
        input_results = map(list, [[]]*number_of_inputs_used) 
        zipped = zip(*val[:-1])  
        for el in zipped:
            input_results[el[2]].append(el)
        for index,res in enumerate(input_results):
            print counter 
            if len(res) > 0:
                image_addr =  base_dir+lOf_run_input_list[index][0] + ".ppm"
                mR, mG, mB, stdR, stdG, stdB = cluster_images.calc_image_mean_std(image_addr)
                if (int(np.mean([mR,mG,mB]))) in z_vals:
                    continue
                el = map(lambda x: list(x), zip(*res))
                quality_values_shifted = map(lambda x: x+1, el[0]) 
                
                print "mean of image : " + (lOf_run_input_list[index][0]) + " is: " +  str(np.mean([mR,mG,mB]))
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
        print quality_list_sorted_based_on_z
        print std_list_sorted_based_on_z
        print energy_list_sorted_based_on_z
        
    """        
    if (post_pone_saving_graph): 
        line_style = ':'
    else:
        line_style = '-'
    #--- generate a spectrum of colors  
    #colors = ['b', 'g'] 
    
    plt.xscale('log')
    if (name == "same_Q_vs_input"):
        plt.xlabel("mean")
        plt.ylabel("Energy")
        Qs, Es, stds, QSs = adjust.adjust_vals_2(quality_list_sorted_based_on_z, energy_list_sorted_based_on_z, std_list_sorted_based_on_z)
        second_axis = Es; 
        third_axis = QSs; 
        third_axis_name = "quality" 
        
        #---limiting
        #third_axis= QSs[:10]
        n_lines = len(third_axis)
        colors = gen_color_spec.gen_color(max(n_lines,2), 'seismic')
        #---limiting 
        
        #--- printing the the Qstates (Q attempted) and the Q found
        for input_index in range(len(Qs)): 
            print "true Qs for input with mean:" + str(stds[input_index]) + "is:"
            for x in range(len(third_axis)):
                print "Q state:" + str(third_axis[x]) + "  found Q:" + str(Qs[input_index][x]) + "En is: " + str(Es[input_index][x]) 

        for x in range(len(third_axis)):
            my_label =  third_axis_name +": " + str(float(third_axis[x]))
            second_axis_as_w_diff_mean = map(lambda y: y[x], second_axis)
            l_mean = map(lambda y: y[x], stds)
            ax.plot(l_mean, second_axis_as_w_diff_mean, marker = symbolsToChooseFrom[x%len(symbolsToChooseFrom)], c= colors[x], label=my_label, linestyle=line_style)
        #finish_up_making_graph(ax, graph_title, graph_title, benchmark_name,  0) 
    elif (name == "same_E_vs_input"):
         plt.xlabel("mean")
         plt.ylabel("quality")
         sys.stdout.flush()  
         third_axis= energy_list_sorted_based_on_z[0]; 
         third_axis_name = "energy" 
         second_axis = quality_list_sorted_based_on_z; 
         n_lines = len(third_axis)
         colors = gen_color_spec.gen_color(n_lines, 'seismic') 
         for x in range(len(third_axis)):
             #--- limiting
#                 if x > 10:
#                     break;
             my_label =  third_axis_name +": " + str(float(third_axis[x]))
             second_axis_as_w_diff_mean = map(lambda y: y[x], second_axis)
             l_mean = map(lambda y: y[x], std_list_sorted_based_on_z)
             print "asdf" + str(second_axis_as_w_diff_mean )
             ax.plot(l_mean, second_axis_as_w_diff_mean, marker = symbolsToChooseFrom[x%len(symbolsToChooseFrom)], c= colors[x], label=my_label, linestyle=line_style)
         #finish_up_making_graph(ax, graph_title, graph_title, benchmark_name,  0) 
    elif(name == "E_vs_Q_adjusted"): 
        plt.xlabel("Quality")
        plt.ylabel("Energy")
        Qs, Es, stds, QSs = adjust.adjust_vals_2(quality_list_sorted_based_on_z, energy_list_sorted_based_on_z, std_list_sorted_based_on_z)
        second_axis = Es; 
        third_axis = std_list_sorted_based_on_z; 
        third_axis_name = "input" 
        n_lines = len(std_list_sorted_based_on_z)
        colors = gen_color_spec.gen_color(n_lines, 'seismic') 
        for x in range(len(third_axis)):
            my_label =  third_axis_name +": " + str(float(third_axis[x][0]))
            #if (third_axis[x][0] == 97): 
            ax.plot(QSs, Es[x], marker = symbolsToChooseFrom[x%len(symbolsToChooseFrom)], c= colors[x], label=my_label, linestyle=line_style)
    elif (name == "E_vs_Q"):
        #---line_style = ''  uncomment for all_points
        plt.xlabel("Quality")
        plt.ylabel("Energy")
        third_axis = std_list_sorted_based_on_z; 
        third_axis_name = "input" 
        n_lines = len(std_list_sorted_based_on_z)
        colors = gen_color_spec.gen_color(n_lines, 'seismic') 
        for x in range(len(third_axis)):
            my_label =  third_axis_name +": " + str(float(third_axis[x][0]))
            #if (third_axis[x][0] == 97): 
            ax.plot(quality_list_sorted_based_on_z[x], energy_list_sorted_based_on_z[x], marker = symbolsToChooseFrom[x%len(symbolsToChooseFrom)], c= colors[x], label=my_label, linestyle=line_style)
    elif (name == "Qstd_vs_E_imposed"):
        plt.ylabel("Quality_std")
        plt.xlabel("Energy")
        n_lines = 1
        colors = gen_color_spec.gen_color(n_lines, 'seismic') 
        my_label =  "nolabel"
        Q_diff = [] 
        for E_index in range(len(energy_list_sorted_based_on_z[0])):
            all_Qs_as_w_index = map(lambda x: x[E_index], quality_list_sorted_based_on_z)
            Q_diff.append(numpy.std(all_Qs_as_w_index))
        ax.plot(energy_list_sorted_based_on_z[0], Q_diff, marker = symbolsToChooseFrom[0%len(symbolsToChooseFrom)], c= colors[0], label=my_label, linestyle=line_style)
    elif (name == "Qmean_normalized_to_Q_promissed"):
        
        plt.ylabel("Quality_mean_normalized_to_Q_promised")
        plt.xlabel("Energy")
        n_lines = 1
        colors = gen_color_spec.gen_color(max(n_lines,2), 'seismic') 
        Q_diff_1 = [] 
        Q_diff_2 = [] 
        for E_index in range(len(energy_list_sorted_based_on_z[0])):
            all_Qs_as_w_index = map(lambda x: x[E_index], quality_list_sorted_based_on_z)
            print "all_Qs" + str(all_Qs_as_w_index) 
            Q_diff_1.append(numpy.mean(all_Qs_as_w_index))
            print "quality_promiseed" + str(quality_list_promised_sorted_based_on_z[0]) 
            imposed_vs_got_diff =  map(operator.sub,  [quality_list_promised_sorted_based_on_z[0][E_index]]*len(all_Qs_as_w_index), all_Qs_as_w_index)
            Q_diff_2.append(numpy.mean(imposed_vs_got_diff))
        print "Q_diff_2)" + str(Q_diff_2) 
        #ax.plot(energy_list_sorted_based_on_z[0], Q_diff_1, marker = symbolsToChooseFrom[0%len(symbolsToChooseFrom)], c= colors[0], label="Q_mean", linestyle=line_style)
        ax.plot(energy_list_sorted_based_on_z[0], Q_diff_2, marker = symbolsToChooseFrom[0%len(symbolsToChooseFrom)], c= colors[1], label="Q_mean_"+"normalized", linestyle=line_style)
    elif (name == "Q_satisfaction_success_rate"):
        
        plt.ylabel("Q_satisfaction_success_rate")
        plt.xlabel("Energy")
        n_lines = 1
        colors = gen_color_spec.gen_color(max(n_lines,2), 'seismic') 
        my_label =  "nolabel"
        Q_diff_2 = [] 
        for E_index in range(len(energy_list_sorted_based_on_z[0])):
            all_Qs_as_w_index = map(lambda x: x[E_index], quality_list_sorted_based_on_z)
            imposed_vs_got_diff =  map(operator.sub, all_Qs_as_w_index, [quality_list_promised_sorted_based_on_z[0][E_index]]*len(all_Qs_as_w_index))
            print "sub_is2" + str(imposed_vs_got_diff)
            success_rate =  float(len(filter(lambda x: x >= 000, imposed_vs_got_diff)))/float(len(imposed_vs_got_diff))
            Q_diff_2.append(success_rate)
      
        ax.get_yaxis().get_major_formatter().set_useOffset(False)
        ax.plot(energy_list_sorted_based_on_z[0], Q_diff_2, marker = symbolsToChooseFrom[0%len(symbolsToChooseFrom)], c= colors[1], label="Q_satisfaction_success_rate", linestyle=line_style)

    
    else:
        print "this name : " + name + " is not defined" 
        sys.exit()

    if not(post_pone_saving_graph): 
        finish_up_making_graph(ax, graph_title, graph_title, benchmark_name,  0) 
    return ax, fig







def generateGraph_for_all(valueList, xName, yName, benchmark_name, graph_title="pareto comparison for", name = "various_inputs", graph_dim = "2d", graph_type ="Q_vs_E", n_graphs="one"):
    assert(1==0, "this graph generation tool can not be used b/c it uses meani")

    name_counter = 0 
    fig = plt.figure(figsize=plt.figaspect(0.5)) 
    #--- sanity check 
    if (graph_dim == "3d"): 
        if (graph_type == "Q_E_product"): 
            print "ERROR: graph_teyp and graph_dim are incompatible"
            sys.exit()
        ax = fig.gca(projection='3d')
        #ax = fig.add_subplot(111, projection='3d') 
        ax.set_xlabel('Quality')
        ax.set_ylabel('mean')
        ax.set_zlabel('Energy')
    else: 
        fig, ax = plt.subplots()
        if (graph_type == "Q_E_product"):
            plt.ylabel("Q_E_product")
            plt.xlabel("mean")
        else: 
            #plt.xscale('log')
            plt.xlabel("mean")
            plt.ylabel("Quality")
#            plt.ylabel(yName)
#            plt.xlabel(xName)
    
    #here
    #----comment if not proving th s4 pont
    symbolsToChooseFrom = ['*', 'x', "o", "+","^", '1', '2', "3"] 
    color =['g', 'y', 'r', 'm']
    
    lOf_run_input_list = input_list.lOf_run_input_list
    number_of_inputs_used = len(lOf_run_input_list)
    input_results = map(list, [[]]*number_of_inputs_used) 
    base_dir = "/home/local/bulkhead/behzad/usr/local/apx_tool_chain/inputPics/"
    counter = 0
    energy_list_to_be_drawn = []
    quality_list_to_be_drawn = []
    std_list_to_be_drawn = []
    image_list_to_be_drawn = [] 
    z_vals = [] 
    

    for val in valueList:
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
                mR, mG, mB, stdR, stdG, stdB = cluster_images.calc_image_mean_std(image_addr)
                if (int(np.mean([mR,mG,mB]))) in z_vals:
                    continue
                el = map(lambda x: list(x), zip(*res))
                quality_values_shifted = map(lambda x: x+1, el[0]) 
                #--here 
                #---un comment the next line whenever you want to provide the resuls t professor, 
                

                #--- sort based on the quality
                Q = quality_values_shifted
                E = el[1]
#                Q_index_sorted = sorted(enumerate(Q), key=lambda x: x[1])
#                index_of_Q_sorted = map(lambda y: y[0], Q_index_sorted)
                
                E_index_sorted = sorted(enumerate(E), key=lambda x: x[1])
                index_of_E_sorted = map(lambda y: y[0], E_index_sorted)
                
#                
#                Q_sorted = [Q[i] for i in index_of_Q_sorted]
#                E_sorted = [E[i] for i in index_of_Q_sorted]

                Q_sorted = [Q[i] for i in index_of_E_sorted]
                E_sorted = [E[i] for i in index_of_E_sorted]

                quality_list_to_be_drawn.append(Q_sorted)
                energy_list_to_be_drawn.append(E_sorted)
                
#                std_list_to_be_drawn.append([int(np.mean([stdR,stdG,stdB]))]*len(E_sorted))
#                z_vals.append( int(np.mean([stdR,stdG,stdB])))

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
        
        #--- generate a spectrum of colors  
        #colors = ['b', 'g'] 
        n_energy_levels = 4
        #colors = gen_color_spec.gen_color(len(quality_list_sorted_based_on_z[0]), 'seismic') 
        colors = gen_color_spec.gen_color(n_energy_levels, 'seismic') 
        
                     
        print "here is the list of (images in the z_order, quality in z order, energy in z order)" 
        print zip([i[0] for i in image_list_sorted_based_on_z], [i[0] for i in quality_list_sorted_based_on_z], [i[0] for i in  std_list_sorted_based_on_z])
        print zip([i[0] for i in image_list_sorted_based_on_z], [i[1] for i in quality_list_sorted_based_on_z], [i[0] for i in  std_list_sorted_based_on_z])

        for x in range(len(energy_list_sorted_based_on_z[0][:n_energy_levels])):
        #for x in range(len(quality_list_sorted_based_on_z)):
            #my_label =  'mean:' + str(int(std_list_sorted_based_on_z[x][0]))
            my_label =  'En:' + str(float(energy_list_sorted_based_on_z[0][x]))
            if (graph_dim == "3d"): 
                """ the following is for plotting a wire_frame or surface plot
        surf = ax.plot_surface(np.asarray(energy_list_sorted_based_on_z), np.asarray(quality_list_sorted_based_on_z), np.asarray(std_list_sorted_based_on_z), rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)
        fig.colorbar(surf, shrink=0.5, aspect=5)
        #ax.plot_wireframe(np.asarray(quality_list_sorted_based_on_z), np.asarray(std_list_sorted_based_on_z), np.asarray(energy_list_sorted_based_on_z))
        """ 
                ax.scatter(quality_list_sorted_based_on_z[x], std_list_sorted_based_on_z[x] , energy_list_sorted_based_on_z[x], c=colors[x], marker = symbolsToChooseFrom[x%len(symbolsToChooseFrom)], depthshade=False)
            else:
                #my_label +=  lOf_run_input_list[index][0] 
                #--- note: get rid of linestyle='None' if you want a line through the graph 
                #line_style = 'None'
                line_style = '-'
                if (graph_type == "Q_E_product") :
                    Q_E_list = [a*b for a,b in zip(quality_list_sorted_based_on_z[x],energy_list_sorted_based_on_z[x])]
                    ax.plot(std_list_sorted_based_on_z[x], Q_E_list, marker = symbolsToChooseFrom[x%len(symbolsToChooseFrom)], c= colors[x], label=my_label, linestyle=line_style)
                else:
                    #ax.plot(quality_list_sorted_based_on_z[x], energy_list_sorted_based_on_z[x], marker = symbolsToChooseFrom[x%len(symbolsToChooseFrom)], c= colors[x], label=my_label, linestyle=line_style)
                    quality_as_w_diff_mean = map(lambda y: y[x], quality_list_sorted_based_on_z)


                    #--- if no quality value under 150, it is possibly the acc\
                    #    setUP. The accurate set up make seeing other setUPs difficult
                    """ 
                    found_one = False 
                    for el in quality_as_w_diff_mean:
                        if el < 150:
                            found_one = True
                            break
                    if not(found_one):
                        continue
                    """

                    l_mean = map(lambda y: y[x], std_list_sorted_based_on_z)
                    
                    ax.plot(l_mean, quality_as_w_diff_mean, marker = symbolsToChooseFrom[x%len(symbolsToChooseFrom)], c= colors[x], label=my_label)
                            #, linestyle=line_style)
                if (n_graphs  == "multiple"):
                    finish_up_making_graph(ax, name, graph_title, benchmark_name, name_counter) 
                    fig = plt.figure(figsize=plt.figaspect(0.5)) 
                    #--- sanity check 
                    if (graph_dim == "3d"): 
                        ax = fig.gca(projection='3d')
                        #ax = fig.add_subplot(111, projection='3d') 
                        ax.set_xlabel('1/Q')
                        ax.set_ylabel('mean')
                        ax.set_zlabel('Energy')
                    else: 
                        fig, ax = plt.subplots()
                        if (graph_type == "Q_E_product"):
                            plt.ylabel("Q_E_product")
                            plt.xlabel("mean")
                        else: 
                            #plt.xscale('log')
                            plt.xlabel("mean")
                            plt.ylabel("Quality")
#                            plt.ylabel(yName)
#                            plt.xlabel(xName)

                    
                    name_counter += 1
        
        if (n_graphs  == "one"):
            finish_up_making_graph(ax, name, graph_title, benchmark_name,  0) 
             
    #---comment up to here if not using proviing s4 point
    #--uncomment the following two lines to return back to without s4 inut consideration
#    for el in valueList: 
#        quality_values_shifted = map(lambda x: x+1, el[0]) 
#        ax.plot(quality_values_shifted, el[1], el[2], label=el[3])
#
    # ---- moving the legend outside of the graph (look bellow for placing inside)
    
    
def generateGraph3D(x, y, z, xName="blah", yName="now", zName="never"):
    fig = plt.figure(figsize=plt.figaspect(0.5)) 
    ax = fig.add_subplot(1, 2, 1, projection='3d') 
    ax.scatter(x, y, z)
    # plt.ylabel(yName)
    # plt.xlabel(xName)
    
x = [1, 2, 4, 8]
y = [10, 20,40, 80 ]
z = [100, 200, 400, 800]

x2 = [100, 20]
y2 = [104, 40]
z2 = [202, 50]

#generateGraph3D(x,y,z)
#generateGraph3D(x2,y2,z2)


#fig = plt.figure(figsize=plt.figaspect(0.5)) 
#ax = fig.add_subplot(1, 2, 1, projection='3d') 
#ax.scatter(x, y, z)
#ax.scatter(x2, y2, z2)
#
#pylab.savefig("sdf.png") #saving the figure generated by generateGraph
# generateGraph3D(x, y, z, "now", "bla", "k")


