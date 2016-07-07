from points_class import *
def extract_unique_noise(lOfPoints, dealingWithPics):
    uniqueListPoints = [] 
    lOfNoise = [] 
    lOfEnergy = [] 
    uniqueListPoints.append(lOfPoints[0]) 
    for point in lOfPoints:
        if(eval(dealingWithPics)): 
            try: 
                 pointIndex = lOfNoise.index(point.get_PSNR())
            except Exception as ex:
                if (type(ex).__name__ == "ValueError"):
                    pointIndex = None 
            if (pointIndex != None):
                if point.get_PSNR() < lOfEnergy[pointIndex]:
                    lOfEnergy[pointIndex] = point.get_energy() 
                    uniqueListPoints[pointIndex].append(point)
            else:
                lOfEnergy.append(point.get_energy()) 
                lOfNoise.append(point.get_PSNR())
                uniqueListPoints.append(point)
        else:
            try: 
                 pointIndex = lOfNoise.index(point.get_quality())
            except Exception as ex:
                if (type(ex).__name__ == "ValueError"):
                    pointIndex = None 
            if (pointIndex != None):
                if point.get_quality() < lOfEnergy[pointIndex]:
                    lOfEnergy[pointIndex] = point.get_energy() 
                    uniqueListPoints[pointIndex] = point
            else:
                lOfEnergy.append(point.get_energy()) 
                lOfNoise.append(point.get_quality())
                uniqueListPoints.append(point)
    return uniqueListPoints

