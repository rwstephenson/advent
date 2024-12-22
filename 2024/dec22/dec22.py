import sys
from math import *
from collections import *
sys.path.append('../../lib')
from point import Point
from interval import Interval
from parsing import *
from aocd import get_data, submit
from itertools import pairwise

def iterate(secret):
    secret = ((secret << 6) ^ secret) & (2**24 - 1)
    secret = ((secret >> 5) ^ secret) & (2**24 - 1)
    secret = ((secret << 11) ^ secret) & (2**24 - 1)
    return secret

def addSequences(priceChanges,sequences):
    seen = set()
    for i in range(3,len(priceChanges)):
        seq = (priceChanges[i-3][1],priceChanges[i-2][1],priceChanges[i-1][1],priceChanges[i][1])
        if seq not in seen:
            sequences[seq] += priceChanges[i][0]
            seen.add(seq)

def solve(filename, pt):
    lines = parseLines(filename)
    secrets = []
    sequences = defaultdict(int)
    for line in lines:
        iterations = [int(line)]
        buyerSequence = defaultdict(int)
        for i in range(2000):
            iterations.append(iterate(iterations[-1]))
        prices = list(map(lambda s : s % 10,iterations))
        changes = list(map(lambda ab : ab[1] - ab[0], pairwise(prices)))
        pricesChange = list(zip(prices,[10] + changes))
        addSequences(pricesChange,sequences)
        secrets.append(iterations[-1])
    maxSeq = max(sequences.keys(), key=(lambda key: sequences[key]))
    return sum(secrets),sequences[maxSeq]

def run(pt,day,year,expect1,expect2):
    with open("input.txt","w") as f:
        f.write(get_data(day=day,year=year))
    resTest1,resTest2 = solve("testInput.txt",pt)
    assert resTest2 == expect2, f"Result was {resTest2}"
    res1,res2 = solve("input.txt",pt)
    submit(res1, part='a', day=day, year=year)
    submit(res2, part='b', day=day, year=year)

run(1,22,2024,37327623,23)
