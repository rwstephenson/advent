import sys
import math
from functools import cache

class Brick:
    x = (0,0)
    y = (0,0)
    z = (0,0)
    bid = 0

    def __init__(self, coords0, coords1, bid):
        self.bid = bid
        self.x = (min(int(coords0[0]),int(coords1[0])), max(int(coords0[0]),int(coords1[0])))
        self.y = (min(int(coords0[1]),int(coords1[1])), max(int(coords0[1]),int(coords1[1])))
        self.z = (min(int(coords0[2]),int(coords1[2])), max(int(coords0[2]),int(coords1[2])))

    def volume(self):
        return (self.x[1]-self.x[0]+1) * (self.y[1]-self.y[0] + 1) * (self.z[1]-self.z[0] + 1)

    def toStr(self):
        return "Brick: " + str(self.bid) + " x= " + str(self.x[0]) + "-" + str(self.x[1]) + " , y= " + str(self.y[0]) + "-" + str(self.y[1]) + " , z= " + str(self.z[0]) + "-" + str(self.z[1])

def makeBrick(x,y,z, bid):
    return Brick([x[0],y[0],z[0]],[x[1],y[1],z[1]],bid)

def parseFile(f):
    bricks = []
    i = 0
    for line in f:
        bricks.append(Brick(line.strip().split('~')[0].split(','),line.strip().split('~')[1].split(','),i))
        i+= 1
    bricks.sort(key=lambda b: b.z[0])
    return bricks

def isInside(d0,d1):
    assert(d0[0] <= d0[1] and d1[0] <= d1[1])
    return (d0[0] >= d1[0] and d0[0] <= d1[1]) or (d0[1] >= d1[0] and d0[1] <= d1[1])

def coordsOverlap(d0, d1):
    return isInside(d0,d1) or isInside(d1,d0)

def xyOverlap(groundBrick, newBrick):
    return coordsOverlap(groundBrick.x, newBrick.x) and coordsOverlap(groundBrick.y, newBrick.y)

def dropBrick(groundBricks, airBrick):
    z0 = 0
    for groundBrick in groundBricks:
        if xyOverlap(groundBrick, airBrick):
            z0 = max(groundBrick.z[1] + 1,z0)
    return makeBrick(airBrick.x,airBrick.y,(z0,z0 + (airBrick.z[1] - airBrick.z[0])), airBrick.bid)

def fall(airBricks):
    groundBricks = []
    for brick in airBricks:
        groundBricks.append(dropBrick(groundBricks, brick))
    return groundBricks

def noDupsList(myList):
    distinct = set()
    for e in myList:
        if e in distinct:
            return False
        else:
            distinct.add(e)
    return True

def getTotalZ(bricks):
    totalVolume = 0
    for brick in bricks:
        totalVolume += brick.z[0]
    return totalVolume

def checkTotalDrops(brickSet, groundBricks, removedBrick):
    total = 0
    print("Removed brick: " + str(removedBrick.bid))
    for groundBrick in groundBricks:
        if brickSet[groundBrick.bid] > groundBrick.z[0]:
            total += 1
    return total


def canDisintigrate(i, bricks, brickSet, totalZ, pt2):
    airBricks = bricks[0:i] + bricks[i+1:]
    assert(len(airBricks) + 1 == len(bricks))
    groundBricks = fall(airBricks)
    if pt2:
        return checkTotalDrops(brickSet, groundBricks, bricks[i])
    else:
        if totalZ == getTotalZ(groundBricks) + bricks[i].z[0]:
            return 1
        else:
            return 0

def countDisintigratable2(bricks, pt2):
    count = 0
    brickSet = {}
    totalZ = 0
    for brick in bricks:
        brickSet[brick.bid] = brick.z[0]
        totalZ += brick.z[0]
    for i in range(len(bricks)):
        count += canDisintigrate(i, bricks, brickSet, totalZ, pt2)
        print(count)
    return count

def countDisintigratable(bricks):
    # Brick -> Bricks directly below it
    support = {}
    # Brick -> Bricks directly above it
    supporting = {}
    for checkBrick in bricks:
        for brick in bricks:
            if checkBrick.z[1] == brick.z[0]-1 and xyOverlap(brick,checkBrick):
                # The brick we are checking is exactly below another one, and they overlap.  It is supporting it.
                if brick.bid in support.keys():
                    support[brick.bid] = support[brick.bid] + [checkBrick.bid]
                else:
                    support[brick.bid] = [checkBrick.bid]
                if checkBrick.bid in supporting.keys():
                    supporting[checkBrick.bid] = supporting[checkBrick.bid] + [brick.bid]
                else:
                    supporting[checkBrick.bid] = [brick.bid]
    count = 0
    for brick in bricks:
        if brick.bid not in supporting:
            # It's not supportin anything, can disintigrate
            print("Brick: " + str(brick.bid) + " is not supporting anything.  Can disintigrate")
            count += 1
        else:
            assert(noDupsList(supporting[brick.bid]))
            # Its supporting at least one brick, check if anybody else is supporting the same bricks
            for brickAbove in supporting[brick.bid]:
                canDisint = True
                if len(support[brickAbove]) == 1:
                    assert(brick.bid == support[brickAbove][0])
                    print("Brick: " + str(brick.bid) + " is the only support for brick " + str(brickAbove) + " Must keep")
                    canDisint = False
            if canDisint:
                print("Brick: " + str(brick.bid) + " is never the only support.  Can disintigrate")
                count += 1
    return count

def pt1(filename, pt2):
    with open(filename, "r") as f:
        # Bricks are sorted, by how close to the ground they are.
        airBricks = parseFile(f)
        for brick in airBricks:
            print(brick.toStr())
        print("DROPPING BRICKS")
        groundBricks = fall(airBricks)
        for brick in groundBricks:
            print(brick.toStr())
        return countDisintigratable2(groundBricks, pt2)

#print(pt1("testInput.txt", True))
print(pt1("input.txt",True))

