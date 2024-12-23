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
        return ['A']
    if s == 'A':
        if e == 'W':
            return ['WSWA','SWWA']
        elif e == 'E':
            return ['SA']
        elif e == 'N':
            return ['WA']
        elif e == 'S':
            return ['WSA','SWA']
    elif s == 'N':
        if e == 'W':
            return ['SWA']
        elif e == 'E':
            return ['SEA','ESA']
        elif e == 'S':
            return ['SA']
        elif e == 'A':
            return ['WA']
    elif s == 'E':
        if e == 'W':
            return ['WWA']
        elif e == 'A':
            return ['NA']
        elif e == 'N':
            return ['NWA','WNA']
        elif e == 'S':
            return ['WA']
    elif s == 'S':
        if e == 'W':
            return ['WA']
        elif e == 'E':
            return ['EA']
        elif e == 'N':
            return ['NA']
        elif e == 'A':
            return ['NEA','ENA']
    elif s == 'W':
        if e == 'S':
            return ['EA']
        elif e == 'E':
            return ['EEA']
        elif e == 'N':
            return ['ENA']
        elif e == 'A':
            return ['EENA','ENEA']

def findPath(rob,value):
    e = rob.find(value)
    path = rob.bfs(e,['X'])
    res = ""
    for p in path:
        if p != rob:
            for d in ['E','N','S','W']:
                n = rob.getNeighboor(d)
                if n and n == p:
                    rob = p
                    res += d
        if p.value == value:
            res += 'A'
    return res,e

def walk(s,path,grid):
    p = Point(s.x,s.y,grid)
    res = ""
    for d in path:
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
    print("Walk path {} presses {} len {}".format(path,res,len(res)))
    return res

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
        dirpad1Walk = ""
        dirpad2Walk = ""
        rob3 = Point(keypadS.x,keypadS.y,keypadS.grid)
        rob2 = Point(dirPadS.x,dirPadS.y,dirPadS.grid)
        rob1 = Point(dirPadS.x,dirPadS.y,dirPadS.grid)
        keypadWalks = []
        for c in keypadNums:
            rob3Path,rob3 = findPath(rob3,c)
            keypadWalk += rob3Path
        for c in keypadWalk:
            rob2Path = findDirpadPaths(rob2.value,c)[0]
            rob2 = rob2.find(c)
            dirpad1Walk += rob2Path
        for c in dirpad1Walk:
            rob1Path = findDirpadPaths(rob1.value,c)[0]
            rob1 = rob1.find(c)
            dirpad2Walk += rob1Path
        print(dirpad2Walk)
        dirpadWalk = walk(dirPadS,dirpad2Walk,dirGrid)
        print("DirpadWalk: {} len {}".format(dirpadWalk,len(dirpadWalk)))
        keypadWalk = walk(dirPadS,dirpadWalk,dirGrid)
        print("KeypadWalk: {} len {}".format(keypadWalk,len(keypadWalk)))
        foundKeypad = walk(keypadS,keypadWalk,keypad)
        print("Found Keypad: {} len {}".format(foundKeypad,len(foundKeypad)))
        assert keypadNums == foundKeypad, f"Input Keypad was {keypadNums}"
        assert derivedKeypad == keypadNums, f"DerivedKeypad was {derivedKeypad}"
        print("Res is {} * {}".format(len(dirpad2Walk),int(foundKeypad[0:3])))
        total += len(dirpad2Walk)*int(keypadNums[0:3])
    return total

def run(pt,day,year,expect):
    with open("input.txt","w") as f:
        f.write(get_data(day=day,year=year))
    resTest = solve("testInput.txt",pt)
    assert resTest == expect, f"Result was {resTest}"
    res = solve("input.txt",pt)
    print(res)
    #print("Test Input: {} Puzzle Input: {}".format(resTest,res))
    if pt == 1:
        c = "a"
    else:
        c = "b"
    submit(res, part=c, day=day, year=year)

run(1,21,2024,126384)
#run(2,21,2024,-1)
