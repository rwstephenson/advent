import sys
from math import *
from collections import *
sys.path.append('../../lib')
from point import Point
from interval import Interval
from parsing import *
from aocd import get_data, submit

def keyFitsLock(lock,key):
    for i in range(len(lock)):
        if lock[i] + key[i] > 5:
            return False
    return True

def solve(filename, pt):
    lines = parseLines(filename)
    i = 0
    locks = []
    keys = []
    while i < len(lines):
        line = lines[i]
        assert(i%8 == 0)
        key = None
        lock = None
        if line.find('#') < 0:
            key = [0,0,0,0,0]
            lock = None
        elif line.find('.') < 0:
            key = None
            lock = [0,0,0,0,0]
        k = 1
        while k <= 5:
            line = lines[i+k]
            for c in range(len(line)):
                if key is None:
                    if line[c] == '#':
                        lock[c] += 1
                if lock is None:
                    if line[c] == '#':
                        key[c] += 1
            k += 1
        if lock is None:
            keys.append(key)
        if key is None:
            locks.append(lock)
        line = lines[i+k]
        if lock is None:
            assert(line.find('.') < 0)
        if key is None:
            assert(line.find('#') < 0)
        i += 8
    total = 0
    for lock in locks:
        for key in keys:
            if keyFitsLock(lock,key):
                total += 1
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

run(1,25,2024,3)
