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
        print(springsLine)
        print(arrangementLine)
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

def findPossibilities(springLine, arrangements):
    print("------------------------------- Checking")
    print(springLine)
    print(arrangements)
    if len(springLine) == 0:
        # The line is empty.
        if len(arrangements) == 0:
            return 1
        else:
            return 0
    elif len(arrangements) == 0:
        # No arrangements left. Check the remaining groups, if they can all be ? then we are good
        assert(len(springLine) > 0)
        for group in springLine:
            if countBroken(group) > 0:
                return 0
        return 1
    elif arrangements[0] == 0:
        # We still have more of this group, but the size is correct.
        if len(springLine[0]) == 0:
            # Nothing left in group, move to next
            return findPossibilities(springLine[1:] ,arrangements[1:])
        elif springLine[0][0] == '#':
            # Another broken immediately.  Can't be true.
            return 0
        else:
            # So this group does not continue, skip the next and continue
            return findPossibilities([springLine[0][1:]] + springLine[1:] ,arrangements[1:])
    elif len(springLine[0]) < arrangements[0]:
        # The first group is smaller than the first desired group.  We can skip the whole group
        return findPossibilities(springLine[1:],arrangements)
    elif countBroken(springLine[0]) > 0:
        # We start the group with some that are broken
        numBroken = countBroken(springLine[0])
        if numBroken == arrangements[0] and numBroken <= len(springLine[0]):
            # We include this group, but the group is bigger..
            #print("Have the right amount broken")
            return findPossibilities([springLine[0][numBroken+1:]] + springLine[1:], arrangements[1:])
        elif numBroken < arrangements[0] and arrangements[0] == len(springLine[0]):
            # We include the whole group.
            return findPossibilities(springLine[1:], arrangements[1:])
        elif numBroken > arrangements[0]:
            # Its too big, return 0
            return 0
        else:
            return findPossibilities([springLine[0][arrangements[0]:]] + springLine[1:] ,[0] + arrangements[1:])
    else:
        firstSpringGroup = springLine[0]
        firstGroupSize = arrangements[0]
        assert(firstSpringGroup[0] == '?')
        assert(firstGroupSize <= len(firstSpringGroup))
        # First char is ? and group is ambiguous
        print("Have ambiguity!: firstSpringGroup = " + firstSpringGroup)
        print(arrangements)
        print ("Checking case in: " + firstSpringGroup + " groupSize: " + str(firstGroupSize))
        caseIn = findPossibilities([firstSpringGroup[firstGroupSize:]] + springLine[1:],[arrangements[0] - firstGroupSize] + arrangements[1:])
        print ("Case in for " + firstSpringGroup + " returned: " + str(caseIn))
        print ("Checking case Out: " + firstSpringGroup + " groupSize: " + str(firstGroupSize))
        caseOut = findPossibilities([firstSpringGroup[1:]] + springLine[1:],arrangements)
        print ("Case out for " + firstSpringGroup + " returned: " + str(caseOut))
        return caseIn + caseOut

def pt1(filename,extra):
    with open(filename, "r") as f:
        springs,springLines,arrangements = parseFile(f,extra)
        sum = 0
        assert(len(springLines) == len(arrangements))
        for i in range(len(springLines)):
            poss = findPossibilities2(springLines[i], arrangements[i], False)
            print("xxROB: result: " + str(poss))
            print(springLines[i] + " " + arrangements[i])
            sum += poss
        return sum

#print(pt1("testInput.txt"))
print(pt1("input.txt",4))

