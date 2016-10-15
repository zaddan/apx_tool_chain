import numpy
def adjust_vals(quality_list_sorted_based_on_z, energy_list_sorted_based_on_z, std_list_sorted_based_on_z):
    #get step i.e the difference between Q-states 
    #--- at the moment use avg of avg 
    l_avg = []
    l_min = []
    l_max = []
    l_min_dis = [] 
    for q_per_in in quality_list_sorted_based_on_z:
        l_avg.append(numpy.mean(numpy.diff(q_per_in)))
        l_min_dis.append(numpy.min(numpy.diff(q_per_in)))
        l_min.append(numpy.min(q_per_in))
        l_max.append(numpy.max(q_per_in))

    avg_of_avg = numpy.mean(l_avg)
    mean_of_min = numpy.mean(l_min)
    mean_of_max = numpy.mean(l_max)
    max_of_min = numpy.max(l_min) 
    min_of_min = numpy.min(l_min)
    max_of_max = numpy.max(l_max)
    min_dis = numpy.min(l_min_dis)
    
#    upper_bound = mean_of_max
#    lower_bound = max_of_min
#    step = avg_of_avg 
#    Q_state_val = lower_bound #we use this cause o.w we can't find a value 
#                              # for some inputs
    
    upper_bound = max_of_max #Q_state upper bound (potential upper bound)
    lower_bound = min_of_min #Q_state lower bound (potential lower bound)
    step = min_dis #Q_state step
    Q_state_val = lower_bound #we use this cause o.w we can't find a value 
                              # for some inputs
    adjusted_q_vals = map(list, [[]]*len(quality_list_sorted_based_on_z))
    adjusted_e_vals = map(list, [[]]*len(quality_list_sorted_based_on_z))
    adjusted_std_vals = map(list, [[]]*len(quality_list_sorted_based_on_z))
    l_Q_state_val  = []
    found_one = False
    
    #--- step through Q_states and multiple values  
    while(Q_state_val < upper_bound):
        l_Q_state_val.append(Q_state_val) 
        for input_index, q_list_per_in in enumerate(quality_list_sorted_based_on_z):
            for index,q_val in enumerate(q_list_per_in):
                if q_val > Q_state_val:
                    found_one = True 
                    if (index == 0):
                        adjusted_q_vals[input_index].append(q_list_per_in[index])
                        adjusted_e_vals[input_index].append(energy_list_sorted_based_on_z[input_index][index])
                        adjusted_std_vals[input_index].append(std_list_sorted_based_on_z[input_index][index])
                    else:
                        adjusted_q_vals[input_index].append(q_list_per_in[index-1])
                        adjusted_e_vals[input_index].append(energy_list_sorted_based_on_z[input_index][index-1])
                        adjusted_std_vals[input_index].append(std_list_sorted_based_on_z[input_index][index-1])
                    break; 
                elif q_val == Q_state_val:
                    adjusted_q_vals[input_index].append(q_list_per_in[index])
                    adjusted_e_vals[input_index].append(energy_list_sorted_based_on_z[input_index][index])
                    adjusted_std_vals[input_index].append(std_list_sorted_based_on_z[input_index][index])
                    found_one = True 
                    break
            
            if not(found_one): #didn't find cause Q-state was bigger than the last element
                adjusted_q_vals[input_index].append(q_list_per_in[-1])
                adjusted_e_vals[input_index].append(energy_list_sorted_based_on_z[input_index][-1])
                adjusted_std_vals[input_index].append(std_list_sorted_based_on_z[input_index][-1])

            found_one = False 
        Q_state_val += step      
 
    #--- get rid of multiples
    for input_index, q_list_per_in in enumerate(adjusted_q_vals):
        counter = 0 
        while(True) :
            if adjusted_q_vals[input_index][counter] == adjusted_q_vals[input_index][counter +1]:
                for input_index_2,_ in enumerate(adjusted_q_vals):
                    adjusted_q_vals[input_index_2].pop(counter)
                    adjusted_e_vals[input_index_2].pop(counter)
                    adjusted_std_vals[input_index_2].pop(counter)
                l_Q_state_val.pop(counter)
                counter -=1; 
            counter +=1
            if (counter >= len(adjusted_q_vals[0]) - 1): 
                break
        

    return adjusted_q_vals, adjusted_e_vals, adjusted_std_vals, l_Q_state_val 
    
#
#a = [[1,4,5, 9 , 10, 15], [2, 6,8, 11, 13 , 14, 19,21], [3,8,10,15,21,23,24]]
#b = [[10,40,50, 90 , 100, 150], [20, 60,80, 110, 130 , 140, 190,210], [30,80,100,150,210,230,240]]
#c = [[100,400,500, 900 , 1000, 1500] , [200, 600,800, 1100, 1300 , 1400, 1900,2100], [300,800,1000,1500,2100,2300,2400]]
#
#
#adjusted_q_vals, adjusted_e_vals, adjusted_std_vals, l_Q_state_val = adjust(a,b,c)
#print adjusted_q_vals
#print adjusted_e_vals
#print adjusted_std_vals
#print l_Q_state_val
