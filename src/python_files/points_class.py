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
        self.quality_is_set = False

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
        assert(not(1 == 2))
        self.SNR = SNR
    def set_quality(self, quality_value):
        self.quality = abs(quality_value)
        self.quality_is_set = True
    
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
    def calculate_quality(self, yourImageName="", originalImageName=""):
        if (error_mode == "nearest_neighbors_2d"):
            mean_of_acc_values =  numpy.mean(map(lambda y: sum(map(lambda x: math.sqrt(float(x[0])**2 + float(x[1])**2), y))/len(y), self.lOfAccurateValues))
            assert (not(mean_of_acc_values == 0))
            NSR= (numpy.mean(self.lOfError)/mean_of_acc_values)
        else: 
            mean_of_acc_values =  numpy.mean(map(lambda x: sum(map (lambda y: float(y), x))/len(x), self.lOfAccurateValues))
            assert (not(mean_of_acc_values == 0))
            NSR= (numpy.mean(self.lOfError)/mean_of_acc_values)
        
        if (quality_mode == "snr"):
            if(NSR == 0):
                print "******* noise is zero, make sure SNR is the right quality mode****"
                if (error_mode == "nearest_neighbors_2d"):
                    self.SNR =  numpy.mean(map(lambda y : sum(map(lambda x: math.sqrt(float(x[0])**2 + float(x[1])**2), y))/len(y), self.lOfAccurateValues))
                    self.quality = abs(self.SNR)
                    self.quality_is_set = True
                else:  
                    self.SNR =  numpy.mean(map(lambda x: sum(map (lambda y: float(y), x))/len(x), self.lOfAccurateValues))
                    self.quality = abs(self.SNR)
                    self.quality_is_set = True
            else: 
                self.SNR =  1/NSR
                self.quality = abs(1/NSR)
                self.quality_is_set = True

        elif (quality_mode == "nsr"):
            self.quality = abs(NSR)
            self.quality_is_set = True
        else:
            print "*****ERROR: this quality_mode is not defined***"
            sys.exit();
       
    def calculate_PSNR(self, yourImageName="", originalImageName=""):
        refImage = self.inputObj.refImage
        noisyImage = self.inputObj.noisyImage
        self.PSNR = calculate_psnr(refImage, noisyImage)
        print self.PSNR
    
    
    def get_PSNR(self):
        return self.PSNR
     
    def get_SNR(self):
        assert(not(1==0))
        return self.SNR
    def get_quality(self):
        assert(self.quality_is_set) 
        assert(self.quality >=0) 
        return self.quality

