import sys
from math import *
from collections import *
sys.path.append('../../lib')
from point import Point
from interval import Interval
from parsing import *
from aocd import get_data, submit
from functools import lru_cache

def getPathNeighboors(path):
    neighboors = set()
    for p in path:
        pns = p.getNeighboors()
        for n in pns:
            neighboors.add(n)
    return neighboors

@lru_cache()
def pathLen(s,e):
    return len(s.bfs(e,['#']))

def getCheatEndpoints(s,seconds):
    assert(s.value != '#')
    endpoints = []
    for x in range(0-seconds,seconds+1):
        for y in range(0-seconds,seconds+1):
            p = Point(s.x + x, s.y+y,s.grid)
            if p.value and p.value != '#' and abs(x) + abs(y) <= seconds:
                endpoints.append(p)
    return endpoints

def solve2(filename, pt, savings,seconds):
    lines = parseLines(filename)
    grid = []
    s = None
    e = None
    total = 0
    for r in range(len(lines)):
        sx = lines[r].find('S')
        ex = lines[r].find('E')
        if sx >= 0:
            sxy = (sx,r)
        if ex >= 0:
            exy = (ex,r)
        row = []
        for c in range(len(lines[r])):
            row.append(lines[r][c])
        grid.append(row)
    s = Point(sxy[0],sxy[1],grid)
    e = Point(exy[0],exy[1],grid)
    baselinePath = s.bfs(e,['#'])
    baselineDist = len(baselinePath) - 1
    print(baselineDist)
    cheats = set()
    for p in baselinePath:
        endpoints = getCheatEndpoints(p,seconds)
        for endpoint in endpoints:
            distanceToCheat = pathLen(s,p) - 1
            cheatDistance = p.distance(endpoint)
            distanceFromCheat = pathLen(endpoint,e) - 1
            newDist = distanceToCheat + cheatDistance + distanceFromCheat
            if baselineDist - newDist >= savings and hash((p,endpoint)) not in cheats:
                print("Cheat from {} to {} Distance To {} Cheat Dist {} Remainig {} ".format(p, endpoint,distanceToCheat,cheatDistance,distanceFromCheat))
                total += 1
    return total


def solve(filename, pt, savings):
    lines = parseLines(filename)
    grid = []
    s = None
    e = None
    total = 0
    for r in range(len(lines)):
        sx = lines[r].find('S')
        ex = lines[r].find('E')
        if sx >= 0:
            sxy = (sx,r)
        if ex >= 0:
            exy = (ex,r)
        row = []
        for c in range(len(lines[r])):
            row.append(lines[r][c])
        grid.append(row)
    s = Point(sxy[0],sxy[1],grid)
    e = Point(exy[0],exy[1],grid)
    baselinePath = s.bfs(e,['#'])
    baselineDist = len(baselinePath)
    assert(baselineDist != 0)
    seen = set()
    toCheck = getPathNeighboors(baselinePath)
    for r in range(len(lines)):
        for c in range(len(lines[0])):
            p = Point(c,r,grid)
            if p.value == '#' and p in toCheck:
                neighboors = p.getNeighboors()
                grid[p.y][p.x] = '.'
                newPath = set(s.bfs(e,['#']))
                newDist = len(newPath)
                if baselineDist - newDist >= savings and p in newPath:
                    print("Removing {} saves {}".format(p,baselineDist - newDist))
                    total += 1
                seen.add(hash(p))
                grid[p.y][p.x] = '#'
    return total

def run(pt,day,year,savings,expect):
    with open("input.txt","w") as f:
        f.write(get_data(day=day,year=year))
    resTest = solve2("testInput.txt",pt,savings,20)
    assert resTest == expect, f"Result was {resTest}"
    res = solve2("input.txt",pt,100,20)
    print("Test Input: {} Puzzle Input: {}".format(resTest,res))
    if pt == 1:
        c = "a"
    else:
        c = "b"
    submit(res, part=c, day=day, year=year)

#run(1,20,2024,2,44)
run(2,20,2024,70,41)
