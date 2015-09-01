class points:
    def set_noise(self, noise):
        self.noise = noise
    def set_energy(self, energy):
        self.energy = energy
    def set_setUp(self, setUp):
        self.setUp = setUp
        
    def get_noise(self):
        return self.noise 
    def get_energy(self):
        return self.energy 
    def get_getUp(self):
        return self.setUp 
        
   def set_properties(self, noise, energy, setUp):
        self.noise = noise
        self.energy = energy
        self.setUp = setUp
   
    def get_properties(self):
        return (self.noise, self.energy, self.setUp)
  
