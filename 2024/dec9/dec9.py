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
    print(filePos)
    print(freeSpace)
    maxPos = pos
    k = maxPos
    freeSpace.reverse()
    while k >= 0:
        if k in filePos:
            # Found a file!
            fileId,fileLength = filePos[k]
            #print("Files: {}".format(filePos))
            freeSpace = list(filter(lambda e: e[1] > 0,freeSpace))
            i = len(freeSpace) - 1
            while i >= 0 and fileLength > 0:
                freeSpacePos,spaceAvailable = freeSpace[i]
                #print("Free Space: {}".format(freeSpace))
                print("Pos {} Found File {} length {}".format(k,fileId,fileLength))
                print("Check open space {} length {}".format(freeSpacePos,spaceAvailable))
                if spaceAvailable == 0 or k < freeSpacePos:
                    i -= 1
                    continue
                elif freeSpacePos > k+fileLength:
                    print("But we're at the end")
                    filePos[k] = (fileId,fileLength)
                    fileLength = 0
                elif fileLength > spaceAvailable:
                    print("Not enough space for the full file")
                    if pt == 1:
                        filePos[freeSpacePos] = fileId,spaceAvailable
                        freeSpace[i] = (freeSpacePos,0)
                        fileLength -= spaceAvailable
                    elif pt == 2:
                        i -= 1
                else:
                    print("Enough space for full file, Popping file {} at pos {}".format(fileId,k))
                    filePos.pop(k)
                    filePos[freeSpacePos] = fileId,fileLength
                    if spaceAvailable > fileLength:
                        freeSpace[i] = (freeSpacePos + fileLength,spaceAvailable - fileLength)
                    elif spaceAvailable == fileLength:
                        freeSpace[i] = (freeSpacePos,0)
                    else:
                        assert(False)
                    fileLength -= spaceAvailable
        k -= 1
    total = 0
    k = 0
    print(filePos)
    while k <= maxPos:
        if k not in filePos:
            k += 1
            continue
        curFile,curLen = filePos[k]
        print("Pos: {} file: {} lenghth: {}".format(k,curFile,curLen))
        for i in range(curLen):
            total += k*curFile
            print("Pos: {} * file: {} = {} Total = {}".format(k,curFile,k*curFile,total))
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
