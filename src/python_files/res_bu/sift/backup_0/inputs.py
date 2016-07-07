import sys
import os
import types
import inspect
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
## common mistakes:
#make sure to add + to the lOfSource files"
##
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## 
# @file inputs.py
# @brief this file contains a inputClass which contains all the inputs 
# @author 
# @date 2015-09-09
repo_root_address = "/home/local/bulkhead/behzad/usr/local"
global CBuildFolderName
##---for my_micro_benchmarks
#CBuildFolderName = "Debug"
               
##---for sdvbs
#CBuildFolderName = "../sd-vbs/benchmarks/disparity/data/sim/"
CBuildFolderName = "../sd-vbs/benchmarks/sift/data/sim/"
#CBuildFolderName = "./Debug"

error_mode = "nearest_neighbors_2d"
#error_mode = "nearest_neighbors"
#error_mode = "simple"



quality_mode = "nsr"
#quality_mode = "snr"

pareto_comparison_mode = "comparison_of_nearest_neighbours"
#pareto_comparison_mode = "subsumption_comparison"  #compares the two based on how much one is subsumed by the other one (there is a wep page explaining this, take a look at the file where it is defined)


class inputClass:
    bench_suit_name = "my_micro_benchmark" #set based on the bench_soot name such as sd-vbs. 
                            #if for my microbenchmarks, don't need to define it.
                            # this is determins the make_run content
    
    # allInputScenarioFileAddress = repo_root_address + "/apx_tool_chain/all_input_scenarios.txt"
    # allInputs_arg0 = [repo_root_address + "/apx_tool_chain/inputPics/roki_320_240.ppm"]
    # allInputs_arg1 = [repo_root_address + "/apx_tool_chain/inputPics/roki_noisy.jpg"] 
    # allInputs_arg2 = ["320"]
    # allInputs_arg3 = ["240"]
    # allInputs_arg4 = ["0"]
    # allInputs_arg5 = ["10"]
    # allInputs = [allInputs_arg0, allInputs_arg1, allInputs_arg2, allInputs_arg3, allInputs_arg4, allInputs_arg5]
    dealingWithPics = "False"
    #CSrcFolderAddress = repo_root_address + "/apx_tool_chain/src/CSrc/" 
    CSrcFolderAddress = repo_root_address + "/apx_tool_chain/src/CSrc" #don't matter
    #lOfCSrcFileAddress = [repo_root_address + "/apx_tool_chain/src/CSrc/main.cpp", repo_root_address + "/apx_tool_chain/src/CSrc/foo.cpp"] 
    
    ##----simple  
    #lOfCSrcFileAddress = [repo_root_address + "/apx_tool_chain/src/CSrc/main.cpp"]
    #lOfCSrcFileAddress += [repo_root_address + "/apx_tool_chain/src/CSrc/foo.cpp"]
     
    ##----matmul 
    #lOfCSrcFileAddress = [repo_root_address + "/apx_tool_chain/src/CSrc/mat_mul_unfolded_algo0.cpp"]
    #lOfCSrcFileAddress += [repo_root_address + "/apx_tool_chain/src/CSrc/mat_mul_unfolded_algo1.cpp"]
    # lOfCSrcFileAddress += [repo_root_address + "/apx_tool_chain/src/CSrc/mat_mul_unfolded_algo2.cpp"]
    
    ##----jpeg (I am not sure if other files need to also be included" 
    # lOfCSrcFileAddress = [repo_root_address + "/apx_tool_chain/src/CSrc/modules_isolated.cpp", repo_root_address + "/apx_tool_chain/src/CSrc/loadjpg.cpp"]
    
   
    #----sift
    bench_suit_name = "sd-vbs"
    lOfCSrcFileAddress = [repo_root_address + "/sd-vbs/benchmarks/sift/src/c/sift.c"]
    lOfCSrcFileAddress += [repo_root_address + "/sd-vbs/benchmarks/sift/src/c/imsmooth.c"]
    lOfCSrcFileAddress += [repo_root_address + "/sd-vbs/benchmarks/sift/src/c/diffss.c"]

    
    #----disparity
    #bench_suit_name = "sd-vbs"
    #lOfCSrcFileAddress = [repo_root_address + "/sd-vbs/benchmarks/disparity/src/c/computeSAD.c"]
    #lOfCSrcFileAddress += [repo_root_address + "/sd-vbs/benchmarks/disparity/src/c/integralImage2D2D.c"]
    #lOfCSrcFileAddress += [repo_root_address + "/sd-vbs/benchmarks/disparity/src/c/finalSAD.c"]
#

    
    generateMakeFile = "NO"
    rootFolder = repo_root_address + "/apx_tool_chain"
    AllInputScenariosInOneFile = "YES"
    AllInputFileOrDirectoryName = repo_root_address + "/apx_tool_chain/all_input_scenarios.txt"
    finalResultFileName = "finalResult.txt"
    PIK = "pickled_results"
    refImage = repo_root_address + "/apx_tool_chain/inputPics/roki.jpg"
    noisyImage = repo_root_address + "/apx_tool_chain/inputPics/roki_noisy.jpg"
    # ---- this function will unfolder the /repo_root_address
    def expandAddress(self): 
        members = [attr for attr in dir(inputClass) if not callable(attr) and not attr.startswith("__")]
        # members = [attr for attr in dir(inputClass) if not hasattr(attr, '__call__') and not attr.startswith("__")]
        for index, element in enumerate(members):
            if not inspect.ismethod(eval("self."+element)):
                if isinstance(eval("self."+element), list):
                    myList =  eval("self."+element)
                    for index,listElement in enumerate(myList):
                        if (listElement).split("/")[0] == repo_root_address + "":
                            exec('self.'+element + "[" + str(index) + "] = os.path.expanduser('/repo_root_address')+ '" + listElement[1:]+"'")
                else:
                    if (eval("self."+element).split("/")[0] == repo_root_address + ""):
                        exec('self.'+element + " = os.path.expanduser('/repo_root_address') + eval('self.'+element)[1:]")
    def returnValues(self): 
        members = [attr for attr in dir(inputClass) if not callable(attr) and not attr.startswith("__")]
        # members = [attr for attr in dir(inputClass) if not hasattr(attr, '__call__') and not attr.startswith("__")]
        for index, element in enumerate(members):
            if not inspect.ismethod(eval("self."+element)):
                print eval('self.'+element)

obj = inputClass() 
obj.expandAddress()
obj.returnValues()
