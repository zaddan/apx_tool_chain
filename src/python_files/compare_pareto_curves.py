import pickle
import copy
import pylab
import sys
import os
from plot_generation import *
import matplotlib.pyplot as plt

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
import datetime
from points_class import *
import pickle
from points_class import *


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
                    print "something went wrong"
                break



    return lOfPoints


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


def main():
    PIK1 = "ref_results_pickled"
    PIK2 = "pareto_curved_combined_pickled" 
     
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
    if (pareto_comparison_mode == "comparison_of_nearest_neighbours"):
        refZipped = zip(curve1FeatureValues[0], curve1FeatureValues[1])
        tobeComparedZipped = zip(curve2FeatureValues[0], curve2FeatureValues[1])
        print "the mean distance between the two curve is:" 
        print np.mean(calc_distance_for_nearest_neighbors_2d(refZipped, tobeComparedZipped))
    if (pareto_comparison_mode == "subsumption_comparison"):
        compare_two_pareto_fronts(curve1FeatureValues, curve2FeatureValues)
    
    # generateGraph(map(lambda x: x.get_PSNR(), lOfParetoPoints1), map(lambda x: x.get_energy(), lOfParetoPoints1), "PSNR", "Energy", symbolsToChooseFrom[symbolIndex])
    # # compare_two_pareto_fronts(PIK1, PIK2)
    # plt.show() 

if __name__ == "__main__":
    main()
