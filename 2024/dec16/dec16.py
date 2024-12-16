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
                    dist[(p,d)] = INF
                    q.append((p,d))
    dist[(start,'E')] = 0
    prev[(start,'E')].add(start)

    while len(q) > 0:
        q.sort(key=lambda pd: dist[(pd[0],pd[1])])
        u,d = q.pop(0)
        val = dist[(u,d)]
        for nd in ['N','E','S','W']:
            n = u.getNeighboor(nd)
            if n and n.value != '#':
                if nd == d:
                    alt = dist[(u,d)] + 1
                else:
                    alt = dist[(u,d)] + 1000 + 1
                if alt < dist[(n,nd)]:
                    dist[(n,nd)] = alt
                    prev[(n,nd)] = prev[(u,d)].copy()
                    prev[(n,nd)].add(n)
                elif alt == dist[(n,nd)]:
                    for p in prev[(u,nd)]:
                        prev[(n,d)].add(p)
    if pt == 1:
        return dist[(end,'N')]
    elif pt == 2:
        return len(prev[(end,'N')])

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
    assert resTest == expect, f"Result was {resTest}"
    res = solve("input.txt",pt)
    print("Test Input: {} Puzzle Input: {}".format(resTest,res))
    if pt == 1:
        c = "a"
    else:
        c = "b"
    submit(res, part=c, day=day, year=year)

run(1,16,2024,7036)
run(2,16,2024,45)
