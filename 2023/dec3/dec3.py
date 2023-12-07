possibleGears = {}

def calculateGearRatios(possibleGears):
    sum = 0
    for posGear in possibleGears:
        if len(possibleGears[posGear]) == 2:
            sum += possibleGears[posGear][0]*possibleGears[posGear][1]
    return sum

def checkGears(row,i,num):
    gearKey = str(row)+","+str(i)
    if (gearKey not in possibleGears):
        possibleGears[gearKey] = [num]
    else:
        possibleGears[gearKey].append(num)

def isSymbol(row,i,c, num):
    if c in digitSet:
        return False
    elif c == '*':
        checkGears(row,i,num)
        return True
    elif c == '.':
        return False
    elif c == '\n':
        return False
    else:
        return True

def checkHorizontal(schema, row, numStart, numEnd, num):
    isPart = False
    if numStart > 0 and isSymbol(row,numStart-1,schema[row][numStart - 1], num):
        print ("Found symbol: " + schema[row][numStart - 1])
        isPart = True
    if numEnd + 1 < len(schema[row]) and isSymbol(row,numEnd+1,schema[row][numEnd + 1], num):
        print ("Found symbol: " + schema[row][numEnd + 1])
        isePart = True
    return isPart

def checkVertical(schema, row, numStart, numEnd, num):
    isPart = False
    if row > 0:
        for i in range(numStart, numEnd+1):
            if isSymbol(row-1,i,schema[row-1][i], num):
                print ("Found symbol above: " + schema[row-1][i])
                isPart = True
    if row + 1 < len(schema):
        for i in range(numStart, numEnd+1):
            if isSymbol(row+1,i,schema[row+1][i], num):
                print ("Found symbol below: " + schema[row+1][i])
                isPart = True
    return isPart

def checkDiagonal(schema, row, numStart, numEnd, num):
    isPart = False
    if row > 0 and numStart > 0 and isSymbol(row-1,numStart-1,schema[row-1][numStart-1], num):
        print ("Found symbol diagonally! case 1")
        isPart = True
    if row > 0 and numEnd + 1 < len(schema[row]) and isSymbol(row-1,numEnd+1,schema[row-1][numEnd+1], num):
        print ("Found symbol diagonally! case 2")
        isPart = True
    if row + 1 < len(schema) and numStart > 0 and isSymbol(row+1,numStart-1,schema[row+1][numStart-1], num):
        print ("Found symbol diagonally! case 3")
        isPart = True
    if row + 1 < len(schema) and numEnd + 1 < len(schema[row]) and isSymbol(row+1,numEnd+1,schema[row+1][numEnd+1], num):
        print ("Found symbol diagonally! case 4")
        isPart = True
    return isPart

def checkForNearbySymbol(schema, row, numStart, numEnd, num):
    return checkHorizontal(schema, row, numStart, numEnd, num) or checkVertical(schema, row, numStart, numEnd, num) or checkDiagonal(schema, row, numStart, numEnd, num)

digitSet = {'0','1','2','3','4','5','6','7','8','9'}

def parseFilePt1(filename):
    schema = []
    with open(filename, "r") as f:
        for line in f:
            schema.append(line)
    sum = 0
    totalSum = 0
    sumIgnored = 0
    count = 0
    for l in range(len(schema)):
        print ("Line: " + str(l) + "-------------------------------------")
        lineLength = len(schema[l])
        numIdx = 0
        numEndIdx = 0
        numberString = ""
        c = 0
        while c < lineLength:
            if len(numberString) == 0:
                # not currently finding a number
                if schema[l][c] in digitSet:
                    # number found
                    numIdx = c
                    numberString = schema[l][c]
            else:
                if schema[l][c] in digitSet:
                    # still finding number
                    numberString = numberString + schema[l][c]
                else:
                    # end of number
                    numEndIdx = c - 1
                    print ("Found number: " + numberString)
                    totalSum += int(numberString)
                    if (checkForNearbySymbol(schema, l, numIdx, numEndIdx,int(numberString))):
                        sum += int(numberString)
                        count += 1
                        print("And the sum is: " + str(sum))
                    else:
                        print ("Number with NO symbol:" + numberString)
                        sumIgnored += int(numberString)
                    numberString = ""
                    numEndIdx = 0
                    numIdx = 0
            c = c + 1
    print("---------------")
    print("Count: " + str(count))
    print ("Total Sum: " + str(totalSum))
    print ("Sum Parts: " + str(sum))
    print ("Sum Ignored: " + str(sumIgnored))
    print ("Total - Ignored: " + str(totalSum - sumIgnored))

    print(calculateGearRatios(possibleGears))

parseFilePt1("input.txt")
