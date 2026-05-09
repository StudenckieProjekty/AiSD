import utils
import random
import math

def getMatrixFilledWithZeros(size):
    return [[0] * (size) for i in range(size)]

def Print():
    matrix = utils.graf
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

def setEdge(nodeId1, nodeId2, value):
    utils.graf[nodeId1][nodeId2] = value
    utils.graf[nodeId2][nodeId1] = value

def adjacent(nodeId1, nodeId2):
    matrix = utils.graf
    return matrix[nodeId1][nodeId2] == 1

def neighbors(nodeId):
    matrix = utils.graf
    nodes = utils.nodes
    listOfNeighbors = []
    for nodeId2 in range(1, nodes + 1):
        if matrix[nodeId][nodeId2] == 1:
            listOfNeighbors.append(nodeId2)
    return listOfNeighbors

def entryDegree(nodeId):
    matrix = utils.graf
    nodes = utils.nodes
    counter = 0
    for nodeId2 in range(1, nodes + 1):
        if matrix[nodeId2][nodeId] == 1: counter += 1
    return counter

def argGenerate(nodes, saturation, bHamilton):
    utils.graf = getMatrixFilledWithZeros(nodes + 1)
    nodesList = [i for i in range(2, nodes + 1)]
    random.shuffle(nodesList)
    nodesList = [1] + nodesList + [1]
    for i in range(len(nodesList) - 1): # Robienie cyklu Hamiltona od jedynki do jedynki przez random wierzcholki
        setEdge(nodesList[i], nodesList[i + 1], 1)
    edgesLeftToMake = math.ceil((nodes * (nodes - 1) / 2) * (saturation / 100)) - nodes
    attemptsCount = 0
    while edgesLeftToMake > 0 and attemptsCount < 69: # Dopelnianie grafu jesli trzeba
        theThreeLittleNodes = random.sample(range(1, nodes + 1), 3)
        bEdgeAlreadyExists = False
        edgesToAdd = []
        for i in range(3):
            for j in range(i + 1, 3):
                nodeId1, nodeId2 = [theThreeLittleNodes[i], theThreeLittleNodes[j]]
                if adjacent(nodeId1, nodeId2): bEdgeAlreadyExists = True
                else: edgesToAdd.append([nodeId1, nodeId2])
        if bEdgeAlreadyExists:
            attemptsCount += 1
            continue
        for nodeId1, nodeId2 in edgesToAdd: setEdge(nodeId1, nodeId2, 1)
        edgesLeftToMake -= 3
        attemptsCount = 0
    if not bHamilton:
        nodeId1 = random.randint(1, nodes)
        for nodeId2 in range(1, nodes + 1): setEdge(nodeId1, nodeId2, 0)

def export():
    nodes = utils.nodes
    radius = max(2.5, nodes * 0.6)
    tikz = "\\begin{tikzpicture}"
    for nodeId in range(1, nodes + 1):
        angle = round((nodeId - 1) * (360 / nodes), 2)
        tikz += f" \\node[circle, draw] ({nodeId}) at ({angle}:{radius:.2f}) {{{nodeId}}};"
    for nodeId1 in range(1, nodes + 1):
        neighborsList = neighbors(nodeId1)
        for nodeId2 in neighborsList:
            if not nodeId1 < nodeId2: continue
            tikz += f" \\draw ({nodeId1}) -- ({nodeId2});"
    tikz += " \\end{tikzpicture}"
    print(f"Exported graph:\n{tikz}")
