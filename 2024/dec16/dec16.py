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
                    dist[hash((hash(p),d))] = INF
                    q.append((p,d))
    dist[hash((hash(start),'E'))] = 0
    prev[hash((hash(start),'E'))].add(start)

    while len(q) > 0:
        q.sort(key=lambda pd: dist[hash((hash(pd[0]),pd[1]))])
        #for ud in q:
        #    print("p {} d {} dist {}".format(ud[0],ud[1],dist[hash((hash(ud[0]),ud[1]))]))
        u,d = q.pop(0)
        val = dist[hash((hash(u),d))]
        print("Checking p: {} d: {} dist: {} prev: {}".format(u,d,val,len(prev[hash((hash(u),d))])))
        for nd in ['N','E','S','W']:
            n = u.getNeighboor(nd)
            if n and n.value != '#':
                #print("Checking Neighboor: {} d: {} dist: {}".format(n,nd,dist[hash((hash(n),nd))]))
                if nd == d:
                    alt = dist[hash((hash(u),d))] + 1
                else:
                    alt = dist[hash((hash(u),d))] + 1000 + 1
                if alt < dist[hash((hash(n),nd))]:
                    dist[hash((hash(n),nd))] = alt
                    print("FOUND A BETTER WAY to {} {} dist: {}".format(n,nd,alt))
                    #print("Adding {} {} to Q".format(n,nd))
                    prev[hash((hash(n),nd))] = prev[hash((hash(u),d))].copy()
                    prev[hash((hash(n),nd))].add(n)
                elif alt == dist[hash((hash(n),nd))]:
                    print("FOUND AN EQUAL ROUTE to add to {}".format(len(prev[hash((hash(u),d))])))
                    for p in prev[hash((hash(n),nd))]:
                        print("Adding new {}".format(p))
                        prev[hash((hash(u),d))].add(p)
                    print("Now {}".format(len(prev[hash((hash(u),d))])))
    if pt == 1:
        return min(dist[hash((hash(end),'N'))],dist[hash((hash(end),'E'))],dist[hash((hash(end),'S'))],dist[hash((hash(end),'W'))])
    elif pt == 2:
        prevN = list(prev[hash((hash(end),'N'))])
        prevN.sort(key=lambda p: p.x*1000 + p.y)
        for p in prevN:
            print(p)
        #prevE = prev[hash((hash(end),'E'))]
        #prevS = prev[hash((hash(end),'S'))]
        #prevW = prev[hash((hash(end),'W'))]
        return len(prevN)

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
    #res = solve("input.txt",pt)
    print("Test Input: {} Puzzle Input: {}".format(resTest,res))
    if pt == 1:
        c = "a"
    else:
        c = "b"
    submit(res, part=c, day=day, year=year)

#run(1,16,2024,7036)
run(2,16,2024,45)
