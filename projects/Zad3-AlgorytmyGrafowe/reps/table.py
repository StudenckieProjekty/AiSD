import utils

def convFromMatrix(matrix, nodes):
    table = set()
    for nodeId1 in range(1, nodes + 1):
        for nodeId2 in range(1, nodes + 1):
            if matrix[nodeId1][nodeId2] != 1: continue
            table.add((nodeId1, nodeId2))
    table = list(table)
    utils.grafIn["table"] = table
    return table

def convFromList(lista, nodes):
    table = set()
    for nodeId1 in range(1, nodes + 1):
        for nodeId2 in lista[nodeId1]:
            table.add((nodeId1, nodeId2))
    table = list(table)
    utils.grafIn["table"] = table
    return table

def Print():
    table = utils.grafIn["table"]
    for nodeId1, nodeId2 in table:
        print(f"{nodeId1} -> {nodeId2}")
    print()
