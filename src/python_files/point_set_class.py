from points_class import *
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class point_set:
    def __init__(self, lOfRawPoints, set_type, maxX , maxY):
        if not(set_type == "pareto" or set_type=="all" or set_type == "unique"):
            print "***ERRR, this set_type does not exist"
            exit()
        self.lOfRawPoints = lOfRawPoints
        self.set_type = set_type; 
        self.delimeter_2_tuple = [0, len(self.lOfRawPoints)]
        self.maxX = maxX
        self.maxY = maxY
    def set_delimeter(self, delimeter_2_tuple): 
        self.delimeter_2_tuple = delimeter_2_tuple

    def get_points(self):
        return self.lOfRawPoints
    def get_pareto_points(self):
        return pareto_frontier(self.lOfRawPoints,self.maxX, self.maxY); 
    def get_delimeter(self):
        return self.delimeter_2_tuple
    def get_type(self):
        return self.set_type
    def get_direction(self):
        if not(self.set_type == "pareto"):
            print "******ERRR*****"
            print "this type of set does not have a direction"
            print "type:" + str(self.set_type) 
            print "****************"
            exit() 
        else:
            return (self.maxX, self.maxY)

