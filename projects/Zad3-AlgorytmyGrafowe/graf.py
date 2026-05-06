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
    connected = [1]
    for i in range(2, nodes + 1): # Generowanie spojnego grafu takiego zeby nie byl "sznurkiem" od 1 do n
        parent = random.choice(connected)
        matrix[parent][i] = 1
        connected.append(i)
    maxEdgesAmount = nodes * (nodes - 1) // 2
    jedynkiLeftToPlace = round((saturation / 100) * maxEdgesAmount) - (nodes - 1)
    allowedCoordinates = [] # Kandydaci koordynatowi zeby do nich jedynke dac
    for i in range(1, nodes):
        for j in range(1 + i, nodes + 1):
            if matrix[i][j] == 0: allowedCoordinates.append([i, j])
    if jedynkiLeftToPlace > 0:
        for i, j in random.sample(allowedCoordinates, min(jedynkiLeftToPlace, len(allowedCoordinates))):
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
    },
    "entryDegree": {
        "matrix": reps.matrix.entryDegree,
        "list": reps.list.entryDegree,
        "table": reps.table.entryDegree
    }
}

def Print(): actionsJson["print"][utils.selectedRep]()
def adjacent(nodeId1, nodeId2): return actionsJson["adjacent"][utils.selectedRep](nodeId1, nodeId2)
def neighbors(nodeId): return actionsJson["neighbors"][utils.selectedRep](nodeId)
def entryDegree(nodeId): return actionsJson["entryDegree"][utils.selectedRep](nodeId)

def find():
    nodeId1 = utils.inputs.validPositiveNumber("from> ", 1, utils.nodes)
    nodeId2 = utils.inputs.validPositiveNumber("  to> ", 1, utils.nodes)
    if actionsJson["adjacent"][utils.selectedRep](nodeId1, nodeId2):
        print(f"True: edge ({nodeId1}, {nodeId2}) exists in the graph.")
    else: print(f"False: edge ({nodeId1}, {nodeId2}) does NOT exist in the graph.")

def BFS():
    output = []
    bVisited = [0, 1] + [0] * (utils.nodes - 1)
    styrta = [1]
    while styrta:
        nodeId1 = styrta.pop(0)
        output.append(f"{nodeId1}")
        for nodeId2 in neighbors(nodeId1):
            if not bVisited[nodeId2]:
                bVisited[nodeId2] = 1
                styrta.append(nodeId2)
    print(" ".join(output))

def DFSmain(nodeId, bVisited, output, bTarjan = False):
    bVisited[nodeId] = 1
    if not bTarjan: output.append(f"{nodeId}")
    for nodeId2 in neighbors(nodeId):
        if not bVisited[nodeId2]:
            DFSmain(nodeId2, bVisited, output, bTarjan)
    if bTarjan: output.append(f"{nodeId}")
    return

def DFS(bTarjan = False):
    bVisited = [0] * (utils.nodes + 1)
    output = []
    for nodeId in range(1, utils.nodes + 1):
        if not bVisited[nodeId]: DFSmain(nodeId, bVisited, output, bTarjan)
    if not bTarjan: print(" ".join(output))
    else: return output

def kahnSort():
    kahn = []
    entryDegrees = [-1] + [entryDegree(nodeId) for nodeId in range(1, utils.nodes + 1)]
    nodesLeftToProcess = [nodeId for nodeId in range(1, utils.nodes + 1) if entryDegrees[nodeId] == 0]
    while nodesLeftToProcess:
        nodeId = nodesLeftToProcess.pop(0)
        kahn.append(f"{nodeId}")
        for nodeId2 in neighbors(nodeId):
            entryDegrees[nodeId2] -= 1
            if entryDegrees[nodeId2] == 0:
                nodesLeftToProcess.append(nodeId2)
    print(" ".join(kahn))

def tarjanSort():
    output = DFS(bTarjan = True)[::-1]
    print(" ".join(output))

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
        angle = round((nodeId - 1) * (360 / nodes), 2)
        tikz += f" \\node[circle, draw] ({nodeId}) at ({angle}:{radius:.2f}) {{{nodeId}}};"
    for nodeId1 in range(1, nodes + 1):
        neighbors = actionsJson["neighbors"][utils.selectedRep](nodeId1)
        for nodeId2 in neighbors:
            tikz += f" \\draw[->] ({nodeId1}) -- ({nodeId2});"
    tikz += " \\end{tikzpicture}"
    print(f"Exported graph:\n{tikz}")
