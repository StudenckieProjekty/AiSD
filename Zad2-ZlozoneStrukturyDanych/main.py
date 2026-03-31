import sys

commandsJson = {
    "help": {
        "func": None,
        "desc": "Show this message."
    },
    "print": {
        "func": None,
        "desc": "Print the tree using In-order, Pre-order, Post-order."
    },
    "remove": {
        "func": None,
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
        "func": sys.exit,
        "desc": "Exits the program (same as CTRL+D)."
    }
}

class menu():
    def validInputType(expectedType = None, inputMessage = None):
        if inputMessage: print(inputMessage, end = "")
        whatToDo = input()
        if expectedType == "intpos":
            while (not whatToDo.isdecimal()) or not (int(whatToDo) > 0):
                print("A positive integer is expected here. Try again")
                if inputMessage: print(inputMessage, end = "")
                whatToDo = input()
        if expectedType == "list":
            bIsAllGood = False
            while not bIsAllGood:
                bIsAllGood = True
                for liczba in whatToDo.split():
                    if not liczba.isdecimal():
                        bIsAllGood = False
                        break
                if not bIsAllGood:
                    print("A space seperated integer list is expected here. Try again")
                    if inputMessage: print(inputMessage, end = "")
                    whatToDo = input()
        return whatToDo

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
        whatToDo = input()
        while whatToDo.lower() not in commandsJson.keys():
            print("Unknown command. Try \"help\" for a list of commands\naction> ", end = "")
            whatToDo = input()
        commandsJson[whatToDo.lower()]["func"]()
    def main():
        commandsJson["help"]["func"] = menu.help
        nodesCount = menu.validInputType("intpos", " nodes> ")
        treeList = list(map(int, menu.validInputType("list", "insert> ").split()))
        print(nodesCount) # temp
        print(treeList) # temp
        while True:
            menu.action()

if __name__ == "__main__": menu.main()
