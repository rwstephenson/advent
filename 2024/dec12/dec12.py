import sys
from math import *
from collections import *
sys.path.append('../../lib')
from point import Point
from interval import Interval
from parsing import *
from aocd import get_data, submit

def getPerimeter(region):
    perimeter = 0
    for s in region:
        perimeter += 4 - len(list(filter(lambda n: n.value == s.value,s.getNeighboors())))
    return perimeter

def getEdges(region):
    edges = []
    for s in region:
        for d in ['N','E','S','W']:
            n = s.getNeighboor(d)
            if n is None or n.value != s.value:
                edges.append((s,d))
    return edges

def opposite(d1,d2):
    return (d1 == 'N' and d2 == 'S') or (d1 == 'S' and d2 == 'N') or (d1 == 'E' and d2 == 'W') or (d1 == 'W' and d2 == 'E')

def innerCorners(p):
    c = 0
    if p.getNeighboor('N') and p.getNeighboor('N').value == p.value and p.getNeighboor('E') and p.getNeighboor('E').value == p.value:
        if p.getNeighboor('NE') is not None and p.getNeighboor('NE').value != p.value:
            c += 1
    if p.getNeighboor('N') and p.getNeighboor('N').value == p.value and p.getNeighboor('W') and p.getNeighboor('W').value == p.value:
        if p.getNeighboor('NW') is not None and p.getNeighboor('NW').value != p.value:
            c += 1
    if p.getNeighboor('S') and p.getNeighboor('S').value == p.value and p.getNeighboor('E') and p.getNeighboor('E').value == p.value:
        if p.getNeighboor('SE') is not None and p.getNeighboor('SE').value != p.value:
            c += 1
    if p.getNeighboor('S') and p.getNeighboor('S').value == p.value and p.getNeighboor('W') and p.getNeighboor('W').value == p.value:
        if p.getNeighboor('SW') is not None and p.getNeighboor('SW').value != p.value:
            c += 1
    return c

def getSides(region):
    edges = getEdges(region)
    assert(len(edges) == getPerimeter(region))
    edgesGrouped = defaultdict(list)
    corners = 0
    for p,d in edges:
        edgesGrouped[p].append(d)
    for p in region:
        ds = edgesGrouped[p]
        if len(ds) == 2:
            if not opposite(ds[0],ds[1]):
                corners += 1
        elif len(ds) == 3:
            corners += 2
        elif len(ds) == 4:
            corners += 4
        corners += innerCorners(p)
    return corners


def findRegion(value,p,region):
    if hash(p) not in region and p.value == value:
        region[hash(p)] = p
        for n in list(filter(lambda n: n.value == value, p.getNeighboors())):
            findRegion(value,n,region)

def solve(filename,pt):
    grid = parseLines(filename)
    total = 0
    regions = []

    seen = set()
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            p = Point(c,r,grid)
            if hash(p) not in seen:
                region = {}
                findRegion(p.value,p,region)
                for p in region.keys():
                    seen.add(p)
                regions.append(region.values())
    for region in regions:
        if pt == 1:
            total += getPerimeter(region)*len(region)
        elif pt == 2:
            total += getSides(region)*len(region)
    return total

def run(pt,day,year,expect):
    with open("input.txt","w") as f:
        f.write(get_data(day=day,year=year))

    resTest = solve("testInput.txt",pt)
    assert resTest == expect, f"Result was {resTest}"
    res = solve("input.txt",pt)
    print("Test Input: {} Puzzle Input: {}".format(resTest,res))

    if pt == 1:
        c = "a"
    else:
        c = "b"
    submit(res, part=c, day=day, year=year)

run(1,12,2024,1930)
run(2,12,2024,1206)
