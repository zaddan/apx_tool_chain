import random
import sys
import copy
import math
import numpy
import settings 
import input_list
from deap import algorithms
from points_class import *
from deap import base
from deap import creator
from deap import tools
from simulating_annealer import *
from inputs import *
import operator
from move_objs import *
from misc2 import *
from error import *
from joblib import Parallel, delayed                                                              
import multiprocessing


# ---- probabilistic algorithm 
def extract_move(pt1, pt2):
    if ((pt1.get_energy() <= pt2.get_energy()) and (pt1.get_quality()<= pt2.get_quality())):
        #print "now: " + str((pt1.get_energy(), pt1.get_quality())) + " " +str((pt2.get_energy(), pt2.get_quality())) 
        return (map(operator.sub, pt1.get_raw_setUp(), pt2.get_raw_setUp()))
    else:
        return []


def collect_moves_of_interest(strategy, list_of_points):
    moves = [] 
    if (strategy == "all"):
        lOfAllPointsTried = list_of_points 
        print "total legnth of lOfAllPointsTried" + str(len(lOfAllPointsTried)) 
        counter = 0 
        for x in range(len(lOfAllPointsTried)):
            for y in range(x+1,len(lOfAllPointsTried)):
                counter +=1; 
                extracted_move =  extract_move(lOfAllPointsTried[x], lOfAllPointsTried[y])
                if (len(extracted_move) > 0):
                    new_move = move_obj(extracted_move, 1) 
                    moves.append(copy.deepcopy(new_move))
                if((counter % 10000) == 0):
                    print "counter: " + str(counter)
    if(strategy == "pareto_by_pareto"):
        lOfAllPointsTried = list_of_points 
        lOfAllPointsTried_cleaned_of_doubles = clean_doubles(lOfAllPointsTried)
        all_pareto_fronts_list = all_pareto_frontiers(lOfAllPointsTried_cleaned_of_doubles, maxX, maxY)
        #print all_pareto_fronts_list 
        for index in range(len(all_pareto_fronts_list) - 1):
            lone = all_pareto_fronts_list[index]
            ltwo = all_pareto_fronts_list[index+1]
            for x in range(len(lone)):
                for y in range(len(ltwo)):
                    extracted_move =  extract_move(lone[x], ltwo[y])
                    if (len(extracted_move) > 0):
                        new_move = move_obj(extracted_move, len(all_pareto_fronts_list)-index) 
                        moves.append(copy.deepcopy(new_move))

    return moves

#def stringify_list(inp):
#    map(lambda x: x.stringify_val())
     
def histogramize_list(l_move):
    my_histogram = {} 
    for el in l_move:
        if el.get_stringified_val() in my_histogram.keys():
            my_histogram[el.get_stringified_val()] +=1
        else:
            my_histogram[el.get_stringified_val()] = el.get_strength()
    return my_histogram

def apply_move_to_individual(individual, move):
    return map(operator.add, individual, move)


#**--------------------**
#**--------------------**
#----disclaimers::: if dealingwith Pic and we are feeding couple of operands,
#----we need to collect their psnr in a list and get an avg. This should be done
#--- this requries adding a PSNR (or SNR) list to the points
#**--------------------**
#--------------------**
def return_conf(config):
    number = 0 
    allConfsLenght = len(config) 
    while True:
        if (number >= allConfsLenght):
            return
        
        yield config[number][2]
        number += 1


def evalOneMax(individual):
    return sum(individual),

# def specializedMutate(individual):
    # individual[1] = int(random.gauss(16 , 5.2))
    # individual[0] = int(random.gauss(16 , 5.2))
    # return individual, 

def modifyOperatorSubSetupExactly(operator, numberOfApxBits):
    operatorType =  operator[0].replace("'", "")
     
    if operatorType == "btm":  
        return ['btm' , operator[1] , numberOfApxBits]
    elif operatorType == "bta":  
        return ['bta' ,operator[1], numberOfApxBits, operator[3], operator[4]] 
    else:
        print "***************ERROR***************"
        print "the operator type with the name of " + operatorType + "is not acceptable"
        exit()

