import sys
import math
from functools import lru_cache


def parseFile(f):
    ground = []
    roundRocks = []
    cubes = []
    y = 0
    lenLine = 0
    for line in f:
        for x in range(len(line.strip())):
            lenLine = len(line.strip()) - 1
            c = line[x]
            if c == 'O':
                roundRocks.append((x,y))
            elif c == '#':
                cubes.append((x,y))
        y += 1
        ground.append(line.strip())
    return roundRocks,cubes,y,lenLine

def calculateLoad(roundRocks,maxDistance):
    totalLoad = 0
    for rock in roundRocks:
        totalLoad += maxDistance - rock[1]
    return totalLoad

def tiltN(rock, blockersForX):
    nearest = -1
    for blocker in blockersForX:
        assert(blocker[1] != rock[1])
        if blocker[1] < rock[1]:
            nearest = max(blocker[1],nearest)
    return (rock[0],nearest + 1)

def tiltS(rock, blockersForX, maxDistance):
    nearest = maxDistance
    for blocker in blockersForX:
        assert(blocker[1] != rock[1])
        if blocker[1] > rock[1]:
            nearest = min(blocker[1],nearest)
    return (rock[0],nearest - 1)

def tiltW(rock, blockersForY):
    nearest = -1
    for blocker in blockersForY:
        assert(blocker[0] != rock[0])
        if blocker[0] < rock[0]:
            nearest = max(blocker[0],nearest)
    return (nearest + 1,rock[1])

def tiltE(rock, blockersForY, maxDistance):
    nearest = maxDistance
    for blocker in blockersForY:
        assert(blocker[0] != rock[0])
        if blocker[0] > rock[0]:
            nearest = min(blocker[0],nearest)
    return (nearest - 1,rock[1])

def tiltAllNS(roundRocks, cubes, maxDistance, maxX, isNorth):
    tiltedRocks = []
    for x in range(maxX+1):
        blockersForX = list(filter(lambda cube: cube[0] == x, cubes))
        roundForX = sorted(list(filter(lambda rock: rock[0] == x, roundRocks)),key=lambda rock: rock[1],reverse=not isNorth)
        for rock in roundForX:
            if isNorth:
                tiltedRock = tiltN(rock, blockersForX)
            else:
                tiltedRock = tiltS(rock, blockersForX,maxX+1)
            blockersForX.append(tiltedRock)
            tiltedRocks.append(tiltedRock)
    return tiltedRocks

def tiltAllEW(roundRocks, cubes, maxDistance, maxY, isWest):
    tiltedRocks = []
    for y in range(maxY+1):
        blockersForY = list(filter(lambda cube: cube[1] == y, cubes))
        roundForY = sorted(list(filter(lambda rock: rock[1] == y, roundRocks)),key=lambda rock: rock[0],reverse=not isWest)
        for rock in roundForY:
            if isWest:
                tiltedRock = tiltW(rock, blockersForY)
            else:
                tiltedRock = tiltE(rock, blockersForY, maxY+1)
            blockersForY.append(tiltedRock)
            tiltedRocks.append(tiltedRock)
    return tiltedRocks

def spin(roundRocks, cubes, maxDistance,maxX,numTilts):
    tiltedRocks = roundRocks
    for i in range(numTilts):
        if i % 4 == 0:
            tiltedRocks = tiltAllNS(tiltedRocks,cubes,maxDistance,maxX,True)
        elif i % 4 == 1:
            tiltedRocks = tiltAllEW(tiltedRocks,cubes,maxDistance,maxX,True)
        elif i % 4 == 2:
            tiltedRocks = tiltAllNS(tiltedRocks,cubes,maxDistance,maxX,False)
        elif i % 4 == 3:
            tiltedRocks = tiltAllEW(tiltedRocks,cubes,maxDistance,maxX,False)
    return tiltedRocks

def pt1(filename):
    with open(filename, "r") as f:
        roundRocks,cubes,maxDistance,x = parseFile(f)
        roundRocks = spin(roundRocks,cubes,maxDistance,x,1)
        return calculateLoad(roundRocks,maxDistance)

def pt2(filename,cycles):
    with open(filename, "r") as f:
        roundRocks,cubes,maxDistance,x = parseFile(f)
        load = 0
        numsSeen = {}
        modulos = {}
        for i in range(cycles):
            roundRocks = spin(roundRocks,cubes,maxDistance,x,4)
            load = calculateLoad(roundRocks, maxDistance)
            print("i = " + str(i) + " Load: " + str(load))
            modulos[i%17] = load
            if load in numsSeen:
                numsSeen[load] = numsSeen[load] + 1
            else:
                numsSeen[load] = 1
        i = 0
        for num in numsSeen:
            if numsSeen[num] > 10:
                print(str(i) + ". " + str(num) + " " + str(numsSeen[num]))
                i+= 1
        print(modulos)
        return load

assert(pt1("input.txt") == 109098)
#print(pt1("testInput2.txt"))
print(pt2("input.txt", 300))

