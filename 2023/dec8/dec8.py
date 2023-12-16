import sys
import math

def parseNodes(f):
    nodes = {}
    for nodeLine in f:
        nodeLineList = nodeLine.split('=')
        node = nodeLineList[0].strip()
        left = nodeLineList[1].split(',')[0][2:5]
        right = nodeLineList[1].split(',')[1][1:4]
        nodes[node] = (left, right)
    return nodes

def findStartingNodes(nodes, lastChar):
    retNodes = []
    for node in nodes.keys():
        if node[-1] == lastChar:
            retNodes.append(node)
    return retNodes

def allNodesOneStep(allNodes, currentNodes, index):
    newNodes = []
    for i in range(len(currentNodes)):
        newNodes.append(allNodes[currentNodes[i]][index])
    return newNodes

def checkIfWeStop(nodes):
    zCount = 0
    for i in range(len(nodes)):
        if (nodes[i][-1] == 'Z'):
            zCount += 1
    if (zCount == len(nodes)):
        return False
    else:
        if (zCount > 1):
            print(nodes)
        return True

# NOTE THIS IS NOT ACTUALLY SOLVED!
def pt2(filename):
    with open(filename, "r") as f:
        rlInstructions = f.readline().strip()
        f.readline()
        nodes = parseNodes(f)
        startingNodes = findStartingNodes(nodes,'A')
        print(startingNodes)
        endNode, instuctionOffset, period = findPeriod(startingNodes[0],nodes,rlInstructions)
        print("For position 0, find periodic endNode: " + endNode + " with period: " + str(period) + " and instruction offset: " + str(instructionOffset))
        return numSteps

def pt2Brute(filename):
    with open(filename, "r") as f:
        rlInstructions = f.readline().strip()
        f.readline()
        nodes = parseNodes(f)
        currentNodes = findStartingNodes(nodes, 'A')
        i = 0
        numSteps = 0
        while (checkIfWeStop(currentNodes)):
            if (i == len(rlInstructions)):
                i = 0
            if rlInstructions[i] == 'L':
                currentNodes = allNodesOneStep(nodes, currentNodes, 0)
            elif rlInstructions[i] == 'R':
                currentNodes = allNodesOneStep(nodes, currentNodes, 1)
            i += 1
            numSteps += 1
        return numSteps

def pt1(filename, start, end, targetK):
    with open(filename, "r") as f:
        rlInstructions = f.readline().strip()
        f.readline()
        nodes = parseNodes(f)
        currentNode = start
        i = 0
        k = 0
        numSteps = 0
        while (k < targetK):
            if (currentNode == end):
                print("start: " + start + "end: " + end + " numSteps: " + str(numSteps))
                if (currentNode[-1] == 'Z' and currentNode != end):
                    print("FOUND ANOTHER Z!! " + currentNode)
                k += 1
            if (i == len(rlInstructions)):
                #print ("resetting i, on " + currentNode)
                i = 0
            if rlInstructions[i] == 'L':
                currentNode = nodes[currentNode][0]
            elif rlInstructions[i] == 'R':
                currentNode = nodes[currentNode][1]
            i += 1
            numSteps += 1
        return numSteps

pos1 = pt1("input.txt", 'GSA', 'DXZ',2) - pt1("input.txt",'GSA','DXZ',1)
pos2 = pt1("input.txt", 'DLA', 'XJZ',2) - pt1("input.txt",'DLA','XJZ',1)
pos3 = pt1("input.txt", 'MLA', 'PXZ',2) - pt1("input.txt",'MLA','PXZ',1)
pos4 = pt1("input.txt", 'MQA', 'QLZ',2) - pt1("input.txt",'MQA','QLZ',1)
pos5 = pt1("input.txt", 'AAA', 'ZZZ',2) - pt1("input.txt",'AAA','ZZZ',1)
pos6 = pt1("input.txt", 'JGA', 'TFZ',2) - pt1("input.txt",'JGA','TFZ',1)
print (math.lcm(pos1,pos2,pos3,pos4,pos5,pos6))

