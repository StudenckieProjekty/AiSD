import utils

def createMatrixForDP(x, y):
    matrix = []
    for i in range(x + 1):
        row = [0] * (y + 1)
        matrix.append(row)
    return matrix

def bpDynamic(dataset):
    backpackCapacity = dataset["backpackCapacity"]
    itemsCount = dataset["itemsCount"]
    items = [[]] + dataset["items"] # Make item IDs start from 1 here
    matrix = createMatrixForDP(itemsCount, backpackCapacity)
    for i in range(1, itemsCount + 1):
        for j in range(1, backpackCapacity + 1):
            if items[i]["weight"] > j:
                matrix[i][j] = matrix[i - 1][j]
            else:
                matrix[i][j] = max(matrix[i - 1][j], matrix[i - 1][j - items[i]["weight"]] + items[i]["value"])
    result = 0
    i, j = [itemsCount, backpackCapacity]
    while i > 0:
        if matrix[i][j] > matrix[i - 1][j]:
            result = result | (1 << (i - 1))
            j -= items[i]["weight"]
        i -= 1
    return result

def bpBruteForce(dataset):
    backpackCapacity = dataset["backpackCapacity"]
    itemsCount = dataset["itemsCount"]
    items = dataset["items"]
    bestComboI = 0
    bestComboValue = 0
    for i in range(1, 2 ** itemsCount):
        weightSum = 0
        valueSum = 0
        for j in range(0, itemsCount):
            if ((i >> j) & 1) == 1:
                weightSum += items[j]["weight"]
                valueSum += items[j]["value"]
        if valueSum > bestComboValue and weightSum <= backpackCapacity:
            bestComboI = i
            bestComboValue = valueSum
    return bestComboI
