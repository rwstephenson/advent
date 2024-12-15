import sys
from math import *
from collections import *
sys.path.append('../../lib')
from point import Point
from interval import Interval
from parsing import *
from aocd import get_data, submit

def getDirection(c):
    if c == '^':
        return 'N'
    elif c == '<':
        return 'W'
    elif c == '>':
        return 'E'
    elif c == 'v':
        return 'S'
    else:
        assert(False)

def getAdjacentBoxes(p,d,pt):
    adjBoxes = []
    if pt == 1:
        while True:
            n = p.getNeighboor(d)
            if n and n.value == 'O':
                adjBoxes.append(n)
                p = n
            else:
                break
    elif pt == 2:
        boxesToMove = [p]
        while len(boxesToMove) > 0:
            p = boxesToMove.pop(0)
            if d == 'E' or d == 'W':
                n = p.getNeighboor(d)
                if n and n.value == '[' or n.value == ']':
                    adjBoxes.append(n)
                    boxesToMove.append(n)
            elif d == 'N' or d == 'S':
                n = p.getNeighboor(d)
                if n.value == '[':
                    adjBoxes.append(n)
                    boxesToMove.append(n)
                    n = n.getNeighboor('E')
                    assert(n.value == ']')
                    adjBoxes.append(n)
                    boxesToMove.append(n)
                elif n.value == ']':
                    adjBoxes.append(n)
                    boxesToMove.append(n)
                    n = n.getNeighboor('W')
                    assert(n.value == '[')
                    adjBoxes.append(n)
                    boxesToMove.append(n)
    return adjBoxes

def move(p,d,grid):
    n = p.getNeighboor(d)
    assert(p.value == 'O' or p.value == '@' or p.value == '[' or p.value == ']')
    if n and n.value == '.':
        strList = list(grid[n.y])
        strList[n.x] = p.value
        grid[n.y] = ''.join(strList)
        strList = list(grid[p.y])
        strList[p.x] = '.'
        grid[p.y] = ''.join(strList)
        p = p.getNeighboor(d)
    return p

def countScore(grid):
    total = 0
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            p = grid[r][c]
            if p == 'O' or p == '[':
                total += 100*r + c
        print(grid[r])
    return total

def getInput(lines,pt):
    grid = []
    instructions = []
    for r in range(len(lines)):
        line = lines[r]
        if len(line) > 0 and line[0] == '#':
            if pt == 2:
                newLine = ""
                for c in line:
                    if c == '#':
                        newLine += '##'
                    elif c == '.':
                        newLine += '..'
                    elif c == 'O':
                        newLine += '[]'
                    elif c == '@':
                        newLine += '@.'
                    else:
                        assert(False)
                grid.append(newLine)
            elif pt == 1:
                grid.append(line)
            if grid[-1].find('@') >= 0:
                robotP = Point(grid[-1].find('@'),r,grid)
                assert(robotP.value == '@')
        elif len(line) > 0:
            instructions += line
    return grid,instructions,robotP

def printGrid(grid):
    print("--------------")
    for line in grid:
        print(line)

def canMoveBoxes(boxes,d):
    for b in boxes:
        if b.getNeighboor(d).value == '#':
            return False
    return True

def solve(filename, pt):
    lines = parseLines(filename)
    grid,instructions,robotP = getInput(lines,pt)
    for c in instructions:
        d = getDirection(c)
        adjBoxes = list(reversed(getAdjacentBoxes(robotP,d,pt)))
        if pt == 1 or (pt == 2 and canMoveBoxes(adjBoxes,d)):
            for b in adjBoxes:
                move(b,d,grid)
            robotP = move(robotP,d,grid)
    return countScore(grid)

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

run(1,15,2024,10092)
run(2,15,2024,9021)
