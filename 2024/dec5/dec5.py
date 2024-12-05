import sys
from math import *
from collections import *
sys.path.append('../../lib')
from point import Point
from node import Node
from interval import Interval
from parsing import *
from aocd import submit

def run(pt,expected,day,year):
    resTest = solve("testInput.txt",pt)
    assert resTest == expected, f"Result was {resTest}"
    res = solve("input.txt",pt)
    print("Test Input: {} Puzzle Input: {}".format(resTest,res))
    if pt == 1:
        c = "a"
    else:
        c = "b"
    submit(res, part=c, day=day, year=year)

def findFirst(badUpdate,rules):
    slimRules = {}
    for i in badUpdate:
        rulesForI = set()
        for r in rules[i]:
            if r in badUpdate:
                rulesForI.add(r)
        slimRules[i] = rulesForI
    for i in badUpdate:
        if len(slimRules[i]) == 0:
            return i

def fix(badUpdate,rules):
    # key cant come before values
    slimRules = {}
    numsLeft = badUpdate.copy()
    goodUpdate = []
    while(len(numsLeft) > 0):
        first = findFirst(numsLeft,rules)
        goodUpdate.append(first)
        numsLeft.remove(first)
    return goodUpdate

def solve(filename, pt):
    rules = defaultdict(set)
    # key cannot come before values
    updates = []
    total = 0
    with open(filename,"r") as f:
        line = f.readline().strip()
        while len(line) > 0:
            rule = line.split('|')
            rules[rule[1]].add(rule[0])
            line = f.readline().strip()
        for line in f:
            updates.append(line.strip().split(','))

        for update in updates:
            assert(len(update) % 2 == 1)
            valid = True
            for i in range(len(update)):
                if update[i] in rules:
                    for ruleY in rules[update[i]]:
                        if ruleY in update[i:]:
                            valid = False
            if valid:
                if pt == 1:
                    total += int(update[len(update) // 2])
            else:
                if pt == 2:
                    total += int(fix(update,rules)[len(update) // 2])
    return total

run(1,143,5,2024)
run(2,123,5,2024)
