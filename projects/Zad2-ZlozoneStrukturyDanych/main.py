import math
import sys
import time
sys.setrecursionlimit(2500000)

class globalVars:
    treeType = None
    nodesCount = 0
    initialTreeList = []
    treeJson = {}
    bBenchmarkMode = False

def exitProgram(statusCode = 0, message = ""):
    print(f"\n{f'{message}\n' if message else ''}Program exited with status: {statusCode}")
    sys.exit()

def safeInput(string = ""):
    try: whatToDo = input(string)
    except EOFError: exitProgram()
    return whatToDo

def validInputType(expectedType = None, inputMessage = None):
    if inputMessage: print(inputMessage, end = "")
    whatToDo = safeInput()
    if expectedType == "intpos":
        while (not whatToDo.isdecimal()) or not (int(whatToDo) > 0):
            print("A positive integer is expected here. Try again")
            if inputMessage: print(inputMessage, end = "")
            whatToDo = safeInput()
    if expectedType == "list":
        bIsAllGood = False
        while not bIsAllGood:
            bIsAllGood = True
            for liczba in whatToDo.split():
                liczba = liczba.replace("-", "")
                if not liczba.isdecimal():
                    bIsAllGood = False
                    break
            if not bIsAllGood:
                print("A space seperated integer list is expected here. Try again")
                if inputMessage: print(inputMessage, end = "")
                whatToDo = safeInput()
    return whatToDo

def callFunction(funcName):
    if globalVars.bBenchmarkMode and commandsJson[funcName]["bBenchmark"]:
        startTime = time.perf_counter()
        commandsJson[funcName]["function"]()
        endTime = time.perf_counter()
        execTime = endTime - startTime
        print(f"\n{commandsJson[funcName]['displayName']} benchmarked time: ({execTime:.6f} s)")
    else: commandsJson[funcName]["function"]()

class sortowator: # wziete prosto z Zad1
    def sortowaniePrzezWstawianie(tablica, indexPoczatku = 0, przyrost = 1): 
        for i in range(indexPoczatku + przyrost, len(tablica), przyrost):
            wartoscPodI = tablica[i]
            j = i - przyrost
            while j >= indexPoczatku and tablica[j] > wartoscPodI:
                tablica[j + przyrost] = tablica[j]
                j -= przyrost
            tablica[j + przyrost] = wartoscPodI
        return tablica
    
    def getListaPrzyrostowShella(tablica):
        przyrosty = [1]
        for k in range(len(tablica)):
            przyrost = 4 ** (k + 1) + 3 * (2 ** k) + 1
            if przyrost > len(tablica) / 2: break
            przyrosty.append(przyrost)
        return przyrosty

    def sortowanieShella(tablica):
        przyrostyShella = sortowator.getListaPrzyrostowShella(tablica)
        for i in range(len(przyrostyShella) - 1, -1, -1):
            przyrost = przyrostyShella[i]
            for j in range(przyrost):
                sortowator.sortowaniePrzezWstawianie(tablica, j, przyrost)
        return tablica

