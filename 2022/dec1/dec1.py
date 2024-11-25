def solve(filename, numElves):
    with open(filename, "r") as f:
        elvesSnacks = []
        elfCalories = 0
        for line in f:
            calories = line.strip()
            if calories == "":
                elvesSnacks.append(elfCalories)
                elfCalories = 0
            else:
                elfCalories += int(calories)
    elvesSnacks.sort(reverse=True)
    sum = 0
    for i in range(numElves):
       sum += elvesSnacks[i]
    return sum

print(solve("input.txt",3))

