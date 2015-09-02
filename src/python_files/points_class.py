import copy 
import sys
class points:
    def set_noise(self, noise):
        self.noise = noise
    def set_energy(self, energy):
        self.energy = energy
    def set_setUp(self, setUp):
        self.setUp = setUp
    def set_setUp_number(self, setUpNumber):
        self.setUpNumber = setUpNumber
    
    def get_noise(self):
        return self.noise 
    def get_energy(self):
        return self.energy 
    def get_setUp(self):
        return self.setUp 
    def get_setUp_number(self):
        return self.setUpNumber 
        
    def set_properties(self, noise, energy, setUp, setUpNumber):
        self.noise = noise
        self.energy = energy
        self.setUp = setUp
        self.setUpNumber = setUpNumber
    
    def get_properties(self):
        #return (self.noise, self.energy, self.setUp, self.setUpNumber)
        return (self.setUpNumber, self.setUp, self.noise, self.energy)


class operandSet:
    def __init__(self, lOfValues):
        self.lOfValues = copy.deepcopy(lOfValues)
    def set_operands_values(self, lOfValues):
        self.lOfValues = copy.deepcopy(lOfValues)
    def set_lOfPoints(self, lOfPoints):
        self.lOfPoints = copy.deepcopy(lOfPoints)
    def set_lOf_noise_requirement(self, lOfNoiseRequirement):
        self.lOfNoiseRequirement = copy.deepcopy(lOfNoiseRequirement)
    def set_lOf_pareto_points(self, lOfParetoPoints):
        self.lOfParetoPoints = copy.deepcopy(lOfParetoPoints)

    def get_operands_values(self):
        return self.lOfValues 
    def get_lOfPoints(self):
        return self.lOfPoints 

    def get_lOf_pareto_points(self):
        return self.lOfParetoPoints
    def get_lOf_noise_requirement(self):
        assert (self.lOfNoiseRequirement), "lOfParetoPoints are empty"
        return self.lOfNoiseRequirement
