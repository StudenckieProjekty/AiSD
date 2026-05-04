import utils

def getMatrixFilledWithZeros(size):
    return [[0] * (size) for i in range(size)]

def convFromList(lista, nodes):
    matrix = getMatrixFilledWithZeros(nodes + 1)
    for nodeId1 in range(1, nodes + 1):
        for nodeId2 in lista[nodeId1]:
            matrix[nodeId1][nodeId2] = 1
    utils.grafIn["matrix"] = matrix
    return matrix

def convFromTable(table, nodes):
    matrix = getMatrixFilledWithZeros(nodes + 1)
    for nodeId1, nodeId2 in table:
        matrix[nodeId1][nodeId2] = 1
    utils.grafIn["matrix"] = matrix
    return matrix

def Print():
    matrix = utils.grafIn["matrix"]
    nodes = len(matrix) - 1
    print(f" {' ' * utils.getIntLength(nodes)}| ", end = "")
    for nodeId in range(1, nodes + 1):
        print(f"{nodeId}" + " " * (utils.getIntLength(nodes) - utils.getIntLength(nodeId)), end = " ")
    print(f"\n-{'-' * utils.getIntLength(nodes)}+", end = "")
    for nodeId in range(1, nodes + 1):
        print("-" * (utils.getIntLength(nodes) + 1), end = "")
    for nodeId1 in range(1, nodes + 1):
        print(f"\n{nodeId1} {' ' * (utils.getIntLength(nodes) - utils.getIntLength(nodeId1))}| ", end = "")
        for nodeId2 in range(1, nodes + 1):
            print(f"{matrix[nodeId1][nodeId2]}", end = "")
            print(" " * (utils.getIntLength(nodes) - utils.getIntLength(matrix[nodeId1][nodeId2]) + 1), end = "")
    print()

def adjacent(nodeId1, nodeId2):
    matrix = utils.grafIn["matrix"]
    return matrix[nodeId1][nodeId2] == 1

def neighbors(nodeId):
    matrix = utils.grafIn["matrix"]
    nodes = utils.nodes
    listOfNeighbors = []
    for nodeId2 in range(1, nodes + 1):
        if matrix[nodeId][nodeId2] == 1:
            listOfNeighbors.append(nodeId2)
    return listOfNeighbors
