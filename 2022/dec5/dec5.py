import sys
from math import *
from collections import *
sys.path.append('../../lib')
from point import Point
from interval import Interval

def printCrates(crates):
    for key in crates.keys():
        print("Crates: {}".format(key))
        for c in crates[key]:
            print(c)

def parseCrates(f):
    lineLength = 0
    crates = defaultdict(list)
    for line in f:
        if line.find('[') < 0:
            for key in crates.keys():
                crates[key].reverse()
            f.readline()
            return crates

        lineLength = len(line)
        numCrates = (lineLength // 4) + 1
        for i in range(lineLength):
            if line[i] == ']':
                crates[i//4 + 1].append(line[i-1])

def move(crates,instructions,pt):
    lineSplit = instructions.split(' ')
    numToMove,sourceStack,destStack = int(lineSplit[1]),int(lineSplit[3]),int(lineSplit[5])
    if pt == 1:
        for i in range(numToMove):
            box = crates[sourceStack].pop()
            crates[destStack].append(box)
    elif pt == 2:
        listToMove = []
        for i in range(numToMove):
            listToMove.append(crates[sourceStack].pop())
        for c in reversed(listToMove):
            crates[destStack].append(c)


def solve(filename,pt):
    with open(filename,"r") as f:
        crates = parseCrates(f)
        for line in f:
            move(crates,line,pt)
            resultStr = ''
        for i in range(1,len(crates.values())+1):
            resultStr += crates[i][-1]
        return resultStr

resTest = solve("testInput.txt",1)
assert(resTest == 'CMZ')
res = solve("input.txt",1)
assert(res == 'FWNSHLDNZ')
print("Part 1 Test Input: {} Puzzle Input: {}".format(resTest,res))
resTest = solve("testInput.txt",2)
assert(resTest == 'MCD')
res = solve("input.txt",2)
print("Part 2 Test Input: {} Puzzle Input: {}".format(resTest,res))
