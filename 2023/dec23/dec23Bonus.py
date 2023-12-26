import sys
import math
from functools import cache
sys.setrecursionlimit(20000)

grid = []

class Point():
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def isValid(self):
        return self.x >= 0 and self.x < len(grid) and self.y >= 0 and self.y < len(grid)

    def value(self):
        assert(self.isValid())
        return grid[self.y][self.x]

    def toStr(self):
        return str(self.x) + "," + str(self.y)

    def canWalk(self, p):
        assert(self.isValid())
        if not p.isValid():
            return False
        elif p.value() == '#':
            return False
        elif self.value() == '>':
            return p.x == self.x+1 and p.y == self.y
        elif self.value() == '<':
            return p.x == self.x-1 and p.y == self.y
        elif self.value() == '^':
            return p.x == self.x and p.y == self.y - 1
        elif self.value() == 'v':
            return p.x == self.x and p.y == self.y + 1
        else:
            return True

    def getNeighboors(self):
        poss = [Point(self.x-1,self.y), Point(self.x+1,self.y), Point(self.x, self.y-1), Point(self.x, self.y+1)]
        return list(filter(lambda p: self.canWalk(p), poss))


def parseFile(f):
    global grid
    i = 0
    s = Point(0,0)
    e = Point(0,0)
    for line in f:
        if i == 0:
            s = Point(line.find('.'), i)
        e = Point(line.find('.'), i)
        grid.append(line.strip())
        print(grid[-1])
        i += 1
    return s, e

maxPathLength = 0

def findLongestPath(s,f,pathSoFar):
    assert(s.value() != '#')
    if s in pathSoFar:
        return -1
    elif s.toStr() == f.toStr():
        global maxPathLength
        maxPathLength = max(maxPathLength, len(pathSoFar))
        print ("Found the end! Max so far: " + str(maxPathLength))
        return len(pathSoFar)
    pathSoFar.add(s.toStr())
    validNeighboors = list(filter(lambda p: p.toStr() not in pathSoFar, s.getNeighboors()))
    longestPath = 0
    for n in validNeighboors:
        if len(validNeighboors) > 1:
            res = findLongestPath(n,f,pathSoFar.copy())
        else:
            res = findLongestPath(n,f,pathSoFar)
        if res == -1:
            pass
        longestPath = max(longestPath, res)
    return longestPath

def pt1(filename):
    with open(filename, "r") as f:
        start, finish = parseFile(f)
        print("Start: " + start.toStr() + " Finish: " + finish.toStr())
        return findLongestPath(start,finish,set())

print(pt1("input.txt"))
