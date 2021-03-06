import error
from math import *
import os.path
from calc_psnr import *
import os
import sys
import matplotlib.pyplot as plt
#import settings
from list_all_files_in_a_folder import *
import numpy
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import numpy as np
from matplotlib import cm
from inputs import *
#from settings import *


def euclid_dis(in1, in2):
    assert (type(in1) == type(in2))  #type checking
    if not(type(in1) is tuple):  #if not a tuple, simply subtract
        return float(in1) - float(in2)
    
    #if tuple:
    in1 = map(lambda x: float(x), in1)
    in2 = map(lambda x: float(x), in2)
    a = numpy.array(in1).flatten();
    b = numpy.array(in2).flatten();
    """ 
    print "here is in1/in2" 
    print in1
    print in2
    if (in1[1] != in2[1]):
        print "they are different"
        print in1[1] - in2[1]
    """ 
    dist = numpy.linalg.norm(a-b)
    return dist

def euclid_dist_from_center(in1):
    try:
        iterator = iter(in1)
    except TypeError:
        return in1
    else:
        in1 = map(lambda x: float(x), in1)
        a = numpy.array(in1).flatten();
        b = [0]*len(in1)
        dist = numpy.linalg.norm(a-b)
        return dist
 

def nearest_neighbors_sorted(x_temp, y_temp) :
    assert(len(x_temp) >0)
    assert(len(y_temp) >0)
    if (len(x_temp) > len(y_temp)):
            x_temp_temp = x_temp
            x_temp = y_temp
            y_temp = x_temp_temp

    x = x_temp
    y = y_temp
    x, y = map(np.asarray, (x, y))
    y_idx = np.argsort(y)
    y = y[y_idx]
    nearest_neighbor = np.empty((len(x),), dtype=np.intp)
    for j, xj in enumerate(x) :
        idx = np.searchsorted(y, xj)
        if idx == len(y) or idx != 0 and y[idx] - xj > xj - y[idx-1] :
            idx -= 1
        nearest_neighbor[j] = y_idx[idx]
        y = np.delete(y, idx)
        y_idx = np.delete(y_idx, idx)
    return nearest_neighbor

#nearst_neighbors = nearest_neighbors_sorted([2,1,99], [0, 50,100,10])
def calc_error_for_nearest_neighbors(x_temp,y_temp):
    assert(len(x_temp) >0)
    assert(len(y_temp) >0)
    if (len(x_temp) > len(y_temp)):
        x_temp_temp = x_temp
        x_temp = y_temp
        y_temp = x_temp_temp
    x = x_temp
    y = y_temp
    error = [] 
    nearst_neighbors = nearest_neighbors_sorted(x,y)
    print "here is x"
    print x
    print "here is y"
    print y
    for i in range(min(len(x), len(y))):
        error.append(abs(x[i] - y[nearst_neighbors[i]]))
    return error


def find_dis(x,y):
    return ((float(x[0]) - float(y[0]))**2 + (float(x[1]) - float(y[1]))**2)



#calculating the nearest neigbour for two lists of 2 dimension
def nearest_neighbors_2d(x, y) :
    #x, y = map(np.asarray, (x, y))
    #y = y.copy()
    y_idx = range(len(y))
    nearest_neighbor = np.empty((len(x),), dtype=np.intp)
    for j, xj in enumerate(x) :
        #idx = np.argmin(map(lambda xtemp, ytemp : np.linalg.norm(ytemp, xtemp), y , xj))
        dist = map(lambda ytemp: euclid_dis(xj, ytemp), y )
        idx = np.argmin(np.asarray(dist))
        nearest_neighbor[j] = y_idx[idx]
        del y[idx] 
        del y_idx[idx] 

    return nearest_neighbor

#turning a list of tuples to dictionary. keep in mind that in this implementation
#the keys are selected from the 3rd, and 4th element of the each tuple
#also plz note the int() conversion since it mattered for the specific benchmark that I was 
#using this for
def dictionarize(mylist):
    mydict = {}
