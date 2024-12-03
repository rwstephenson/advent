import sys
from math import *
from collections import *
sys.path.append('../../lib')
from point import Point
from interval import Interval
from parsing import *

INF = 9999999999999

def solve(filename,pt):
    lines = parseLines(filename)
    total = 0
    enabled = True
    for line in lines:
        enables = findAll(line,'do()')
        disables = findAll(line,'don\'t()')
        mults = findAll(line,'mul(')
        assert(len(mults) > 0)

        while len(mults) > 0:
            if len(enables) == 0:
                enables += [INF]
            if len(disables) == 0:
                disables += [INF]

            if enables[0] < min(disables[0],mults[0]):
                enabled = True
                enables.pop(0)
            elif disables[0] < min(enables[0],mults[0]):
                enabled = False
                disables.pop(0)
            elif mults[0] < min(disables[0],enables[0]):
                s = mults[0] + len('mul(')
                e = s + line[s:].find(')')
                subline = line[s:e]
                prod = subline.split(',')
                if len(prod) == 2 and len(prod[0]) <= 3 and len(prod[1]) <= 3 and prod[0].isdigit() and prod[1].isdigit():
                    if pt == 1 or (pt == 2 and enabled):
                        total += int(prod[0])*int(prod[1])
                mults.pop(0)
            else:
                assert(False)
    return total

resTest = solve("testInput.txt",1)
assert resTest == 161, f"Result was {resTest}"
res = solve("input.txt",1)
print("Part 1: Test Input: {} Puzzle Input: {}".format(resTest,res))
resTest = solve("testInput2.txt",2)
assert resTest == 48, f"Result was {resTest}"
res = solve("input.txt",2)
print("Part 2: Test Input: {} Puzzle Input: {}".format(resTest,res))
