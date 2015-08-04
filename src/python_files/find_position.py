def findPosition(pair, xList, yList, setUpNumberList):
    result = [] 
    for i in range(0, len(xList)):
        if pair[0] == xList[i]:
            if pair[1] == yList[i]:
                if (i in setUpNumberList):
                    continue
                else:
                    return i
        
    print "*****************ERROR****************"
    print "could not find the element in the list" 
    exit()

#
#
#def testFindPosition():
#    xList = [1,4,5,6,7,9]
#    yList = [4,5,1,8,9,10]
#    pair = (6,8)
#    result = findPosition(pair, xList, yList)
#    print "result is" + str(result)
#
#    pair(9, 4)
#    result = find_position(pair, xList, yList)
#    print "result is" + str(result)
#
#
#testFindPosition()

