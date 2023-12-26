import sys
import math
from functools import cache

grid = []

class Point():
    x = -1
    y = -1

    def __init__(self,x,y):
        self.x = x
        self.y = y

    def valueAt(self):
        return int(grid[self.y][self.x])

    def toStr(self):
        return str(self.x) + "," + str(self.y)

    def getNeighboor(self,direction):
        if direction == 'L' and self.x > 0:
            return Point(self.x-1,self.y)
        if direction == 'R' and self.x + 1 < len(grid[0]):
            return Point(self.x+1,self.y)
        if direction == 'U' and self.y > 0:
            return Point(self.x,self.y-1)
        if direction == 'D' and self.y + 1 < len(grid):
            return Point(self.x,self.y+1)
        return None

def parseFile(f):
    global grid
    for line in f:
        grid.append(line.strip())
        print(grid[-1])
    return grid

def getValidDirections(node, maxX, maxY, prevDir, streak, maxStreak):
    directions = []
    if node[0] > 0 and prevDir != 'R' and (streak == maxStreak and prevDir != 'L'):
        directions.append('L')
    if node[0] < maxX and prevDir != 'L' and (streak == maxStreak and prevDir != 'R'):
        directions.append('R')
    if node[1] > 0 and prevDir != 'D' and (streak == maxStreak and prevDir != 'U'):
        directions.append('U')
    if node[1] < maxY and prevDir != 'U' and (streak == maxStreak and prevDir != 'D'):
        directions.append('D')
    return directions

INF = 1000000

def getMin(qDict):
    minDist = 1000000
    minKey = "null"
    for stateStr in qDict.keys():
        if qDict[stateStr] < minDist:
            minDist = qDict[stateStr]
            minKey = stateStr
    assert(minKey != "null") # Meant there was no distance less than infinte, which cannot be true.
    return minKey

def printDict(d):
    for k in d.keys():
        if d[k] < 1000000:
            print("Node: " + k + " dist: " + str(d[k]))


class State():
    point = Point(-1,-1)
    streak = -1
    direction = 'S'
    prev = None

    def __init__(self, point, streak, direction):
        self.point = point
        self.streak = streak
        self.direction = direction

    def toStr(self):
        return self.point.toStr() + "," + str(self.streak) + "," + self.direction

    def validNeighboorStates(self,minSteps, maxSteps):
        validNeighboorStates = []
        validDirections = []
        if self.direction == 'R' or self.direction == 'L':
            validDirections = ['U','D']
        elif self.direction == 'U' or self.direction == 'D':
            validDirections = ['L','R']
        if self.streak != maxSteps:
            validDirections.append(self.direction)
        if self.streak < minSteps:
            validDirections = [self.direction]
        for direction in validDirections:
            neighboor = self.point.getNeighboor(direction)
            newStreak = self.streak + 1
            if direction != self.direction:
                newStreak = 1
            validNeighboorStates.append(State(neighboor, newStreak, direction))
        return list(filter(lambda s: s.point is not None, validNeighboorStates))

def makeState(stateStr):
    line = stateStr.split(',')
    point = Point(int(line[0]),int(line[1]))
    streak = int(line[2])
    direction = line[3]
    return State(point,streak,direction)

def getMinFinalState(target,maxSteps, distance):
    res = INF
    for direction in ['U','D','L','R']:
        for s in range(maxSteps + 1):
            res = min(res,distance[State(target,s,direction)])
    return res



def findShortestPath(start,target,minSteps, maxSteps):
    distance = {}
    prev = {}
    q = {}
    lenX = len(grid[0])
    lenY = len(grid)
    streak = 0

    for y in range(lenY):
        for x in range(lenX):
            for s in range(maxSteps+1):
                for direction in ['U','D','L','R']:
                    state = State(Point(x,y),s,direction)
                    distance[state.toStr()] = INF

    startState = State(start,0,'R').toStr()
    q[startState] = 0
    distance[startState] = 0

    while len(q) > 0:
        print("Length of Q: " + str(len(q)))
        stateStr = getMin(q)
        dist = q.pop(stateStr)
        state = makeState(stateStr)
        if state.point.toStr() == target.toStr():
            return state,dist
        neighboorStates = state.validNeighboorStates(minSteps, maxSteps)
        for neighboorState in neighboorStates:
            newDist = distance[state.toStr()] + neighboorState.point.valueAt()
            if newDist < distance[neighboorState.toStr()]:
                neighboorState.prev = state
                distance[neighboorState.toStr()] = newDist
                q[neighboorState.toStr()] = newDist

def pt1(filename):
    with open(filename, "r") as f:
        parseFile(f)
        endState, dist = findShortestPath(Point(0,0),Point(len(grid[0])-1,len(grid)-1),4,10)
        return dist

#assert(pt1("testInput.txt") == 94)
#print(pt1("testInput.txt"))
print(pt1("input.txt"))


