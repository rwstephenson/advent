import sys
from math import *
from collections import *
sys.path.append('../../lib')
from point import Point
from interval import Interval
from parsing import *
from aocd import get_data, submit
from functools import lru_cache

def pathLen(s, e, cache):
    if hash((s,e)) in cache:
        return cache[hash((s,e))]
    path = s.bfs(e,['#'])
    dist = len(path)
    for i in range(len(path)):
        cache[hash((path[i],e))] = dist - i
    return dist

def getCheatEndpoints(s,seconds):
    assert(s.value != '#')
    endpoints = []
    for x in range(0-seconds,seconds+1):
        for y in range(0-seconds,seconds+1):
            p = Point(s.x + x, s.y+y,s.grid)
            if p.value and p.value != '#' and abs(x) + abs(y) <= seconds:
                endpoints.append(p)
    return endpoints

def solve2(filename, savings, seconds):
    lines = parseLines(filename)
    cache = {}
    grid = []
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
    baselineDist = pathLen(s,e,cache)
    assert(len(baselinePath) == baselineDist)
    for p in baselinePath:
        endpoints = getCheatEndpoints(p,seconds)
        for endpoint in endpoints:
            distanceToCheat = pathLen(s,p,cache) - 1
            cheatDistance = p.distance(endpoint)
            distanceFromCheat = pathLen(endpoint,e,cache) - 1
            newDist = distanceToCheat + cheatDistance + distanceFromCheat
            if baselineDist - newDist >= savings and hash((p,endpoint)):
                print("Cheat from {} to {} of length {} has shortest path {} for a savings of {}".format(p,endpoint, cheatDistance, newDist, baselineDist - newDist))
                total += 1
    return total

def run(pt,day,year,expect):
    with open("input.txt","w") as f:
        f.write(get_data(day=day,year=year))
    if pt == 1:
        seconds = 2
        testSavings = 2
    elif pt == 2:
        seconds = 20
        testSavings = 70
    resTest = solve2("testInput.txt",testSavings,seconds)
    assert resTest == expect, f"Result was {resTest}"
    res = solve2("input.txt",100,seconds)
    print("Test Input: {} Puzzle Input: {}".format(resTest,res))
    if pt == 1:
        c = "a"
    else:
        c = "b"
    submit(res, part=c, day=day, year=year)

run(1,20,2024,44)
run(2,20,2024,41)
