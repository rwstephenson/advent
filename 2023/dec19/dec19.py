import sys
import math
from copy import deepcopy
from functools import cache

class Interval():
    low = 0
    exclHigh = 0

    def __init__(self,low,exclHigh):
        self.low = low
        self.exclHigh = exclHigh

    def toStr(self):
        return "[" + str(self.low) + "-" + str(self.exclHigh) + ")"

    def isInside(self,num):
        return num >= self.low and num < self.exclHigh

    def width(self):
        return self.exclHigh - self.low

    def union(self,interval):
        if interval.exclHigh <= self.low:
            # Totally below
            return [interval,self]
        elif interval.low < self.low and interval.exclHigh > self.low and interval.exclHigh <= self.exclHigh:
            # Partly below
            overlap = [Interval(self.low, interval.exclHigh)]
            notOverlap = [Interval(interval.exclHigh, self.exclHigh)]
            return overlap+notOverlap
        elif interval.low < self.low and interval.exclHigh >= self.exclHigh:
            # Both below and above
            return [Interval(self.low, self.exclHigh)]
        elif interval.low >= self.low and interval.exclHigh <= self.exclHigh:
            # Fully inside
            notOverlap = [Interval(self.low, interval.low), Interval(interval.exclHigh,self.exclHigh)]
            overlap = [Interval(interval.low, interval.exclHigh)]
            return overlap + notOverlap
        elif interval.low >= self.low and interval.exclHigh > self.exclHigh:
            # Partly above
            notOverlap = [Interval(self.low, interval.low)]
            overlap = [Interval(interval.low, self.exclHigh)]
            return notOverlap + overlap
        elif interval.low >= self.exclHigh:
            # Totally above
            notOverlap = [self,interval]
        else:
            assert(False)
        sumRet = 0
        for i in overlap + notOverlap:
            sumRet += i.width()
        assert(sumRet == self.width())
        return overlap,notOverlap

    def splitRange(self,interval):
        overlap = []
        notOverlap = []
        if interval.exclHigh <= self.low:
            # Totally below
            notOverlap = [self]
            overLap = []
        elif interval.low < self.low and interval.exclHigh > self.low and interval.exclHigh <= self.exclHigh:
            # Partly below
            overlap = [Interval(self.low, interval.exclHigh)]
            notOverlap = [Interval(interval.exclHigh, self.exclHigh)]
        elif interval.low < self.low and interval.exclHigh >= self.exclHigh:
            # Both below and above
            overlap = [Interval(self.low, self.exclHigh)]
            notOverlap = []
        elif interval.low >= self.low and interval.exclHigh <= self.exclHigh:
            # Fully inside
            notOverlap = [Interval(self.low, interval.low), Interval(interval.exclHigh,self.high)]
            overlap = [Interval(interval.low, interval.exclHigh)]
        elif interval.low >= self.low and interval.exclHigh > self.exclHigh:
            # Partly above
            notOverlap = [Interval(self.low, interval.low)]
            overlap = [Interval(interval.low, self.exclHigh)]
        elif interval.low >= self.exclHigh:
            # Totally above
            overlap = []
            notOverlap = [self]
        else:
            assert(False)
        sumRet = 0
        for i in overlap + notOverlap:
            sumRet += i.width()
        assert(sumRet == self.width())
        return overlap,notOverlap

def parseFile(f):
    grid = []
    for line in f:
        if len(line.strip()) == 0:
            break
        grid.append(line.strip())
        print(grid[-1])
    return grid

rulesDict = {}

def addRules(rules):
    global rulesDict
    rulesDict['A'] = 'A'
    rulesDict['R'] = 'R'
    for ruleLine in rules:
        idx = ruleLine.find('{')
        ruleName = ruleLine[:idx]
        ruleCases = ruleLine[idx+1:-1].split(',')
        rulesDict[ruleName] = ruleCases

def applyRuleCase(part,case):
    idx = case.find(':')
    if idx == -1:
        # This is the last case, just return it
        return case
    c = case[0]
    op = case[1]
    idx = case.find(':')
    if idx == -1:
        return case
    comp = int(case[2:idx])
    res = case[idx+1:]
    if op == '>':
        if part[c] > comp:
            return res
        else:
            return None
    elif op == '<':
        if part[c] < comp:
            return res
        else:
            return None
    else:
        assert(False)

