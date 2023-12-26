import sys
import math
from functools import cache
sys.setrecursionlimit(20000)

def parseFile(f):
    lines = []
    for line in f:
        tokens = line.strip().split(' ')
        direction = tokens[0]
        length = tokens[1]
        colour = tokens[2]
        assert(len(tokens) == 3)
        lines.append((direction, int(length), colour))
    return lines

grid = []

def makeGrid(length):
    global grid
    grid = []
    for i in range(length):
        s = []
        for j in range(length):
            s.append('.')
        grid.append(s)
    return grid

def countDug(length):
    sum = 0
    for line in grid:
        s = ""
        for c in line:
            if c == '#':
                sum += 1
            s += c
        print(s)
    return sum

def dig(start, direction, length, colour):
    global grid
    nextPos = start
    for i in range(length):
        if direction == 'R':
            grid[nextPos[1]][nextPos[0]] = '#'
            nextPos = (nextPos[0]+1,nextPos[1])
        elif direction == 'D':
            grid[nextPos[1]][nextPos[0]] = '#'
            nextPos = (nextPos[0],nextPos[1]+1)
        elif direction == 'L':
            grid[nextPos[1]][nextPos[0]] = '#'
            nextPos = (nextPos[0]-1,nextPos[1])
        elif direction == 'U':
            grid[nextPos[1]][nextPos[0]] = '#'
            nextPos = (nextPos[0],nextPos[1]-1)
    return nextPos

def findValidNeighboors(pos):
    neighboors = [(pos[0]+1,pos[1]),(pos[0]-1,pos[1]),(pos[0],pos[1]+1),(pos[0],pos[1]-1)]
    return list(filter(lambda p: grid[p[1]][p[0]] == '.',neighboors))

def digInterior(pos):
    global grid
    grid[pos[1]][pos[0]] = '#'
    neighboors = findValidNeighboors(pos)
    for n in neighboors:
        digInterior(n)

def pt1(filename,gridSize):
    with open(filename, "r") as f:
        lines = parseFile(f)
        grid = makeGrid(gridSize)
        start = (0,0)
        for direction,length,colour in lines:
            start = dig(start,direction,length,colour)
        digInterior((1,1))
        return countDug(gridSize)

def getDirection(directionIdx):
    if directionIdx == '0':
        return 'R'
    elif directionIdx == '1':
        return 'D'
    elif directionIdx == '2':
        return 'L'
    elif directionIdx == '3':
        return 'U'
    else:
        assert(False)

def newPos(pos, direction, distance):
    if direction == 'R':
        return (pos[0]+distance,pos[1])
    elif direction == 'D':
        return (pos[0],pos[1]+distance)
    elif direction == 'L':
        return (pos[0]-distance,pos[1])
    elif direction == 'U':
        return (pos[0],pos[1]-distance)

def determinant(pos1, pos2):
    return pos1[0]*pos2[1] - pos1[1]*pos2[0]

def shoelace(coords):
    total = 0
    for i in range(len(coords)-1):
        det = determinant(coords[i],coords[i+1])
        total += det
    det = determinant(coords[len(coords)-1],coords[0])
    total += det
    print("Total is: " + str(total))
    return total/2

def pt2(filename):
    with open(filename, "r") as f:
        lines = parseFile(f)
        pos = (0,0)
        coords = []
        circum = 0
        for _,_,hexString in lines:
            coords.append(pos)
            direction = getDirection(hexString[-2])
            distance = int(hexString[2:-2],16)
            circum += distance
            pos = newPos(pos,direction,distance)
        assert(pos[0] == 0 and pos[1] == 0)
        print("Circumference: " + str(circum))
        return shoelace(coords) + circum/2 + 1

#assert(pt1("testInput.txt",10) == 62)
#assert(pt1("testInput2.txt",10) == pt2("testInput2.txt"))
print(pt2("input.txt"))


