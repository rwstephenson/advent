import sys
from math import *
from collections import *
sys.path.append('../../lib')
from point import Point
from interval import Interval

def makeMap(f):
    myMaps = []
    while (mapLine := f.readline()):
        entry = mapLine.strip().split(' ')
        if len(entry) == 3:
            myMaps.append((Interval(int(entry[1]),int(entry[1])+int(entry[2])-1),int(entry[0])-int(entry[1])))
        else:
            break
    return sorted(myMaps,key=lambda x: x[0].low)

def readMaps(f):
    maps = []
    for i in range (7):
        f.readline();
        m = makeMap(f)
        maps.append(m)
    return maps

def pt1(filename):
    with open(filename, "r") as f:
        seeds = list(map(int,f.readline().split(':')[1].strip().split(' ')))
        f.readline()
        maps = readMaps(f)
        for i in range(len(maps)):
            newSeeds = []
            seedsNotTranslated = set(seeds)
            for s in seeds:
                for mapInterval,translation in maps[i]:
                    if mapInterval.contains(s):
                        seedsNotTranslated.remove(s)
                        newSeeds.append(s+translation)
            # Add direct mapping for which have no mapping
            for s in seedsNotTranslated:
                newSeeds.append(s)
            assert(len(seeds) == len(newSeeds))
            seeds = newSeeds
        return min(seeds)

def parseSeedRanges(line):
    seedLine = list(map(int,line.split(':')[1].strip().split(' ')))
    seedRanges = []
    i = 0
    while (i < len(seedLine)):
        seedRanges.append(Interval(seedLine[i],seedLine[i] + seedLine[i+1]))
        i+=2
    return sorted(seedRanges,key=lambda i: i.low)

def printSeedRanges(sr):
    for i in sr:
        print(i)

def printMaps(sm):
    for i in sm:
        print("{} translation: {}".format(i[0],i[1]))

def checkRanges(sm):
    prev = None
    for i in sm:
        assert(i.getIntersection(prev) is None)
        prev = i

def pt2(filename):
    with open(filename, "r") as f:
        seedRanges = parseSeedRanges(f.readline())
        f.readline()
        maps = readMaps(f)
        for m in maps:
            newSeedRanges = []
            for seedRange in seedRanges:
                for translation in m:
                    intersection = seedRange.getIntersection(translation[0])
                    if intersection is not None:
                        newSeedRange = Interval(intersection.low+translation[1],intersection.high+translation[1])
                        newSeedRanges.append(newSeedRange)
            ## Need to add the seed ranges which are lower and higher than the translation
            ## ASSUMES SORTED
            i = 0
            while i < len(seedRanges):
                rangeBelow = seedRanges[i].getBelow(m[0][0])
                if rangeBelow is None:
                    break
                newSeedRanges.append(rangeBelow)
                i += 1
            i = 0
            while i < len(seedRanges):
                rangeAbove = seedRanges[-1-i].getAbove(m[-1][0])
                if rangeAbove is None:
                    break
                newSeedRanges.append(rangeAbove)
                i += 1
            seedRanges = sorted(newSeedRanges,key=lambda sr: sr.low)
            checkRanges(seedRanges)
        return seedRanges[0].low

resTest = pt1("testInput.txt")
assert resTest == 35, f"Result was {resTest}"
res = pt1("input.txt")
print("Part 1: Test: {}, Input: {}".format(resTest,res))
resTest = pt2("testInput.txt")
assert resTest == 46, f"Result was {resTest}"
res = pt2("input.txt")
print("Part 2: Test: {}, Input: {}".format(resTest,res))

