import sys
import math
sys.setrecursionlimit(10000)


pipeStrings = set(['F','J','7','L','-','|'])

def findTwoStepsFromStart(coordinates, firstNode):
    x = firstNode[0]
    y = firstNode[1]
    pipeStringsAbove = set(['F','7','|'])
    pipeStringsBelow = set(['J','L','|'])
    pipeStringsLeft = set(['F','L','-'])
    pipeStringsRight = set(['J','7','-'])
    nodes = []
    assert(coordinates[y][x] == 'S')
    if y != 0 and coordinates[y-1][x] in pipeStringsAbove:
        nodes.append((x,y-1))
    if x != 0 and coordinates[y][x-1] in pipeStringsLeft:
        nodes.append((x-1,y))
    if x != len(coordinates[y]) - 1 and coordinates[y][x+1] in pipeStringsRight:
        nodes.append((x+1,y))
    if y != len(coordinates) - 1 and coordinates[y+1][x] in pipeStringsBelow:
        nodes.append((x,y+1))
    assert(len(nodes) == 2)
    return nodes[0],nodes[1]

def takeStep(coordinates, node, lastNode):
    x = node[0]
    y = node[1]
    nodeStr = coordinates[y][x]
    if nodeStr == 'F':
        if lastNode[0] == x:
            return (x+1,y),node
        else:
            return (x,y+1),node
    elif nodeStr == 'J':
            if lastNode[0] == x:
                return (x-1,y),node
            else:
                return (x,y-1),node
    elif nodeStr == '7':
            if lastNode[0] == x:
                return (x-1,y),node
            else:
                return (x,y+1),node
    elif nodeStr == 'L':
            if lastNode[0] == x:
                return (x+1,y),node
            else:
                return (x,y-1),node
    elif nodeStr == '-':
            if lastNode[0] == x-1:
                return (x+1,y),node
            else:
                return (x-1,y),node
    elif nodeStr == '|':
            if lastNode[1] == y-1:
                return (x,y+1),node
            else:
                return (x,y-1),node
    assert (nodeStr in pipeStrings)

def nodeToStr(node):
    return str(node[0]) + "," + str(node[1])

def traverseLoop(coordinates, firstNode):
    loopNodes = set()
    loopNodes.add(nodeToStr(firstNode))
    leftNode,rightNode = findTwoStepsFromStart(coordinates,firstNode)
    lastNodeLeft = firstNode
    lastNodeRight = firstNode
    loopNodes.add(nodeToStr(leftNode))
    loopNodes.add(nodeToStr(rightNode))
    i = 1
    while not (leftNode[0] == rightNode[0] and leftNode[1] == rightNode[1]):
        leftNode,lastNodeLeft = takeStep(coordinates, leftNode, lastNodeLeft)
        loopNodes.add(nodeToStr(leftNode))
        rightNode,lastNodeRight = takeStep(coordinates, rightNode, lastNodeRight)
        loopNodes.add(nodeToStr(rightNode))
        if leftNode[0] == lastNodeRight[0] and leftNode[1] == lastNodeRight[1]:
            #We just passed eachother, return before incrementing
            return i
        i +=1
    return i, loopNodes

def parseFile(f):
    coordinates = []
    y = 0
    i = 0
    for line in f:
        if line.find('S') != -1:
            x = line.find('S')
            y = i
        coordinates.append(line.strip())
        i+=1
    return coordinates, x, y

def findStart(coordinates):
    for i in range(len(coordinates)-1):
        for j in range(len(coordinates[i])-1):
            if coordinates[i][j] == 'S':
                return (j,i)

def pt1(filename):
    with open(filename, "r") as f:
        coordinates, startX, startY = parseFile(f)
        return(traverseLoop(coordinates, (startX, startY))[0])

# Will return True ONLY if we are certain there is a way out.
def knownWayOut(neighboors, notEnclosed):
    for neighboor in neighboors:
        if neighboor in notEnclosed:
            return True
    else:
        return False

def notVisitedNeighboors(node, enclosed, loopNodes, currentPath, coordinates):
    filteredNeighboors = []
    neighboors = getStepsAround(node, coordinates)
    for i in neighboors:
        if nodeToStr(i) not in enclosed and nodeToStr(i) not in loopNodes and nodeToStr(i) not in currentPath:
            filteredNeighboors.append(i)
    #filter(lambda x: nodeToStr(x) not in enclosed and nodeToStr(x) not in loopNodes, neighboors)
    return filteredNeighboors

def isOnEdge(node, coordinates):
    x,y = node
    return x == 0 or x == len(coordinates[0])-1 or y == 0 or y == len(coordinates) - 1

def getStepsAround(node, coordinates):
    x,y = node
    assert(not isOnEdge(node, coordinates))
    return [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]

