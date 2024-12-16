import sys
from math import *
from collections import *
sys.path.append('../../lib')
from point import Point
from interval import Interval
from parsing import *
from aocd import get_data, submit
import sympy

INF = 99999999999999

def getGame(lines,pt):
    buttonA = getInts(lines[0])
    buttonB = getInts(lines[1])
    prize = getInts(lines[2])
    if pt == 2:
        prize[0] += 10000000000000
        prize[1] += 10000000000000
    return (buttonA,buttonB,prize)

def getMinCostBrute(game,maxPresses):
    xTotal = 0
    yTotal = 0
    minSoFar = INF
    for aPresses in range(maxPresses):
        xTotal = game[0][0] * aPresses
        yTotal = game[0][1] * aPresses
        if xTotal < game[2][0] and yTotal < game[2][1]:
            for bPresses in range(maxPresses):
                if xTotal + game[1][0]*bPresses == game[2][0] and yTotal + game[1][1]*bPresses == game[2][1]:
                    minSoFar = min(minSoFar,aPresses*3 + bPresses)
    return minSoFar

def getMinCost(game):
    a,b = sympy.symbols('a b')
    equations = []
    equations.append(a*game[0][0] + b*game[1][0] - game[2][0])
    equations.append(a*game[0][1] + b*game[1][1] - game[2][1])
    res = sympy.solve(equations)
    a = res[a]
    b = res[b]
    if a.is_integer and b.is_integer and a > 0 and b > 0:
        return a*3+b
    else:
        return INF

def solve(filename, pt):
    lines = parseLines(filename)
    games = []
    total = 0
    i = 0
    while i < len(lines):
        games.append(getGame(lines[i:i+3],pt))
        i+=4
    for game in games:
        if pt == 1:
            bestResult = getMinCost(game)
            bestResultBrute = getMinCostBrute(game,100)
            assert(bestResult == bestResultBrute)
        elif pt == 2:
            bestResult = getMinCost(game)
        if bestResult != INF:
            total += bestResult
    return int(total)

def run(pt,day,year,expect):
    with open("input.txt","w") as f:
        f.write(get_data(day=day,year=year))
    resTest = solve("testInput.txt",pt)
    assert resTest == expect, f"Result was {resTest}"
    res = solve("input.txt",pt)
    print("Test Input: {} Puzzle Input: {}".format(resTest,res))
    if pt == 1:
        c = "a"
    else:
        c = "b"
    submit(res, part=c, day=day, year=year)

run(1,13,2024,480)
run(2,13,2024,875318608908)
