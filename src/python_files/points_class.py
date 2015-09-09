import copy 
import sys
import math
import numpy
# class points:
    # def set_error(self, error):
        # self.error = error
    # def set_energy(self, energy):
        # self.energy = energy
    # def set_setUp(self, setUp):
        # self.setUp = setUp
    # def set_setUp_number(self, setUpNumber):
        # self.setUpNumber = setUpNumber
    
    # def get_error(self):
        # return self.error 
    # def get_energy(self):
        # return self.energy 
    # def get_setUp(self):
        # return self.setUp 
    # def get_setUp_number(self):
        # return self.setUpNumber 
        
    # def set_properties(self, error, energy, setUp, setUpNumber):
        # self.error = error
        # self.energy = energy
        # self.setUp = setUp
        # self.setUpNumber = setUpNumber
    
    # def get_properties(self):
        # #return (self.error, self.energy, self.setUp, self.setUpNumber)
        # return (self.setUpNumber, self.setUp, self.error, self.energy)


class points:
    def __init__(self):
        self.lOfError = []
        self.lOfOperand = [] 
        self.lOfAccurateValues = [] 

    
    def append_error(self, error):
        self.lOfError.append(error)
    def set_energy(self, energy):
        self.energy = energy
    def set_setUp(self, setUp):
        self.setUp = setUp
    def set_setUp_number(self, setUpNumber):
        self.setUpNumber = setUpNumber
    def append_lOf_operand(self, operand):
        self.lOfOperand.append(operand) 
    def append_accurate_values(self, value):
        self.lOfAccurateValues.append(value)
    def set_SNR(self, SNR):
        self.SNR = SNR



    def get_accurate_values(self):
        return self.accurateValues
    def get_lOfError(self):
        return self.lOfError 
    def get_energy(self):
        return self.energy 
    def get_setUp(self):
        return self.setUp 
    def get_setUp_number(self):
        return self.setUpNumber 
    def get_lOf_operand(self, operand):
        return self.lOfOperand
    def get_accurate_values(self):
        return self.lOfAccurateValues
    
    def calculate_SNR(self):
        self.SNR = numpy.mean(self.lOfError)/numpy.mean(map(lambda x: int(x[0]), self.lOfAccurateValues))
        
    def get_SNR(self):
        return self.SNR

# class operandSet:
    # def __init__(self, lOfValues):
        # self.lOfValues = copy.deepcopy(lOfValues)
    # def set_operands_values(self, lOfValues):
        # self.lOfValues = copy.deepcopy(lOfValues)
    # def set_lOfPoints(self, lOfPoints):
        # self.lOfPoints = copy.deepcopy(lOfPoints)
    # def set_lOf_error_requirement(self, lOfErrorRequirement):
        # self.lOfErrorRequirement = copy.deepcopy(lOfErrorRequirement)
    # def set_lOf_pareto_points(self, lOfParetoPoints):
        # self.lOfParetoPoints = copy.deepcopy(lOfParetoPoints)
    # def set_accurate_values(self, accurateValue):
        # self.accurateValues = accurateValue

    # def get_operands_values(self):
        # return self.lOfValues 
    # def get_lOfPoints(self):
        # return self.lOfPoints 
    # def get_accurate_values(self):
        # return self.accurateValues


    # def get_lOf_pareto_points(self):
        # return self.lOfParetoPoints
    # def get_lOf_error_requirement(self):
        # assert (self.lOfErrorRequirement), "lOfParetoPoints are empty"
        # return self.lOfErrorRequirement

# class configuration:
    # def __init__(self, config):
        # self.config= copy.deepcopy(config)
        # self.lOfAccuratePoints = []  
        # self.lOfInAccuratePoints = []  
    
    # def set_configuration(self, config):
        # self.config = copy.deepcopy(config)
    # def set_lOf_accurate_points(self, lOfPoints):
        # self.lOfAccuratePoints = lOfPoints
    # def set_lOf_inAccurate_points(self, lOfPoints):
        # self.lOfInAccuratePoints = lOfPoints
    # def set_energy_value(self, value):
        # self.energy = value
    
    # def get_lOf_inAccurate_points(self)
        # return self.lOfInAccuratePoints
    # def get_lOf_accurate_points(self)
        # return self.lOfAccuratePoints
    # def get_SNR(self):
        # return numpy.mean(map(lambda x,y: math.fabs(x), self.lOfInAccuratePoints.getError())/numpy.mean(self.lOfAccurateValues)
    # def get_energy(self):
        # return self.energy
