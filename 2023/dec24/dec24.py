import sys
import math
from sympy import symbols, solve
from functools import cache

class Stone():
    x = 0
    y = 0
    z = 0
    t = 0
    vx = 0
    vy = 0
    vz = 0
    vt = 1
    slope = 0
    b = 0
    sid = 0

    def __init__(self, pos, vel, sid):
        self.x = int(pos[0].strip())
        self.y = int(pos[1].strip())
        self.z = int(pos[2].strip())
        self.vx = int(vel[0].strip())
        self.vy = int(vel[1].strip())
        self.vz = int(vel[2].strip())
        self.slope = self.vy / self.vx
        self.b = self.y - self.slope * self.x
        self.sid = sid

    def toStr(self):
        return "Stone: " + str(self.sid) + " (" + str(self.x) + "," + str(self.y) + "," + str(self.z) + ") and velocity (" + str(self.vx) + "," + str(self.vy) + "," + str(self.vz) + ")"

    def toStrSlope(self):
        return "Stone: " + str(self.sid) + " : y = " + str(self.slope) + "x + " + str(self.b)

    def position(self, t):
        return (self.x + t*self.vx,self.y + t*self.vy, self.z + t*self.vz)

def parseFile(f):
    stones = []
    i = 0
    for line in f:
        pos,vel = line.split('@')
        stones.append(Stone(pos.split(','),vel.split(','),i))
        print(stones[-1].toStr())
        i += 1
    return stones


def checkIntersection(stone1,stone2,testArea):
    if stone1.slope == stone2.slope:
        return True,(0,0)
    #mx1 + b1 = mx2 + b2
    #mx1 - mx2 = b2 - b1
    #(m1-m2)x = (b2-b1)
    #x = (b2-b1)/(m1-m2)
    else:
        x = (stone2.b - stone1.b) / (stone1.slope - stone2.slope)
        y = stone1.slope * x + stone1.b
        return False,(x,y)

def isInPast(stone,point):
    if stone.vx >= 0:
        if stone.x > point[0]:
            return True
    else:
        if stone.x < point[0]:
            return True
    return False

def findIntersections(stones,testArea):
    total = 0
    for i in range(len(stones)):
        for j in range(len(stones)):
            if i < j:
                parallel,poi = checkIntersection(stones[i],stones[j],testArea)
                x,y = poi
                if not parallel and x >= testArea[0] and x <= testArea[1] and y >= testArea[0] and y <= testArea[1]:
                    if not isInPast(stones[i],poi) and not isInPast(stones[j],poi):
                        total += 1
    return total

def findCollinear(stones3):
    x0, y0, z0, xv, yv, zv, t1, t2, t3 = symbols('x0 y0 z0 xv yv zv t1 t2 t3')
    equations = []
    for stone, t in zip(stones3, [t1, t2, t3]):
        equations.append(stone.x + stone.vx * t - (x0 + xv * t))
        equations.append(stone.y + stone.vy * t - (y0 + yv * t))
        equations.append(stone.z + stone.vz * t - (z0 + zv * t))
    res = solve(equations, x0, y0, z0, xv, yv, zv, t1, t2, t3, dict=True)[0]
    return res[x0],res[y0],res[z0]

def pt1(filename,testRange):
    with open(filename, "r") as f:
        stones = parseFile(f)
        return findIntersections(stones,testRange)

def pt2(filename):
    with open(filename, "r") as f:
        stones = parseFile(f)
        startingPosition = findCollinear(stones[:3])
        print("Starting Position: (" + str(startingPosition[0]) + "," + str(startingPosition[1]) + "," + str(startingPosition[2]) + ")")
        return startingPosition[0] + startingPosition[1] + startingPosition[2]

assert(pt1("testInput.txt",(7,27)) == 2)
assert(pt1("input.txt",(200000000000000,400000000000000)) == 21843)

print(pt2("input.txt"))


