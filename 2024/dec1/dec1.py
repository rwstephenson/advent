import sys
from math import *
from collections import *
sys.path.append('../../lib')
from point import Point
from interval import Interval
from parsing import *

def solve(filename,pt):
    with open(filename,"r") as f:
        ints = []
        for line in f:
            ints.append(getInts(line))
        left = sorted(i[0] for i in ints)
        right = sorted(i[1] for i in ints)
        if (pt == 1):
            return sum(abs(l-r) for l,r in zip(left,right))
        elif (pt == 2):
            return sum(l*right.count(l) for l,r in zip(left,right))

resTest = solve("testInput.txt",1)
assert(resTest == 11)
res = solve("input.txt",1)
print("Part 1: Test Input: {} Puzzle Input: {}".format(resTest,res))
resTest = solve("testInput.txt",2)
assert(resTest == 31)
res = solve("input.txt",2)
print("Part 2: Test Input: {} Puzzle Input: {}".format(resTest,res))
