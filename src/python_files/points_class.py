import copy 
import sys
import math
import numpy
from calc_psnr import *
from inputs import *
#**--------------------**
#**--------------------**
#----disclaimers::: SNR needs to modified when noise is Zero
#**--------------------**
#--------------------**
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
    def set_PSNR(self, PSNR):
        self.PSNR = PSNR
    def set_input_obj(self, inputObj):
        self.inputObj = inputObj 
    

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
    def get_input_obj(self):
        return inputObj 
    
    def get_dealing_with_pics(self):
        return self.dealingWithPics 
    def calculate_SNR(self, yourImageName="", originalImageName=""):
        NSR= (numpy.mean(self.lOfError)/numpy.mean(map(lambda x: sum(map (lambda y: float(y), x))/len(x), self.lOfAccurateValues)))
        if (NSR == 0):
            # self.SNR = 50
            self.SNR =  numpy.mean(map(lambda x: sum(map (lambda y: float(y), x))/len(x), self.lOfAccurateValues))
        else: 
            self.SNR =  1/NSR
    def calculate_PSNR(self, yourImageName="", originalImageName=""):
        refImage = self.inputObj.refImage
        noisyImage = self.inputObj.noisyImage
        self.PSNR = calculate_psnr(refImage, noisyImage)
        print self.PSNR
    
    
    def get_PSNR(self):
        return self.PSNR
     
    def get_SNR(self):
        return self.SNR
