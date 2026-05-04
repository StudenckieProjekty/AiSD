import reps.matrix
import reps.list
import reps.table
import utils
import random

convFromTo = {
    "matrix": {
        "list": reps.list.convFromMatrix,
        "table": reps.table.convFromMatrix
    },
    "list": {
        "matrix": reps.matrix.convFromList,
        "table": reps.table.convFromList
    },
    "table": {
        "matrix": reps.matrix.convFromTable,
        "list": reps.list.convFromTable
    }
}

def argGenerate(nodes, saturation):
    matrix = reps.matrix.getMatrixFilledWithZeros(nodes + 1)
    for i in range(1, nodes): # Wypelnienie nad przekątną po prawej zeby byl na pewno spojny
        matrix[i][i + 1] = 1
    maxEdgesAmount = nodes * (nodes - 1) // 2
    jedynkiLeftToPlace = round((saturation / 100) * maxEdgesAmount) - (nodes - 1)
    allowedCoordinates = [] # Kandydaci koordynatowi zeby do nich jedynke dac
    for i in range(1, nodes - 1):
        for j in range(2 + i, nodes + 1):
            allowedCoordinates.append([i, j])
    if jedynkiLeftToPlace > 0:
        for i, j in random.sample(allowedCoordinates, jedynkiLeftToPlace):
            matrix[i][j] = 1
    if utils.selectedRep == "matrix": utils.grafIn["matrix"] = matrix
    else: convFromTo["matrix"][utils.selectedRep](matrix, utils.nodes)

def argUserProvided(nodes):
    lista = [[]]
    for i in range(1, nodes + 1):
        values = utils.inputs.validListOrEmpty(f"{i}> ", nodes).split()
        lista.append(list(map(int, values)))
    if utils.selectedRep == "list": utils.grafIn["list"] = lista
    else: convFromTo["list"][utils.selectedRep](lista, utils.nodes)

actionsJson = {
    "print": {
        "matrix": reps.matrix.Print,
        "list": reps.list.Print,
        "table": reps.table.Print
    }
}

def Print():
    actionsJson["print"][utils.selectedRep]()
