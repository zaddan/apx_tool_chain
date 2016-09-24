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
import numpy as np
from matplotlib import cm
plt.ioff()
import image_list
from extract_result_properties import *
from extract_pareto_set_from_raw_material import *
import cluster_images 
import gen_color_spec 
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



def generateGraph_for_all(valueList, xName, yName, benchmark_name, graph_title="pareto comparison for", name = "various_inputs", graph_type = "3d"):
    
    fig = plt.figure(figsize=plt.figaspect(0.5)) 
    if (graph_type == "3d"): 
        ax = fig.gca(projection='3d')
        #ax = fig.add_subplot(111, projection='3d') 
        ax.set_xlabel('1/Q')
        ax.set_ylabel('std')
        ax.set_zlabel('Energy')
    else: 
        fig, ax = plt.subplots()
        plt.xscale('log')
        plt.ylabel(yName)
        plt.xlabel(xName)
    
    #here
    #----comment if not proving th s4 pont
    symbolsToChooseFrom = ['*', 'x', "o", "+","^", '1', '2', "3"] 
    #color =['k', 'c', 'b','g', 'y', 'r', 'm']
    color =['.9', '.4', '.9','g', 'y', 'r', 'm']
    
    lOf_run_input_list = image_list.lOf_run_input_list
    number_of_inputs_used = len(lOf_run_input_list)
    input_results = map(list, [[]]*number_of_inputs_used) 
    base_dir = "/home/local/bulkhead/behzad/usr/local/apx_tool_chain/inputPics/"
    counter = 0
    energy_list_to_be_drawn = []
    quality_list_to_be_drawn = []
    std_list_to_be_drawn = []
    z_vals = [] 
    
    for val in valueList:
        input_results = map(list, [[]]*number_of_inputs_used) 
        zipped = zip(*val[:-1])  
        for el in zipped:
            input_results[el[2]].append(el)
        for index,res in enumerate(input_results):
            print counter 
