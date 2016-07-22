from math import *
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


def generateGraph_for_all(valueList, xName, yName):
    fig, ax = plt.subplots()
    #plt.yscale('log')
    plt.xscale('log')
    plt.ylabel(yName)
    plt.xlabel(xName)
    for el in valueList:
        ax.plot(el[0], el[1], el[2], label=el[3])
    
    # ---- moving the legend outside of the graph (look bellow for placing inside)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.7, box.height])
    # Put a legend to the right of the current axis (note: prop changes the fontsize)
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), prop={'size':8})
    
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


