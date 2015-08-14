import math
def findTotalTime(timeBeforeFindingResults, timeAfterFindingResults):
    beforeDay = timeBeforeFindingResults.day
    beforeHour = timeBeforeFindingResults.hour
    beforeMinute = timeBeforeFindingResults.minute

    afterDay = timeAfterFindingResults.day
    afterHour = timeAfterFindingResults.hour
    afterMinute = timeAfterFindingResults.minute

    return (afterDay - beforeDay)*1440 + (afterHour - beforeHour)*60 + (afterMinute - beforeMinute)

def findTotalTimeInSecond(timeBeforeFindingResults, timeAfterFindingResults):
    beforeDay = timeBeforeFindingResults.day
    beforeHour = timeBeforeFindingResults.hour
    beforeMinute = timeBeforeFindingResults.minute
    beforeSecond = timeBeforeFindingResults.second
    
    afterDay = timeAfterFindingResults.day
    afterHour = timeAfterFindingResults.hour
    afterMinute = timeAfterFindingResults.minute
    afterSecond = timeAfterFindingResults.second
    
    return (afterDay - beforeDay)*1440*60 + (afterHour - beforeHour)*60*60 + (afterMinute - beforeMinute)*60 + (afterSecond - beforeSecond)





def floatRange(start, stop, step):
    result = []
    i = start 
    while i < stop:
        result.append(i)
        i += step

    return result

def withinSomePercent(valOfInquiry, refVal, desiredMargin):
#    print "here is the refVal" + str(refVal)
#    print "valOfInquiry" + str(valOfInquiry)
    percentageError =  (math.fabs(refVal - valOfInquiry))/refVal
#    print percentageError
#    print (float(desiredMargin)/100)
#    print "done" 
    if percentageError < (float(desiredMargin)/100):
#        print "gotit" 
        return True
    else:
        return False



def getApxBit(setUp):
    return int(setUp[0].split()[2])