def specializedMutate(ignoreIndexList, settings_obj, setUp):
    newSetUp = copy.copy(setUp)
    operatorToChooseIndex = random.choice(range(0, len(setUp)))
    # numberOfApxBits = int(random.gauss(10 , 5.2))
    numberOfApxBits = int(random.choice(range(settings_obj.apxLowBound, settings_obj.apxUpBound)))
    newSetUp[operatorToChooseIndex] = numberOfApxBits 
#    if operatorToChooseIndex in ignoreIndexList:
#        return newSetUp,
#    operatorModified = modifyOperatorSubSetupExactly(setUp[operatorToChooseIndex], numberOfApxBits) 
#    newSetUp[operatorToChooseIndex] = operatorModified
    return newSetUp,
    

def generate_possibly_worse_case_setup(accurateSetUp, settings_obj):
    population = [] 
    newSetUp = copy.copy(accurateSetUp)
    for index, element in enumerate(newSetUp): 
        # operatorToChooseIndex = random.choice(range(0, len(accurateSetUp)))
        # numberOfApxBits = int(random.gauss(10 , 4))
        numberOfApxBits = settings_obj.worseCase
        
        operatorModified = modifyOperatorSubSetupExactly(accurateSetUp[index], numberOfApxBits) 
        newSetUp[index] = operatorModified
    population.append(copy.deepcopy(newSetUp)) 
    return population
 

def generateInitialPopulation(accurateSetUp, numberOfIndividualsToStartWith,inputObj, ignoreIndexList, limitedListValues, limitedListIndecies, settings_obj):
    population = [] 
    population.append(accurateSetUp) 
    for count in range(numberOfIndividualsToStartWith - 1):
        newSetUp = copy.copy(accurateSetUp)
        for index, element in enumerate(newSetUp): 
            if (index in ignoreIndexList):
                continue
            # operatorToChooseIndex = random.choice(range(0, len(accurateSetUp)))
            # numberOfApxBits = int(random.gauss(10 , 4))
            if (index in limitedListIndecies):
                numberOfApxBits = int(random.choice(limitedListValues[index]))
            else: 
                numberOfApxBits = int(random.choice(range(settings_obj.apxLowBound, settings_obj.apxUpBound)))
            
            operatorModified = modifyOperatorSubSetupExactly(accurateSetUp[index], numberOfApxBits) 
            newSetUp[index] = operatorModified
        population.append(copy.deepcopy(newSetUp)) 
    return population
 

def doNothing(individual):
    return individual,


