
strIntDict = {
        "1":'1',
        "2":'2',
        "3":'3',
        "4":'4',
        "5":'5',
        "6":'6',
        "7":'7',
        "8":'8',
        "9":'9',
        "0":'0',
        "one":'1',
        "two":'2',
        "three":'3',
        "four":'4',
        "five":'5',
        "six":'6',
        "seven":'7',
        "eight":'8',
        "nine":'9',
        "zero":'0'
}

def solveDec1pt2(filename, validNumbSet):
    sum = 0
    with open(filename, "r") as f:
        for line in f:
            first_char = "0"
            last_char = "0"
            lowestIndex = 1000
            highestIndex = -1
            for entry in validNumbSet:
                idx = line.find(entry)
                ridx = line.rfind(entry)
                if idx != -1:
                    if idx < lowestIndex:
                        lowestIndex = idx
                        first_char = entry
                if ridx != -1:
                    if ridx > highestIndex:
                        highestIndex = ridx
                        last_char = entry
            number = int(strIntDict[first_char] + strIntDict[last_char])
            sum += number
    return sum

def solveDec1(filename, validNumbSet):
    sum = 0
    with open(filename, "r") as f:
        for line in f:
            first_char = 0
            last_char = 0
            for c in line:
                if c in validNumbSet:
                    first_char = int(c)
                    break
            for c in line[::-1]:
                if c in validNumbSet:
                    last_char = int(c)
                    break
            number = int(str(first_char) + str(last_char))
            sum += number
    return sum

validNumbersPt1 = ['1','2','3','4','5','6','7','8','9']
validNumbersPt2 = validNumbersPt1 + ["one","two","three","four","five","six","seven","eight","nine"]
#solveDec1("input.txt",validNumbersPt1)
print(solveDec1pt2("input.txt",validNumbersPt2))
