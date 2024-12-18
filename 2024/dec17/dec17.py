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
    regs[0] = regs[0] // (2 ** getCombo(operand,regs))

def bxl(operand,regs):
    if operand != 2 and operand != 3:
        assert(False)
    regs[1] = regs[1] ^ operand

def bst(operand,regs):
    assert(operand == 4)
    regs[1] = getCombo(operand,regs) % 8

def jnz(operand, regs):
    if regs[0] == 0:
        return -1
    else:
        assert(operand % 2 == 0)
        return operand

def bxc(operand, regs):
    regs[1] = regs[1] ^ regs[2]

def out(operand, regs):
    assert(operand == 5)
    return getCombo(operand,regs) % 8

def bdv(operand, regs):
    assert(False)
    regs[1] = regs[0] // (2**getCombo(operand,regs))

def cdv(operand, regs):
    assert(operand == 5)
    regs[2] = regs[0] // (2**getCombo(operand,regs))

def iteration(a):
    b = (a % 8) ^ 2
    c = a // (2**b)
    b = (b ^ c) ^ 3
    return b%8

def runProgram(a):
    s = ""
    while a > 0:
        s += str(iteration(a)) + ','
        a = a // 8
    return s[:-1]

def programToStr(program):
    s = ""
    for i in program:
        s += str(i) + ','
    return s[0:-1]

def solve2(filename):
    program = getInts(parseLines(filename)[4])
    res = solve3(0,program.copy())
    assert(programToStr(program) == runProgram(res))
    return res

def solve3(a,program):
    if len(program) > 0:
        target = program.pop()
        for i in range(8):
            if iteration(a+i) == target:
                if len(program) > 0:
                    res = solve3((a+i)*8,program.copy())
                    if res != -1:
                        return res
                else:
                    return a+i
        return -1


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
            o = out(operand,regs)
            res += str(o)
            res += ','
        elif instr == 6:
            assert(False)
            bdv(operand,regs)
        elif instr == 7:
            cdv(operand,regs)
        pc += 2
    return res[0:-1]

def run(pt,day,year):
    with open("input.txt","w") as f:
        f.write(get_data(day=day,year=year))
    if pt == 1:
        res = solve("input.txt",pt)
        res2 = runProgram(27575648)
        assert res2 == res, f"Result was {res2} but expected {res}"
    elif pt == 2:
        res = solve2("input.txt")
    if pt == 1:
        c = "a"
    else:
        c = "b"
    submit(res, part=c, day=day, year=year)

run(1,17,2024)
run(2,17,2024)