#    for el in mylist:
#        if not((int(float(el[2])),int(float(el[3]))) in  mydict.keys()):
#            mydict[(int(float(el[2])), int(float(el[3])))] = [(el[0], el[1])]
#        else: 
#            mydict[(int(float(el[2])), int(float(el[3])))].append((el[0], el[1]))
#
    for el in mylist:
        if not(int(float(el[3])) in  mydict.keys()):
            mydict[int(float(el[3]))] = [(el[0], el[1], el[2])]
        else: 
            mydict[int(float(el[3]))].append((el[0], el[1], el[2]))
    
    
    
    return mydict

#calculating the error ass with 2d array (note that this uses nearest neighbour
#as the error calculation method)
def calc_error_for_nearest_neighbors_2d(accurate_values, current_values, settings_obj):
    error = [] 
    #---turn the lists into dictionaries 
    mydict_of_acc = dictionarize(accurate_values)
    mydict_of_cur = dictionarize(current_values);
    
    for key in mydict_of_cur.keys():  #go through each key and cal error
        if  key in mydict_of_acc.keys():
            #make sure ref1 is the small list 
            if len(mydict_of_acc[key]) > len(mydict_of_cur[key]):
                ref1 = mydict_of_acc
                ref2 = mydict_of_cur
            else:
                ref2 = mydict_of_acc
                ref1 = mydict_of_cur
            
            #get the list of indecies of nearest neighbors
            indecies = nearest_neighbors_2d(ref2[key][:], ref1[key][:])
            #calculate error 
            for i in range(len(indecies)):
                error.append(tuple(numpy.subtract(ref2[key][i], ref1[key][indecies[i]])))
                #error.append(find_dis(ref2[key][i], ref1[key][indecies[i]]))
    if (len(error) == 0  and not(settings_obj.benchmark_name == "sift")):
        print "assert(len(error)>0) unless benchmark =sift"
        exit(0)
    """
    if (settings.benchmark_name == "sift"):
        if len(error) == 0: #the reason for it to be None is b/c in sift there is a 
                          #possibility that the octaves (with sift points) don't overlap 
            error = float("inf")
    """
    return error







global_counter = 0
## 
# @brief : name is self explanatory
# 
# @param accurateValues
# @param currentValues
# 
# @return 
def calculateError(accurateValues, currentValues, settings_obj):
    
    result = [] 
#    global global_counter 
#    global_counter +=1
#    if (global_counter % 10 == 9):
#        accurateValues = []
    try: 
        if (accurateValues == None or len(accurateValues)==0):
            raise error.AccurateValueNoneError
        if (currentValues== None or len(currentValues)==0):
            raise error.CurrentValueNoneError
        if not(len(accurateValues) == len(currentValues)):
            print "--- len of acc and cur vals are not the same" 
            print "accvals:" + str(accurateValues) 
            print "curvals " + str(currentValues)
            raise error.NoneLengthEqualityError
    
    except error.AccurateValueNoneError as er:
            raise error.WithinCalcError(type(er).__name__)
            exit()
    except error.CurrentValueNoneError as er:
            raise error.WithinCalcError(type(er).__name__)
            exit()
    except error.NoneLengthEqualityError  as er:
            raise error.WithinCalcError(type(er).__name__)
            exit()




    if (settings_obj.error_mode == "corresponding_elements"): 
        if not(len(accurateValues) == len(currentValues)):
            print "**********ERRR********" 
            print "here is the accurate values: " + str(accurateValues)
            print "here is the current values: " + str(currentValues)
            print "number of results subelements for currentValues and accuratValues are not the same"
            print "check the " + settings_obj.rawresultFileName + " file"
            print "**********ERROR********" 
            exit()
        
        #result = 0 
        if type(accurateValues[0]) is tuple:
            result = map(lambda x: tuple(numpy.subtract(x[1],x[0])),  zip(accurateValues,currentValues))
        else:  
            result = map(lambda x: (numpy.subtract(x[1],x[0])),  zip(accurateValues,currentValues))
        #for accurateValue,currentValue in zip(accurateValues,currentValues):
        #    result += [(euclid_dis(accurateValue, currentValue))]
            #result += pow(float(accurateValue) - float(currentValue), 2)
        #print "acc vals" +str(accurateValues)
        #print "cur vals" + str(currentValues)
        #print "result of subtraction"  + str(result)
    elif (settings_obj.error_mode == "nearest_neighbors"): 
        result = calc_error_for_nearest_neighbors(map(lambda x: float(x), accurateValues), map(lambda x: float(x), currentValues))
    elif (settings_obj.error_mode == "nearest_neighbors_2d"): 
        if (settings_obj.benchmark_name == "sift"): 
            result = calc_error_for_nearest_neighbors_2d(accurateValues , currentValues, settings_obj)
        else:
            print "*****ERRR****"
            print "nearest neigbour for benchmarks other than sift has not yet. There are minor changes that need to be applied to calc_error_for_nearest_neighbors_2d function to allow this"
            sys.exit()
    elif (settings_obj.error_mode == "image"): 
        result = [1] #this shouldn't mattejjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjr
    else:
        print "***ERRR: this mode:" + str(settings_obj.error_mode) + "  is not defined"
        sys.exit()
    #print "here is the error calculated"
    #print result
    
    return result
    #return sqrt(result)/len(accurateValues)


