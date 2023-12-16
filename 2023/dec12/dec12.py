import sys
import math
from functools import cache
sys.setrecursionlimit(10000)

def parseFile(f,extra):
    springGroups = []
    springLines = []
    arrangements = []
    for line in f:
        springsLine = line.split(' ')[0].strip()
        fullSpringsLine = springsLine
        arrangementLine = line.split(' ')[1].strip()
        fullArrangements = arrangementLine
        for i in range(extra):
            fullSpringsLine = fullSpringsLine + '?' + springsLine
            fullArrangements = fullArrangements + "," + arrangementLine
        springLines.append(fullSpringsLine)
        arrangements.append(fullArrangements)
        springGroup = []
        entry = ""
        for c in springsLine:
            if c != '.':
                entry += c
            elif entry == "":
                pass
            else:
                springGroup.append(entry)
                entry = ""
        if entry != "":
            springGroup.append(entry)
        springGroups.append(springGroup)
    return springGroups,springLines,arrangements

def countBroken(group):
    i = 0
    for c in group:
        if c != '#':
            return i
        i += 1
    return i

def arrangementsToLine(arrangements):
    s = ""
    for i in range(len(arrangements)):
        if i == 0:
            s += str(arrangements[i])
        else:
            s += "," + str(arrangements[i])
    return s


@cache
def findPossibilities2(line, arrangementLine, inGroup):
    arrangements = []
    if len(arrangementLine) > 0:
        arrangements = list(map(int,arrangementLine.strip().split(',')))
    if len(line) == 0:
        return len(arrangements) == 0 or (len(arrangements) == 1 and arrangements[0] == 0)
    else:
        c = line[0]
        if c == '.':
            if inGroup and arrangements[0] == 0:
                return findPossibilities2(line[1:],arrangementsToLine(arrangements[1:]), False)
            elif inGroup and arrangements[0] > 0:
                return 0
            elif not inGroup:
                return findPossibilities2(line[1:],arrangementsToLine(arrangements), False)
        elif c == '#':
            if len(arrangements) == 0 or arrangements[0] == 0:
                return 0
            else:
                return findPossibilities2(line[1:], arrangementsToLine([arrangements[0] - 1] + arrangements[1:]),True)
        elif c == '?':
            caseIn = findPossibilities2("#" + line[1:], arrangementsToLine(arrangements), inGroup)
            caseOut = findPossibilities2("." + line[1:], arrangementsToLine(arrangements), inGroup)
            return caseIn + caseOut
        else:
            assert(False)

def pt1(filename,extra):
    with open(filename, "r") as f:
        springs,springLines,arrangements = parseFile(f,extra)
        sum = 0
        assert(len(springLines) == len(arrangements))
        for i in range(len(springLines)):
            poss = findPossibilities2(springLines[i], arrangements[i], False)
            print("result: " + str(poss))
            print(springLines[i] + " " + arrangements[i])
            sum += poss
        return sum

#print(pt1("testInput.txt"))
print(pt1("input.txt",4))