def noWayOut(node, enclosed, notEnclosed, loopNodes, coordinates, currentPath):
    assert (nodeToStr(node) not in loopNodes)
    if nodeToStr(node) in enclosed:
        return currentPath
    if nodeToStr(node) in notEnclosed:
        return set()
    # Haven't seen this before
    x,y = node
    if isOnEdge(node, coordinates):
        return set()
    # Not on the edge, check steps around
    neighboors = notVisitedNeighboors(node, enclosed, loopNodes, currentPath, coordinates)
    if knownWayOut(neighboors, notEnclosed):
        # Neighboor has a way out
        return set()
    elif len(neighboors) == 0:
        # All neighboors visited
        return currentPath
    # There's a neighboor we haven't seen any neighboors before, check it.
    for neighboor in neighboors:
        currentPath.add(nodeToStr(neighboor))
        if len(noWayOut(neighboor, enclosed, notEnclosed, loopNodes, coordinates, currentPath)) == 0:
            return set()
    return currentPath

def cleanedCoordinates(coordinates, loopNodes):
    cleanedOutput = []
    for y in range(len(coordinates)):
        cleanLine = ""
        for x in range(len(coordinates[y])):
            if nodeToStr((x,y)) in loopNodes:
                cleanLine += coordinates[y][x]
            else:
                cleanLine += '.'
        print(cleanLine)
        cleanedOutput.append(cleanLine)
    return cleanedOutput

def cleanAnddoubleInput(coordinates, loopNodes):
    cleanCoords = cleanedCoordinates(coordinates, loopNodes)
    zoomedInCoords = []
    x = 0
    y = 0
    while y < len(cleanCoords):
        zoomedInLine = ""
        while x < len(cleanCoords[y]):
            c = cleanCoords[y][x]
            if c == '.':
                zoomedInLine += 'o.'
            elif c == '-':
                zoomedInLine += '--'
            elif c == '|':
                zoomedInLine += 'o|'
            elif c == 'S':  ## Note that this is a dirty special case for the input
                zoomedInLine += 'oS'
            elif c == '7':
                zoomedInLine += '-7'
            elif c == 'F':
                zoomedInLine += 'oF'
            elif c == 'J':
                zoomedInLine += '-J'
            elif c == 'L':
                zoomedInLine += 'oL'
            else:
                print(c)
                assert(False)
            x+=1
        x = 0
        zoomedInCoords.append(zoomedInLine)
        #print(zoomedInLine)
        zoomedInLine2 = ""
        while x < len(zoomedInLine):
            c = zoomedInLine[x]
            if c == '.' or c == 'o':
                zoomedInLine2 += 'o'
            elif c == '-':
                zoomedInLine2 += 'o'
            elif c == '|':
                zoomedInLine2 += '|'
            elif c == '7':
                zoomedInLine2 += '|'
            elif c == 'F':
                zoomedInLine2 += '|'
            elif c == 'S':
                zoomedInLine2 += '|'
            elif c == 'J':
                zoomedInLine2 += 'o'
            elif c == 'L':
                zoomedInLine2 += 'o'
            else:
                assert(False)
            x+=1
        x = 0
        assert(len(zoomedInLine) == len(cleanCoords[y]*2))
        assert(len(zoomedInLine) == len(zoomedInLine2))
        #print(zoomedInLine2)
        zoomedInCoords.append(zoomedInLine2)
        y += 1
    return zoomedInCoords

def realNodes(enclosed,coordinates):
    print(enclosed)
    sum = 0
    for i in enclosed:
        x = int(i.strip().split(',')[0])
        y = int(i.strip().split(',')[1])
        if coordinates[y][x] != 'o':
            sum += 1
        elif coordinates[y]:
            pass
    return sum


def pt2(filename):
    with open(filename, "r") as f:
        coordinates, startX, startY = parseFile(f)
        loopNodes = traverseLoop(coordinates, (startX, startY))[1]
        coordinates = cleanAnddoubleInput(coordinates,loopNodes)
        startX, startY = findStart(coordinates)
        loopNodes = traverseLoop(coordinates, (startX, startY))[1]
        x = 0
        y = 0
        totalEnclosed = set()
        newEnclosed = set()
        notEnclosed = set()
        while y < len(coordinates):
            while x < len(coordinates[0]):
                if nodeToStr((x,y)) in loopNodes:
                    pass
                else:
                    newEnclosed = noWayOut((x,y),totalEnclosed,notEnclosed,loopNodes,coordinates, set())
                    if len(newEnclosed) == 0:
                        notEnclosed.add(nodeToStr((x,y)))
                    else:
                        for node in newEnclosed:
                            totalEnclosed.add(node)
                x += 1
            x = 0
            y += 1
        return realNodes(totalEnclosed, coordinates)

assert(pt2("testInput2.txt") == 4)
print(pt2("input.txt"))


