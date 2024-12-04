import sys
from math import *
from collections import *
sys.path.append('../../lib')
from point import Point
from interval import Interval
from parsing import *

def findXMAS(x):
    dirs = ['N','S','E','W','NE','NW','SE','SW']
    xmas = 0
    for d in dirs:
        m = x.getNeighboor(d)
        if m and m.value == 'M':
            a = m.getNeighboor(d)
            if a and a.value == 'A':
                s = a.getNeighboor(d)
                if s and s.value == 'S':
                    xmas += 1
    return xmas

def findMASX(a):
    m1dirs = ['NE','NW','SE','SW']
    masx = 0
    for m1dir in m1dirs:
        m2dir = s1dir = s2dir = ''
        if m1dir == 'NE':
            m2dir = 'SE'
            s1dir = 'NW'
            s2dir = 'SW'
        elif m1dir == 'SE':
            m2dir = 'SW'
            s1dir = 'NW'
            s2dir = 'NE'
        elif m1dir == 'SW':
            m2dir = 'NW'
            s1dir = 'NE'
            s2dir = 'SE'
        elif m1dir == 'NW':
            m2dir = 'NE'
            s1dir = 'SE'
            s2dir = 'SW'
        else:
            assert(False)
        m1 = a.getNeighboor(m1dir)
        m2 = a.getNeighboor(m2dir)
        s1 = a.getNeighboor(s1dir)
        s2 = a.getNeighboor(s2dir)
        if (m1 and m2 and s1 and s2) and (m1.value == 'M' and m2.value == 'M' and s1.value == 'S' and s2.value == 'S'):
            masx += 1
    return masx

def solve(filename):
    grid = []
    total = 0
    with open(filename,"r") as f:
        for line in f:
            grid.append(line.strip())
        for row in range(len(grid)):
            xs = findAll(grid[row],'X')
            for x in xs:
                total += findXMAS(Point(x,row,grid))
    return total

def solve2(filename):
    grid = []
    total = 0
    with open(filename,"r") as f:
        for line in f:
            grid.append(line.strip())
        for row in range(len(grid)):
            xs = findAll(grid[row],'A')
            for a in xs:
                total += findMASX(Point(a,row,grid))
    return total

resTest = solve2("testInput.txt")
assert resTest == 9, f"Result was {resTest}"
res = solve2("input.txt")
print("Test Input: {} Puzzle Input: {}".format(resTest,res))
