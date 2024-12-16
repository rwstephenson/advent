import sys
from math import *
from collections import *
sys.path.append('../../lib')
from point import Point
from interval import Interval
from parsing import *
from aocd import get_data, submit

INF = 99999999999999999

def shortestPath(start,end,grid,pt):
    dist = defaultdict(int)
    prev = defaultdict(set)
    q = []
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] != '#':
                p = Point(c,r,grid)
                for d in ['N','E','S','W']:
                    dist[(hash(p),d)] = INF
                    q.append((p,d))
    dist[(hash(start),'E')] = 0
    prev[(hash(start),'E')].add(start)

    while len(q) > 0:
        q.sort(key=lambda pd: dist[(hash(pd[0]),pd[1])])
        u,d = q.pop(0)
        val = dist[(hash(u),d)]
        for nd in ['N','E','S','W']:
            n = u.getNeighboor(nd)
            if n and n.value != '#':
                if nd == d:
                    alt = dist[(hash(u),d)] + 1
                else:
                    alt = dist[(hash(u),d)] + 1000 + 1
                if alt < dist[(hash(n),nd)]:
                    dist[(hash(n),nd)] = alt
                    prev[(hash(n),nd)] = prev[(hash(u),d)].copy()
                    prev[(hash(n),nd)].add(n)
                elif alt == dist[(hash(n),nd)]:
                    for p in prev[(hash(u),nd)]:
                        prev[(hash(n),d)].add(p)
    if pt == 1:
        return dist[(hash(end),'N')]
    elif pt == 2:
        return len(prev[(hash(end),'N')])

def solve(filename, pt):
    grid = parseLines(filename)
    start = None
    end = None
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == 'S':
                start = Point(c,r,grid)
            if grid[r][c] == 'E':
                end = Point(c,r,grid)
    return shortestPath(start,end,grid,pt)

def run(pt,day,year,expect):
    with open("input.txt","w") as f:
        f.write(get_data(day=day,year=year))
    resTest = solve("testInput.txt",pt)
    print(resTest)
    assert resTest == expect, f"Result was {resTest}"
    res = solve("input.txt",pt)
    print("Test Input: {} Puzzle Input: {}".format(resTest,res))
    if pt == 1:
        c = "a"
    else:
        c = "b"
    submit(res, part=c, day=day, year=year)

#run(1,16,2024,7036)
run(2,16,2024,45)