def extractCurrentValuesForOneInput(sourceFileName, inputObj, settings_obj):
    start = 0 
    currentValues = []
    #whether the file exist or no 
    if not(os.path.isfile(sourceFileName)):
        print "source file with the name " + sourceFileName + "doesn't exist"
        exit();
    
    if (settings_obj.error_mode == "image"): #this means we are dealing with an image,
                                         #in the case of an image, we don't write the 
                                         #pixel values into the output text file
                                         #but keep it in the .png file (and never update
                                         #the usual output file located in the generated_text/
                                         #csource_output_folder
        
        refImageRVal, refImageGVal, refImageBVal, img_size = get_RGB_values(inputObj.noisyImage)
        return refImageRVal + refImageGVal + refImageBVal
    else: 
        with open(sourceFileName) as f:
            for line in f:
                if len(line.split()) >0: 
                    for words in line.rstrip().replace(',', ' ').replace('/',' ').replace(';', ' ').split(' '): #find the lines with key word and write it to another file
                        if "end" in words: 
                            if (settings_obj.outputMode == "uniform"): 
                                flattened  = [val for sublist in currentValues for val in sublist]                            
                                return flattened
                            else: 
                                return zip(*(currentValues[settings_obj.outputNumber_lower_bound_element:]))#if havn't gotten accurate values
                        elif (start==1):
                            #currentValues = [maplambda x:, (line.rstrip().split())]
                            currentValues = [map(lambda x:float(x), (line.rstrip().split()))]
                            start +=1
                            break 
                        elif "start" in words: 
                            start = 1 
                            break
                        elif (start >1):
                            #currentValues.append((line.rstrip().split()))
                            currentValues.append(map(lambda x:float(x), (line.rstrip().split())))
                            break
                        else:
                            break



## 
# @brief name is explantory
# 
# @param sourceFileName
# 
# @return 
def extractInputFileName(sourceFileName):
    start = 0 
    #whether the file exist or no 
    if not(os.path.isfile(sourceFileName)):
        print "source file with the name " + sourceFileName + "doesn't exist"
        exit();
    with open(sourceFileName) as f:
        for line in f:
            if len(line.split()) >0: 
                for words in line.rstrip().replace(',', ' ').replace('/',' ').replace(';', ' ').split(' '): #find the lines with key word and write it to another file
                    if ("INPUT" in words): 
                        return line.split()[3]
    print "*****ERROR*******"
    print "the source file with the name of: " + str(sourceFileName) + " required for getting the inputFileName does not contain the proper format"
    print "*****ERROR******"
    




