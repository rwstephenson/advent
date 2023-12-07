
def getBonus(line):
    cardid = line.split(":")[0]
    input = line.split(":")[1].strip()
    winners = set(input.split("|")[0].strip().split(" "))
    cardStrings = input.split("|")[1].strip().split(" ")

    cardEntries = []
    numFound = 0
    for entry in cardStrings:
        if entry != '':
            e = entry
            if entry in winners:
                numFound += 1
    print ("Found " + str(numFound) + " matches for " + cardid)
    return numFound

def getRoundPoints(line):
    input = line.split(":")[1].strip()
    winners = set(input.split("|")[0].strip().split(" "))
    cardStrings = input.split("|")[1].strip().split(" ")

    cardEntries = []
    numFound = 0
    for entry in cardStrings:
        if entry != '':
            e = entry
            if entry in winners:
                numFound += 1
    if numFound > 0:
        return 2**(numFound - 1)
    else:
        return 0

def parseFile(filename):
    with open(filename, "r") as f:
        sum = 0
        for line in f:
            sum += getRoundPoints(line)
    return sum

bonusCards = {}

def incrementBonusCards(id, matches, numCards):
    newCards = 0
    if matches > 0:
        for i in range(matches):
            if id+i+1 not in bonusCards:
                bonusCards[id+i+1] = numCards
                print ("Adding " + str(numCards) + " new " + str(id+i+1) + " cards")
            else:
                bonusCards[id+i+1] = bonusCards[id+i+1] + numCards
            newCards += numCards
    print ("Had " + str(numCards) + " copies of card " + str(id) + ", increasing the next " + str(matches))
    return newCards

def parseFilePt2(filename):
    with open(filename, "r") as f:
        totalCards = 0
        row = 1
        id = 1
        for line in f:
            matches = getBonus(line)
            numCards = 1
            if id in bonusCards:
                numCards = bonusCards[id] + 1
            totalCards += numCards #adding original
            incrementBonusCards(id, matches, numCards)
            id += 1
    return totalCards

print(parseFilePt2("input.txt"))

