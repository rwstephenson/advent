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
        print(m)
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

def pt2Brute(filename):
    with open(filename, "r") as f:
        seedLine = list(map(int,f.readline().split(':')[1].strip().split(' ')))
        seedRanges = []
        i = 0
        while (i < len(seedLine)):
            seedRanges.append([seedLine[i],seedLine[i+1]])
            i+=2
        print(seedRanges)
        f.readline()
        maps = readMaps(f)
        bigAssSet = set()
        for k in range(len(seedRanges)):
            for i in range(seedRanges[k][0],seedRanges[k][0] + seedRanges[k][1]):
                bigAssSet.add(i)
        return findMinOfCandidates(bigAssSet,maps)

def translateCandidateRange(r, sortedTranslationMap):
    #must be sorted!
    entryRangeStart = r[0]
    entryRangeEnd = r[0]+r[1]
    destinationMap = []
    for translation in translationMap:
        sourceRangeStart = translation[1]
        sourceRangeEnd = translation[1] + translation[2]
        destinationStart = translation[0]

        if entryRangeEnd < sourceRangeStart:
            # Totally below maps - direct translation


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
        for i in range(len(maps)):
            print (candidateRanges)
            print ("----------- NEW MAP: i = " + str(i) + " Num ranges: " + str(len(candidateRanges)))
            newCandidates = []
            print(maps[i])
            for r in candidateRanges:
                candidateRangeStart = r[0]
                candidateRangeEnd = r[0] + r[1]
                print("Candidate Range: (start:" + str(r[0]) + ", range:" + str(r[1]) + ")")
                newCandidates.append(translateCandidateRange)

                for entry in maps[i]:
                    print("MapEntry: (destination: " + str(entry[0]) + ",source:" + str(entry[1]) + ",range:" + str(entry[2]) + ")")
                    sourceRangeStart = entry[1]
                    sourceRangeEnd = entry[1]+entry[2]
                    destinationRangeStart = entry[0]
                    rangelength = entry[2]

                    if candidateRangeEnd < sourceRangeStart:
                        #totally below
                        print("Totally below, adding the same [" + str(candidateRangeStart) + ',' + str(candidateRangeEnd-candidateRangeStart) + "]")
                        newCandidates.append(candidateRangeStart,candidateRangeEnd-candidateRangeStart)

                    elif candidateRangeStart < sourceRangeStart and candidateRangeEnd >= sourceRangeStart and candidateRangeEnd < sourceRangeEnd:
                        #start of range misses, end of range overlaps
                        print("Partial overlap start, adding: " + str(destinationRangeStart) + " , " + str(candidateRangeEnd-sourceRangeStart))
                        newCandidates.append([destinationRangeStart, candidateRangeEnd-sourceRangeStart])
                    elif candidateRangeStart >= sourceRangeStart and candidateRangeEnd <= sourceRangeEnd:
                        #full range is inside
                        print("FULL overlap INNER, adding: " + str(destinationRangeStart + (candidateRangeStart - sourceRangeStart)) + " , " + str(r[1]))
                        newCandidates.append([destinationRangeStart + (candidateRangeStart - sourceRangeStart), r[1]])
                    elif candidateRangeStart <= sourceRangeEnd and candidateRangeEnd >= sourceRangeEnd:
                        #start of range overlaps, end of range misses
                        print("FULL overlap OUTER, adding: " + str(destinationRangeStart) + " , " + str(sourceRangeEnd-sourceRangeStart))
                        newCandidates.append([destinationRangeStart, sourceRangeEnd-sourceRangeStart])
                    elif candidateRangeStart >= sourceRangeStart and candidateRangeStart <= sourceRangeEnd and candidateRangeEnd > sourceRangeEnd:
                        #start of range overlaps, end of range misses
                        print("Partial overlap end, adding: " + str(destinationRangeStart + (candidateRangeStart - sourceRangeStart) )+ " , " + str(sourceRangeEnd-candidateRangeEnd))
                        newCandidates.append([destinationRangeStart + (candidateRangeStart - sourceRangeStart),sourceRangeEnd-candidateRangeStart])
                    elif candidateRangeStart > sourceRangeEnd:
                        pass
            candidateRanges = newCandidates
        print (candidateRanges)
        minLocation = sys.maxsize
        for i in range(len(candidateRanges)):
            minLocation = min(minLocation, candidateRanges[i][0])
        return min(candidateRanges)

print(pt2("testInput.txt"))

