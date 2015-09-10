import sys
import os
import types
import inspect
## 
# @file inputs.py
# @brief this file contains a inputClass which contains all the inputs 
# @author 
# @date 2015-09-09


class inputClass:
    CSrcFolderAddress = "~/apx_tool_chain/src/CSrc/" 
    lOfCSrcFileAddress = ["~/apx_tool_chain/src/CSrc/test.cpp", "~/apx_tool_chain/src/CSrc/foo.cpp"] 
    # lOfCSrcFileAddress = ["~/apx_tool_chain/src/CSrc/test.cpp"]
    generateMakeFile = "YES"
    rootFolder = "~/apx_tool_chain"
    AllOperandScenariosInOneFiles = "YES"
    AllOperandsFileOrDirectoryName = "~/apx_tool_chain/all_operands_scenarios.txt"
    finalResultFileName = "finalResult.txt"
    PIK = "pickled_results"

    # ---- this function will unfolder the ~
    def expandAddress(self): 
        members = [attr for attr in dir(inputClass) if not callable(attr) and not attr.startswith("__")]
        # members = [attr for attr in dir(inputClass) if not hasattr(attr, '__call__') and not attr.startswith("__")]
        for index, element in enumerate(members):
            if not inspect.ismethod(eval("self."+element)):
                if isinstance(eval("self."+element), list):
                    myList =  eval("self."+element)
                    for index,listElement in enumerate(myList):
                        if (listElement).split("/")[0] == "~":
                            exec('self.'+element + "[" + str(index) + "] = os.path.expanduser('~')+ '" + listElement[1:]+"'")
                else:
                    if (eval("self."+element).split("/")[0] == "~"):
                        exec('self.'+element + " = os.path.expanduser('~') + eval('self.'+element)[1:]")

    def returnValues(self): 
        members = [attr for attr in dir(inputClass) if not callable(attr) and not attr.startswith("__")]
        # members = [attr for attr in dir(inputClass) if not hasattr(attr, '__call__') and not attr.startswith("__")]
        for index, element in enumerate(members):
            if not inspect.ismethod(eval("self."+element)):
                print eval('self.'+element)

obj = inputClass() 
obj.expandAddress()
obj.returnValues()
