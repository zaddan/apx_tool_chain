from inputs import *
import pickle
from compare_pareto_curves import *
from settings import *


#---Exception classes
class AccurateValueNoneError(Exception):
    pass


class CurrentValueNoneError(Exception):
    pass


class NoneLengthEqualityError(Exception):
    pass


#class WithinTaskError(Exception):
#    pass
class WithinSpecEval(Exception):
    def __init__(self, error_name, setUp):
        self.error_name = error_name
        self.setUp = setUp

    def __reduce__(self):
        return (self.__class__, (self.error_name, self.setUp))



class WithinCalcError(Exception):
    def __init__(self, error_name):
        self.error_name = error_name

    def __reduce__(self):
        return (self.__class__, (self.error_name, ))





#---error at the Task level. A task here is defined as one primary input with  
#---a set of setUps (apply_heuristic_on_task_with_primary_input) or one input  
#--- and one setUp (run_task_with_one_set_up_and_collect_info)
class TaskError(Exception):
    def __init__(self, error_name, input_obj, setUp):
        self.error_name = error_name
        self.input_obj = input_obj
        self.setUp = setUp

    def __reduce__(self):
        return (self.__class__, (self.error_name, self.input_obj, self.setUp))


class BenchMarkError(Exception):
    def __init__(self, error_name, input_obj, setUp):
        self.error_name = error_name
        self.input_obj = input_obj
        self.setUp = setUp

    def __reduce__(self):
        return (self.__class__, (self.error_name, self.input_obj, self.setUp))


class ToolError(Exception):
    pass


def write_error(error):
    print "writing the error in the " + error.input_obj.error_dump_file
    with open(error.input_obj.error_dump_file, "a") as f:
        pickle.dump(error, f)

#def write_system_exception(ex):
#    with open(exception_dump_file, "w") as f:
#        f.write(type(ex).__name__)
#        f.write("\n") 
#        f.write(str(ex.args))
#
def read_error(file_addr):
    l_of_error = getPoints(file_addr)
    for er in l_of_error:
        print "error name: ", er.error_name
        print "run_input: ", er.input_obj.run_input
        print "setUpFailedOn: ", er.setUp
        print "benchmarkName: ", er.input_obj.settings_obj.benchmark_name
        
