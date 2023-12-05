#def parseSeeds(line):

seedProperties = {}

def makeMap(f):
    myMap = []
    while (mapLine := f.readline()):
        entry = mapLine.strip().split(' ')
        if len(entry) == 3:
            myMap.append(entry)
        else:
            return myMap
    return myMap

def readMaps(f):
        f.readline(); f.readline()
        maps = []
        # seed to soil
        maps.append(makeMap(f))
        f.readline(); f.readline()
        #soil to fertil
        maps.append(makeMap(f))
        f.readline(); f.readline()
        # fertilToWater
        maps.append(makeMap(f))
        f.readline(); f.readline()
        # waterToLight
        maps.append(makeMap(f))
        f.readline(); f.readline()
        #lightToTemp
        maps.append(makeMap(f))
        f.readline(); f.readline()
        #tempToHumid
        maps.append(makeMap(f))
        f.readline(); f.readline()
        #humidToLocal
        maps.append(makeMap(f))
        return maps

def pt1(filename):
    with open(filename, "r") as f:
        seeds = list(map(int,f.readline().split(':')[1].strip().split(' ')))
        maps = readMaps(f)
        soil = []
        fertil = []
        water = []
        light = []
        temp = []
        humid = []
        local = []
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

print(pt1("input.txt"))

