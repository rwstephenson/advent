import sys
from math import *
from collections import *
sys.path.append('../../lib')
from point import Point
from interval import Interval
from parsing import *
from aocd import submit

def solve(filename, pt):
    line = ""
    i = 0
    fileId = 0
    filePos = {}
    freeSpace = []
    pos = 0
    with open(filename,"r") as f:
        line = f.readline().strip()
        for c in line:
            if i % 2 == 0:
                # Is file length
                filePos[pos] = (fileId,int(c))
                fileId += 1
            else:
                # is free space length
                if int(c) > 0:
                    freeSpace.append((pos,int(c)))
            pos += int(c)
            i += 1
    maxPos = pos
    k = maxPos
    freeSpace.reverse()
    while k >= 0:
        if k in filePos:
            # Found a file!
            fileId,fileLength = filePos[k]
            i = len(freeSpace) - 1
            while i >= 0 and fileLength > 0:
                freeSpacePos,spaceAvailable = freeSpace[i]
                if k < freeSpacePos:
                    break
                elif fileLength > spaceAvailable:
                    if pt == 1:
                        filePos[freeSpacePos] = fileId,spaceAvailable
                        filePos[k] = (fileId,fileLength - spaceAvailable)
                        freeSpace.pop(i)
                        i -= 1
                        fileLength -= spaceAvailable
                    elif pt == 2:
                        i -= 1
                else:
                    filePos.pop(k)
                    filePos[freeSpacePos] = fileId,fileLength
                    if spaceAvailable > fileLength:
                        freeSpace[i] = (freeSpacePos + fileLength,spaceAvailable - fileLength)
                    elif spaceAvailable == fileLength:
                        freeSpace.pop(i)
                        i -= 1
                    else:
                        assert(False)
                    fileLength -= spaceAvailable
        k -= 1
    total = 0
    k = 0
    while k <= maxPos:
        if k not in filePos:
            k += 1
            continue
        curFile,curLen = filePos[k]
        for i in range(curLen):
            total += k*curFile
            k += 1
    return total

def run(pt,day,year,expect):
    resTest = solve("testInput.txt",pt)
    assert resTest == expect, f"Result was {resTest}"
    res = solve("input.txt",pt)
    print("Test Input: {} Puzzle Input: {}".format(resTest,res))
    if pt == 1:
        c = "a"
    else:
        c = "b"
    submit(res, part=c, day=day, year=year)

run(1,9,2024,1928)
run(2,9,2024,2858)
