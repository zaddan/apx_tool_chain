class move_obj:
    def __init__(self):
        self.value =[] 
        self.strength = 0 
        self.stringified_val = '' 
        
    def __init__(self, value, strength):
        self.value = value 
        self.strength = strength 
        self.stringified_val = '' 
    
    def set_move(self, move_value):
        self.value = []

    def set_strength(self, strength_val):
            self.strength = strength_val

    def stringify_val(self):
        self.stringified_val = ''.join(( map(lambda x: (str((x+32)).zfill(2)), self.value)))
        
    def get_stringified_val(self):
        assert not(self.stringified_val == '')     
        return self.stringified_val
    
    def get_move(self):
        assert not(self.value == []) 
        return self.value
    
    def get_strength(self):
        assert (self.strength > 0) 
        return self.strength

