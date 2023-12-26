import sys
import math
import graphviz
from functools import cache
sys.setrecursionlimit(10000)

dot = graphviz.Graph('myGraph')
dot.graph_attr['layout'] = 'neato'

class Node():
    nid = ""
    neighboors = []

    def __init__(self, nid, neighboors):
        self.nid = nid
        self.neighboors = neighboors

def parseFile(f):
    global dot
    nodes = {}
    edges = []
    for line in f:
        nid = line.split(':')[0]
        neighboors = line.split(':')[1].strip().split(' ')
        if nid not in nodes:
            node = Node(nid,neighboors)
            dot.node(nid)
            nodes[nid] = node
        else:
            node = nodes[nid]
            node.neighboors += neighboors
        for dest in node.neighboors:
            if dest not in nodes:
                print("Adding node: " + dest + " with only node " + nid + " as neighboor")
                newDest = Node(dest,[nid])
                dot.node(dest,dest)
                nodes[dest] = newDest
                print(nodes[dest].neighboors)
            else:
                if nid not in nodes[dest].neighboors:
                    print("Adding node: " + nid + " to neighboors for " + dest)
                    nodes[dest].neighboors.append(nid)
                    print(nodes[dest].neighboors)
        for dest in neighboors:
            dot.edge(node.nid,dest,node.nid + "," + dest)
            edges.append((node.nid,dest))
    dot.render('my-graph.gv', format='png', view=True)
    return nodes, edges

def getConnectedSize(nid, cutSet, nodes, visited):
    node = nodes[nid]
    visited.add(node.nid)
    size = 1
    for n in node.neighboors:
        inCutSet = False
        for edge in cutSet:
            if (node.nid == edge[0] and n == edge[1]) or (node.nid == edge[1] and n == edge[0]):
                print("Edge is in the cutset, skip")
                # This edge is in the cutset, don't traverse
                inCutSet = True
        if n not in visited and not inCutSet:
            size += getConnectedSize(nodes[n].nid,cutSet,nodes,visited)
    return size

def isCutSet(nodes, cutSet):
    subGraph0Len = getConnectedSize(cutSet[0][0], cutSet, nodes, set())
    if subGraph0Len == len(nodes):
        print("Not a cutset")
        return [subGraph0Len]
    else:
        print("xxFound a cutSet, node: " + cutSet[0][0] + " was disconnected! Checking other side: " + cutSet[0][1])
        return [subGraph0Len,getConnectedSize(cutSet[0][1],cutSet,nodes,set())]

def isCutVertex(nodes,cutVertex):
    subGraph0Len = getConnectedSizeCutVertex(nodes[cutVertex].neighboors[0],cutVertex,nodes,set())
    if subGraph0Len == len(nodes)-1:
        return [subGraph0Len]
    elif len(nodes[cutVertex].neighboors) > 4:
        return [subGraph0Len]
    elif len(nodes[cutVertex].neighboors) < 4:
        return [subGraph0Len]
    else:
        subGraph1Len = getConnectedSizeCutVertex(nodes[cutVertex].neighboors[1],cutVertex,nodes,set())
        subGraph2Len = getConnectedSizeCutVertex(nodes[cutVertex].neighboors[2],cutVertex,nodes,set())
        subGraph3Len = getConnectedSizeCutVertex(nodes[cutVertex].neighboors[3],cutVertex,nodes,set())
        if subGraph0Len == subGraph1Len and subGraph0Len == subGraph2Len:
            return [subGraph0Len+1, subGraph3Len]
        elif subGraph0Len == subGraph1Len and subGraph0Len == subGraph3Len:
            return [subGraph0Len+1, subgraph2Len]
        else:
            return [subGraph0Len+1, subgraph1Len]

def getConnectedSizeCutVertex(nid, cutVertex, nodes, visited):
    node = nodes[nid]
    visited.add(node.nid)
    size = 1
    for n in node.neighboors:
        if n == cutVertex:
            pass
        elif n not in visited:
            size += getConnectedSizeCutVertex(nodes[n].nid,cutVertex,nodes,visited)
    return size

def findDisconnectedSubgraphsCutVertex(nodes, edges):
    for node in nodes.keys():
        subgraphs = isCutVertex(nodes, node)
        if len(subgraphs) == 2:
            return subgraphs[0],subgraphs[1]
    print("Found no cut vertex with cardinality 4")
    return 0,0

def getCutSetCandidates(nodes, edges):
    cutSetCandidates = []
    for i in range(0,len(edges)):
        for j in range(i,len(edges)):
            for k in range(j,len(edges)):
                if i != j and j != k and i != k:
                    cutSetCandidates.append([edges[i],edges[j],edges[k]])
    return cutSetCandidates


def findDisconnectedSubgraphs(nodes, edges):
    cutSetCandidates = [[('vkb','jzj'),('hhx','vrx'),('grh','nvh')]] #getCutSetCandidates(nodes,edges)
    for cutSet in cutSetCandidates:
        print("Checking new cutset")
        subgraphs = isCutSet(nodes, cutSet)
        if len(subgraphs) == 2:
            print("Found a cutset!")
            return subgraphs[0],subgraphs[1]
    print("Found no cutset")
    return 0,0


def pt1(filename,start):
    with open(filename, "r") as f:
        nodes,edges = parseFile(f)
        graphSize = len(nodes)

        # This asserts that everything is connected
        #for node in nodes.keys():
        #    assert(graphSize == getConnectedSize(node,("xxROB","xyROB"),nodes,set()))
        totalNeighboors = 0
        nodesWith4 = 0
        for node in nodes:
            totalNeighboors += len(nodes[node].neighboors)
            if len(nodes[node].neighboors) == 4:
                nodesWith4 += 1
            print("Node : " + node + " has neighboors:")
            print(nodes[node].neighboors)
        print(str(nodesWith4) + " nodes with 4 neighboors")
        print("Total Neighboors: " + str(totalNeighboors))
        print("Edges: " + str(len(edges)))
        assert(totalNeighboors == len(edges) * 2)
        subgraphs = findDisconnectedSubgraphs(nodes, edges)
        total = 0
        result = 1
        for sub in subgraphs:
            total += sub
            result *= sub
        assert(total == len(nodes))
        return result

#assert(pt1("testInput.txt",'ntq') == 54)
print(pt1("input.txt",'ntq'))