#            if (index >5):
#                break;
            if len(res) > 0:
                el = map(lambda x: list(x), zip(*res))
                quality_values_shifted = map(lambda x: x+1, el[0]) 
                #--here 
                #---un comment the next line whenever you want to provide the resuls t professor, 
                #-- this requires manually updating lOf_run_input_list (by copying it from test_bench_mark_4.._)
                image_addr =  base_dir+lOf_run_input_list[index][0] + ".ppm"
                mR, mG, mB, stdR, stdG, stdB = cluster_images.calc_image_mean_std(image_addr)
                if (graph_type == "3d"): 
                    my_label =  lOf_run_input_list[index][0] 
                else: 
                    #my_label =  lOf_run_input_list[index][0] 
                    my_label =  str(int(np.mean([mR,mG,mB]))) + "," + str(int(np.mean([stdR,stdG,stdB])))
                
                if (graph_type == "3d"): 
                    #""" the following is for plotting a zframe
                    #--- sort based on the quality
                    Q = quality_values_shifted[:20]
                    E = el[1][:20]
                    Q_index_sorted = sorted(enumerate(Q), key=lambda x: x[1])
                    index_of_Q_sorted = map(lambda y: y[0], Q_index_sorted)
                    Q_sorted = [Q[i] for i in index_of_Q_sorted]
                    E_sorted = [E[i] for i in index_of_Q_sorted]
                    
                    quality_list_to_be_drawn.append(Q_sorted)
                    energy_list_to_be_drawn.append(E_sorted)
                    std_list_to_be_drawn.append([int(np.mean([mR,mG,mB]))]*20)
                    z_vals.append( int(np.mean([mR,mG,mB])))
                    #ax.scatter(quality_values_shifted, [int(np.mean([mR,mG,mB]))]*len(quality_values_shifted) , el[1], c=color[counter/len(color)], marker = symbolsToChooseFrom[counter%len(symbolsToChooseFrom)])
                    #""" 
                    #ax.scatter(quality_values_shifted, [int(np.mean([mR,mG,mB]))]*len(quality_values_shifted) , el[1], c=color[counter/len(color)], marker = symbolsToChooseFrom[counter%len(symbolsToChooseFrom)])
                    #ax.scatter(quality_values_shifted,  el[1], [int(np.mean([mR,mG,mB]))]*len(quality_values_shifted) ,c=color[counter%len(color)], marker = symbolsToChooseFrom[counter/len(symbolsToChooseFrom)])
                else:
                    ax.plot(quality_values_shifted, el[1], symbolsToChooseFrom[counter%len(symbolsToChooseFrom)]+color[counter%len(symbolsToChooseFrom)], label=my_label)
                counter +=1
            reminder(True,"the following lines which creates a new image every len(symbolsToChooseFrom) should be commented if we use any flag but various_inputs")
            #if (counter % (len(symbolsToChooseFrom)*len(color)) == 0): 
        #if (counter % 10 == 0):
        if (graph_type == "3d"): 
            zvals_index_sorted = sorted(enumerate(z_vals), key=lambda x: x[1])
            index_of_zvals_sorted = map(lambda y: y[0], zvals_index_sorted)
            quality_list_sorted_based_on_z = [quality_list_to_be_drawn[i] for i in index_of_zvals_sorted]                
            energy_list_sorted_based_on_z = [energy_list_to_be_drawn[i] for i in index_of_zvals_sorted]                
            std_list_sorted_based_on_z = [std_list_to_be_drawn[i] for i in index_of_zvals_sorted]                
            
            """ the following is for plotting a wire_frame or surface plot
            print  np.asarray(quality_list_sorted_based_on_z)
            print np.asarray(std_list_sorted_based_on_z)
            print np.asarray(energy_list_sorted_based_on_z)
            surf = ax.plot_surface(np.asarray(energy_list_sorted_based_on_z), np.asarray(quality_list_sorted_based_on_z), np.asarray(std_list_sorted_based_on_z), rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)
            fig.colorbar(surf, shrink=0.5, aspect=5)
            #ax.plot_wireframe(np.asarray(quality_list_sorted_based_on_z), np.asarray(std_list_sorted_based_on_z), np.asarray(energy_list_sorted_based_on_z))
            """ 
            colors = gen_color_spec.gen_color(len(quality_list_sorted_based_on_z), 'seismic') 
            for x in range(len(quality_list_sorted_based_on_z)):
                ax.scatter(quality_list_sorted_based_on_z[x], std_list_sorted_based_on_z[x] , energy_list_sorted_based_on_z[x], c=colors[x], marker = symbolsToChooseFrom[x%len(symbolsToChooseFrom)])
                #ax.scatter(quality_list_sorted_based_on_z[x], std_list_sorted_based_on_z[x] , energy_list_sorted_based_on_z[x], c=color[x/len(color)], marker = symbolsToChooseFrom[x%len(symbolsToChooseFrom)])
        
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.85, box.height])
        # Put a legend to the right of the current axis (note: prop changes the fontsize)
        ax.legend(loc='center left', bbox_to_anchor=(1, .9), prop={'size':8})
        plt.title(graph_title + str(benchmark_name) + " benchmark")
        pylab.savefig(name+ str(int(counter/len(symbolsToChooseFrom)))+".png") #saving the figure generated by generateGraph
        plt.close()
        fig, ax = plt.subplots()
        #plt.yscale('log')
        plt.xscale('log')
        plt.ylabel(yName)
        plt.xlabel(xName)
            #sys.exit()
               
    sys.exit() 
    #---comment up to here if not using proviing s4 point
    #--uncomment the following two lines to return back to without s4 inut consideration
#    for el in valueList: 
#        quality_values_shifted = map(lambda x: x+1, el[0]) 
#        ax.plot(quality_values_shifted, el[1], el[2], label=el[3])
#
    # ---- moving the legend outside of the graph (look bellow for placing inside)
    
    
    """
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.85, box.height])
    # Put a legend to the right of the current axis (note: prop changes the fontsize)
    ax.legend(loc='center left', bbox_to_anchor=(1, .9), prop={'size':8})
    plt.title(graph_title + str(benchmark_name) + " benchmark")
    if (counter % len(symbolsToChooseFrom) != 0):
        pylab.savefig(name+ str(int(counter/len(symbolsToChooseFrom)) + 1)+".png") #saving the figure generated by generateGraph
    plt.close()   
    """
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