# ---- redefinging the eaMulPlusLambda to have a better understanding
# ---- and control over it
def eaMuPlusLambda_redefined(population, toolbox, MU, LAMBDA, CXPB, MUTPB, NGEN):
    for i in range(NGEN):
        # ----determine the offspring and evaluate the fitness,w
        offspring = algorithms.varOr(population, toolbox, LAMBDA, CXPB, MUTPB)
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        
        # ---- evaluate fitness values for the population
        invalid_ind = [ind for ind in population if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        
        population = toolbox.select(offspring + population, MU) 

    return population

   
def specializedEval_multiple_inputs(normalize,possibly_worse_case_result_quality, _mld_ , ignoreListIndecies, accurateSetUp, inputObj, nameOfAllOperandFilesList, rootResultFolderName,executableName,
        executableInputList, CBuildFolder, operandSampleFileName, lOfAccurateValues, allPointsTried, collect_pts, unique_point_list, output_list, previous_ideal_setUp,iteration, settings_obj,
        run_input_list, lOf_accurateValues, individual):
    if inputObj.quality_calc_mode in ["avg", "worse_case"]:
        reminder(True, "quality_calc_mode  of avg and worse_case has not been verified for other benchmarks besides jpeg")
        #assert(inputObj.benchmark_name == "jpeg")
        collect_pts = False
        reminder(True, " can not collect points when quality_calc_mode is avg or worse_case")
        l_energy = []
        l_quality = []
        for index,input_val in enumerate(input_list.lOf_run_input_list):
            lOfAccurateValues = [lOf_accurateValues[index]]
            print "changed the lOfAccurateValues" + str(lOfAccurateValues)
            print input_val
            inputObj.set_run_input(input_val) 
            print "input_val " + str(input_val) 
            energy, quality = specializedEval(normalize,possibly_worse_case_result_quality, _mld_ , ignoreListIndecies, accurateSetUp, inputObj, nameOfAllOperandFilesList, rootResultFolderName,executableName,
        executableInputList, CBuildFolder, operandSampleFileName, lOfAccurateValues, allPointsTried, collect_pts, unique_point_list, output_list, previous_ideal_setUp,iteration, settings_obj,
        input_val, individual)
            l_energy.append(energy)
            l_quality.append(quality)
        if (inputObj.quality_calc_mode == "avg"): 
            print "l_energy " + str(l_energy)
            print "l_quality" + str(l_quality)
            print "indi" + str(individual)
            return (numpy.mean(l_energy), numpy.mean(l_quality))
        elif(inputObj.quality_calc_mode == "worse_case"):
            return (numpy.min(l_energy), numpy.min(l_quality))
        else:
            print "this quality_calc_mode " + inputObj.quality_calc_mode + " is not defined"
            sys.exit()
    elif inputObj.quality_calc_mode in ["individual"]:
        energy, quality = specializedEval(normalize,possibly_worse_case_result_quality, _mld_ , ignoreListIndecies, accurateSetUp, inputObj, nameOfAllOperandFilesList, rootResultFolderName,executableName,
        executableInputList, CBuildFolder, operandSampleFileName, lOfAccurateValues, allPointsTried, collect_pts, unique_point_list, output_list, previous_ideal_setUp,iteration, settings_obj,
        run_input_list, individual)
        return (energy,quality)


def specializedEval(normalize,possibly_worse_case_result_quality, _mld_ , ignoreListIndecies, accurateSetUp, inputObj, nameOfAllOperandFilesList, rootResultFolderName,executableName,
        executableInputList, CBuildFolder, operandSampleFileName, lOfAccurateValues, allPointsTried, collect_pts, unique_point_list, output_list, previous_ideal_setUp,iteration, settings_obj,
        run_input_list, individual):
        exe_annex = 0
        if (settings_obj.runMode == "parallel"): 
            if(multiprocessing.current_process()._identity == ()):
                exe_annex = 0
            else:
                exe_annex = multiprocessing.current_process()._identity[0] - 1
            print "proccess id: " 

        #print "-----end" 
        #print multiprocessing.current_process()
        #--- zeroing out the ignoreList 
        for x in ignoreListIndecies:
            individual[x] = previous_ideal_setUp[x]
        newSetUp = modifyMold(accurateSetUp, individual) 
        sys.stdout.flush() 
        newPoint = points() 
        newPoint.set_dealing_with_pics(eval(inputObj.dealingWithPics))
        for operandIndex, operandSampleFileName in enumerate(nameOfAllOperandFilesList):
            if (settings_obj.runMode == "parallel"): 
                CSourceOutputForVariousSetUpFileName =  rootResultFolderName + "/" + settings_obj.rawResultFolderName + "/" + settings_obj.csourceOutputFileName + str(exe_annex) + ".txt" #where to collect C++ source results
                operatorSampleFileFullAddress = rootResultFolderName + "/"+ settings_obj.operatorSampleFileName + str(exe_annex) + ".txt"
            else: 
                CSourceOutputForVariousSetUpFileName =  rootResultFolderName + "/" + settings_obj.rawResultFolderName + "/" + settings_obj.csourceOutputFileName + str(0) + ".txt" #where to collect C++ source results
                operatorSampleFileFullAddress = rootResultFolderName + "/"+ settings_obj.operatorSampleFileName + str(0) + ".txt"

            open(CSourceOutputForVariousSetUpFileName, "w").close()

            modifyOperatorSampleFile(operatorSampleFileFullAddress, newSetUp)

            print "input to operate on:" + str(run_input_list) 
            print "input's index"+ str(input_list.lOf_run_input_list.index(run_input_list))
            if not(settings_obj.errorTest): #if errorTest generate acc.txt and apx.txt which contain accurate and apx values
                make_run(executableName, executableInputList, rootResultFolderName, CSourceOutputForVariousSetUpFileName, CBuildFolder, operandSampleFileName, inputObj.bench_suit_name,exe_annex,
                        settings_obj, run_input_list) 
            # print "here is the accurate" + str(lOfAccurateValues) 
            input_index = input_list.lOf_run_input_list.index(run_input_list)
            accurate_design_energy = input_list.lOf_accurate_points_energy[input_index]
            energyValue = [float(getEnergy(newSetUp, settings_obj))/float(accurate_design_energy)]
            if (settings_obj.errorTest):
                newPath = "/home/local/bulkhead/behzad/usr/local/apx_tool_chain/src/python_files/scratch/apx.txt"
                if(settings_obj.errorTest):
                    print "Acurate Vals:"
                    print lOfAccurateValues
                    errantValues =  extractCurrentValuesForOneInput(newPath, inputObj, settings_obj)
                    print "errant Vals:" 
                    print errantValues
                    errorValue = [calculateError(lOfAccurateValues[operandIndex],errantValues, settings_obj)]
                    print "error Vals:"
                    print errorValue 
                    print "------" 
            else:
                errantValues =  extractCurrentValuesForOneInput(CSourceOutputForVariousSetUpFileName, inputObj, settings_obj)
                try: 
                    errorValue = [calculateError(lOfAccurateValues[operandIndex], errantValues, settings_obj)]
                except WithinCalcError as er:
                    raise WithinSpecEval(er.error_name, map(lambda x: x, individual))
                
                #print "Acurate Vals:" + str(lOfAccurateValues)
                #print "errant Vals:" +str(errantValues)
                #print "error Vals:" + str(errorValue)

            #here sys 
            configValue = [newSetUp]
            rawValues = [extractCurrentValuesForOneInput(CSourceOutputForVariousSetUpFileName, inputObj, settings_obj)]
            #print errorValue
            # print "where" 
            # print errorValue 
            newPoint.append_raw_values(rawValues[0])  
            newPoint.append_error(errorValue[0])
            newPoint.set_energy(energyValue[0])
            #newPoint.set_raw_setUp(individual)
            newPoint.set_raw_setUp(map(lambda x: x, individual))
            newPoint.set_setUp(configValue[0])
            newPoint.append_lOf_operand(get_operand_values(operandSampleFileName))
            newPoint.append_accurate_values(lOfAccurateValues[operandIndex])
            newPoint.set_dealing_with_pics(eval(inputObj.dealingWithPics)) 
            newPoint.set_dealing_with_pics(eval(inputObj.dealingWithPics)) 
            newPoint.set_input_obj(inputObj)
            if (eval(inputObj.dealingWithPics)):
                newPoint.calculate_PSNR()



        # print "here is the config " + str(newPoint.get_setUp())
        newPoint.set_input_number(iteration) 
        if not(eval(inputObj.dealingWithPics)):
            newPoint.calculate_quality(normalize, possibly_worse_case_result_quality, settings_obj, input_list.lOf_accurate_points_quality[input_index])
            if (settings_obj.DEBUG):
                print "quality is: " + str(newPoint.get_quality())
            if (settings_obj.errorTest):
                print "quality is" 
                print newPoint.get_quality()
                sys.exit()
            #print "here is my quality values"
            #print newPoint.get_quality()
        if eval(inputObj.dealingWithPics):
            if (collect_pts): 
                allPointsTried.append(newPoint)
                update_unique(newPoint, output_list, unique_point_list)
            return (newPoint.get_energy(), newPoint.get_PSNR())
        else:
            if(collect_pts): 
                allPointsTried.append(newPoint)
                update_unique(newPoint, output_list, unique_point_list)
            return (newPoint.get_energy(), newPoint.get_quality())


def run_SP(population, NGEN_to_use,
        CSourceOutputForVariousSetUpFileName, operatorSampleFileFullAddress, 
        executableName, executableInputList, rootResultFolderName, 
        CBuildFolder, operandSampleFileName, lOfAccurateValues, nameOfAllOperandFilesList, inputObj, ignoreListIndecies, possibly_worse_case_result_quality,accurateSetUp, allConfs, unique_point_list,
        output_list, allPointsTried, previous_ideal_setUp, settings_obj):
   
    def generate(size, pmin, pmax, smin, smax):
        part = creator.Particle(random.uniform(pmin, pmax) for _ in range(size)) 
        part.speed = [random.uniform(smin, smax) for _ in range(size)]
        part.pmin = pmin
        part.pmax = pmax
        part.smin = smin
        part.smax = smax
        return part
    

    def updateParticle(part, best, phi1, phi2):
        u1 = (random.uniform(0, phi1) for _ in range(len(part)))
        u2 = (random.uniform(0, phi2) for _ in range(len(part)))
        v_u1 = map(operator.mul, u1, map(operator.sub, part.best, part))
        v_u2 = map(operator.mul, u2, map(operator.sub, best, part))
        part.speed = list(map(operator.add, part.speed, map(operator.add, v_u1, v_u2)))
        for i, speed in enumerate(part.speed):
            if (speed+part[i])<part.pmin or (speed + part[i]) > part.pmax:
                part.speed[i] = 0
            elif speed < part.smin:
                part.speed[i] = part.smin
            elif speed > (part.smax) :
                part.speed[i] = part.smax
        
        part[:] = list(map(operator.add, part, part.speed))  

    #allPointsTried = []
    if (settings_obj.maxX):
            x_direction = 1
    else:
        x_direction = -1

    if (settings_obj.maxY):
        y_direction = 1
    else:
        y_direction = -1

    MU = settings_obj.MU#number of indi for the next gen
    LAMBDA = settings_obj.LAMBDA#number of children
    CXPB = settings_obj.CXPB 
    MUTPB = settings_obj.MUTPB
    creator.create("FitnessMin", base.Fitness, weights=(x_direction, y_direction))
    creator.create("Particle", list, fitness=creator.FitnessMin, speed=list, 
               smin=None, smax=None, best=None, pmin=None, pmax=None)
    toolbox = base.Toolbox()
    toolbox.register("particle", generate, size=len(allConfs[0]), pmin=0, pmax=17, smin=0, smax=12)
    toolbox.register("population", tools.initRepeat, list, toolbox.particle)
    toolbox.register("update", updateParticle, phi1=2.0, phi2=2.0)
    toolbox.register("evaluate", specializedEval, True, possibly_worse_case_result_quality, accurateSetUp, ignoreListIndecies, accurateSetUp, inputObj, nameOfAllOperandFilesList, rootResultFolderName,
            executableName, executableInputList, CBuildFolder, operandSampleFileName, lOfAccurateValues, allPointsTried, True, unique_point_list, output_list, previous_ideal_setUp, iteration,
            settings_obj, run_input_list)
       
    pop = toolbox.population(n=settings_obj.numberOfIndividualsToStartWith)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)
    logbook = tools.Logbook()
    logbook.header = ["gen", "evals"] + stats.fields
    best = None
    
    for g in range(NGEN_to_use):
        for part in pop:
            part.fitness.values = toolbox.evaluate(part)
            if not part.best or part.best.fitness < part.fitness:
                part.best = creator.Particle(part)
                part.best.fitness.values = part.fitness.values
            if not best or best.fitness < part.fitness:
                best = creator.Particle(part)
                best.fitness.values = part.fitness.values
        for part in pop:
            toolbox.update(part, best)

        # Gather all the fitnesses in one list and print the stats
        logbook.record(gen=g, evals=len(pop), **stats.compile(pop))
        print(logbook.stream)
    
    
    
    return pop


