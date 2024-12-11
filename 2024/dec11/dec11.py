import sys
from math import *
from collections import *
sys.path.append('../../lib')
from point import Point
from interval import Interval
from parsing import *
from aocd import get_data, submit

def blinkStone(stone):
    stoneDigs = len(str(stone))
    if stone == 0:
        return [1]
    elif stoneDigs % 2 == 0:
        return[int(str(stone)[0:stoneDigs // 2]),int(str(stone)[stoneDigs // 2:])]
    else:
        return[stone*2024]

def blinkBrute(stones):
    newStones = []
    for stone in stones:
        newStones += blinkStone(stone)
    return newStones

def blink(groupedStones):
    newGroupedStones = defaultdict(int)
    for s in groupedStones.keys():
        newStones = blinkStone(s)
        for n in newStones:
            newGroupedStones[n] += groupedStones[s]
    return newGroupedStones

def groupStones(stones):
    distinctStones = list(set(stones))
    groupedStones = defaultdict(int)
    for s in distinctStones:
        groupedStones[s] = stones.count(s)
    return groupedStones

def solve(filename, pt):
    lines = parseLines(filename)
    stones = getInts(lines[0])
    groupedStones = groupStones(stones)
    if pt == 1:
        blinksLeft = 25
        while blinksLeft > 0:
            stones = blinkBrute(stones)
            blinksLeft -= 1
        return len(stones)
    elif pt == 2:
        blinksLeft = 75
        while blinksLeft > 0:
            groupedStones = blink(groupedStones)
            blinksLeft -= 1
        return sum(groupedStones.values())

def run(pt,day,year,expect):
    with open("input.txt","w") as f:
        f.write(get_data(day=day,year=year))
    resTest = solve("testInput.txt",pt)
    #assert resTest == expect, f"Result was {resTest}"
    res = solve("input.txt",pt)
    print("Test Input: {} Puzzle Input: {}".format(resTest,res))
    if pt == 1:
        c = "a"
    else:
        c = "b"
    submit(res, part=c, day=day, year=year)

run(1,11,2024,55312)
run(2,11,2024,65601038650482)
