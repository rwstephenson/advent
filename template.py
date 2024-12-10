import sys
from math import *
from collections import *
sys.path.append('../../lib')
from point import Point
from interval import Interval
from parsing import *
from aocd import submit

def solve(filename, pt):
    lines = parseLines(filename)
    total = 0
    return total

def run(pt,day,year,expect):
    resTest = solve("testInput.txt",pt)
    assert resTest == -1, f"Result was {resTest}"
    res = solve("input.txt",pt)
    print("Test Input: {} Puzzle Input: {}".format(resTest,res))
    if pt == 1:
        c = "a"
    else:
        c = "b"
    submit(res, part=c, day=day, year=year)

run(1,0,2024,-1)
run(2,0,2024,-1)
