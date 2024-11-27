def getValue(c):
    asci = ord(c)
    if asci >= 97:
        return asci % 96
    elif asci <= 90:
        return 26 + asci % 64

def solvePt1(filename):
    with open(filename, "r") as f:
        total = 0
        for line in f:
            rucksack = line.strip()
            midpoint = len(rucksack)//2
            assert(len(rucksack) % 2 == 0)
            comp1,comp2 = rucksack[0:midpoint],rucksack[midpoint:]
            assert(len(comp1) == len(comp2))
            found = False
            for c in comp1:
                if comp2.find(c) >= 0 and not found:
                    found = True
                    total += getValue(c)
        return total

def solvePt2(filename):
    with open(filename, "r") as f:
        total = 0
        i = 0
        lastSack = ""
        lastlastSack = ""
        for line in f:
            rucksack = line.strip()
            if i % 3 == 2:
                for c in rucksack:
                    if lastSack.find(c) >= 0 and lastlastSack.find(c) >= 0:
                        total += getValue(c)
                        break
            else:
                lastlastSack = lastSack
                lastSack = rucksack
            i += 1
        return total

print(solvePt2("input.txt"))