def run_spea2(population, 
        CSourceOutputForVariousSetUpFileName, operatorSampleFileFullAddress, 
        executableName, executableInputList, rootResultFolderName, 
        CBuildFolder, operandSampleFileName, lOfAccurateValues, nameOfAllOperandFilesList, inputObj, ignoreListIndecies, possibly_worse_case_result_quality,accurateSetUp, allConfs, NGEN, MU, LAMBDA,
        unique_point_list, output_list, allPointsTried, previous_ideal_setUp,
        iteration, settings_obj, run_input_list, lOf_accurateValues):
    
    
    #allPointsTried = []
    if (settings_obj.maxX):
            x_direction = 1
    else:
        x_direction = -1

    if (settings_obj.maxY):
        y_direction = 1
    else:
        y_direction = -1


    
    
    #NGEN = settings.NGEN
    #MU = settings.MU#number of indi for the next gen
    #LAMBDA = settings.LAMBDA#number of children
    CXPB = settings_obj.CXPB 
    MUTPB = settings_obj.MUTPB
    
    reminder(settings_obj.reminder_flag, "xdirectino and y_direction are reverese b/c I was returning them in a reverse direction");
    creator.create("FitnessMin", base.Fitness, weights=(y_direction,  x_direction))
    creator.create("Individual", list, fitness=creator.FitnessMin)
    toolbox = base.Toolbox()
    
    # generating the initial population
    
    
    
    # Operator registering
    toolbox.register("individual", tools.initRepeat, creator.Individual)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    toolbox.register("evaluate", specializedEval_multiple_inputs, True, possibly_worse_case_result_quality, accurateSetUp, ignoreListIndecies, accurateSetUp, inputObj, nameOfAllOperandFilesList, rootResultFolderName,
            executableName, executableInputList, CBuildFolder, operandSampleFileName, lOfAccurateValues, allPointsTried, True, unique_point_list, output_list, previous_ideal_setUp, iteration,
            settings_obj, run_input_list, lOf_accurateValues)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", specializedMutate, ignoreListIndecies, settings_obj)
    toolbox.register("select", tools.selSPEA2)
    """ 
    if (settings_obj.runMode == "parallel"): 
        #the_lock = multiprocessing.Lock() 
        #pool = multiprocessing.Pool() 
        toolbox.register("map", pool.map)
        #allPointsTried = [] #since deap is not compatible with multiprocessor
                            #library (when it comes to sharing a list accross
                            #processes), we set allPointsTried to empty to 
                            #avoid any unwanted consequences
    """
    
    #--run the genetic algo
    print("\n......running genetic algo\n")
    for index in range(len(allConfs)):
            myGenerator = return_conf(allConfs[index])
            population.append(toolbox.individual(lambda: next(myGenerator), len(allConfs[index])))

    algorithms.eaMuPlusLambda(population, toolbox, MU, LAMBDA, CXPB, MUTPB, NGEN, stats)
    return population


