import sys
from math import *
from collections import *
sys.path.append('../../lib')
from point import Point
from interval import Interval

def solve(filename):
    total = 0
    with open(filename,"r") as f:
        left = []
        right = []
        for line in f:
            l,r = line.strip().split('   ')
            left.append(int(l))
            right.append(int(r))
            left.sort()
            right.sort()
            assert(len(left) == len(right))
        for i in range(len(left)):
            total += abs(left[i]-right[i])
    return total

def solve2(filename):
    total = 0
    with open(filename,"r") as f:
        left = []
        right = defaultdict(int)
        for line in f:
            l,r = line.strip().split('   ')
            left.append(int(l))
            right[int(r)] += 1
        for i in range(len(left)):
            total += left[i] * right[left[i]]
    return total

resTest = solve("testInput.txt")
assert(resTest == 11)
res = solve("input.txt")
print("Test Input: {} Puzzle Input: {}".format(resTest,res))
resTest = solve2("testInput.txt")
assert(resTest == 31)
res = solve2("input.txt")
print("Test Input: {} Puzzle Input: {}".format(resTest,res))
