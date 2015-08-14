import itertools
import sys
from GenOpSpace import GenOpSpace
import os.path
import pylab
import matplotlib.mlab as mlb
from misc import *
# Copyright (C) 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
# 
## 
# @file settings.py
# @brief this file contains all the settings (or otherwise called config information for the tool_chain)
# @author Behzad Boroujerdian
# @date 2015-07-01


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------guide::: file and folder names
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
global AllPossibleApxOpScenarios
AllPossibleApxOpScenarios =  "all_possible_apx_operators_scenarios.txt"


global AllOperandScenarios
AllOperandScenarios =  "all_operands_scenarios.txt"




global GENERATE_ONE_OUTPUT  
GENERATE_ONE_OUTPUT = -1 #if this flag is set, the program only generates one output. mainly used for debugging and fascilitate testing

global outputFolderName

global operatorSampleFileName
operatorSampleFileName = "operator_sample.txt"

global operandSampleFileName
operandSampleFileName = "operand_sample.txt"


global rawresultFileName 
rawresultFileName = "raw_results.txt"

global resultsChareceteristics
resultsChareceteristics = "resultsCharacteristics.txt"

global AllOperandsFolderName
AllOperandsFolderName = "all_operands_folder"

global rawResultFolderName
rawResultFolderName = "csource_output_folder"


#global finalResultFileName  #this file contains the final result 
#finalResultFileName = "final_results.txt"
#
global csourceOutputFileName 
csourceOutputFileName = "csource_output"

global generatedTextFolderName
generatedTextFolderName = "generated_text"
global CBuildFolderName
CBuildFolderName = "Debug"



global resultsBackups #this variable contains the back of all the results (settings.generatedTextFolderName)
resultsBackups = "all_backups" 

global totalNumberOfOpCombinations #total number of operator combinations possible


global annealerOutputFileName 
annealerOutputFileName = "annealer_output.txt" #this file contains the noiseRequirements, noise and energy result fo the annealer (less inclusvie comparing to the annealerProgressionOutputFileName"

global annealerProgressionOutputFileName
annealerProgressionOutputFileName = "annealer_progression_output.txt"  #the file that contains information regarding the output of the anneler

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------guide::: other variables 
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
IOAndProcessCharFileName = "IOAndProcessChar.txt" #this file will contain the information about the input(operands, operators of the CSource) and output and process characteristics such as the time that it took or the number of the operators that were explored
#mode = "allPermutations" 
mode = "simulated_annealing"
signalToNoiseRatioRange =  floatRange(.5, .67, .1)
numberOfApxBitsStepSize = .01
numberOfApxBitsInitialTemperature = 1
operatorPickInitialTemperature = 3
operatorPickStepSize = 1
             

#--------- only need to change the following lines, 
#these are the flags that need to be mentioned by the src file author
global lAccurateOpFlags
lAccurateOpFlags = ["AdditionOp", "MultiplicationOp"] #all of the defined operations

#given the boundaries generate all each ops space(this means, all the apx and accurate versions of one operation)
global lAllApxVersionOfEachOps 


#lAllApxVersionOfEachOps = [GenOpSpace("bta", 8,[32,33, 0,10, 0,1, 0, 1]), GenOpSpace("btm", 4,[32, 33, 0, 10])]
lAllApxVersionOfEachOps = [GenOpSpace("bta", 8,[32,33, 0,3, 0,1, 0, 1]), GenOpSpace("btm", 4,[32, 33, 0, 10])]
#lAllApxVersionOfEachOps = [GenOpSpace("bta", 8,[32,33, 0,2, 0,1, 0, 1]), GenOpSpace("btm", 4,[32, 33, 0, 1])]

for element in lAllApxVersionOfEachOps:
    element.sweepInput()


global OpTypeOpKind 
#OpTypeOpKind = { lAccurateOpFlags[0]: lAllApxVersionOfEachOps[0].permutedList + lAllApxVersionOfEachOps[1].permutedList, lAccurateOpFlags[1]: lAllApxVersionOfEachOps[2].permutedList} #various types of each of the opertions mentioned in the lAccurateOpFlags


OpTypeOpKind = { lAccurateOpFlags[0]: lAllApxVersionOfEachOps[0].permutedList, lAccurateOpFlags[1]: lAllApxVersionOfEachOps[1].permutedList} #various types of each of the opertions mentioned in the lAccurateOpFlags


global annealersAcceptableEnergyMarginePercentage #sets the Energy margin that the annealer would accept in taking a specific setUp as a valid next step. Meaning, annealer only accepts this setup as a temporarily answer (a new anchor) if the difference between this setup's energy and previous setup's energy falls within the percent margin indicated by this variable
annealersAcceptableEnergyMarginePercentage = 1

global annealersAcceptableImprovementOnNoiseMarginePercentage #similar to annealersAcceptableEnergyMarginePercentage but for closeness to the noiseRequirment
annealersAcceptableImprovementOnNoiseMarginePercentage = 1

