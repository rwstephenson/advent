import sys
from math import *
from collections import *
sys.path.append('../../lib')
from point import Point

def parseGrid(filename):
    grid = []
    with open(filename,"r") as f:
        for line in f:
            ## Adding padding to the end to break parts on newlines
            grid.append(line.strip() + '.')
    return grid

def hasNeighboorSymbol(p):
    for n in p.getNeighboors(True):
        if n.value != '.' and not n.value.isdigit():
            return n
    return None

def findGearValues(possibleGears):
    total = 0
    for gear in possibleGears:
        if len(possibleGears[gear]) == 2:
            total += prod(possibleGears[gear])
    return total

def solve(filename):
    grid = parseGrid(filename)
    parts = []
    magnitude = 0
    partValue = 0
    possibleGears = defaultdict(list)
    partSymbol = None
    for y in range(len(grid)):
        for x in reversed(range(len(grid[0]))):
            p = Point(x,y,grid)
            if p.value.isdigit():
                if partSymbol is None:
                    partSymbol = hasNeighboorSymbol(p)
                partValue += int(p.value)*10**magnitude
                magnitude += 1
            else:
                if partValue != 0:
                    if partSymbol:
                        parts.append(partValue)
                        if partSymbol.value == '*':
                            possibleGears[hash(partSymbol)].append(partValue)
                    partSymbol = None
                partValue = 0
                magnitude = 0
    return sum(parts),findGearValues(possibleGears)

res = solve("input.txt")
print("Pt1: {}, Pt2: {}".format(res[0],res[1]))
