import sys
import math
from functools import cache

grid = []

def nodeToStr(n):
    return str(n[0]) + ',' + str(n[1])

def countHash(line):
    total = 0
    for c in line:
        if c == '#':
            total += 1
    return total

def parseFile(f):
    global grid
    y = 0
    startX = -1
    startY = -1
    totalHash = 0
    for line in f:
        totalHash += countHash(line)
        grid.append(line.strip())
        s = grid[-1].find('S')
        if s > -1:
             startX = s
             startY = y
        y += 1
        #print(grid[-1])
    print("Grid had " + str(totalHash) + " has spots.  Total available spots: " + str(len(grid) * len(grid[0]) - totalHash))
    print("Grid len: " + str(len(grid[0])) + " width: " + str(len(grid)))
    return len(grid[0]), len(grid)

def findNeighboors2(x,y):
    validN = []
    maxX = len(grid[0])
    maxY = len(grid)
    if grid[y%maxY][(x-1)%maxX] == '.':
        validN.append((x-1,y))
    if grid[y%maxY][(x+1)%maxX] == '.':
        validN.append((x+1,y))
    if grid[(y-1)%maxY][x%maxX] == '.':
        validN.append((x,y-1))
    if grid[(y+1)%maxY][x%maxX] == '.':
        validN.append((x,y+1))
    return validN

def findNeighboors(x,y):
    validN = []
    if x > 0:
        if grid[y][x-1] == '.':
            validN.append((x-1,y))
    if x < len(grid[0])-1:
        if grid[y][x+1] == '.':
            validN.append((x+1,y))
    if y > 0:
        if grid[y-1][x] == '.':
            validN.append((x,y-1))
    if y < len(grid) - 1:
        if grid[y+1][x] == '.':
            validN.append((x,y+1))
    return validN

def bfs(q,visited,pos,inf):
    while len(q) > 0:
        n = q.pop(0)
        stepsLeft = n[2]
        visited.add(nodeToStr(n))
        if stepsLeft % 2 == 1:
            pos.add(nodeToStr(n))
        if stepsLeft > 0:
            if inf:
                neighboors = findNeighboors2(n[0],n[1])
            else:
                neighboors = findNeighboors(n[0],n[1])
            for nN in neighboors:
                if nodeToStr(nN) not in visited:
                    q.append((nN[0],nN[1],stepsLeft-1))
                    visited.add(nodeToStr(nN))
    return len(pos)

def getTotalGrids(radius):
    print("Radius: " + str(radius))
    total = 0
    for i in range(radius+1):
        total += radius+1 -i
    return total*4 + 1 # Center grid

