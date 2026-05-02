import reps.matrix
import reps.list
import reps.table
import utils
import math

def argGenerate(nodes, saturation):
    matrix = [[0] * (nodes + 1) for i in range(nodes + 1)]
    for i in range(1, nodes): # Wypelnienie nad przekątną po prawej zeby byl na pewno spojny
        matrix[i][i + 1] = 1
    maxEdgesAmount = nodes * (nodes - 1) // 2
    jedynkiLeftToPlace = round((saturation / 100) * maxEdgesAmount) - (nodes - 1)
    for i in range(1, nodes - 1): # Wypelnienie resztą jedynek jesli mozna
        if jedynkiLeftToPlace <= 0: break
        for j in range(2 + i, nodes + 1):
            if jedynkiLeftToPlace <= 0: break
            matrix[i][j] = 1
            jedynkiLeftToPlace -= 1
    utils.grafInMatrix = matrix

def argUserProvided(nodes):
    for i in range(1, nodes + 1):
        values = utils.inputs.validListOrEmpty(f"{i}> ", nodes).split()
        utils.grafInList.append(list(map(int, values)))

def create():
    return

def printM():
    return
