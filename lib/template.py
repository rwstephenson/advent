import sys
from math import *
from collections import *
sys.path.append('../../lib')
from point import Point

def solve(filename):
    grid = []
    total = 0
    with open(filename,"r") as f:
        for line in f:
            grid.append(line.strip())
    return total

resTest = solve("testInput.txt")
res = solve("input.txt")
print("Test Input: {} Puzzle Input: {}".format(resTest,res))