def pt2(filename, startX, startY, numSteps):
    with open(filename, "r") as f:
        length, width = parseFile(f)
        assert(length == width)
        radius = (numSteps - startX) // length # 202300
        # one center grid
        farStraight = 1         # Enters at the center edge, with 0 steps remaining
        oneDiamStraight = 1   # Enters at the center edge, with grid diameter remaining (131)
        corner = radius         # Enters at the corner, with grid radius remaining (65)
        twoEdges = (radius - 1) # NW = Count twice, Enters at N edge with diameters (131) remaining.  Same comes from W.
        fullGrids = getTotalGrids(radius) - farStraight*4 - oneDiamStraight*4 - corner*4 - twoEdges*4 - 1
        print("Total Grids: " + str(getTotalGrids(radius)))
        print("Full grids: " + str(fullGrids))
        centerGridWeight = bfs([(startX,startY,232)],set(),set(),False)
        print("Weight from Center Grid: " + str(centerGridWeight))
        fullGridAvgWeight = (bfs([(0,startY,231)],set(),set(),False) + bfs([(0,startY,232)],set(),set(),False))//2
        print("Full grid weight: " + str(fullGridAvgWeight))
        print("Weight from Full Grids: " + str(fullGrids * fullGridAvgWeight))
        straightEastWeight = bfs([(width-1,startY, 1)],set(),set(),False)
        straightNorthWeight = bfs([(startX,0, 1)],set(),set(),False)
        straightWestWeight = bfs([(0, startY, 1)],set(),set(),False)
        straightSouthWeight = bfs([(startX, length-1, 1)],set(),set(),False)
        cornerNEWeight = bfs([(0,0,(numSteps) % length)],set(),set(),False)
        print("CornerNE Weight:" + str(cornerNEWeight))
        cornerNWWeight = bfs([(width-1,0,(numSteps) % length)],set(),set(),False)
        print("CornerNW Weight:" + str(cornerNWWeight))
        cornerSEWeight = bfs([(0,length-1,(numSteps) % length)],set(),set(),False)
        print("CornerSE Weight:" + str(cornerSEWeight))
        cornerSWWeight = bfs([(width-1,length-1,(numSteps) % length)],set(),set(),False)
        print("CornerSW Weight:" + str(cornerSWWeight))
        oneDiamEWeight = bfs([(width-1,startY, length)],set(),set(),False)
        print("lastEWeight: " + str(oneDiamEWeight))
        oneDiamNWeight = bfs([(startX,0, length)],set(),set(),False)
        print("lastNWeight: " + str(oneDiamNWeight))
        oneDiamSWeight = bfs([(startX,length-1, length)],set(),set(),False)
        print("lastSWeight: " + str(oneDiamSWeight))
        oneDiamWWeight = bfs([(0,startY, length)],set(),set(),False)
        print("lastWWeight: " + str(oneDiamWWeight))
        northEastSet = set()
        bfs([(width-1,startY, length)],set(),northEastSet,False)
        bfs([(startX,0, length)],set(),northEastSet,False)
        twoEdgesNEWeight = len(northEastSet)
        print("twoEdgesNEWeight: " + str(twoEdgesNEWeight))
        northWestSet = set()
        bfs([(startX,0, length)],set(),northWestSet,False)
        bfs([(0,startY, length)],set(),northWestSet,False)
        twoEdgesNWWeight = len(northWestSet)
        print("twoEdgesNWWeight: " + str(twoEdgesNWWeight))
        southEastSet = set()
        bfs([(width-1,startY, length)],set(),southEastSet,False)
        bfs([(startX,length-1, length)],set(),southEastSet,False)
        twoEdgesSEWeight = len(southEastSet)
        print("twoEdgesSEWeight: " + str(twoEdgesSEWeight))
        southWestSet = set()
        bfs([(startX,length-1, length)],set(),southWestSet,False)
        bfs([(0,startY, length)],set(),southWestSet,False)
        twoEdgesSWWeight = len(southWestSet)
        print("twoEdgesSWWeight: " + str(twoEdgesSWWeight))
        return (centerGridWeight * 1) + \
                (fullGridAvgWeight * fullGrids) + \
                (straightEastWeight * farStraight) + \
                (straightWestWeight * farStraight) + \
                (straightNorthWeight * farStraight) + \
                (straightSouthWeight * farStraight) + \
                (oneDiamEWeight * oneDiamStraight) + \
                (oneDiamNWeight * oneDiamStraight) + \
                (oneDiamWWeight * oneDiamStraight) + \
                (oneDiamSWeight * oneDiamStraight) + \
                (cornerNEWeight * corner) + \
                (cornerNWWeight * corner) + \
                (cornerSEWeight * corner) + \
                (cornerSWWeight * corner) + \
                (twoEdgesNEWeight * twoEdges) + \
                (twoEdgesNWWeight * twoEdges) + \
                (twoEdgesSEWeight * twoEdges) + \
                (twoEdgesSWWeight * twoEdges) + 8 + 12*(radius-1)


def pt1(filename,startX, startY, numSteps,inf):
    with open(filename, "r") as f:
        length, width = parseFile(f)
        return bfs([(startX,startY,numSteps+1)],set(),set(),inf)

radius = 3
#pt2Res = pt2("input.txt",65,65,65+(131*radius))
#pt1Res = pt1("input.txt",65,65,65+(131*radius),True)
#print("Part2: " + str(pt2Res))
#print("Part1: " + str(pt1Res))
#print("delta: " + str(pt2Res - pt1Res))
print(pt2("input.txt",65,65,26501365))
#print(pt1("testInput2.txt",5,5,5+11+11,True))
#print(pt1("testInput3.txt",27,27,5+11+11,False))
#print(pt2("testInput2.txt",5,5,5+11+11))
