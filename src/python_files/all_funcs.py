
def polyThree(variableList, *Coeff):
    return Coeff[0]*pow(variableList[0],3) + Coeff[1]*pow(variableList[0],2) + Coeff[2]*pow(variableList[0],1) + Coeff[3] 
 
    
def polyTwo(variableList,*Coeff):
    return Coeff[0]*pow(variableList[0],2) + Coeff[1]*pow(variableList[0],1) + Coeff[2]
 
def multiVarFoo3(variableList,*Coeff):
    return Coeff[0]*variableList[0]*variableList[1]

def multiVarFoo2(variableList,*Coeff):
    return Coeff[0]*variableList[0] + variableList[1]
 

global funcNumberOfCoeffDic
funcNumberOfCoeffDic = {}
funcNumberOfCoeffDic[polyThree] = 4
funcNumberOfCoeffDic[polyTwo] = 3
funcNumberOfCoeffDic[multiVarFoo2] = 1
funcNumberOfCoeffDic[multiVarFoo3] = 1
