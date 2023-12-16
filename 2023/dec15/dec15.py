import sys
import math
from functools import lru_cache


def parseFile(f):
    hashes = []
    for line in f:
        hashes += line.strip().split(',')
    return hashes

def getValue(h):
    sum = 0
    for c in h:
        sum = (sum+(ord(c)))*17%256
    return sum


def pt1(filename):
    with open(filename, "r") as f:
        hashStrings = parseFile(f)
        sum = 0
        for h in hashStrings:
            sum += getValue(h)
        return sum

def isOpAdd(h):
    idx = h.find('=')
    if h.find('=') >= 0:
        return True, h[:idx],h[idx+1]
    else:
        return False,h[:idx],-1


lensMap = {}

def updateBoxContents(contents, lens, newFocal):
    newContents = []
    found = False
    idxMax = 0
    for boxLens in contents:
        if boxLens[1] == lens:
            newContents.append((boxLens[0],lens,newFocal))
            found = True
        else:
            newContents.append(boxLens)
            idxMax = max(boxLens[0],idxMax)
    if found:
        return newContents
    else:
        newContents.append((idxMax+1,lens,newFocal))
        return newContents

def addToLensMap(lens,focal):
    box = getValue(lens)
    if box not in lensMap:
        lensMap[box] = [(0, lens, int(focal))]
    else:
        lensMap[box] = updateBoxContents(lensMap[box], lens, int(focal))

def removeFromLensMap(lens):
    box = getValue(lens)
    if box in lensMap:
        newContent = []
        for boxLens in lensMap[box]:
            if boxLens[1] == lens:
                pass
            else:
                newContent.append(boxLens)
        lensMap[box] = newContent

def getBoxValue(box):
    if box in lensMap:
        boxContents = lensMap[box]
        sum = 0
        for i in range(len(boxContents)):
            lens = boxContents[i]
            sum += (box+1) * (i+1) * lens[2]
        return sum
    else:
        return 0

def pt2(filename):
    with open(filename, "r") as f:
        hashStrings = parseFile(f)
        sum = 0
        for h in hashStrings:
            isAdd,lens,focal = isOpAdd(h)
            if isAdd:
                addToLensMap(lens,focal)
            else:
                removeFromLensMap(lens)
        for box in range(256):
            sum += getBoxValue(box)
        return sum

#print(pt1("testInput2.txt"))
print(pt2("input.txt"))