def parseParts(partLines):
    parts = []
    for line in partLines:
        partAttributes = line[1:-1].split(',')
        assert(len(partAttributes) == 4)
        x = int(partAttributes[0][2:])
        m = int(partAttributes[1][2:])
        a = int(partAttributes[2][2:])
        s = int(partAttributes[3][2:])
        partDict = {}
        partDict['x'] = x
        partDict['m'] = m
        partDict['a'] = a
        partDict['s'] = s
        parts.append(partDict)
    return parts

def applyRuleCase(part,case):
    idx = case.find(':')
    if idx == -1:
        # This is the last case, just return it
        return case
    c = case[0]
    op = case[1]
    idx = case.find(':')
    if idx == -1:
        return case
    comp = int(case[2:idx])
    res = case[idx+1:]
    if op == '>':
        if part[c] > comp:
            return res
        else:
            return None
    elif op == '<':
        if part[c] < comp:
            return res
        else:
            return None
    else:
        assert(False)

def applyRules(part):
    nextRule = "in"
    while True:
        for case in rulesDict[nextRule]:
            nextRule = applyRuleCase(part, case)
            if nextRule is not None:
                # Applied a case.  Return if its accepted or rejected
                if nextRule == 'A':
                    return True
                elif nextRule == 'R':
                    return False
                else:
                    break

INF = 1000000000

def applyRuleForRanges(acceptedRanges, ruleCases):
    print(ruleCases)
    case = ruleCases[0]
    print("Case: " + case)
    if case.find(':') == -1:
        assert(len(ruleCases) == 1)
        if case == 'A':
            return acceptedRanges
        elif case == 'R':
            return []
        else:
            return applyRuleForRanges(acceptedRanges, rulesDict[case])
    else:
        for rangeSet in acceptedRanges:
            print(case)
            caseChar = case[0]
            op = case[1]
            comp = int(case[2:case.find(':')])
            passCase = case[case.find(':')+1:]
            newRangeSet = []
            if op == '>':
                caseInterval = Interval(comp+1,INF)
            elif op == '<':
                caseInterval = Interval(0,comp)
            for r in rangeSet[caseChar]:
                print("RuleCases: ")
                print(ruleCases)
                passesCondition,rest = r.splitRange(caseInterval)
                passingRanges = deepcopy(rangeSet)
                passingRanges[caseChar] = passesCondition
                passingRanges = applyRuleForRanges([passingRanges], rulesDict[passCase])
                notPassingRanges = deepcopy(rangeSet)
                notPassingRanges[caseChar] = rest
                notPassingRanges = applyRuleForRanges([notPassingRanges], ruleCases[1:])
                newRangeSet = newRangeSet + passingRanges + notPassingRanges
            return newRangeSet

def sumRanges(ranges):
    mySet = set()
    for r in ranges:
        for j in range(r.low,r.exclHigh):
            mySet.add(j)
    return len(mySet)

def solve(filename,problem):
    with open(filename, "r") as f:
        rules = parseFile(f)
        addRules(rules)
        partLines = parseFile(f)
        parts = parseParts(partLines)

        if problem == 1:
            result = 0
            for part in parts:
                if applyRules(part):
                    value = part['x'] + part['m'] + part['a'] + part['s']
                    result += value
            return result
        else:
            acceptedRanges = {}
            for c in ['x','m','a','s']:
                acceptedRanges[c] = [Interval(1,4001)]
            acceptedRangeSets = applyRuleForRanges([acceptedRanges],rulesDict["in"])
            print(acceptedRangeSets)
            rangeStr = ""
            total = 0
            for acceptedRanges in acceptedRangeSets:
                for c in ['x','m','a','s']:
                    rangeStr += "Ranges for " + c + " : "
                    for r in acceptedRanges[c]:
                        rangeStr += " " + r.toStr()
                    print(rangeStr)
                    rangeStr = ""
                rangeSetSum = sumRanges(acceptedRanges['x']) * sumRanges(acceptedRanges['m']) * sumRanges(acceptedRanges['a']) * sumRanges(acceptedRanges['s'])
                total += rangeSetSum
                print("Total for this rangeSet: " + str(rangeSetSum))
            return total

#assert(solve("input.txt",1) == 383682)
print(solve("input.txt",2))


