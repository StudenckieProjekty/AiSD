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

class sortowator:
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
    def createAVL(lista, i = None, j = None, parentId = None, bIsLeft = False):
        if i == j == None:
            lista = sortowator.sortowanieShella(lista)
            i, j = [0, len(lista) - 1]
        elif j - i < 0: return
        indexMediany = (i + j) // 2
        if parentId:
            globalVars.treeJson[parentId]["left" if bIsLeft else "right"] = lista[indexMediany]
        if not lista[indexMediany] in globalVars.treeJson:
            globalVars.treeJson[lista[indexMediany]] = {
                "left": None,
                "right": None,
                "parent": parentId
            }
        tree.createAVL(lista, i, indexMediany - 1, lista[indexMediany], True)
        tree.createAVL(lista, indexMediany + 1, j, lista[indexMediany], False)
    
    def create():
        if globalVars.treeType == "avl": tree.createAVL(globalVars.initialTreeList)
        print(globalVars.treeJson) # temp
        
    def print():
        return
    
    def remove():
        whatToDo = validInputType("int", "remove> ")
        safeInput()

commandsJson = {
    "help": {
        "func": None,
        "desc": "Show this message."
    },
    "print": {
        "func": tree.print,
        "desc": "Print the tree using In-order, Pre-order, Post-order."
    },
    "remove": {
        "func": tree.remove,
        "desc": "Remove elements of the tree."
    },
    "delete": {
        "func": None,
        "desc": "Delete whole tree."
    },
    "export": {
        "func": None,
        "desc": "Export the tree to tickzpicture."
    },
    "rebalance": {
        "func": None,
        "desc": "Rebalance the tree."
    },
    "exit": {
        "func": exitProgram,
        "desc": "Exits the program (same as CTRL+D)."
    }
}

class menu():
    def getTreeType():
        if len(sys.argv) == 1: exitProgram(2, "U forgor about launch arguments. Try again")
        if len(sys.argv) != 3: exitProgram(2, "Wrong launch arguments. Try again")
        if not sys.argv[1].lower() == "--tree": exitProgram(2, "No --tree argument. Try again")
        if not sys.argv[2].lower() in ["avl", "bst"]: exitProgram(2, "Invalid tree type in arg. Try Again")
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
            print(f"{command.capitalize()}{' ' * (spacesCount - len(command))}{commandsJson[command]['desc']}")
    
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
