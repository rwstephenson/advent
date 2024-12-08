import sys
from math import *
from collections import *
sys.path.append('../../lib')
from point import Point
from interval import Interval
from parsing import *
from aocd import submit

def choose2(listN):
    res = []
    for i in range(len(listN)):
        for k in range(i+1,len(listN)):
            res.append((listN[i],listN[k]))
    return res

def findLocations(pa,pb,grid,pt):
    delta = Point(pb.x - pa.x,pb.y - pa.y,grid)
    if pt == 1:
        return [pa - delta, pb + delta]
    elif pt == 2:
        ret = []
        i = 1
        locA,locB = (pa, pb)
        while locA.value or locB.value:
            ret.append(locA)
            ret.append(locB)
            locA,locB = (pa - Point(delta.x * i, delta.y * i,grid),pb + Point(delta.x * i, delta.y * i,grid))
            i += 1
        return ret

def solve(filename, pt):
    grid = parseLines(filename)
    frequencies = defaultdict(set)
    found = set()
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            p = Point(c,r,grid)
            if p.value != '.':
                frequencies[p.value].add(p)
    for f in frequencies.keys():
        for pa,pb in choose2(list(frequencies[f])):
            for loc in findLocations(pa,pb,grid,pt):
                if loc.value:
                    found.add(hash(loc))
    return len(found)

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

run(1,8,2024,14)
run(2,8,2024,34)
