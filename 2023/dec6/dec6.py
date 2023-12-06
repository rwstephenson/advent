import sys

def getGamesPt1(f):
    timeline = list(filter(lambda x: x != '',f.readline().split(":")[1].strip().split(' ')))
    distline = list(filter(lambda x: x!= '',f.readline().split(":")[1].strip().split(' ')))
    assert(len(timeline) == len(distline))
    games = []
    for i in range(len(timeline)):
        games.append((timeline[i], distline[i]))
    return games

def getGamesPt2(f):
    timeline = list(filter(lambda x: x != '',f.readline().split(":")[1].strip().split(' ')))
    distline = list(filter(lambda x: x!= '',f.readline().split(":")[1].strip().split(' ')))
    gameTime = ""
    gameDistance = ""
    for i in range(len(timeline)):
        gameTime += timeline[i]
        gameDistance += distline[i]
    return (gameTime, gameDistance)

def getNumWinnersBrute(time, threshold):
    sum = 0
    for i in range(time):
        speed = i
        result = speed*(time-i)
        if result > threshold:
            sum += 1
    return sum

def getFirstWinner(time, threshold):
    sum = 0
    for i in range(time):
        speed = i
        result = speed*(time-i)
        if result > threshold:
            return i

def getLastWinner(time, threshold):
    sum = 0
    for i in range(time):
        speed = time - i
        result = speed*i
        if result > threshold:
            return time-i

def pt1(filename):
    with open(filename, "r") as f:
        games = getGames(f)
        print(games)
    result = 1
    for game in games:
        time = int(game[0])
        distThreshold = int(game[1])
        result *= getNumWinners(time, distThreshold)
    return result

def pt2Brute(filename):
    with open(filename, "r") as f:
        game = getGamesPt2(f)
        print(game)
    result = 1
    time = int(game[0])
    distThreshold = int(game[1])
    return getNumWinnersBrute(time, distThreshold)

def pt2(filename):
    with open(filename, "r") as f:
        game = getGamesPt2(f)
        print(game)
    result = 1
    time = int(game[0])
    distThreshold = int(game[1])
    first = getFirstWinner(time, distThreshold)
    last = getLastWinner(time, distThreshold)
    print ("First winner: " + str(first))
    print ("Last winner: " + str(last))
    return last-first + 1

print(pt2("input.txt"))

