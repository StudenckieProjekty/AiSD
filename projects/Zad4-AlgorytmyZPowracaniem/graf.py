import utils
import random
import math
import copy

nodes = None
grafCopy = None
graf = None
initialNodeId = None

def getMatrixFilledWithZeros(size):
    return [[0] * (size) for i in range(size)]

def Print():
    print(f" {' ' * utils.getIntLength(nodes)}| ", end = "")
    for nodeId in range(1, nodes + 1):
        print(f"{nodeId}" + " " * (utils.getIntLength(nodes) - utils.getIntLength(nodeId)), end = " ")
    print(f"\n-{'-' * utils.getIntLength(nodes)}+", end = "")
    for nodeId in range(1, nodes + 1):
        print("-" * (utils.getIntLength(nodes) + 1), end = "")
    for nodeId1 in range(1, nodes + 1):
        print(f"\n{nodeId1} {' ' * (utils.getIntLength(nodes) - utils.getIntLength(nodeId1))}| ", end = "")
        for nodeId2 in range(1, nodes + 1):
            print(f"{graf[nodeId1][nodeId2]}", end = "")
            print(" " * (utils.getIntLength(nodes) - utils.getIntLength(graf[nodeId1][nodeId2]) + 1), end = "")
    print()

def makeGrafGreatAgain():
    global graf, grafCopy
    graf = copy.deepcopy(grafCopy)

def setEdge(nodeId1, nodeId2, value):
    graf[nodeId1][nodeId2] = value
    graf[nodeId2][nodeId1] = value

def adjacent(nodeId1, nodeId2):
    return graf[nodeId1][nodeId2] == 1

def neighbors(nodeId):
    listOfNeighbors = []
    for nodeId2 in range(1, nodes + 1):
        if graf[nodeId][nodeId2] == 1:
            listOfNeighbors.append(nodeId2)
    return listOfNeighbors

def entryDegree(nodeId):
    counter = 0
    for nodeId2 in range(1, nodes + 1):
        if graf[nodeId2][nodeId] == 1: counter += 1
    return counter

def argGenerate(nodesCount, saturation, bHamilton):
    global graf, grafCopy, nodes, initialNodeId
    nodes = nodesCount
    graf = getMatrixFilledWithZeros(nodes + 1)
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
    grafCopy = copy.deepcopy(graf)
    initialNodeId = next(nodeId for nodeId in range(1, nodes + 1) if neighbors(nodeId))

def robertsFloresAlg():
    nodesAndNeighbors = [[]] + [neighbors(nodeId) for nodeId in range(1, nodes + 1)]
    stack = [initialNodeId]
    def bVisitedAllNodes(): return len(stack) == nodes
    while stack:
        nodeId = stack[-1]
        if bVisitedAllNodes() and adjacent(nodeId, initialNodeId): 
            return stack + [1]
        bFoundNextNode = False
        while nodesAndNeighbors[nodeId]:
            nextNodeId = nodesAndNeighbors[nodeId].pop()
            if nextNodeId not in stack:
                stack.append(nextNodeId)
                bFoundNextNode = True
                break
        if not bFoundNextNode:
            poppedNodeId = stack.pop()
            nodesAndNeighbors[poppedNodeId] = neighbors(poppedNodeId)
    return []

eulerStack = []
def eulerDFS(nodeId1 = None, bStartingCall = True):
    global eulerStack, graf
    if not nodeId1:
        nodeId1 = initialNodeId
        eulerStack = []
    for nodeId2 in neighbors(nodeId1):
        if adjacent(nodeId1, nodeId2):
            setEdge(nodeId1, nodeId2, 0)
            eulerDFS(nodeId2, False)
    eulerStack.append(nodeId1)
    if bStartingCall:
        return eulerStack[::-1]

def export():
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
