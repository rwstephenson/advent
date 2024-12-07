import sys
from math import *
from collections import *
sys.path.append('../../lib')
from point import Point
from interval import Interval
from parsing import *
from aocd import submit

def check(value,target,ints,pt):
    if len(ints) == 0:
        return value == target
    elif value > target:
        return False
    else:
        intDigs = len(str(ints[0]))
        if pt == 2:
            worksWithConcat = check(value*10**intDigs + ints[0],target,ints[1:],pt)
        else:
            worksWithConcat = False
        return check(value + ints[0],target,ints[1:],pt) or check(value * ints[0],target,ints[1:],pt) or worksWithConcat

def solve(filename, pt):
    lines = parseLines(filename)
    total = 0
    for line in lines:
        value = getInts(line)[0]
        ints = getInts(line)[1:]
        if check(ints[0],value,ints[1:],pt):
            total += value
    return total

def run(pt,day,year,expected):
    resTest = solve("testInput.txt",pt)
    assert resTest == expected, f"Result was {resTest}"
    res = solve("input.txt",pt)
    print("Test Input: {} Puzzle Input: {}".format(resTest,res))
    if pt == 1:
        c = "a"
    else:
        c = "b"
    submit(res, part=c, day=day, year=year)

run(1,7,2024,3749)
run(2,7,2024,11387)
