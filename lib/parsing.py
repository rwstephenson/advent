import re

_integer_pattern = re.compile("-?[0-9]+")

def getInts(line):
    return [int(m) for m in _integer_pattern.findall(line)]

def findAll(string,substring):
    return [m.start() for m in re.finditer(re.escape(substring), string)]

def parseLines(filename):
    lines = []
    with open(filename,"r") as f:
        for line in f:
            lines.append(line.strip())
    return lines