def calculateAdderEnergy(numberOfBits):
#    print "&&&" 
#    print numberOfBits
#    print "&&&" 
    return numberOfBits



def calculateMultiplierEnergy(numberOfBits):
    return 31*calculateAdderEnergy(numberOfBits)

## 
# @brief : name is self explanatory
# 
# @param accurateValues
# @param currentValues
# 
# @return 
def calculateEnergy(operatorNumberOfBitsList, settings_obj):
    with open("../../" + settings_obj.generatedTextFolderName + "/energy_result.txt") as f:
        for line in f:
            for words in line.split():
                print "energyval: " + str(words);
                result = float(words); 
                sys.stdout.flush()


    if not(os.path.exists("../../" + settings_obj.generatedTextFolderName + "/energy_result.txt")):
        print "file doesn't exist" 
        sys.exit()
    os.system("rm ../../" + settings_obj.generatedTextFolderName + "/energy_result.txt")
    return result
    result = 0 
    for element in operatorNumberOfBitsList:
        if (element[0][-1] == 'a'):  #it is an adder
            result += calculateAdderEnergy(float(element[1])) 
        elif (element[0][-1] == 'm'):  #it is an mulitplier 
            result += calculateMultiplierEnergy(float(element[1])) 
        else:
            print "**************************ERROR*****************"
            print "the operator with the name: " + element[0] + " is operator is not defined"
            exit()
    
    return result 

## 
# @brief name is explantory
# 
# @param sourceFileName
# 
# @return 
def extractEnergyAndConfig(sourceFileName):
    start = 0 
    values = []
    configValues = []
    config = [] 
    #whether the file exist or no 
    if not(os.path.isfile(sourceFileName)):
        print "************EROR******" 
        print "the source file with the Name " + sourceFileName + " necessary for calculateing energy does not exist"

        exit();
    energy = [] 
    
    with open(sourceFileName) as f:
        for line in f:
            if len(line.split()) > 0: 
                for words in line.rstrip().replace(',', ' ').replace('/',' ').replace(';', ' ').split(' '): #find the lines with key word and write it to another file
                    values.append((line.split()[0], int(line.split()[1]) - int(line.split()[2])))
                    configValues.append(line.rstrip())
                    break


    return [configValues]


## 
# @brief self explan
# 
# @param sourceFileName
# 
# @return 
#def extract_properties(operatorSampleFileName, rawResultsFolderName, resultFileName, gotAccurateValue, accurateValues, operandFileName):
#    inputFileNameList = [] 
#    error = [] 
#    if not(os.path.isdir(rawResultsFolderName)):
#        print "rawResultFolder with the Name " + rawResultsFolderName + " does not exist"
#        exit();
# 
#    nameOfAllResultsList = getNameOfFilesInAFolder(rawResultsFolderName)
#    #config = extractEnergyAndConfig(operatorSampleFileName)
#    error = extractErrorForOneInput(resultFileName, gotAccurateValue, accurateValues)
#    result = error
#    
#    return result
#


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#******The rest of the file is for testing the modules defined above
def energyTest():
	#testing the modules defined in this file
	#print calculateEnergy([4,6])
	print extractEnergyAndConfig(repo_root_address  + "/apx_tool_chain/input_output_text_files/all_possible_apx_operators_scenarios.txt")
	
	
def errorTesting():
	#testing the modules defined in this file
	#print calculateError([4,6],[4,0,3])
	print extractErrorForOne(repo_root_address + "/apx_tool_chain/input_output_text_files/raw_result_foraw_results.txt")




def extractPropertyTest():
    energy, error= extract_properties(repo_root_address + "/apx_tool_chain/input_output_text_files/all_possible_apx_operators_scenarios.txt",repo_roo_address + "/apx_tool_chain/input_output_text_files/raw_result_folder")
    print energy
    for errorElement in error:
        print errorElement

#energyTest()
#errorTesting()
#extractPropertyTest()
