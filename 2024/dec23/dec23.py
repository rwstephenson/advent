import sys
from math import *
from collections import *
sys.path.append('../../lib')
from point import Point
from node import Node
from interval import Interval
from parsing import *
from aocd import get_data, submit
import networkx as nx

def findLoopLen3(target,n,dist,path):
    path.append(n.value)
    if n.value == target.value and dist == 0:
        return [path[0:-1]]
    elif dist == 0:
        return [None]
    else:
        res = []
        for c in n.children:
            res += list(filter(lambda r: r is not None,findLoopLen3(target,c,dist-1,path.copy())))
        return res

def getPassword(seq):
    seq.sort()
    res = ""
    for s in seq:
        res += s + ','
    return res[0:-1]

def buildGraph(lines):
    nodes = {}
    G = nx.Graph()
    for line in lines:
        nodesLine = line.split('-')
        nv1 = nodesLine[0].strip()
        nv2 = nodesLine[1].strip()
        if nv1 not in nodes and nv2 not in nodes:
            n1 = Node(nv1)
            nodes[nv1] = n1
            G.add_node(nv1)
            n2 = Node(nv2)
            nodes[nv2] = n2
            G.add_node(nv2)
            n1.children.append(n2)
            n2.children.append(n1)
        elif nv1 in nodes and nv2 not in nodes:
            n = Node(nv2)
            nodes[nv2] = n
            G.add_node(nv2)
            nodes[nv1].children.append(n)
            n.children.append(nodes[nv1])
        elif nv2 in nodes and nv1 not in nodes:
            n = Node(nv1)
            nodes[nv1] = n
            G.add_node(nv1)
            nodes[nv2].children.append(n)
            n.children.append(nodes[nv2])
        else:
            nodes[nv1].children.append(nodes[nv2])
            nodes[nv2].children.append(nodes[nv1])
        G.add_edge(nv1,nv2)
    return nodes,G

def solve(filename, pt):
    lines = parseLines(filename)
    nodes,G = buildGraph(lines)
    if pt == 1:
        nodesWithT = list(filter(lambda nv: nv[0] == 't',nodes.keys()))
        res = set()
        for nv in nodesWithT:
            n = nodes[nv]
            found = findLoopLen3(n,n,3,[])
            for seq in found:
                res.add(tuple(list(sorted(seq))))
        return len(res)
    elif pt == 2:
        cliques = nx.find_cliques(G)
        maxClique = []
        for c in cliques:
            if len(c) > len(maxClique):
                maxClique = c
        return getPassword(maxClique)


def run(pt,day,year,expect):
    with open("input.txt","w") as f:
        f.write(get_data(day=day,year=year))
    resTest = solve("testInput.txt",pt)
    assert resTest == expect, f"Result was {resTest}"
    res = solve("input.txt",pt)
    print("Test Input: {} Puzzle Input: {}".format(resTest,res))
    if pt == 1:
        c = "a"
    else:
        c = "b"
    submit(res, part=c, day=day, year=year)

run(1,23,2024,7)
run(2,23,2024,"co,de,ka,ta")
