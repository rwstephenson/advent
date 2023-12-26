import sys
import math
from functools import cache
import queue

totalLow = 0
totalHigh = 0

modules = {}
pulseQ = queue.Queue()

class BroadcasterModule:
    dests = []
    name = ""

    def __init__(self,name,dests):
        self.dests = dests
        self.name = name

    def sendPulse(self, isHigh):
        global pulseQ
        global totalLow
        global totalHigh
        global modules
        for dest in self.dests:
            pulseQ.put((self.name, dest, isHigh))
            #print ("---------------------------Enqueuing (" + self.name + "," + dest + "," + str(isHigh) +")")
            if isHigh:
                totalHigh += 1
            else:
                totalLow += 1

    def receivePulse(self, source, isHigh):
        self.sendPulse(isHigh)

class FlipFlop (BroadcasterModule):
    state = False

    def __init__(self, name, dests):
        self.state = False
        self.name = name
        self.dests = dests

    def receivePulse(self, source, isHigh):
        if not isHigh:
            self.state = not self.state
            self.sendPulse(self.state)

class Conjunct (BroadcasterModule):
    inputStates = None

    def __init__(self, name, dests):
        self.name = name
        self.dests = dests
        self.inputStates = {}

    def receivePulse(self, fromName, isHigh):
        self.inputStates[fromName] = isHigh
        for i in self.inputStates.keys():
            if not self.inputStates[i]:
                self.sendPulse(True)
                return
        self.sendPulse(False)


def parseFile(f):
    global modules
    conjuncts = {}
    for line in f:
        moduleStr = line.split('-')[0].strip()
        dests = list(map(lambda x: x.strip(),line.split('-')[1][1:].split(',')))
        print (dests)
        if moduleStr[0] == '%':
            name = moduleStr[1:]
            modules[name] = FlipFlop(name, dests)
        elif moduleStr[0] == '&':
            name = moduleStr[1:]
            modules[name] = Conjunct(name, dests)
            conjuncts[name] = modules[name]
        elif moduleStr == "broadcaster":
            modules[moduleStr] = BroadcasterModule(moduleStr, dests)
        else:
            assert(False)

    #initiailise conjucts to false
    for conjunct in conjuncts.keys():
        for module in modules.keys():
            for dest in modules[module].dests:
                if dest == conjunct:
                    modules[conjunct].inputStates[module] = False

def pushButton(times, src, finalDest):
    global pulseQ
    global modules
    global totalLow
    global lastSeenHigh

    for i in range(times):
        pulseQ.put(("broadcaster",src,False))
        totalLow += 1
        while not pulseQ.empty():
            source,dest,isHigh = pulseQ.get()
            #print ("Sending (" + source + "," + dest + "," + str(isHigh) +")")
            if dest == finalDest:
                if isHigh:
                    print(source + " sent high pulse to dd. i = " + str(i))
                    print(modules['dd'].inputStates)
                modules[dest].receivePulse(source, isHigh)
            elif dest not in modules:
                pass
                #print("Sent to dev/null")
            else:
                modules[dest].receivePulse(source, isHigh)

def pt1(filename):
    with open(filename, "r") as f:
        global totalHigh
        global totalLow
        parseFile(f)
        pushButton(1000,"broadcaster",None)
        print("Total High: " + str(totalHigh))
        print("Total Low: " + str(totalLow))
        return totalHigh * totalLow

def pt2(filename, src, finalDest):
    with open(filename, "r") as f:
        parseFile(f)
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx Source: " + src + " Dest: " + finalDest)
        pushButton(100000,src,finalDest)

#print(pt1("input.txt"))
print(pt2("input.txt","cz", "dd"))
print(pt2("input.txt","gm", "dd"))
print(pt2("input.txt","jn", "dd"))
print(pt2("input.txt","ts", "dd"))


