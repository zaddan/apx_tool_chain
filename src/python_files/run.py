import os
def run(executableFileName, runInput1, runInput2, runInput3, runInput4):
    #print executable + " " + ' '.join(executableInputList);
    os.system("./"+str(executableFileName) + " " + runInput1 + " " +  runInput2 + " " + runInput3 + " " + runInput4)



