import sys
from math import *
from collections import *
sys.path.append('../../lib')
from point import Point
from interval import Interval

def solve(filename):
    totalPt1 = 0
    totalPt2 = 0
    with open(filename,"r") as f:
        for line in f:
            a,b = line.strip().split(',')
            int0 = Interval.fromStr(a)
            int1 = Interval.fromStr(b)
            intersect = int0.getIntersection(int1)
            if intersect:
                totalPt2 += 1
                if intersect.size() == int0.size() or intersect.size() == int1.size():
                    totalPt1 += 1
    return totalPt1,totalPt2

resTest = solve("testInput.txt")
assert(resTest[0] == 2)
assert(resTest[1] == 4)
res = solve("input.txt")
print("Part 1: Test Input: {} Puzzle Input: {}".format(resTest[0],res[0]))
print("Part 2: Test Input: {} Puzzle Input: {}".format(resTest[1],res[1]))
