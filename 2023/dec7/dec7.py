import sys

def getGroupStrength(groupings, withJokers):
    numJokers = 0
    if withJokers:
        numJokers = groupings.pop('J',0)
    cardCounts = list(groupings.values())
    most = numJokers
    secondMost = 1
    for count in cardCounts:
        if count+numJokers > most:
            most = count+numJokers
        elif count > secondMost:
            secondMost = count
    if most == 5:
        return 7
    elif most == 4:
        return 6
    elif most == 3 and len(cardCounts) == 2:
        return 5
    elif most == 3:
        return 4
    elif most == 2 and secondMost == 2:
        return 3
    elif most == 2:
        return 2
    else:
        return 1

def getHandStrength(handLine, withJokers):
    groupings = {}
    for c in handLine:
        if c in groupings:
            groupings[c] = groupings[c]+1
        else:
            groupings[c] = 1
    return getGroupStrength(groupings, withJokers)

def getTieBreakStr(handLine, withJokers):
    str = ""
    for c in handLine:
        if c >= '1' and c <= '9':
            str+=c
        elif c == 'T':
            str +='a'
        elif c == 'J':
            if withJokers:
                str += '0'
            else:
                str += 'b'
        elif c == 'Q':
            str += 'c'
        elif c == 'K':
            str += 'd'
        elif c == 'A':
            str += 'e'
    return str

def getHand(line, withJokers):
    bid = line.split(' ')[1].strip()
    handLine = line.split(' ')[0]
    handStrength = getHandStrength(handLine, withJokers)
    tiebreaker = int(str(handStrength) + getTieBreakStr(handLine, withJokers),16)
    return tiebreaker, int(bid), handLine

def getHands(f, withJokers):
    hands = []
    for line in f:
        hands.append(getHand(line.strip(), withJokers))
    hands.sort(key=lambda x: x[0])
    return hands

def pt1(filename, withJokers):
    with open(filename, "r") as f:
        hands = getHands(f, withJokers)
        sum = 0
        current = '0'
        for i in range(len(hands)):
            if current != str(hex(hands[i][0]))[2]:
                current = str(hex(hands[i][0]))[2]
                print ("------------------------------------ Current Category: " + current)

            print("Hand: " + hands[i][2] + ", tiebreaker: " + hex(hands[i][0]) + ", rank: " + str(i+1) + " bid: " + str(hands[i][1]))

            sum += hands[i][1] * (i+1)
        return sum

print(pt1("input.txt", True))