def de_stringify_and_disect(s):
    o = []    
    while s:
        o.append(s[:2])
        s = s[2:]
    result = map(lambda x: int(x)-32, o)
    return result

def fish_a_move(my_histogram_inv_map, prob_dis, setting_obj):
    move_intensity = random.choice(prob_dis)
    move = random.choice(my_histogram_inv_map[int(move_intensity)])
#    print move_intensity
#    print my_histogram_inv_map
#    print move 
    result = de_stringify_and_disect(move) 
    
    return result 

def probabilistic_heuristic(points_to_explore_from,
                        CSourceOutputForVariousSetUpFileName, operatorSampleFileFullAddress,
                        executableName, executableInputList, rootResultFolderName, CBuildFolder,
                        operandSampleFileName, lOfAccurateValues, nameOfAllOperandFilesList, inputObj, ignoreListIndecies, possibly_worse_case_result_quality, accurateSetUp, allConfs,
                        lOfAllPointsTried, settings_obj):
    print "accomedate previous ideal setUp to probabilistic_heuristic as well. for ref, look at run_spea2"
    print "accomodate the iteration" #iteration tells us which input we are using to feed into the stage of interest
    sys.exit()
    print "I ma not using adjust_NGEN. incorperate it"
    sys.exit()
    #---get improvement_vectors
    impv_vectors = []
    #impv_vectors = collect_moves_of_interest("all", lOfAllPointsTried)
    impv_vectors = collect_moves_of_interest("pareto_by_pareto", lOfAllPointsTried)
     
