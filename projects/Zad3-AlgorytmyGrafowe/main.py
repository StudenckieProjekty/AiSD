import sys
import argparse
import graf
import utils
sys.setrecursionlimit(2500000)

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("--generate", action="store_true")
parser.add_argument("--user-provided", action="store_true")
args = parser.parse_args()

commandsJson = {
    "help": {
        "function": None,
        "displayName": "Help",
        "description": "Shows this message.",
        "bHideFromUser": False
    },
    "print": {
        "function": graf.Print,
        "displayName": "Print",
        "description": "Prints the Graph in selected data structure.",
        "bHideFromUser": False
    },
    "find": {
        "function": graf.find,
        "displayName": "Find",
        "description": "Finds out whether a provided edge exists in the graph.",
        "bHideFromUser": False
    },
    "bfs": {
        "function": graf.BFS,
        "displayName": "BFS",
        "description": "Performs Breadth First Search and displays the results.",
        "bHideFromUser": False
    },
    "dfs": {
        "function": graf.DFS,
        "displayName": "DFS",
        "description": "Performs Depth First Search and displays the results.",
        "bHideFromUser": False
    },
    "kahn": {
        "function": graf.kahnSort,
        "displayName": "Kahn",
        "description": "Displays Kahn's topological sort results.",
        "bHideFromUser": False
    },
    "tarjan": {
        "function": graf.tarjanSort,
        "displayName": "Tarjan",
        "description": "Displays Tarjan's topological sort results.",
        "bHideFromUser": False
    },
    "changerep": {
        "function": graf.changeRep,
        "displayName": "ChangeRep",
        "description": "Changes the graph representation.",
        "bHideFromUser": False
    },
    "export": {
        "function": graf.export,
        "displayName": "Export",
        "description": "Exports the graph to tickzpicture.",
        "bHideFromUser": False
    },
    "exit": {
        "function": utils.exitProgram,
        "displayName": "Exit",
        "description": "Exits the program (same as CTRL+D).",
        "bHideFromUser": False
    }
}
commandAliases = {
    "breadth-first search": "bfs",
    "depth-first search": "dfs",
    "kahn_sort": "kahn",
    "tarjan_sort": "tarjan"
}

class menu():
    def help():
        def howManySpacesNum():
            longestWordCount = 0
            for command in commandsJson:
                if commandsJson[command]["bHideFromUser"]: continue
                dlugosc = len(command)
                if dlugosc > longestWordCount: longestWordCount = dlugosc
            return longestWordCount + 3
        
        spacesCount = howManySpacesNum()
        for command in commandsJson:
            if commandsJson[command]["bHideFromUser"]: continue
            print(f"{commandsJson[command]['displayName']}{' ' * (spacesCount - len(command))}{commandsJson[command]['description']}")
    
    def selectGraphRepresentation():
        utils.selectedRep = utils.inputs.validInList(["matrix", "list", "table"], "type> ", "Invalid type! Expected: matrix, list or table.")
    
    def inputAndInitGraf():
        utils.nodes = int(utils.inputs.validPositiveNumber("nodes> ", 2))
        if args.generate:
            utils.saturation = float(utils.inputs.validPositiveNumber("saturation> ", utils.getMinSaturation(utils.nodes), 100, float))
            graf.argGenerate(utils.nodes, utils.saturation)
        elif args.user_provided:
            graf.argUserProvided(utils.nodes)

    def action():
        print("action> ", end = "")
        try:
            whatToDo = utils.safeInput().lower()
            if whatToDo in commandAliases: whatToDo = commandAliases[whatToDo]
            while whatToDo not in [i for i in commandsJson.keys() if not commandsJson[i]["bHideFromUser"]]:
                print("Unknown command. Try \"help\" for a list of commands\naction> ", end = "")
                whatToDo = utils.safeInput().lower()
                if whatToDo in commandAliases: whatToDo = commandAliases[whatToDo]
        except EOFError: whatToDo = "exit"
        commandsJson[whatToDo]["function"]()

    def main():
        commandsJson["help"]["function"] = menu.help
        if (not args.generate) and (not args.user_provided): utils.exitProgram(1, "U forgor about a --generate or --user-provided flag.")
        menu.selectGraphRepresentation()
        menu.inputAndInitGraf()
        while True: menu.action()

if __name__ == "__main__": menu.main()
