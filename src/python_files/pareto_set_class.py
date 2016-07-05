from points_class import *
from extract_pareto_set_from_raw_material import *
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ---- further modification is necessary to expand the class for more than
# ---- 2 dimensional optimization objectives
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class pareto_set:
    def __init__(self, lOfRawPoints, maxX, maxY):
        self.lOfRawPoints = lOfRawPoints
        self.lOfParetoPoints = pareto_frontier(lOfRawPoints, maxX, maxY)
        self.axis_1 = maxX
        self.axis_2 = maxY
        self.delimeter_2_tuple = [0, len(self.lOfParetoPoints)]
    def set_module_name(self, moduleName):
        self.moduleName = moduleName
    def set_delimeter(self, delimeter_2_tuple): 
        self.delimeter_2_tuple = delimeter_2_tuple

    def get_pareto_values(self):
        return self.lOfParetoPoints 
    def get_module_name(self):
        return self.moduleName 
    def get_delimeter(self):
        return self.delimeter_2_tuple
    def get_direction(self):
        return (self.axis_1, self.axis_2)


