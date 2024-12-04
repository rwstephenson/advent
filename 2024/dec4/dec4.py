import sys
from math import *
from collections import *
sys.path.append('../../lib')
from point import Point
from interval import Interval
from parsing import *

def findXMAS(x):
    dirs = ['N','S','E','W','NE','NW','SE','SW']
    MAS = 'MAS'
    xmas = 0
    for d in dirs:
        p = x
        for i in range(len(MAS)):
            p = p.getNeighboor(d)
            if p and p.value == MAS[i]:
                if i == len(MAS) - 1:
                    xmas += 1
            else:
                break
    return xmas

def findMASX(a):
    dirs = ['NE','NW','SE','SW']
    neighboors = []
    masx = 0
    for d in dirs:
        n = a.getNeighboor(d)
        if n:
            neighboors.append(n.value)
    sCount = neighboors.count('S')
    mCount = neighboors.count('M')
    if sCount == 2 and mCount == 2 and neighboors[0] != neighboors[3]:
        masx += 1
    return masx

def solve(filename,pt):
    grid = []
    total = 0
    with open(filename,"r") as f:
        for line in f:
            grid.append(line.strip())
        for row in range(len(grid)):
            if pt == 1:
                xs = findAll(grid[row],'X')
                for x in xs:
                    total += findXMAS(Point(x,row,grid))
            elif pt == 2:
                xs = findAll(grid[row],'A')
                for a in xs:
                    total += findMASX(Point(a,row,grid))
    return total

resTest = solve("testInput.txt",1)
assert resTest == 18, f"Result was {resTest}"
res = solve("input.txt",1)
print("Part 1: Test Input: {} Puzzle Input: {}".format(resTest,res))
resTest = solve("testInput.txt",2)
assert resTest == 9, f"Result was {resTest}"
res = solve("input.txt",2)
print("Part 2: Test Input: {} Puzzle Input: {}".format(resTest,res))
