import copy 
import sys
import math
import numpy
import settings
from calc_psnr import *
from inputs import *
from extract_result_properties import *
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
        self.lOfOutput = [] 
        self.dealingWithPics = False
        self.quality_is_set = False
        self.quality_calculatable = True

    def set_dealing_with_pics(self, dealingWithPics):
        self.dealingWithPics = dealingWithPics
    def append_Output(self, output):
        self.lOfOutput.append(output)
    def get_lOf_output(self):
        assert (len(self.lOfOutput) > 0) 
        return self.lOfOutput
    def append_error(self, error):
        self.lOfError.append(error)
    def set_energy(self, energy):
        self.energy = energy
    def set_raw_setUp(self, raw_setUp):
        self.raw_setUp = raw_setUp
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
    def get_raw_setUp(self):
        return self.raw_setUp 
    def get_setUp_number(self):
        return self.setUpNumber 
    def get_lOf_operand(self, operand):
        return self.lOfOperand
    def get_accurate_values(self):
        return self.lOfAccurateValues
    def get_raw_values(self):
        assert(len(self.lOfRawValues)>0)
        return self.lOfRawValues
    def get_input_obj(self):
        return inputObj 
    
    def get_dealing_with_pics(self):
        return self.dealingWithPics 
    def calculate_PSNR(self, yourImageName="", originalImageName=""):
        refImage = self.inputObj.refImage
        noisyImage = self.inputObj.noisyImage
        self.PSNR = calculate_psnr(refImage, noisyImage)
    
    def calculate_quality(self,normalize, possibly_worse_case_result_quality):
        #---- calculate mean of accurate values 
        if (settings.error_mode == "image"):
            mean_of_acc_values = calculate_mean_acc_for_image(self.inputObj.refImage, self.inputObj.noisyImage)
        elif(settings.error_mode == "nearest_neighbors_2d" and benchmark_name =="sift"):
            mean_of_acc_values = numpy.mean(map( lambda x: numpy.mean(x, axis=0)[:-1], self.lOfAccurateValues), axis=0)
        else: 
            mean_of_acc_values = numpy.mean(map( lambda x: numpy.mean(x, axis=0), self.lOfAccurateValues),axis=0)
        
        #--- calculate mean of error values
        if (settings.error_mode == "image"):
            mean_of_error_values = calculate_error_for_image(self.inputObj.refImage, self.inputObj.noisyImage)
        else: 
            mean_of_error_values = numpy.mean(map( lambda x: numpy.mean(x, axis=0), self.lOfError), axis=0)
        
        #--- specific case of errorTest
        if (errorTest): 
            print "---------------" 
            print "Vector ass with mean of Acc Vals"
            print numpy.mean(self.lOfAccurateValues[0], axis=0) 
            print "magnitued of mean of Acc Val"
            print mean_of_acc_values
            
            print "Vector ass with mean of Erro Vals"
            print numpy.mean(self.lOfError[0], axis=0) 
            print "magnitued of mean of Error"
            print mean_of_error_values
            print "---------------" 
       
        if (settings.outputMode == "uniform"): #convert to a list for compatibility issues
            mean_of_error_values = [float(mean_of_error_values)]
            mean_of_acc_values = [ float(mean_of_acc_values)]
        
        #semi_sanity check (semi b/c it'll cause problems but it's not wrong perse
        for el in mean_of_acc_values:
            if el==0:
                print "acc_val can not be zero"#there is gonna be problems later on
                                              #if mean is zero, but technically there 
                                              #there is nothing wrong with that
                sys.exit()
#         assert (not(mean_of_acc_values == 0)) #there is gonna be problems later on
                                              #if mean is zero, but technically there 
                                              #there is nothing wrong with that
         
#         NSR= (mean_of_error_values/mean_of_acc_values)
        
        #divide the corresponding values for avg of errors and acc values  
        if (settings.DEBUG):
            print "mean of acc-val: " + str(mean_of_acc_values);
            print "mean of error-val: " + str(mean_of_error_values);
        
        NSR_vector = np.divide(mean_of_error_values,mean_of_acc_values) #should be a vector
        NSR_vector_abs = map(lambda x: abs(x), NSR_vector) #should be a vector
        NSR = np.mean(NSR_vector_abs) #this should be a scalar number
        if (normalize and not(possibly_worse_case_result_quality == float("inf"))):
            NSR = NSR/possibly_worse_case_result_quality
        if (settings.quality_mode == "snr"):
            if(NSR == 0):
                print "*******ERROR(kind of) noise is zero, make sure SNR is the right quality mode****"
                self.quality_calculatable = False
                self.SNR =  mean_of_acc_values
                self.quality = abs(self.SNR)
                self.quality_is_set = True
            else: 
                self.SNR =  1/NSR
                self.quality = abs(1/NSR)
                self.quality_is_set = True
        elif (settings.quality_mode == "nsr"):
            self.quality = abs(NSR)
            self.quality_is_set = True
        else:
            print "*****ERROR: this quality_mode: " + str(settings.quality_mode) + " is not defined***"
            sys.exit();
       
    
    
    
    def get_PSNR(self):
        return self.PSNR
     
    def get_SNR(self):
        assert(not(1==0)) #should never get here
        return self.SNR
    def get_quality(self):
        assert(self.quality_is_set) 
        assert(self.quality >=0) 
        return self.quality

