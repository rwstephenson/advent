import sys
import math
from functools import lru_cache
sys.setrecursionlimit(10000)


def parseFile(f):
    grid = []
    for line in f:
        grid.append(line.strip())
        print(grid[-1])
    return grid

energizedCoords = set()

def numEnergized():
    energized = set()
    for coordsAndDistance in energizedCoords:
        idx = coordsAndDistance.find(':')
        energized.add(coordsAndDistance[0:idx])
    return len(energized)

def shineBeam(x,y,direction,grid):
    if x == -1 or x == len(grid[0]) or y == -1 or y == len(grid):
        return
    hashStr = str(x) + ',' + str(y) + ':' + direction
    if hashStr in energizedCoords:
        return
    energizedCoords.add(hashStr)
    c = grid[y][x]
    if direction == 'L':
        if c == '.' or c == '-':
            shineBeam(x-1,y,direction,grid)
        elif c == '/':
            shineBeam(x,y+1,'D',grid)
        elif c == '\\':
            shineBeam(x,y-1,'U',grid)
        elif c == '|':
            shineBeam(x,y-1,'U',grid)
            shineBeam(x,y+1,'D',grid)
    elif direction == 'R':
        if c == '.' or c == '-':
            shineBeam(x+1,y,direction,grid)
        elif c == '/':
            shineBeam(x,y-1,'U',grid)
        elif c == '\\':
            shineBeam(x,y+1,'D',grid)
        elif c == '|':
            shineBeam(x,y-1,'U',grid)
            shineBeam(x,y+1,'D',grid)
    elif direction == 'U':
        if c == '.' or c == '|':
            shineBeam(x,y-1,direction,grid)
        elif c == '/':
            shineBeam(x+1,y,'R',grid)
        elif c == '\\':
            shineBeam(x-1,y,'L',grid)
        elif c == '-':
            shineBeam(x-1,y,'L',grid)
            shineBeam(x+1,y,'R',grid)
    elif direction == 'D':
        if c == '.' or c == '|':
            shineBeam(x,y+1,direction,grid)
        elif c == '\\':
            shineBeam(x+1,y,'R',grid)
        elif c == '/':
            shineBeam(x-1,y,'L',grid)
        elif c == '-':
            shineBeam(x-1,y,'L',grid)
            shineBeam(x+1,y,'R',grid)



def pt1(filename):
    with open(filename, "r") as f:
        grid = parseFile(f)
        return runProblem(0,0,'R',grid)

def runProblem(x,y,d,grid):
    energizedCoords.clear()
    shineBeam(x,y,d,grid)
    result = numEnergized()
    print("Result of simulation for : " + str(x) + "," + str(y) + ',' + d + " : " + str(result))
    return result

def pt2(filename):
    with open(filename, "r") as f:
        grid = parseFile(f)
        maxEnergized = 0
        for y in range(len(grid)):
            maxEnergized = max(maxEnergized, runProblem(0,y,'R',grid))
            maxEnergized = max(maxEnergized, runProblem(len(grid[0])-1,y,'L',grid))
        for x in range(len(grid[0])):
            maxEnergized = max(maxEnergized, runProblem(x,0,'D',grid))
            maxEnergized = max(maxEnergized, runProblem(x, len(grid)-1,'U',grid))
        return maxEnergized

#assert(pt1("testInput.txt") == 46)
print(pt2("input.txt"))


