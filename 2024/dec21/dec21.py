import sys
from math import *
from collections import *
sys.path.append('../../lib')
from point import Point
from interval import Interval
from parsing import *
from aocd import get_data, submit

def makeKeypadGrid():
    grid = []
    grid.append("789")
    grid.append("456")
    grid.append("123")
    grid.append("X0A")
    return Point(2,3,grid),grid

def makeDirectionalGrid():
    grid = []
    grid.append("XNA")
    grid.append("WSE")
    return Point(2,0,grid),grid

def findDirpadPaths(s,e):
    if s == e:
        return 'A'
    if s == 'A':
        if e == 'W':
            return 'SWWA'
        elif e == 'E':
            return 'SA'
        elif e == 'N':
            return 'WA'
        elif e == 'S':
            return 'WSA'
    elif s == 'N':
        if e == 'W':
            return 'SWA'
        elif e == 'E':
            return 'SEA'
        elif e == 'S':
            return 'SA'
        elif e == 'A':
            return 'EA'
    elif s == 'E':
        if e == 'W':
            return 'WWA'
        elif e == 'A':
            return 'NA'
        elif e == 'N':
            return 'NWA'
        elif e == 'S':
            return 'WA'
    elif s == 'S':
        if e == 'W':
            return 'WA'
        elif e == 'E':
            return 'EA'
        elif e == 'N':
            return 'NA'
        elif e == 'A':
            return 'NEA'
    elif s == 'W':
        if e == 'S':
            return 'EA'
        elif e == 'E':
            return 'EEA'
        elif e == 'N':
            return 'ENA'
        elif e == 'A':
            return 'EENA'

def findPath(rob,value):
    s = rob.value
    e = rob.find(value)
    path = rob.bfs(e,['X'])
    res = ""
    dirs = defaultdict(int)
    for p in path:
        if p != rob:
            for d in ['E','N','S','W']:
                n = rob.getNeighboor(d)
                if n and n == p:
                    rob = p
                    dirs[d] += 1
    dirsOrder = ['W','N','S','E']
    if s == '0' or s == 'A':
        if value == '7' or value == '4' or value == '1':
            dirsOrder = ['N','W','E','S']
    if s == '7' or s == '4' or s == '1':
        if value == '0' or value == 'A':
            dirsOrder = ['N','W','E','S']
    for d in dirsOrder:
        for i in range(dirs[d]):
            res += d
    res += 'A'
    return res,e

def walk(s,path,grid):
    p = Point(s.x,s.y,grid)
    res = ""
    for d in path:
        #print("{} go {}".format(p.value,d))
        if d == 'A':
            res += p.value
        elif d == '<':
            p = p.getNeighboor('W')
        elif d == '>':
            p = p.getNeighboor('E')
        elif d == '^':
            p = p.getNeighboor('N')
        elif d == 'v':
            p = p.getNeighboor('S')
        else:
            p = p.getNeighboor(d)
    #print("Walk path {} presses {} len {}".format(path,res,len(res)))
    return res

