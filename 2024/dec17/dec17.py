import sys
from math import *
from collections import *
sys.path.append('../../lib')
from point import Point
from interval import Interval
from parsing import *
from aocd import get_data, submit

def getCombo(operand,regs):
    if operand >= 0 and operand <= 3:
        return operand
    elif operand >= 4 and operand <= 6:
        return regs[operand%4]
    else:
        assert(False)

def adv(operand,regs):
    assert(operand == 3)
    print("Reduce A by 8x")
    regs[0] = regs[0] // (2 ** getCombo(operand,regs))

def bxl(operand,regs):
    if operand == 2:
        print("XOR B with 10")
    elif operand == 3:
        print("XOR B with 11")
    else:
        assert(False)
    regs[1] = regs[1] ^ operand

def bst(operand,regs):
    print("B becomes A % 8")
    assert(operand == 4)
    regs[1] = getCombo(operand,regs) % 8

def jnz(operand, regs):
    print("Repeat if A isn't 0")
    if regs[0] == 0:
        return -1
    else:
        assert(operand % 2 == 0)
        return operand

def bxc(operand, regs):
    print("XOR B and C")
    regs[1] = regs[1] ^ regs[2]

def out(operand, regs):
    print("output B % 8")
    assert(operand == 5)
    return getCombo(operand,regs) % 8

def bdv(operand, regs):
    assert(False)
    regs[1] = regs[0] // (2**getCombo(operand,regs))

def cdv(operand, regs):
    print("Set C to A // (2^B)")
    assert(operand == 5)
    regs[2] = regs[0] // (2**getCombo(operand,regs))


#Input: 2,4,1,2,7,5,4,1,1,3,5,5,0,3,3,0
# while a > 0
#   B = (A % 8) ^ 2
#   C = A % (2^B)
#   B = (B ^ C) ^ 3
#   print(B%8)
#   a = a // 8

def solve(filename, pt):
    lines = parseLines(filename)
    regs = [getInts(lines[0])[0],getInts(lines[1])[0],getInts(lines[2])[0]]
    program = getInts(lines[4])
    pc = 0
    res = ""

    while pc < len(program)-1:
        instr = program[pc]
        operand = program[pc+1]
        if instr == 0:
            adv(operand,regs)
        elif instr == 1:
            bxl(operand,regs)
        elif instr == 2:
            bst(operand,regs)
        elif instr == 3:
            jumpTo = jnz(operand,regs)
            if jumpTo > -1:
                pc = jumpTo - 2
        elif instr == 4:
            bxc(operand,regs)
        elif instr == 5:
            res += str(out(operand,regs) )
            res += ','
        elif instr == 6:
            assert(False)
            bdv(operand,regs)
        elif instr == 7:
            cdv(operand,regs)
        pc += 2
        print(regs)
    return res[0:-1]

def run(pt,day,year,expect):
    with open("input.txt","w") as f:
        f.write(get_data(day=day,year=year))
    #resTest = solve("testInput.txt",pt)
    #assert resTest == expect, f"Result was {resTest}"
    res = solve("input.txt",pt)
    print("Test Input: {} Puzzle Input: {}".format(resTest,res))
    if pt == 1:
        c = "a"
    else:
        c = "b"
    submit(res, part=c, day=day, year=year)

run(1,17,2024,"4,6,3,5,6,3,5,2,1,0")
#run(2,17,2024,"")