class tree:
    def createAVL(lista, i = None, j = None, parentId = None, direction = None):
        if i == j == None:
            lista = sortowator.sortowanieShella(lista)
            i, j = [0, len(lista) - 1]
        elif j - i < 0: return
        indexMediany = (i + j) // 2
        if parentId and direction:
            globalVars.treeJson[parentId][direction] = lista[indexMediany]
        if not lista[indexMediany] in globalVars.treeJson:
            globalVars.treeJson[lista[indexMediany]] = {
                "left": None,
                "right": None,
                "parent": parentId
            }
        tree.createAVL(lista, i, indexMediany - 1, lista[indexMediany], "left")
        tree.createAVL(lista, indexMediany + 1, j, lista[indexMediany], "right")
    
    def createBST(lista):
        for i in range(len(lista)):
            if not lista[i] in globalVars.treeJson:
                globalVars.treeJson[lista[i]] = {
                    "left": None,
                    "right": None,
                    "parent": None
                }
            poprzedniParent = lista[0]
            while i != 0:
                if lista[i] < poprzedniParent:
                    if not globalVars.treeJson[poprzedniParent]["left"]:
                        globalVars.treeJson[poprzedniParent]["left"] = lista[i]
                        globalVars.treeJson[lista[i]]["parent"] = poprzedniParent
                        break
                    poprzedniParent = globalVars.treeJson[poprzedniParent]["left"]
                else:
                    if not globalVars.treeJson[poprzedniParent]["right"]:
                        globalVars.treeJson[poprzedniParent]["right"] = lista[i]
                        globalVars.treeJson[lista[i]]["parent"] = poprzedniParent
                        break
                    poprzedniParent = globalVars.treeJson[poprzedniParent]["right"]
    
    def create():
        if globalVars.treeType == "avl": tree.createAVL(globalVars.initialTreeList)
        else: tree.createBST(globalVars.initialTreeList)

    def getRoot():
        return next(i for i in globalVars.treeJson if globalVars.treeJson[i]["parent"] is None)

    def findMinMax(korzen = None):
        values = {
            "min": {
                "direction": "left",
                "value": None
            },
            "max": {
                "direction": "right",
                "value": None
            }
        }
        if not korzen: korzen = tree.getRoot()
        for extremumType in values:
            currentNode = korzen
            values[extremumType]["value"] = currentNode
            while globalVars.treeJson[currentNode][values[extremumType]["direction"]]:
                currentNode = globalVars.treeJson[currentNode][values[extremumType]["direction"]]
                values[extremumType]["value"] = currentNode
        print(f"Min: {values['min']['value']}\nMax: {values['max']['value']}")
        return values

    def printPreOrder(currentNode = None):
        if currentNode is None:
            currentNode = tree.getRoot()
            print(f" Pre-order: {currentNode}", end = "")
        else: print(f", {currentNode}", end = "")
        for direction in ["left", "right"]:
            if globalVars.treeJson[currentNode][direction]:
                tree.printPreOrder(globalVars.treeJson[currentNode][direction])  
    
    bFirstInOrderPrint = True
    def printInOrder(currentNode = None):
        if currentNode is None:
            currentNode = tree.getRoot()
            print(f"  In-order:", end = "")
        for direction in ["left", "right"]:
            if globalVars.treeJson[currentNode][direction]:
                tree.printInOrder(globalVars.treeJson[currentNode][direction])
            if direction == "left":
                print(f"{' ' if tree.bFirstInOrderPrint else ', '}{currentNode}", end = "")
                if tree.bFirstInOrderPrint: tree.bFirstInOrderPrint = False
    
    bFirstPostorderPrint = True
    def printPostOrder(currentNode = None):
        if currentNode is None:
            currentNode = tree.getRoot()
            print(f"Post-order:", end = "")
        for direction in ["left", "right"]:
            if globalVars.treeJson[currentNode][direction]:
                tree.printPostOrder(globalVars.treeJson[currentNode][direction])
        print(f"{' ' if tree.bFirstPostorderPrint else ', '}{currentNode}", end = "")
        if tree.bFirstPostorderPrint: tree.bFirstPostorderPrint = False
        
    def print():
        tree.bFirstInOrderPrint, tree.bFirstPostorderPrint = [True, True]
        callFunction("printpreorder"); print()
        callFunction("printinorder"); print()
        callFunction("printpostorder"); print()
    
    def remove(nodeId):
        parentId = globalVars.treeJson[nodeId]["parent"]
        if globalVars.treeJson[nodeId]["left"] is None and globalVars.treeJson[nodeId]["right"] is None:
            for direction in ["left", "right"]:
                if parentId is None: break
                childId = globalVars.treeJson[parentId][direction]
                if childId == nodeId:
                    globalVars.treeJson[parentId][direction] = None
                    break
            del globalVars.treeJson[nodeId]
        elif globalVars.treeJson[nodeId]["left"] is None or globalVars.treeJson[nodeId]["right"] is None:
            childId, parentsNodeDirection = [None, None]
            for direction in ["left", "right"]:
                if globalVars.treeJson[nodeId][direction]:
                    childId = globalVars.treeJson[nodeId][direction]
            if childId is not None:
                globalVars.treeJson[childId]["parent"] = parentId
            if parentId is not None:
                for direction in ["left", "right"]:
                    if globalVars.treeJson[parentId][direction] == nodeId:
                        parentsNodeDirection = direction
                globalVars.treeJson[parentId][parentsNodeDirection] = childId
            del globalVars.treeJson[nodeId]
        else:
            leftNodeId = globalVars.treeJson[nodeId]["left"]
            nodeIdToReplace = tree.findMinMax(leftNodeId)["max"]["value"]
            tree.remove(nodeIdToReplace)
            globalVars.treeJson[nodeIdToReplace] = globalVars.treeJson[nodeId].copy()
            for direction in ["left", "right"]:
                childId = globalVars.treeJson[nodeIdToReplace][direction]
                if childId is None: continue
                globalVars.treeJson[childId]["parent"] = nodeIdToReplace
            if globalVars.treeJson[nodeId]["parent"] is not None:
                parentId = globalVars.treeJson[nodeId]["parent"]
                for direction in ["left", "right"]:
                    if globalVars.treeJson[parentId][direction] == nodeId:
                        globalVars.treeJson[parentId][direction] = nodeIdToReplace
            del globalVars.treeJson[nodeId]
    
    def removeInput():
        nodesToRemove = validInputType("list", "remove> ").split()
        for nodeId in nodesToRemove:
            nodeId = int(nodeId)
            if not nodeId in globalVars.treeJson: continue 
            tree.remove(nodeId)
            globalVars.nodesCount -= 1
        
    def delete(currentNode = None):
        if currentNode is None: currentNode = tree.getRoot()
        for direction in ["left", "right"]:
            if globalVars.treeJson[currentNode][direction]:
                tree.delete(globalVars.treeJson[currentNode][direction])
        tree.remove(currentNode)
        globalVars.nodesCount -= 1
    
    def export(node = None, bFirstRun = True):
        if bFirstRun: node = tree.getRoot()
        left, right = [globalVars.treeJson[node]["left"], globalVars.treeJson[node]["right"]]
        if not left and not right: result = f"node {{{node}}}"
        else:
            lStr = f"child {{ {tree.export(left, False)} }}" if left else "child[missing] {}"
            rStr = f"child {{ {tree.export(right, False)} }}" if right else "child[missing] {}"
            result = f"node {{{node}}} {lStr} {rStr}"
        if bFirstRun: print(f"Exported tree:\n\\{result};\n")
        return result
    
    def rotate(pivotId, rotatorId, direction):
        getOppositeDirection = {
            "left": "right",
            "right": "left"
        }
        pivotChildId = globalVars.treeJson[pivotId][direction]
        globalVars.treeJson[rotatorId][getOppositeDirection[direction]] = pivotChildId
        if pivotChildId is not None: globalVars.treeJson[pivotChildId]["parent"] = rotatorId
        globalVars.treeJson[pivotId][direction] = rotatorId
        rotatorParentId = globalVars.treeJson[rotatorId]["parent"]
        if rotatorParentId is not None:
            for direction2 in ["left", "right"]:
                if globalVars.treeJson[rotatorParentId][direction2] == rotatorId:
                    globalVars.treeJson[rotatorParentId][direction2] = pivotId
                    break
        globalVars.treeJson[pivotId]["parent"] = rotatorParentId
        globalVars.treeJson[rotatorId]["parent"] = pivotId
        
    def rebalance():
        nodeId = tree.getRoot()
        while True:
            nodeLeftId = globalVars.treeJson[nodeId]["left"]
            while nodeLeftId is not None:
                tree.rotate(nodeLeftId, nodeId, "right")
                nodeId, nodeLeftId = [nodeLeftId, globalVars.treeJson[nodeLeftId]["left"]]
            nodeRightId = globalVars.treeJson[nodeId]["right"]
            if nodeRightId is not None: nodeId = nodeRightId
            else: break
        wsp = math.floor(math.log2(globalVars.nodesCount + 1))
        liczbaRotacji = globalVars.nodesCount + 1 - 2 ** wsp
        nodeId = tree.getRoot()
        for i in range(liczbaRotacji):
            rChildId = globalVars.treeJson[nodeId]["right"]
            if rChildId is None: break
            tree.rotate(rChildId, nodeId, "left")
            nodeId = globalVars.treeJson[rChildId]["right"]
        y = globalVars.nodesCount - liczbaRotacji
        while y > 1:
            nodeId = tree.getRoot()
            for i in range(math.floor(y / 2)):
                rChildId = globalVars.treeJson[nodeId]["right"]
                if rChildId is None: break
                tree.rotate(rChildId, nodeId, "left")
                nodeId = globalVars.treeJson[rChildId]["right"]
            y = y // 2
        