#    for el in impv_vectors:
#        print ("move_val: " + str(el.get_move()) + " strength: " + str(el.get_strength()))
#    sys.exit()
#
    
    #---stringify the impv_vector by adding 32(to get rid of <0 values and then zfill) 
    for el in impv_vectors:
        el.stringify_val()
        
    #impv_vectors_stringtified.append(el.get_stringified_val())
    
    #---histogramize 
    my_histogram = histogramize_list(impv_vectors)

    #---soring the dictionary(histogram)   
    #sorted_imp = sorted(my_histogram.items(), key=operator.itemgetter(1))
    #sorted_imp.reverse()
    
    #---creating a prob distribution for fishing 
    unique_values = set(my_histogram.values())
#     print unique_values 
    unique_values_string = map(lambda(x) : [str(x)], unique_values)
#     print unique_values_string
    prob_dis_unflattened = map(operator.mul, unique_values, unique_values_string)
    prob_dis = list(itertools.chain.from_iterable(prob_dis_unflattened))
    
    #---inverse mapping of histogram (swapping keys, and values)
    my_histogram_inv_map = {}
    for k, v in my_histogram.iteritems():
        my_histogram_inv_map[v] = my_histogram_inv_map.get(v, [])
        my_histogram_inv_map[v].append(k) 
    

    prob_heur_points = [] #points acquired by running the probabilistic algo
    print str(len(points_to_explore_from)*settings_obj.number_of_probabilistic_trial) + " more points were explored" 
    for pt in points_to_explore_from:
        for i in range(settings_obj.number_of_probabilistic_trial): 
            move = fish_a_move(my_histogram_inv_map, prob_dis, settings_obj)
            individual = pt.get_raw_setUp() 
            new_individual_raw_setUp = apply_move_to_individual(individual, move) 
            result = specializedEval(True,possibly_worse_case_result_quality,  accurateSetUp, ignoreListIndecies, accurateSetUp, inputObj, nameOfAllOperandFilesList, rootResultFolderName,executableName,
        executableInputList, CBuildFolder, operandSampleFileName, lOfAccurateValues, lOfAllPointsTried, False, unique_point_list, output_list, previous_ideal_setUp, new_individual_raw_setUp,
        iteration, settings_obj, run_input_list)
            newPoint = points()
            newPoint.set_energy(result[0])
            newPoint.set_quality(result[1])
            newPoint.set_setUp(modifyMold(accurateSetUp, new_individual_raw_setUp))
            newPoint.set_raw_setUp(new_individual_raw_setUp)
            newPoint.set_setUp_number(0)
            prob_heur_points.append(newPoint)
         
    return prob_heur_points



