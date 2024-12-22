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
    #assert(res != "ENEA" and res != "WSWA")
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
        for c in keypadNums:
            rob3Path,rob3 = findPath(rob3,c)
            keypadWalk += rob3Path
        for c in keypadWalk:
            rob2Path,rob2 = findPath(rob2,c)
            dirpad1Walk += rob2Path
        for c in dirpad1Walk:
            rob1Path,rob1 = findPath(rob1,c)
            dirpad2Walk += rob1Path
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
