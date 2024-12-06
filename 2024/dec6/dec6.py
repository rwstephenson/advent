import sys
from math import *
from collections import *
sys.path.append('../../lib')
from point import Point
from interval import Interval
from parsing import *
from aocd import submit

def guardOnMap(guardLocation):
    return guardLocation.x >= 0 and guardLocation.x <= guardLocation.maxX and guardLocation.y >= 0 and guardLocation.y <= guardLocation.maxY

def nextDirection(direction):
    if direction == 'N':
        return 'E'
    elif direction == 'E':
        return 'S'
    elif direction == 'S':
        return 'W'
    elif direction == 'W':
        return 'N'
    else:
        assert(False)

def guardWalk(guard,obstacles,direction):
    seen = defaultdict(set)
    steps = 1
    while(True):
        nextSpot = guard.getNeighboor(direction)
        if not nextSpot:
            return (False,steps)
        elif hash(nextSpot) in obstacles:
            direction = nextDirection(direction)
        elif len(seen[hash(guard)]) > 0:
            guard = nextSpot
            if direction in seen[hash(guard)]:
                return (True,steps)
        else:
            seen[hash(guard)].add(direction)
            guard = nextSpot
            steps += 1

def solve(filename, pt):
    grid = parseLines(filename)
    guard = None
    obstacles = set()
    total = 0
    for r in range(len(grid)):
        g = grid[r].find('^')
        o = findAll(grid[r],'#')
        if g >= 0:
            guard = Point(g,r,grid)
        for ob in o:
            obstacles.add(hash(Point(ob,r,grid)))
    if pt == 1:
        return guardWalk(guard,obstacles,'N')[1]
    elif pt == 2:
        for r in range(len(grid)):
            for c in range(len(grid[r])):
                newObstacle = Point(c,r,grid)
                if newObstacle.value == '.':
                    obstacles.add(hash(newObstacle))
                    loops,steps = guardWalk(guard,obstacles,'N')
                    if loops:
                        total += 1
                    obstacles.remove(hash(newObstacle))
        return total

def run(pt,expected,day,year):
    resTest = solve("testInput.txt",pt)
    assert resTest == expected, f"Result was {resTest}"
    res = solve("input.txt",pt)
    print("Test Input: {} Puzzle Input: {}".format(resTest,res))
    if pt == 1:
        c = "a"
    else:
        c = "b"
    submit(res, part=c, day=day, year=year)

run(1,41,6,2024)
run(2,6,6,2024)
