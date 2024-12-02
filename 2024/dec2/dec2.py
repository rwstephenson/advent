import sys
from math import *
from collections import *
sys.path.append('../../lib')
from point import Point
from interval import Interval
from parsing import *

def blowUpRow(row):
    newRow = [row.copy()]
    for i in range(len(row)):
        if i == 0:
            newRow.append(row[1:])
        elif i == len(row) - 1:
            newRow.append(row[:-1])
        else:
            newRow.append(row[0:i] + row[i+1:])
    return newRow

def isSafe(ints,pt):
    if len(ints) > 1:
        if pt == 1:
            isIncreasing = ints[1] > ints[0]
            for i in range(1,len(ints)):
                delta = abs(ints[i]-ints[i-1])
                stillIncreasing = ints[i] > ints[i-1]
                if (isIncreasing and not stillIncreasing) or (not isIncreasing and stillIncreasing) or delta > 3 or delta == 0:
                    return False
            return True
        elif pt == 2:
            for row in blowUpRow(ints):
                if isSafe(row,1):
                    return True
            return False
        else:
            assert(False)

def solve(filename,pt):
    ints = []
    total = 0
    with open(filename,"r") as fd:
        for line in fd:
            ints = getInts(line)
            if isSafe(ints,pt):
                total += 1
    return total

resTest = solve("testInput.txt",1)
assert resTest == 2, f"Result was {resTest}"
res = solve("input.txt",1)
assert res == 321, f"Result was {resTest}"
print("Part 1: Test Input: {} Puzzle Input: {}".format(resTest,res))
resTest = solve("testInput.txt",2)
assert resTest == 4, f"Result was {resTest}"
res = solve("input.txt",2)
print("Part 2: Test Input: {} Puzzle Input: {}".format(resTest,res))
