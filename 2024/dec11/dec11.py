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

def solve(filename, pt1target, pt2target, brute):
    lines = parseLines(filename)
    stones = getInts(lines[0])
    groupedStones = groupStones(stones)
    res = 0
    for i in range(pt2target):
        if brute:
            stones = blinkBrute(stones)
            res = len(stones)
        else:
            groupedStones = blink(groupedStones)
            res = sum(groupedStones.values())
        if i == pt1target - 1:
            submit(res, part=1, day=11, year=2024)
    submit(res, part=2, day=11, year=2024)


def run(day,year,brute=False):
    with open("input.txt","w") as f:
        f.write(get_data(day=day,year=year))
    solve("input.txt",25,75,brute)

run(11,2024)
