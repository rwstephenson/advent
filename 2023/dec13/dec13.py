import sys
import math

def parseFile(f):
    blocks = []
    block = []
    for line in f:
        if len(line.strip()) == 0:
            blocks.append(block)
            block = []
        else:
            block.append(line.strip())
    return blocks

#Checking between x and x+1
def checkForHorizontalMirror(x,block):
    numDiff = 0
    smudgeX = 0
    smudgeY = 0
    for y in range(len(block)):
        blockLine = block[y]
        i = 0
        while x+i+1 < len(blockLine) and x-i >= 0:
            if blockLine[x-i] == blockLine[x+i+1]:
                i += 1
            else:
                numDiff += 1
                smudgeX = x-i
                smudgeY = y
                i += 1
    return numDiff, smudgeX, smudgeY

#Checking between y and y+1
def checkForVerticalMirror(y,block):
    i = 0
    numDiff = 0
    smudgeX = 0
    smudgeY = 0
    while y+i+1 < len(block) and y-i >= 0:
        x = 0
        while x < len(block[y]):
            blockLine0 = block[y-i]
            blockLine1 = block[y+i+1]
            if blockLine0[x] != blockLine1[x]:
                smudgeX = x
                smudgeY = y-i
                numDiff += 1
            x += 1
        i += 1
    return numDiff,smudgeX,smudgeY

def findHorizontalMirror(block):
    mirrors = []
    for x in range(0,len(block[0])-1):
        if checkForHorizontalMirror(x,block)[0] == 0:
            mirrors.append(x+1)
    return mirrors

def findVerticalMirror(block):
    mirrors = []
    for y in range(0,len(block)-1):
        if checkForVerticalMirror(y,block)[0] == 0:
            mirrors.append(y+1)
    return mirrors

def cleanVertical(block):
    foundSmudge = False
    foundX = 0
    foundY = 0
    for y in range(0,len(block)-1):
        numDiff,smudgeX,smudgeY = checkForVerticalMirror(y,block)
        if numDiff == 1:
            assert(not foundSmudge)
            foundSmudge = True
            foundX = smudgeX
            foundY = smudgeY
    return foundSmudge,foundX,foundY

def fixSmudge(block, smudgeX, smudgeY):
    cleanBlock = []
    for y in range(len(block)):
        blockLine = block[y]
        if y != smudgeY:
            cleanBlock.append(blockLine)
        else:
            cleanString = ""
            for x in range(len(block[0])):
                if x != smudgeX:
                    cleanString += blockLine[x]
                else:
                    if blockLine[x] == '.':
                        cleanString += '#'
                    elif blockLine[x] == '#':
                        cleanString += '.'
            cleanBlock.append(cleanString)
    return cleanBlock

def cleanHorizontal(block):
    foundSmudge = False
    foundX = 0
    foundY = 0
    for x in range(0,len(block[0])-1):
        numDiff,smudgeX,smudgeY = checkForHorizontalMirror(x,block)
        if numDiff == 1:
            assert(not foundSmudge)
            foundSmudge = True
            foundX = smudgeX
            foundY = smudgeY
    return foundSmudge,foundX,foundY

def cleanSmudges(blocks):
    cleanBlocks = []
    for block in blocks:
        foundSmudge,smudgeX,smudgeY = cleanHorizontal(block)
        if not foundSmudge:
            foundSmudge,smudgeX,smudgeY = cleanVertical(block)
        assert(foundSmudge)
        cleanBlocks.append(fixSmudge(block,smudgeX,smudgeY))
    return cleanBlocks

def sumUpMirrors(blocks,oldBlocks=None):
        sum = 0
        i = 0
        for block in blocks:
            vert = 0
            hor = 0
            if oldBlocks:
                oldHor = findHorizontalMirror(oldBlocks[i])
                assert(len(oldHor) <= 1)
                horMirrors = findHorizontalMirror(block)
                if len(oldHor) == 0 and len(horMirrors) == 0:
                    hor = 0
                elif len(oldHor) == 0:
                    assert(len(horMirrors) == 1)
                    hor = horMirrors[0]
                elif len(horMirrors) == 1 and horMirrors[0] != oldHor[0]:
                    hor = horMirrors[0]
                elif len(horMirrors) == 2 and oldHor[0] == horMirrors[0]:
                    hor = horMirrors[1]
                elif len(horMirrors) == 2 and oldHor[0] == horMirrors[1]:
                    hor = horMirrors[0]
                else:
                    hor = 0
            else:
                horMirrors = findHorizontalMirror(block)
                if len(horMirrors) > 0:
                    hor = horMirrors[0]
                else:
                    hor = 0
            if oldBlocks:
                oldVert = findVerticalMirror(oldBlocks[i])
                assert(len(oldVert) <= 1)
                vertMirrors = findVerticalMirror(block)
                if len(oldVert) == 0 and len(vertMirrors) == 0:
                    vert = 0
                elif len(oldVert) == 0 :
                    assert(len(vertMirrors) == 1)
                    vert = vertMirrors[0]
                elif len(vertMirrors) == 1 and vertMirrors[0] != oldVert[0]:
                    vert = vertMirrors[0]
                elif len(vertMirrors) == 2 and vertMirrors[0] == oldVert[0]:
                    vert = vertMirrors[1]
                elif len(vertMirrors) == 2 and vertMirrors[1] == oldVert[0]:
                    vert = vertMirrors[0]
                else:
                    vert = 0
            else:
                vertMirrors = findVerticalMirror(block)
                if len(vertMirrors) > 0:
                    vert = vertMirrors[0]
                else:
                    vert = 0
            assert(not (hor > 0 and vert > 0))
            assert(not (hor == 0 and vert == 0))
            sum += hor + vert*100
            i+= 1
        return sum

def pt1(filename):
    with open(filename, "r") as f:
        blocks = parseFile(f)
        return sumUpMirrors(blocks)

def pt2(filename):
    with open(filename, "r") as f:
        blocks = parseFile(f)
        fixedBlocks = cleanSmudges(blocks)
        return sumUpMirrors(fixedBlocks,blocks)

#print(pt1("testInput.txt"))
#assert(pt1("input.txt") == 40006)
#assert(pt2("testInput.txt") == 400)
print(pt2("input.txt"))

