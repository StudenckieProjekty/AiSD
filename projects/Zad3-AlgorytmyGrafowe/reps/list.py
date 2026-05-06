import utils

def getEmptyListOfLists(size):
    return [[] for i in range(size)]

def convFromMatrix(matrix, nodes):
    lista = getEmptyListOfLists(nodes + 1)
    for nodeId1 in range(1, nodes + 1):
        for nodeId2 in range(1, nodes + 1):
            if matrix[nodeId1][nodeId2] == 1:
                lista[nodeId1].append(nodeId2)
    utils.grafIn["list"] = lista
    return lista

def convFromTable(table, nodes):
    lista = getEmptyListOfLists(nodes + 1)
    for nodeId1, nodeId2 in table:
        lista[nodeId1].append(nodeId2)
    utils.grafIn["list"] = lista
    return lista

def Print():
    lista = utils.grafIn["list"]
    nodes = len(lista) - 1
    for nodeId1 in range(1, nodes + 1):
        print(f"{nodeId1}", end = "")
        for nodeId2 in lista[nodeId1]:
            print(f" -> {nodeId2}", end = "")
        print()

def adjacent(nodeId1, nodeId2):
    lista = utils.grafIn["list"]
    return nodeId2 in lista[nodeId1]

def neighbors(nodeId):
    lista = utils.grafIn["list"]
    return lista[nodeId]

def entryDegree(nodeId):
    lista = utils.grafIn["list"]
    nodes = len(lista) - 1
    counter = 0
    for nodeId2 in range(1, nodes + 1):
        if nodeId in lista[nodeId2]: counter += 1
    return counter
