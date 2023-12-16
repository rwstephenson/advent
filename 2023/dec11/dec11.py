import sys
import math

def readGalaxy(f):
    spaces = []
    for line in f:
        spaces.append(line.strip())
    return spaces

def expandSpaceLine(spaceLine, expandingX,expandFactor):
    newSpaceLine = ""
    i = 0
    for x in expandingX:
        newSpaceLine += spaceLine[i:x]
        for k in range(expandFactor - 1):
            newSpaceLine += '.'
        i = x
    newSpaceLine += spaceLine[i:]
    return newSpaceLine

def findGalaxies(spaceLine,y,expandingX, expandFactor):
    foundGalaxies = []
    xExpandAdditions = 0
    for x in range(len(spaceLine)):
        if spaceLine[x] == '#':
            foundGalaxies.append((x + xExpandAdditions,y))
        if x in expandingX:
            xExpandAdditions += expandFactor - 1
        x += 1
    return foundGalaxies

def expandSpace(origSpace,expandFactor):
    galaxies = []
    expandedSpace = []
    expandingX = []
    expandingY = []
    y = 0
    x = 0
    for line in origSpace:
        if line.find("#") == -1:
            expandingY.append(y)
        y += 1
    y = 0
    while x < len(origSpace[0]):
        found = False
        while y < len(origSpace):
            if origSpace[y][x] == '#':
                found = True
            y += 1
        if not found:
            expandingX.append(x)
        x += 1
        y = 0

    for spaceLine in origSpace:
        if spaceLine.find("#") > -1:
            galaxies += findGalaxies(spaceLine,y, expandingX, expandFactor)
        else:
            y += expandFactor - 1
        y += 1
    return galaxies

def pairUp(galaxies):
    galaxyPairs = []
    sum = 0
    for g in range(len(galaxies)):
        for i in range(g,len(galaxies)):
            if galaxies[g][0] != galaxies[i][0] or galaxies[g][1] != galaxies[i][1]:
                galaxyPairs.append((galaxies[g],galaxies[i]))
                sum += 1
    return galaxyPairs

def calcDistance(g1, g2):
    dist = 0
    if g1[0] == g2[0]:
        dist = abs(g1[1]-g2[1])
    elif g1[1] == g2[1]:
        dist = abs(g1[0]-g2[0])
    else:
        dist = abs(g1[0]-g2[0]) + abs(g1[1]-g2[1])
    return dist

def pt1(filename, expandFactor):
    with open(filename, "r") as f:
        origSpace = readGalaxy(f)
        galaxies = expandSpace(origSpace,expandFactor)
        galaxyPairs = pairUp(galaxies)
        sum = 0
        for galaxyPair in galaxyPairs:
            sum += calcDistance(galaxyPair[0],galaxyPair[1])
        return sum

print(pt1("input.txt", 1000000))

