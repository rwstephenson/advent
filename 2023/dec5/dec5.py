import sys

def makeMap(f):
    myMap = []
    while (mapLine := f.readline()):
        entry = mapLine.strip().split(' ')
        if len(entry) == 3:
            myMap.append(list(map(int,entry)))
        else:
            break
    return sorted(myMap,key=lambda x: x[1])

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
        i = 0
        candidates = seeds
        for i in range(len(maps)):
            newCandidates = []
            for s in candidates:
                for entry in maps[i]:
                    sourcerangestart = int(entry[1])
                    destinationrangestart = int(entry[0])
                    rangelength = int(entry[2])
                    if s >= sourcerangestart and s < sourcerangestart + rangelength:
                        newCandidates.append(destinationrangestart + (s - sourcerangestart))
            candidates = newCandidates
        return min(candidates)

def findMinOfCandidates(candidates, maps):
    for i in range(len(maps)):
        newCandidates = set()
        for s in candidates:
            for entry in maps[i]:
                sourcerangestart = int(entry[1])
                destinationrangestart = int(entry[0])
                rangelength = int(entry[2])
                if s >= sourcerangestart and s < sourcerangestart + rangelength:
                    newCandidates.add(destinationrangestart + (s - sourcerangestart))
        candidates = newCandidates
    return min(candidates)

# Takes a range (starting with seeds), and a sorted map of the source to destination translations.
# Return is list of new ranges, according to those translation
def translateCandidateRange(r, sortedTranslationMap):
    #must be sorted!
    entryRangeStart = r[0]
    entryRangeEnd = r[0]+r[1] # END IS EXCLUSIVE
    destinationMap = [] # This is what we will return, the mapped range for the next iteration
    i = 0
    while True:
        lowestTranslation = sortedTranslationMap[i]
        sourceRangeStart = lowestTranslation[1]
        sourceRangeEnd = lowestTranslation[1] + lowestTranslation[2] # END IF EXCLUSIDE
        destinationStart = lowestTranslation[0]

        if entryRangeEnd < sourceRangeStart:
            # Totally below maps - add direct ranslation
            destinationMap.append([entryRangeStart, entryRangeEnd - entryRangeStart])
            return destinationMap
        elif entryRangeStart < sourceRangeStart and entryRangeEnd > sourceRangeStart:
            # Low part of range is below, add a direct translation for that
            destinationMap.append([entryRangeStart, sourceRangeStart - entryRangeStart])
            # and add a new translation for the area in the range
            if entryRangeEnd < sourceRangeEnd:
                destinationMap.append([destinationStart,entryRangeEnd - sourceRangeStart])
                return destinationMap
            else:
                # FULL OVERLAP, part below was added above, now add the segment, and reset the range
                destinationMap.append([destinationStart, sourceRangeEnd - sourceRangeStart])
                entryRangeStart = sourceRangeEnd
                i += 1
        elif entryRangeStart >= sourceRangeStart and entryRangeStart < sourceRangeEnd and entryRangeEnd < sourceRangeEnd:
            # entire range is in the map, add mapped translation for that
            destinationMap.append([destinationStart + (entryRangeStart - sourceRangeStart), entryRangeEnd - entryRangeStart])
            return destinationMap
        elif entryRangeStart >= sourceRangeStart and entryRangeStart < sourceRangeEnd and entryRangeEnd >= sourceRangeEnd:
            # Start of range is in the map, but the end of the range is not. Add mapped translation for start of range
            destinationMap.append([destinationStart + (entryRangeStart - sourceRangeStart), sourceRangeEnd - entryRangeStart])
            # and modify the entry range, as we are not fully covered
            entryRangeStart = sourceRangeEnd
        elif entryRangeStart >= sourceRangeEnd and i < len(sortedTranslationMap) - 1:
            # Totally above the range, but there are more ranges to check.  Add nothing, increment i
            i += 1
        elif entryRangeStart >= sourceRangeEnd and i == len(sortedTranslationMap) - 1:
            # Totally above the HIGHEST range, and we're at the end of the map.  Add a direct translation
            destinationMap.append([entryRangeStart, entryRangeEnd - entryRangeStart])
            return destinationMap
        else:
            assert(False)

def checkSortedRangesForOverlap(ranges):
    for i in range(len(ranges)-1):
        assert(ranges[i][0] + ranges[i][1] <= ranges[i+1][0])


def checkTotalSeedRange(ranges):
    total = 0
    for r in ranges:
        total += r[1]
    return total

def pt2(filename):
    with open(filename, "r") as f:
        seedLine = list(map(int,f.readline().split(':')[1].strip().split(' ')))
        seedRanges = []
        i = 0
        while (i < len(seedLine)):
            seedRanges.append([seedLine[i],seedLine[i+1]])
            i+=2
        f.readline()
        maps = readMaps(f)
        i = 0
        candidateRanges = sorted(seedRanges, key=lambda x: x[0])
        totalSeedSpace = checkTotalSeedRange(candidateRanges)
        for i in range(len(maps)):
            checkSortedRangesForOverlap(candidateRanges)
            newCandidates = []
            for r in candidateRanges:
                newCandidates += translateCandidateRange(r,maps[i])
            candidateRanges = sorted(newCandidates, key=lambda x: x[0])
            assert(checkTotalSeedRange(candidateRanges) == totalSeedSpace)
        return candidateRanges[0][0]

assert(pt2("testInput.txt") == 46)
print(pt2("input.txt"))

