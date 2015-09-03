import pickle
import copy
import pylab
import sys
import os

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


if len(sys.argv) < 2:
    print "******ERROR***"
    print "the following inputs with the order mentioned needs to be provided"
    print "1.pickle file containing the first pareto curve "
    print "2.pickle file containing the second pareto curve"

for index, element in enumerate(sys.argv):
    if element.split("/")[0] == "~":
        sys.argv[index] = home + sys.argv[index][1:]

PIK1= sys.argv[1] #src file to be analyzet
PIK2 = sys.argv[2] #src file to be analyzet

lOfOperandSetFile1 = [] 
lOfNoiseFile1= [] 
lOfEnergyFile1= [] 

lOfOperandSetFile2 = [] 
lOfNoiseFile2= [] 
lOfEnergyFile2= [] 


with open(PIK1, "rb") as f:
    # pickle.load(f)
    while True: 
        try: 
            operandSetItem = pickle.load(f)# 
            lOfOperandSetFile1.append(operandSetItem)# 
            # listOfPeople.append(copy.copy(person))# 
        except Exception as ex:
            if not (type(ex).__name__ == "EOFError"):
                print type(ex).__name__ 
                print ex.args
            break


with open(PIK2, "rb") as f:
    # pickle.load(f)
    while True: 
        try: 
            operandSetItem = pickle.load(f)# 
            lOfOperandSetFile2.append(operandSetItem)# 
            # listOfPeople.append(copy.copy(person))# 
        except Exception as ex:
            if not (type(ex).__name__ == "EOFError"):
                print type(ex).__name__ 
                print ex.args
            break

resultTuple = [] 
noiseRequirement = [400, 600]
operandSetdiffList = []
operandSet_paretoDiffDic = {}
for index in range(len(lOfOperandSetFile1)):
    
    operandSetFile1 = lOfOperandSetFile1[index]
    operandSetFile2 = lOfOperandSetFile2[index]
    diffList = []  
    for noise in noiseRequirement:
        for index1, point in enumerate(operandSetFile1.get_lOf_pareto_points()):
            if noise == point.get_noise():
                file1OptimalPoint =  operandSetFile1.get_lOf_pareto_points()[index1 -1]
            elif noise < point.get_noise():
                if (index1 == 0): 
                    print "no point satisfied this requirement"
                    exit() 
                else: 
                    file1OptimalPoint =  operandSetFile1.get_lOf_pareto_points()[index1 -1]
                break;
        
        for index2, point in enumerate(operandSetFile2.get_lOf_pareto_points()):
            if noise == point.get_noise():
                file2OptimalPoint =  operandSetFile2.get_lOf_pareto_points()[index2 -1]
            elif noise < point.get_noise():
                if (index2 == 0): 
                    print "no point satisfied this requirement"
                    exit() 
                else: 
                   file2OptimalPoint =  operandSetFile2.get_lOf_pareto_points()[index2 -1]
                break;
        print "***************"
        print file1OptimalPoint.get_noise()
        print file1OptimalPoint.get_energy()
        print file2OptimalPoint.get_noise()
        print file2OptimalPoint.get_energy()
        print "*******************" 

        diffList.append(distance.euclidean((file1OptimalPoint.get_noise(), file1OptimalPoint.get_energy()), (file2OptimalPoint.get_noise(), file2OptimalPoint.get_energy())))
    
    operandSet_paretoDiffDic[tuple(lOfOperandSetFile1[index].get_operands_values())] = sum(diffList)      /len(diffList)

print operandSet_paretoDiffDic

