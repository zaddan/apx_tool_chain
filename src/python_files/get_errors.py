from error import *
from inputs import *
import pickle
from compare_pareto_curves import *
from settings import *

#---if run, read the error
if __name__ == "__main__":
    settings_obj = settingsClass("texture_synthesis", "sdf", "sd-vbs","small")
    inputObj = inputClass(settings_obj)
    read_error(inputObj.error_dump_file)
