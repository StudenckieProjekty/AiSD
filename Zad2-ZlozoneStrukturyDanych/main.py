import sys
sys.setrecursionlimit(2500000)

class globalVars:
    treeType = None
    nodesCount = 0
    initialTreeList = []
    treeJson = {}

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
        print(globalVars.treeJson) # temp

    def getRoot():
        return next(i for i in globalVars.treeJson if globalVars.treeJson[i]["parent"] is None)

    def findMinMax():
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
        korzen = tree.getRoot()
        for extremumType in values:
            currentNode = korzen
            values[extremumType]["value"] = currentNode
            while globalVars.treeJson[currentNode][values[extremumType]["direction"]]:
                currentNode = globalVars.treeJson[currentNode][values[extremumType]["direction"]]
                values[extremumType]["value"] = currentNode
        print(f"Min: {values['min']['value']}\nMax: {values['max']['value']}")

    def printPreOrder(currentNode = None):
        if currentNode is None:
            currentNode = tree.getRoot()
            print(f" Pre-order: {currentNode}", end = "")
        else: print(f", {currentNode}", end = "")
        for direction in ["left", "right"]:
            if globalVars.treeJson[currentNode][direction]:
                tree.printPreOrder(globalVars.treeJson[currentNode][direction])       
    
    bFirstPreorderPrint = True
    def printInOrder(currentNode = None):
        if currentNode is None:
            currentNode = tree.getRoot()
            print(f"  In-order:", end = "")
        for direction in ["left", "right"]:
            if globalVars.treeJson[currentNode][direction]:
                tree.printInOrder(globalVars.treeJson[currentNode][direction])
            if direction == "left":
                print(f"{' ' if tree.bFirstPreorderPrint else ', '}{currentNode}", end = "")
                if tree.bFirstPreorderPrint: tree.bFirstPreorderPrint = False
    
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
        tree.bFirstPreorderPrint, tree.bFirstPostorderPrint = [True, True]
        tree.printPreOrder(); print()
        tree.printInOrder(); print()
        tree.printPostOrder(); print()
    
    def remove():
        whatToDo = validInputType("int", "remove> ")
        safeInput()
    
    def export(node=None, bFirstRun=True):
        if bFirstRun: node = tree.getRoot()
        left, right = [globalVars.treeJson[node]["left"], globalVars.treeJson[node]["right"]]
        if not left and not right: result = f"node {{{node}}}"
        else:
            lStr = f"child {{ {tree.export(left, False)} }}" if left else "child[missing] {}"
            rStr = f"child {{ {tree.export(right, False)} }}" if right else "child[missing] {}"
            result = f"node {{{node}}} {lStr} {rStr}"
        if bFirstRun: print(f"Exported tree:\n\\{result};\n")
        return result

commandsJson = {
    "help": {
        "func": None,
        "displayName": "Help",
        "desc": "Show this message."
    },
    "print": {
        "func": tree.print,
        "displayName": "Print",
        "desc": "Print the tree using In-order, Pre-order, Post-order."
    },
    "findminmax": {
        "func": tree.findMinMax,
        "displayName": "FindMinMax",
        "desc": "Print the minimum and maximum values of the tree."
    },
    "remove": {
        "func": tree.remove,
        "displayName": "Remove",
        "desc": "Remove elements of the tree."
    },
    "delete": {
        "func": None,
        "displayName": "Delete",
        "desc": "Delete whole tree."
    },
    "export": {
        "func": tree.export,
        "displayName": "Export",
        "desc": "Export the tree to tickzpicture."
    },
    "rebalance": {
        "func": None,
        "displayName": "Rebalance",
        "desc": "Rebalance the tree."
    },
    "exit": {
        "func": exitProgram,
        "displayName": "Exit",
        "desc": "Exits the program (same as CTRL+D)."
    }
}

class menu():
    def getTreeType():
        if len(sys.argv) == 1: exitProgram(2, "U forgor about launch arguments. Try again")
        if len(sys.argv) != 3: exitProgram(2, "Wrong launch arguments. Try again")
        if not sys.argv[1].lower() == "--tree": exitProgram(2, "No --tree argument. Try again")
        if not sys.argv[2].lower() in ["avl", "bst"]: exitProgram(2, f"Invalid tree type in arg. {sys.argv[2]}? Never heard of it. Try Again")
        return sys.argv[2].lower()

    def help():
        def howManySpacesNum():
            longestWordCount = 0
            for command in commandsJson:
                dlugosc = len(command)
                if dlugosc > longestWordCount: longestWordCount = dlugosc
            return longestWordCount + 3
        
        spacesCount = howManySpacesNum()
        for command in commandsJson:
            print(f"{commandsJson[command]['displayName']}{' ' * (spacesCount - len(command))}{commandsJson[command]['desc']}")
    
    def action():
        print("action> ", end = "")
        try:
            whatToDo = safeInput()
            while whatToDo.lower() not in commandsJson.keys():
                print("Unknown command. Try \"help\" for a list of commands\naction> ", end = "")
                whatToDo = safeInput()
        except EOFError: whatToDo = "exit"
        commandsJson[whatToDo.lower()]["func"]()
    
    def main():
        commandsJson["help"]["func"] = menu.help
        globalVars.treeType = menu.getTreeType()
        globalVars.nodesCount = int(validInputType("intpos", " nodes> "))
        treeList = validInputType("list", "insert> ").split()
        while len(treeList) != globalVars.nodesCount:
            print(f"The amount of elements in the list is not equal to the nodes count ({globalVars.nodesCount} vs {len(treeList)}). Try again")
            treeList = validInputType("list", "insert> ").split()
        globalVars.initialTreeList = list(map(int, treeList))
        print(globalVars.treeType) # temp
        print(globalVars.nodesCount) # temp
        print(globalVars.initialTreeList) # temp
        tree.create()
        while True:
            menu.action()

if __name__ == "__main__": menu.main()
