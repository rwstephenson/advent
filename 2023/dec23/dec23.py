import sys
import math
from functools import cache
import time
sys.setrecursionlimit(20000)

grid = []
branchPoints = {}

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

    def canWalk(self, p, pt1):
        assert(self.isValid())
        if not p.isValid():
            return False
        elif p.value() == '#':
            return False
        elif self.value() == '>' and pt1:
            return p.x == self.x+1 and p.y == self.y
        elif self.value() == '<' and pt1:
            return p.x == self.x-1 and p.y == self.y
        elif self.value() == '^' and pt1:
            return p.x == self.x and p.y == self.y - 1
        elif self.value() == 'v' and pt1:
            return p.x == self.x and p.y == self.y + 1
        else:
            return True

    def getNeighboors(self, pt1):
        poss = [Point(self.x-1,self.y), Point(self.x+1,self.y), Point(self.x, self.y-1), Point(self.x, self.y+1)]
        return list(filter(lambda p: self.canWalk(p,pt1), poss))


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

def sumPathSoFar(pathSoFar):
    total = 0
    for n in pathSoFar:
        total += pathSoFar[n]
    return total

maxPath = {}

def findLongestPath2(s,f,edgeWeight,pathSoFar):
    assert(s.value() != '#')
    if s.toStr() in pathSoFar:
        return -1
    elif s.toStr() == f.toStr():
        global maxPathLength
        global maxPath
        pathSoFar[s.toStr()] = edgeWeight
        if sumPathSoFar(pathSoFar) > maxPathLength:
            maxPath = pathSoFar.copy()
        maxPathLength = max(maxPathLength, sumPathSoFar(pathSoFar))
        print(maxPathLength)
        return sumPathSoFar(pathSoFar)
    pathSoFar[s.toStr()] = edgeWeight
    validNeighboors = list(filter(lambda p: p[0].toStr() not in pathSoFar, branchPoints[s.toStr()]))
    longestPath = 0
    for neighboor in validNeighboors:
        newPathSoFar = {}
        for p in pathSoFar.keys():
            newPathSoFar[p] = pathSoFar[p]
        res = findLongestPath2(neighboor[0],f,neighboor[1],newPathSoFar)
        longestPath = max(longestPath, res)
    return longestPath

def buildBranchGraph(start,finish):
    global branchPoints
    visited = set()
    visited.add(start.toStr())
    branchPoints[start.toStr()] = []
    branchQ = [start]
    while len(branchQ) > 0:
        lastBranch = branchQ.pop(0)
        assert(lastBranch.toStr() in branchPoints)
        branchPaths = list(filter(lambda p: p.toStr() not in visited, lastBranch.getNeighboors(False)))
        for pathStart in branchPaths:
            n = pathStart
            edgeWeight = 0
            while True:
                edgeWeight += 1
                branchNeighboors = list(filter(lambda p: p.toStr() in branchPoints, n.getNeighboors(False)))
                assert(len(branchNeighboors) <= 1)
                neighboors = list(filter(lambda p: p.toStr() not in visited, n.getNeighboors(False)))
                if len(branchNeighboors) == 1 and branchNeighboors[0].toStr() != lastBranch.toStr():
                    # We've seen this branch point before.  Add to the adjacency lists, check next path
                    branchPoints[lastBranch.toStr()] = branchPoints[lastBranch.toStr()] + [(branchNeighboors[0],edgeWeight+1)]
                    branchPoints[branchNeighboors[0].toStr()] = branchPoints[branchNeighboors[0].toStr()] + [(lastBranch,edgeWeight+1)]
                    break
                elif len(neighboors) > 1:
                    # This is another branch point, but we haven't seen it before.
                    # Add to adjancency lists, add to q.  Next Path
                    assert(n.toStr() not in visited)
                    branchPoints[lastBranch.toStr()] = branchPoints[lastBranch.toStr()] + [(n,edgeWeight)]
                    branchPoints[n.toStr()] = [(lastBranch,edgeWeight)]
                    visited.add(n.toStr())
                    branchQ.append(n)
                    break
                elif len(neighboors) == 0:
                    # Dead End, quit
                    visited.add(n.toStr())
                    if n.toStr() == finish.toStr():
                        branchPoints[lastBranch.toStr()] = branchPoints[lastBranch.toStr()] + [(finish,edgeWeight)]
                        branchPoints[finish.toStr()] = [(lastBranch,edgeWeight)]
                    break
                else:
                    # Not a branch, just keep moving.
                    assert(len(neighboors) == 1)
                    visited.add(n.toStr())
                    n = neighboors[0]
    for junction in branchPoints.keys():
        print("For junction: " + junction)
        for adjacent in branchPoints[junction]:
            print(adjacent[0].toStr() + " with weight: " + str(adjacent[1]))
    return len(branchPoints)

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
    validNeighboors = list(filter(lambda p: p.toStr() not in pathSoFar, s.getNeighboors(True)))
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

def pt2(filename):
    with open(filename, "r") as f:
        start, finish = parseFile(f)
        print("Start: " + start.toStr() + " Finish: " + finish.toStr())
        print(buildBranchGraph(start,finish))
        res = findLongestPath2(start,finish,0,{})
        print(maxPath)
        return res

print(pt2("input.txt"))


