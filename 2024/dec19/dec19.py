import sys
from math import *
from collections import *
sys.path.append('../../lib')
from point import Point
from interval import Interval
from parsing import *
from aocd import get_data, submit
from functools import lru_cache

@lru_cache()
def checkPattern(supply,pattern,pt):
    if len(pattern) == 0:
        return True
    else:
        total = 0
        for towel in supply:
            if len(pattern) >= len(towel) and towel == pattern[0:len(towel)]:
                total += checkPattern(supply,pattern[len(towel):],pt)
        if pt == 2:
            return total
        elif pt == 1:
            if total == 0:
                return 0
            else:
                return 1

def solve(filename, pt):
    lines = parseLines(filename)
    supply = tuple(lines[0].split(', '))
    total = 0
    for pattern in lines[2:]:
        total += checkPattern(supply,pattern,pt)
    return total

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

run(1,19,2024,6)
run(2,19,2024,16)