commandsJson = {
    "create": {
        "function": tree.create,
        "displayName": "Create",
        "description": "Creates a BST or AVL tree.",
        "bHideFromUser": True,
        "bBenchmark": True
    },
    "help": {
        "function": None,
        "displayName": "Help",
        "description": "Show this message.",
        "bHideFromUser": False,
        "bBenchmark": False
    },
    "print": {
        "function": tree.print,
        "displayName": "Print",
        "description": "Print the tree using In-order, Pre-order, Post-order.",
        "bHideFromUser": False,
        "bBenchmark": False
    },
    "printinorder": {
        "function": tree.printInOrder,
        "displayName": "In-order",
        "description": "Print the tree using In-order",
        "bHideFromUser": True,
        "bBenchmark": True
    },
    "printpreorder": {
        "function": tree.printPreOrder,
        "displayName": "Pre-order",
        "description": "Print the tree using Pre-order.",
        "bHideFromUser": True,
        "bBenchmark": True
    },
    "printpostorder": {
        "function": tree.printPostOrder,
        "displayName": "Post-order",
        "description": "Print the tree using Post-order.",
        "bHideFromUser": True,
        "bBenchmark": True
    },
    "findminmax": {
        "function": tree.findMinMax,
        "displayName": "FindMinMax",
        "description": "Print the minimum and maximum values of the tree.",
        "bHideFromUser": False,
        "bBenchmark": True
    },
    "remove": {
        "function": tree.removeInput,
        "displayName": "Remove",
        "description": "Remove elements of the tree.",
        "bHideFromUser": False,
        "bBenchmark": True
    },
    "delete": {
        "function": tree.delete,
        "displayName": "Delete",
        "description": "Delete whole tree.",
        "bHideFromUser": False,
        "bBenchmark": True
    },
    "export": {
        "function": tree.export,
        "displayName": "Export",
        "description": "Export the tree to tickzpicture.",
        "bHideFromUser": False,
        "bBenchmark": True
    },
    "rebalance": {
        "function": tree.rebalance,
        "displayName": "Rebalance",
        "description": "Rebalance the tree.",
        "bHideFromUser": False,
        "bBenchmark": True
    },
    "exit": {
        "function": exitProgram,
        "displayName": "Exit",
        "description": "Exits the program (same as CTRL+D).",
        "bHideFromUser": False,
        "bBenchmark": False
    }
}

