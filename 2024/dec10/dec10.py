import sys
from math import *
from collections import *
sys.path.append('../../lib')
from point import Point
from interval import Interval
from parsing import *
from aocd import submit

def dfsTo9(t,seen,pt):
    if pt == 1 and hash(t) in seen:
        return 0
    elif int(t.value) == 9:
        seen.add(hash(t))
        return 1
    else:
        neighboors = t.getNeighboors()
        seen.add(hash(t))
        total = 0
        for n in neighboors:
            if int(n.value) == int(t.value) + 1:
                total += dfsTo9(n,seen,pt)
        return total

def solve(filename, pt):
    grid = parseLines(filename)
    total = 0
    trailheads = []
    for r in range(len(grid)):
        for c in findAll(grid[r],'0'):
            trailheads.append(Point(c,r,grid))
    for t in trailheads:
        total += dfsTo9(t,set(),pt)
    return total

def run(pt,day,year,expected):
    resTest = solve("testInput.txt",pt)
    assert resTest == expected, f"Result was {resTest}"
    res = solve("input.txt",pt)
    print("Test Input: {} Puzzle Input: {}".format(resTest,res))
    if pt == 1:
        c = "a"
    else:
        c = "b"
    submit(res, part=c, day=day, year=year)

run(1,10,2024,36)
run(2,10,2024,81)
