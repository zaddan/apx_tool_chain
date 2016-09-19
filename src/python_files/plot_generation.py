from math import *
from reminder import *
import pylab
import os
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
from extract_result_properties import *
from extract_pareto_set_from_raw_material import *
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
                ax.plot(quality_values_shifted, el[1], symbolsToChooseFrom[input_number]+color[0], label=my_label)
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



def generateGraph_for_all(valueList, xName, yName, benchmark_name, graph_title="pareto comparison for", name = "various_inputs"):
    fig, ax = plt.subplots()
    #plt.yscale('log')
    plt.xscale('log')
    plt.ylabel(yName)
    plt.xlabel(xName)
    
    #here
    #----comment if not proving th s4 pont
    symbolsToChooseFrom = ['*', 'x', "o", "+","^"] #symbols to draw the plots with
    symbolsToChooseFrom += ['1', '2', "3"] #symbols to draw the plots with
    
    #color =['r','y', 'g', 'b', 'w']
    color =['b','g', 'r', 'c', 'm', 'y', 'k', 'w']
    
    #lOf_run_input_list = [["flowerpots_1"], ["aloe_1"], ["monopoly_1"], ["baby1_1"], ["plastic_1"], ["rocks1_1"]]
    #lOf_run_input_list = [["room_1.bmp", "room_2.bmp"], ["papers_1.bmp", "papers_2.bmp"], ["odd_1.bmp", "odd_2.bmp"], ["baby1_1.bmp", "baby1_2.bmp"], ["plastic_1.bmp", "plastic_2.bmp"], ["rocks1_1.bmp", "rocks1_2.bmp"]]
    
    lOf_run_input_list = [['Buildings.0007'], ['Fabric.0018'], ['Buildings.0003'], ['GroundWaterCity.1'], ['WheresWaldo.0001'    ], ['GroundWaterCity.2'], ['PrisonWindow.0002'], ['Clouds.0001'],
                ['Terrain.0010'], ['Bark.0005'], [    'Brick.0002'], ['Tile.0003'], ['Fabric.0002'], ['Fabric.0003'], ['Water.0003'], ['GrassPlantsSky.0002'], ['Fabric.0015'], ['MtValley.0000'],
                ['Buildings.0008'], ['Flowers.0006'], ['GrassLand.0006'], [    'Water.0004'], ['Water.0000'], ['GrassLand.0001'], ['Sand.0005'], ['GrassLand2.2'], ['Grass.0002'], ['GrassLand2.0001'], ['Sand.0001'], ['DocCageCity.0003'], ['PrisonWindow.0004'], ['DocCageCity.0006'], ['Bark.0009'], ['Leaves.0009'], ['Fabric.0000'], ['Tile.0000'], ['PrisonWindow.0010'], ['BrickPaint.1'], ['Sand.0002'], ['Misc.0003'], ['Brick.0004'], ['PrisonWindow.0011'], ['Metal.0001'], [    'Terrain.0009'], ['Food.0009'], ['Tile.0006'], ['Grass.0001'], ['Terrain.0006'], ['Leaves.0011'], ['Terrain.0004'], ['Leaves.0006'], ['Metal.0005'], ['FenceSign.0002'], ['Leaves.0013'], ['Tile.0001'],     ['Food.0007'], ['Wood.0001'], ['Terrain.0007'], ['GrassPlantsSky.0004'], ['GrassLand2.1'], ['Terrain.0003'], ['Paintings.21.0001'], ['Leaves.0004'], ['GrassLand.0000'], ['Brick.0007'], ['Buildings.0010'], ['Leaves.0015'], ['GroundWaterCity.0004'], ['Bark.0011'], ['Fabric.0004'], ['GrassLand.1'], ['GroundWaterCity.0008'], ['Paintings.41.0000'], ['GroundWaterCity.0001'], ['MtValley.1'], ['Fabric.0006'], ['Food.0002'], ['Bark.0012'], ['Food.0000'], ['Buildings.0005'], ['Leaves.0010'], ['Leaves.0016'], ['Stone.0005'], ['PrisonWindow.0005'], ['BrickPaint.0002'], ['Tile.0005'], ['GrassLand2.0000'],     ['Paintings.11.0001'], ['Tile.0007'], ['ValleyWater.2'], ['Paintings.41.0001'], ['PrisonWindow.0001'], ['Tile.0009'], ['Grass.0000'], ['Fabric.0019'], ['Food.0010'], ['ValleyWater.0004'], ['Leaves.0002'], ['Brick.0008'], ['BrickPaint.0000'], ['Tile.0002'], ['GrassLand.0003'], ['FenceSign.0000'], ['Fabric.0007'], ['DocCageCity.0007'], ['Bark.0000'], ['ValleyWater.1'], ['Brick.0001'], ['GrassPlantsSky.0005'], ['Brick.0005'], ['Water.0006'], ['Stone.0003'], ['Wood.0000'], ['Buildings.0000'], ['PrisonWindow.2'], ['Corridor.0001'], ['Brick.0000'], ['Stone.0004'], ['PrisonWindow.0009'], ['Clouds.0000'], ['Terrain.0008'], ['Misc.0000'], ['WheresWaldo.0000'], ['Buildings.0004'], ['Flowers.0003'], [    'Paintings.21.0000'], ['Food.0003'], ['PrisonWindow.0008'], ['Buildings.0002'], ['Bark.0010'], ['ValleyWater.0002'], ['Food.0006'], ['GrassPlantsSky.0003'], ['GrassLand.0005'], ['GrassPlantsSky.1'], [    'BrickPaint.0001'], ['Bark.0003'], ['Fabric.0010'], ['Paintings.11.0003'], ['GroundWaterCity.0007'],     ['Leaves.0005'], ['Leaves.0007'], ['Misc.0001'], ['Flowers.0002'], ['GrassPlantsSky.0001'], ['ValleyWater.0003'], ['PrisonWindow.0003'], ['ValleyWater.0000'], ['Stone.0002'], ['Water.0002'], ['Fabric.0011'], ['Fabric.0016'], ['Fabric.0017'], ['FenceSign.1'], ['Buildings.0009'], ['Tile.0004'], ['Paintings.31.0000'], ['Flowers.0001'], ['DocCageCity.0004'], ['Fabric.0014'], ['Terrain.0002'], ['Terrain.0000'], ['Leaves.0003'], ['GroundWaterCity.0009'], ['PrisonWindow.0006'], ['Water.0001'], ['DocCageCity.0005'], ['Leaves.0012'], ['Water.0007'], ['Sand.0004'], ['Food.0001'], ['GroundWaterCity.0003'], ['Flowers.0005'], ['Metal.0000'], ['Leaves.0014'], ['Paintings.31.0001'], ['Fabric.0013'], ['Buildings.0006'], ['Paintings.11.0004'], ['Bark.0008'], ['DocCageCity.1'], ['ValleyWater.0001'], ['GroundWaterCity.0005'], ['Leaves.0001'], ['PrisonWindow.1'], ['Stone.0000'], ['Misc.0002'], ['Bark.0006'], ['Bark.0004'], ['Bark.0002'], ['Fabric.0005'], ['Corridor.1'], ['Food.0011'], ['Brick.0003'], ['Metal.0002'], ['Buildings.0001'], ['Bark.0001'], ['Water.0005'], ['WheresWaldo.0002'], ['GrassLand.0002'], ['Paintings.11.0000'], ['GrassLand.0004'], ['Fabric.0008'], ['Fabric.0009'], ['Wood.0002'], ['Stone.0001'], ['Flowers.0007'], ['Paintings.1.0001'], ['Food.0004'], ['Metal.0003'], ['Sand.0003'],['GroundWaterCity.0006'], ['Terrain.0001'], ['Sand.0006'], ['GrassPlantsSky.0006'], ['GroundWaterCity.0002'], ['Fabric.0012'], ['DocCageCity.0000'], ['Tile.0008'], ['Tile.0010'], ['Food.0008'], ['PrisonWindow.0000'], ['Leaves.0008'], ['Leaves.0000'], ['Food.0005'], ['Flowers.0000'], ['Paintings.11.0002'], ['Sand.0000'], ['Paintings.1.0000'], ['Flowers.0004'], ['MtValley.0001'], ['Bark.0007'], ['Brick.0006'], ['Metal.0004'], ['DocCageCity.0002'], ['DocCageCity.0001'], ['Fabric.0001'], ['FenceSign.0001'], ['PrisonWindow.0007'], ['Terrain.0005'], ['GroundWaterCity.0000'], ['Corridor.0000']] 

    
    number_of_inputs_used = len(lOf_run_input_list)
    #= [[] for i in range(settings_obj.n_clusters)]
    input_results = map(list, [[]]*number_of_inputs_used) 
    counter = 0
    for val in valueList:
        input_results = map(list, [[]]*number_of_inputs_used) 
        zipped = zip(*val[:-1])  
        for el in zipped:
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
                ax.plot(quality_values_shifted, el[1], symbolsToChooseFrom[counter%len(symbolsToChooseFrom)]+color[counter%len(symbolsToChooseFrom)], label=my_label)
                #ax.plot(quality_values_shifted, el[1], symbolsToChooseFrom[counter%len(symbolsToChooseFrom)]+color[counter%len(symbolsToChooseFrom)], label=val[3])
                counter +=1
            reminder(True,"the following lines which creates a new image every len(symbolsToChooseFrom) should be commented if we use any flag but various_inputs")
            if (counter % len(symbolsToChooseFrom) == 0): 
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
               
    #---comment up to here if not using proviing s4 point
    #--uncomment the following two lines to return back to without s4 inut consideration
#    for el in valueList: 
#        quality_values_shifted = map(lambda x: x+1, el[0]) 
#        ax.plot(quality_values_shifted, el[1], el[2], label=el[3])
#
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

def generateGraph3D(x, y, z, xName, yName, zName):
    fig = plt.figure(figsize=plt.figaspect(0.5)) 
    ax = fig.add_subplot(1, 2, 1, projection='3d') 
    ax.scatter(x, y, z)
    # plt.ylabel(yName)
    # plt.xlabel(xName)
    

# generateGraph3D(x, y, z, "now", "bla", "k")