class menu():
    def getTreeType():
        if len(sys.argv) == 1: exitProgram(2, "U forgor about launch arguments. Try again")
        if len(sys.argv) not in [3, 4]: exitProgram(2, "Wrong launch arguments. Try again")
        if not sys.argv[1].lower() == "--tree": exitProgram(2, "No --tree argument. Try again")
        if not sys.argv[2].lower() in ["avl", "bst"]: exitProgram(2, f"Invalid tree type in arg. {sys.argv[2]}? Never heard of it. Try Again")
        return sys.argv[2].lower()
    
    def getBenchmarkFlag(): return "--benchmark" in [i.lower() for i in sys.argv]
    
    def inputToTree():
        treeList = validInputType("list", "insert> ").split()
        while len(treeList) != globalVars.nodesCount:
            print(f"The amount of elements in the list is not equal to the nodes count ({globalVars.nodesCount} vs {len(treeList)}). Try again")
            treeList = validInputType("list", "insert> ").split()
        while len(treeList) != len(set(treeList)):
            print(f"The provided list contains duplicate nodes! There must be no duplicates. Try again")
            treeList = validInputType("list", "insert> ").split()
        return list(map(int, treeList))

    def help():
        def howManySpacesNum():
            longestWordCount = 0
            for command in commandsJson:
                dlugosc = len(command)
                if dlugosc > longestWordCount: longestWordCount = dlugosc
            return longestWordCount + 3
        
        spacesCount = howManySpacesNum()
        for command in commandsJson:
            if commandsJson[command]["bHideFromUser"]: continue
            print(f"{commandsJson[command]['displayName']}{' ' * (spacesCount - len(command))}{commandsJson[command]['description']}")
    
    def action():
        print("action> ", end = "")
        try:
            whatToDo = safeInput()
            while whatToDo.lower() not in [i for i in commandsJson.keys() if not commandsJson[i]["bHideFromUser"]]:
                print("Unknown command. Try \"help\" for a list of commands\naction> ", end = "")
                whatToDo = safeInput()
        except EOFError: whatToDo = "exit"
        if globalVars.nodesCount == 0 and whatToDo.lower() not in ["exit", "help"]:
            print(f"You deleted the tree. You cannot {commandsJson[whatToDo.lower()]['displayName']}!")
            print("Why are we still here? Just to suffer?")
        else: callFunction(whatToDo.lower())
    
    def main():
        commandsJson["help"]["function"] = menu.help
        globalVars.treeType = menu.getTreeType()
        globalVars.nodesCount = int(validInputType("intpos", " nodes> "))
        globalVars.initialTreeList = menu.inputToTree()
        globalVars.bBenchmarkMode = menu.getBenchmarkFlag()
        callFunction("create")
        while True: menu.action()

if __name__ == "__main__": menu.main()
