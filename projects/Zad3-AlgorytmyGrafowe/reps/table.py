import utils

def convFromMatrix(matrix, nodes):
    table = []
    for nodeId1 in range(1, nodes + 1):
        for nodeId2 in range(1, nodes + 1):
            if matrix[nodeId1][nodeId2] != 1: continue
            table.append([nodeId1, nodeId2])
    utils.grafIn["table"] = table
    return table

def convFromList(lista, nodes):
    table = []
    for nodeId1 in range(1, nodes + 1):
        for nodeId2 in lista[nodeId1]:
            table.append([nodeId1, nodeId2])
    utils.grafIn["table"] = table
    return table

def Print():
    table = utils.grafIn["table"]
    counter = 1
    for nodeId1, nodeId2 in table:
        print(f"({nodeId1}, {nodeId2})", end = "\n" if counter % 4 == 0 else " ")
        counter += 1

def adjacent(nodeId1, nodeId2):
    table = utils.grafIn["table"]
    return [nodeId1, nodeId2] in table

def neighbors(nodeId):
    table = utils.grafIn["table"]
    listOfNeighbors = []
    for edge in table:
        if edge[0] == nodeId:
            listOfNeighbors.append(edge[1])
    return listOfNeighbors
