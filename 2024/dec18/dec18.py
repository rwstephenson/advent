import sys
from math import *
from collections import *
sys.path.append('../../lib')
from point import Point
from interval import Interval
from parsing import *
from aocd import get_data, submit

def solve(filename, gridSize, b, pt):
    lines = parseLines(filename)
    grid = []
    for y in range(gridSize+1):
        line = []
        for x in range(gridSize+1):
            line.append('.')
        grid.append(line)
    for line in lines[0:b]:
        xy = getInts(line)
        grid[xy[1]][xy[0]] = '#'
    s = Point(0,0,grid)
    e = Point(gridSize,gridSize,grid)
    pathA = s.bfs(e,set('#'))
    if pt == 1:
        return len(pathA)-1
    elif pt == 2:
        for i in range(b,len(lines)):
            xy = getInts(lines[i])
            grid[xy[1]][xy[0]] = '#'
            p = Point(xy[0],xy[1],grid)
            if p in pathA:
                pathA = s.bfs(e,set('#'))
                if len(pathA) == 0:
                    return str(p.x) + ',' + str(p.y)

def run(pt,day,year,expect):
    with open("input.txt","w") as f:
        f.write(get_data(day=day,year=year))
    resTest = solve("testInput.txt",6,12,pt)
    assert resTest == expect, f"Result was {resTest}"
    res = solve("input.txt",70,1024,pt)
    print("Test Input: {} Puzzle Input: {}".format(resTest,res))
    if pt == 1:
        c = "a"
    else:
        c = "b"
    submit(res, part=c, day=day, year=year)

run(1,18,2024,22)
run(2,18,2024,"6,1")
