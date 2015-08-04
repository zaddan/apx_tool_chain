import itertools

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
# @file GenOpSpace.py
# @brief this file contains the class for generating all the possible apx version of an operation that is defined as a class
# @author Behzad Boroujerdian
# @date 2015-06-30


## 
# @brief this class generates all the possible versions of a specific operator. it ueses the name to figure out the type of input. for example, in the case of multipliation, it generates all the multipliactions possible such as accurate and apx version (apx versions can have different kinds)
#some of the inputs are just names and some of the inputs are ranges and need to be first generated and then permutated. 
#for example the name passed to this class, is just one element and doesn't need to be expanded, but the rest of the inputs acquire a low bound and high bound
#the way to use this class is the following way:
#set the numberOfInputs. For example in the case of Eta1 the number of inputs equal 8. These inputs include the low bound and high bound of the followi
##
class GenOpSpace():
    def __init__(self, name, numberOfInputs,  lInput):      
        self.name = [name]
        self.inputList = [] #this list containg the input that user provided (this can vary from Op to Op. for example in the case of GenEta1Input, this list contains
                            #NtLB, NtHB, NiaLB, NiaHB, msbLB, msbHB, lsbLB, lsbHB):
        self.eachCategoryAllValues = []  #this list stores all the values possible for each input catgory. for example in the case of Eta1 the categories are:
                                     #Nia, msb, lsb, Nt
        
        self.numberOfInputs = numberOfInputs 
        for i in range(0, self.numberOfInputs):
            self.inputList.append(lInput[i])

        
        self.combineList = [] #putting all the values of different categories in one list
        self.permutedTuples= []  #using itertool to generate all the permutations of the combineList
        self.permutedList= []   #converting the permutedTuples from tuple form to listForm
    
    def sweepInput(self):
        self.combineList.append(self.name); 
        for i in range(0, self.numberOfInputs, 2):
            self.eachCategoryAllValues.append(range(self.inputList[i], self.inputList[i+1]))
            self.combineList.append(self.eachCategoryAllValues[i/2])

        self.permutedTuples= list(itertools.product(*(self.combineList)))
        for element in self.permutedTuples:
            self.permutedList.append(list(element)); 
        #print self.permutedList 
    def printPermutations(self):
        print self.permutedList


#testing framework
#GenOps = [GenOpSpace("Eta", 8,[1,4, 2,6, 3,5, 4, 6]), GenOpSpace("btm", 4,[10, 11, 100, 110])]
#for element in GenOps:
#    element.sweepInput()
#    element.printPermutations()
#