def solve2(filename, pt):
    print("-------------------------------------")
    lines = parseLines(filename)
    keypadS,keypad = makeKeypadGrid()
    dirPadS,dirGrid = makeDirectionalGrid()
    total = 0
    for line in lines:
        lineSplit = line.split(': ')
        keypadNums = lineSplit[0]
        keypadWalk = ""
        dirpad1Walks = [""]
        rob3 = Point(keypadS.x,keypadS.y,keypadS.grid)
        rob2 = Point(dirPadS.x,dirPadS.y,dirPadS.grid)
        rob1 = Point(dirPadS.x,dirPadS.y,dirPadS.grid)
        for c in keypadNums:
            rob3Path,rob3 = findPath(rob3,c)
            keypadWalk += rob3Path
        print(keypadWalk)
        for c in keypadWalk:
            rob2Paths = findDirpadPaths(rob2.value,c)
            if len(rob2Paths) == 1:
                for w in range(len(dirpad1Walks)):
                    #print("From {} to {} adding {} to {}".format(rob2.value, c, rob2Paths[0],dirpad1Walks[w]))
                    dirpad1Walks[w] += rob2Paths[0]
            elif len(rob2Paths) == 2:
                newDirpadWalks = []
                for w in range(len(dirpad1Walks)):
                    newDirpadWalks.append(dirpad1Walks[w] + rob2Paths[0])
                    newDirpadWalks.append(dirpad1Walks[w] + rob2Paths[1])
                dirpad1Walks = newDirpadWalks
            rob2 = rob2.find(c)
        newWalks = []
        for w in dirpad1Walks:
            dirpad2Walks = [""]
            derivedKeypadWalk = walk(dirPadS,w,dirGrid)
            assert(derivedKeypadWalk == keypadWalk)
            #print("keypadWalk: {} len: {}".format(derivedKeypadWalk,len(derivedKeypadWalk)))
            for c in w:
                rob1Paths = findDirpadPaths(rob1.value,c)
                if len(rob1Paths) == 1:
                    for w in range(len(dirpad2Walks)):
                        dirpad2Walks[w] += rob1Paths[0]
                elif len(rob1Paths) == 2:
                    newDirpad2Walks = []
                    for w in range(len(dirpad2Walks)):
                        newDirpad2Walks.append(dirpad2Walks[w] + rob1Paths[0])
                        newDirpad2Walks.append(dirpad2Walks[w] + rob1Paths[1])
                    dirpad2Walks = newDirpad2Walks
                rob1 = rob1.find(c)
            for w in dirpad2Walks:
                newWalks.append(w)
        minWalk = 99999999999999999999999999
        for w in newWalks:
            dirpadWalk = walk(dirPadS,w,dirGrid)
            #print("DirpadWalk: {} len {}".format(dirpadWalk,len(dirpadWalk)))
            keypadWalk = walk(dirPadS,dirpadWalk,dirGrid)
            #print("KeypadWalk: {} len {}".format(keypadWalk,len(keypadWalk)))
            foundKeypad = walk(keypadS,keypadWalk,keypad)
            #print("Found Keypad: {} len {}".format(foundKeypad,len(foundKeypad)))
            #print("{} {} len {}".format(foundKeypad,w,len(w)))
            assert keypadNums == foundKeypad, f"Input Keypad was {keypadNums}"
            #if len(w) < minWalk:
            #    print(dirpadWalk)
            #    print(keypadWalk)
            #    print(foundKeypad)
            minWalk = min(minWalk,len(w))
        print("Res is {} * {}".format(minWalk,int(foundKeypad[0:3])))
        total += minWalk*int(keypadNums[0:3])
    return total

def solve(filename, pt):
    print("-------------------------------------")
    lines = parseLines(filename)
    keypadS,keypad = makeKeypadGrid()
    dirPadS,dirGrid = makeDirectionalGrid()
    total = 0
    for line in lines:
        lineSplit = line.split(': ')
        keypadNums = lineSplit[0]
        if len(lineSplit) > 1:
            examplePath = lineSplit[1].strip()
            exampleDirpadWalk = walk(dirPadS,examplePath,dirGrid)
            print("dirPadWalk: {} len {}".format(exampleDirpadWalk,len(exampleDirpadWalk)))
            exampleKeypadWalk = walk(dirPadS,exampleDirpadWalk,dirGrid)
            print("keypadWalk: {} len {}".format(exampleKeypadWalk,len(exampleKeypadWalk)))
            derivedKeypad = walk(keypadS,exampleKeypadWalk,keypad)
            print("derivedKeypad: {} len {}".format(derivedKeypad,len(derivedKeypad)))
            print("Explicit input: {} Derived Input: {}".format(keypadNums,derivedKeypad))
        keypadWalk = ""
        dirpad1Walk = []
        dirpad2Walk = ""
        rob3 = Point(keypadS.x,keypadS.y,keypadS.grid)
        rob2 = 'A'
        for c in keypadNums:
            rob3Path,rob3 = findPath(rob3,c)
            keypadWalk += rob3Path
        oldWalk = list(keypadWalk)
        if pt == 1:
            robots = 2
        elif pt == 2:
            robots = 25
        res = 0
        for i in range(robots):
            print("Robot: {} len Walk: {}".format(i,len(oldWalk)))
            for c in oldWalk:
                rob2Path = findDirpadPaths(rob2,c)
                rob2 = c
                for d in rob2Path:
                    if i < robots - 1:
                        dirpad1Walk.append(d)
                    else:
                        res += 1
            oldWalk = dirpad1Walk
            dirpad1Walk = []
        #for c in dirpad1Walk:
        #    rob1Path = findDirpadPaths(rob1.value,c)[0]
        #    rob1 = rob1.find(c)
        #    dirpad2Walk += rob1Path
        print("Res is {} * {}".format(res,int(keypadNums[0:3])))
        total += res*int(keypadNums[0:3])
    return total

def run(pt,day,year,expect):
    with open("input.txt","w") as f:
        f.write(get_data(day=day,year=year))
    #resTest = solve("testInput.txt",pt)
    #assert resTest == expect, f"Result was {resTest}"
    res = solve("input.txt",pt)
    print(res)
    #print("Test Input: {} Puzzle Input: {}".format(resTest,res))
    if pt == 1:
        c = "a"
    else:
        c = "b"
    submit(res, part=c, day=day, year=year)

run(1,21,2024,126384)
run(2,21,2024,-1)
