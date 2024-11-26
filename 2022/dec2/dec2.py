import sys
sys.path.append('../../lib')
from point import Point

values = {'X':1, 'Y':2, 'Z':3}

def scorePt1(you, me):
    score = 0
    if you == 'A':
        if me == 'X':
            score += 3
        elif me == 'Y':
            score += 6
    elif you == 'B':
        if me == 'Y':
            score += 3
        elif me == 'Z':
            score += 6
    elif you == 'C':
        if me == 'Z':
            score += 3
        elif me == 'X':
            score += 6
    return score + values[me]

def scorePt2(you, me):
    score = 0
    if you == 'A':
        if me == 'X':
            score += values['Z']
        elif me == 'Y':
            score += 3 + values['X']
        elif me == 'Z':
            score += 6 + values['Y']
    elif you == 'B':
        if me == 'X':
            score += values['X']
        elif me == 'Y':
            score += 3 + values['Y']
        elif me == 'Z':
            score += 6 + values['Z']
    elif you == 'C':
        if me == 'X':
            score += values['Y']
        elif me == 'Y':
            score += 3 + values['Z']
        elif me == 'Z':
            score += 6 + values['X']
    return score

def solve(filename, pt):
    with open(filename, "r") as f:
        total = 0
        for line in f:
            (you,me) = line.strip().split(' ')
            if pt == 1:
                total += scorePt1(you,me)
            if pt == 2:
                total += scorePt2(you,me)
    return total

print(solve("input.txt", 2))

