import reps.matrix
import reps.list
import reps.table
import utils
import random
import math

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
    },
    "adjacent": {
        "matrix": reps.matrix.adjacent,
        "list": reps.list.adjacent,
        "table": reps.table.adjacent
    },
    "neighbors": {
        "matrix": reps.matrix.neighbors,
        "list": reps.list.neighbors,
        "table": reps.table.neighbors
    }
}

def Print():
    actionsJson["print"][utils.selectedRep]()

def find():
    nodeId1 = utils.inputs.validPositiveNumber("from> ", 1, utils.nodes)
    nodeId2 = utils.inputs.validPositiveNumber("  to> ", 1, utils.nodes)
    if actionsJson["adjacent"][utils.selectedRep](nodeId1, nodeId2):
        print(f"True: edge ({nodeId1}, {nodeId2}) exists in the graph.")
    else: print(f"False: edge ({nodeId1}, {nodeId2}) does NOT exist in the graph.")

def BFS():
    return

def changeRep():
    allowedValues = list(convFromTo[utils.selectedRep].keys())
    print(f"You can change the graph representation to: {' or '.join(allowedValues)}")
    oldRep = utils.selectedRep
    utils.selectedRep = utils.inputs.validInList(allowedValues, "type> ", f"Invalid type! Expected: {' or '.join(allowedValues)}")
    convFromTo[oldRep][utils.selectedRep](utils.grafIn[oldRep], utils.nodes)

def export():
    nodes = utils.nodes
    radius = max(2.5, nodes * 0.6)
    tikz = "\\begin{tikzpicture}[>=stealth]"
    for nodeId in range(1, nodes + 1):
        angle = (nodeId - 1) * (360 / nodes)
        tikz += f" \\node[circle, draw] ({nodeId}) at ({angle}:{radius:.2f}) {{{nodeId}}};"
    for nodeId1 in range(1, nodes + 1):
        neighbors = actionsJson["neighbors"][utils.selectedRep](nodeId1)
        for nodeId2 in neighbors:
            tikz += f" \\draw[->] ({nodeId1}) -- ({nodeId2});"
    tikz += " \\end{tikzpicture}"
    print(f"Exported graph:\n{tikz}")
