import sys
import math

def notAll0(intList):
    for i in range(len(intList)):
        if intList[i] != 0:
            return True
    return False


def calculateDiffList(intList):
    outputList = []
    for i in range(1,len(intList)):
        outputList.append(intList[i]-intList[i-1])
    return outputList

def pt1(filename, prepend):
    with open(filename, "r") as f:
        sum = 0
        for line in f:
            origIntList = list(map(int,line.strip().split(' ')))
            intListList = [origIntList]
            while notAll0(intListList[-1]):
                intListList.append(calculateDiffList(intListList[-1]))
            i = len(intListList) - 1
            extrapDiff = 0
            while i > -1:
                if prepend:
                    newDiff = intListList[i][0] - extrapDiff
                else:
                    newDiff = intListList[i][-1] + extrapDiff
                extrapDiff = newDiff
                i -= 1
            sum += newDiff
        return sum

print(pt1("input.txt",True))

