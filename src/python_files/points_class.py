import copy 
import sys
import math
import numpy

class points:
    def __init__(self):
        self.lOfError = []
        self.lOfOperand = [] 
        self.lOfAccurateValues = [] 
        self.lOfRawValues = []
        self.dealingWithPics = False

    def set_dealing_with_pics(self, dealingWithPics):
        self.dealingWithPics = dealingWithPics
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
    def append_raw_values(self, rawValue):
        self.lOfRawValues.append(rawValue)


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
    def get_raw_values(self):
        return self.lOfRawValues

    def calculate_SNR(self):
        if (self.dealingWithPics):
            self.SNR = sum(map(lambda x : sum(x)/len(x), self.lOfRawValues))/len(self.lOfRawValues)
        else:
            self.SNR = numpy.mean(self.lOfError)/numpy.mean(map(lambda x: float(x[0]), self.lOfAccurateValues))
        
    def get_SNR(self):
        return self.SNR
