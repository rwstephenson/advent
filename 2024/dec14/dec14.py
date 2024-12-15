import sys
from math import *
from collections import *
sys.path.append('../../lib')
from point import Point
from interval import Interval
from parsing import *
from aocd import get_data, submit

def takeStep(pos,v,maxX,maxY,steps):
    return ((pos[0]+v[0]*steps)%(maxX+1),(pos[1]+v[1]*steps)%(maxY+1))

def countResult(robots,maxX,maxY):
    midX = maxX // 2
    midY = maxY // 2
    assert(midX == maxX - midX)
    quads = [0,0,0,0]
    for robot in robots:
        if robot[0][0] < midX and robot[0][1] < midY:
            quads[0] += 1
        elif robot[0][0] > midX and robot[0][1] < midY:
            quads[1] += 1
        elif robot[0][0] < midX and robot[0][1] > midY:
            quads[2] += 1
        elif robot[0][0] > midX and robot[0][1] > midY:
            quads[3] += 1
        else:
            assert(robot[0][0] == midX or robot[0][1] == midY)
    return quads[0]*quads[1]*quads[2]*quads[3]

def checkTree(robots,maxX,maxY,i):
    grid = []
    robotDict = defaultdict(set)
    for robot in robots:
        robotDict[robot[0][1]].add(robot[0][0])
    for y in range(maxY):
        line = ""
        for x in range(maxX):
            if x in robotDict[y]:
                line += "R"
            else:
                line += "."
        if i == 7036:
            print(line)
        grid.append(line)

    for y in range(maxY):
        for x in robotDict[y]:
            seP = Point(x,y,grid)
            swP = Point(x,y,grid)
            for k in range(10):
                if seP and swP and seP.value == 'R' and swP.value == 'R':
                    if k > 4:
                        return True
                    seP = seP.getNeighboor('SE')
                    swP = swP.getNeighboor('SW')
                else:
                    break
    return False

def checkAllPeriods(robots,period,maxX,maxY):
    for robot in robots:
        newPos = takeStep(robot[0],robot[1],maxX,maxY,period)
        if robot[0][0] != newPos[0] or robot[0][1] != newPos[1]:
            return False
    return True

def solve(filename, pt):
    lines = parseLines(filename)
    origRobots = []
    maxX = 0
    maxY = 0
    part1Result = 0
    for line in lines:
        ints = getInts(line)
        assert(len(ints) == 4)
        origRobots.append(((ints[0],ints[1]),(ints[2],ints[3])))
        maxX = max(ints[0],maxX)
        maxY = max(ints[1],maxY)
    if pt == 1:
        steps = 100
        newRobots = []
        for robot in origRobots:
            newRobots.append(((takeStep((robot[0][0],robot[0][1]),robot[1],maxX,maxY,steps)),robot[1]))
        return countResult(newRobots,maxX,maxY)
    elif pt == 2:
        steps = 10403
        #assert(checkAllPeriods(origRobots,steps,maxX,maxY))
        for i in range(steps):
            newRobots = []
            for robot in origRobots:
                newRobots.append(((takeStep((robot[0][0],robot[0][1]),robot[1],maxX,maxY,1)),robot[1]))
            origRobots = newRobots.copy()
            newRobots = []
            if checkTree(origRobots,maxX,maxY,i):
                return i+1
    return -1

def run(pt,day,year,expect):
    with open("input.txt","w") as f:
        f.write(get_data(day=day,year=year))
    resTest = solve("testInput.txt",pt)
    assert resTest == expect, f"Result was {resTest}"
    res = solve("input.txt",pt)
    print("Test Input: {} Puzzle Input: {}".format(resTest,res))
    if pt == 1:
        c = 'a'
    elif pt == 2:
        c = 'b'
    submit(res, part=c, day=day, year=year)

run(1,14,2024,12)
run(2,14,2024,-1)
