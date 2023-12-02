testLine = "Game 1: 13 red, 18 green; 5 green, 3 red, 5 blue; 5 green, 9 red, 6 blue; 3 blue, 3 green"

def getGameId(line):
    return line.split(":")[0].split(" ")[1]

def getValidRounds(line, limitR, limitG, limitB):
    rounds = []
    gameId = int(getGameId(line))
    roundLines = line.split(":")[1].split(";")
    for rLine in roundLines:
        colours = rLine.split(",")
        for c in colours:
            colour = c.split(" ")[2].strip()
            num = int(c.split(" ")[1])
            if colour == "red" and num > limitR:
                print ("Rejecting round: " + str(gameId) + " because " + colour + " is too high: " + str(num))
                return 0
            elif colour == "green" and num > limitG:
                print ("Rejecting round: " + str(gameId) + " because " + colour + " is too high: " + str(num))
                return 0
            elif colour == "blue" and num > limitB:
                print ("Rejecting round: " + str(gameId) + " because " + colour + " is too high: " + str(num))
                return 0
    print(gameId)
    return gameId

def getRoundPower(line):
    rounds = []
    gameId = int(getGameId(line))
    roundLines = line.split(":")[1].split(";")
    maxR = 0
    maxB = 0
    maxG = 0
    for rLine in roundLines:
        colours = rLine.split(",")
        for c in colours:
            colour = c.split(" ")[2].strip()
            num = int(c.split(" ")[1])
            if colour == "red" and num > maxR:
                maxR = num
            elif colour == "green" and num > maxG:
                maxG = num
            elif colour == "blue" and num > maxB:
                maxB = num
    print("min set for  gameId: " + str(gameId) + " is (R: " + str(maxR) + ",G: " + str(maxG) + ",B: " + str(maxB) + ")")
    return maxR * maxG * maxB


def parseFilePt1(filename, limitR, limitG, limitB):
    with open(filename, "r") as f:
        sum = 0
        for line in f:
            sum += getValidRounds(line,limitR,limitG,limitB)
    return sum

def parseFilePt2(filename):
    with open(filename, "r") as f:
        sum = 0
        for line in f:
            sum += getRoundPower(line)
    return sum

print(parseFilePt2("input.txt"))

