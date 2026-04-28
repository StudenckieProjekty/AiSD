import sys
import time
import argparse
import graf
import utils
sys.setrecursionlimit(2500000)

class gVars:
    selectedRep = None

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("--generate", action="store_true")
parser.add_argument("--user-provided", action="store_true")
parser.add_argument("--benchmark", action="store_true")
args = parser.parse_args()

def callFunction(funcName):
    if args.benchmark and commandsJson[funcName]["bBenchmark"]:
        startTime = time.perf_counter()
        commandsJson[funcName]["function"]()
        endTime = time.perf_counter()
        execTime = endTime - startTime
        print(f"\n{commandsJson[funcName]['displayName']} benchmarked time: ({execTime:.6f} s)")
    else: commandsJson[funcName]["function"]()

commandsJson = {
    "create": {
        "function": graf.create,
        "displayName": "Create",
        "description": "Creates a Graph.",
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
        "function": graf.print,
        "displayName": "Print",
        "description": "Print the Graph in selected data structure.",
        "bHideFromUser": False,
        "bBenchmark": False
    },
    "exit": {
        "function": utils.exitProgram,
        "displayName": "Exit",
        "description": "Exits the program (same as CTRL+D).",
        "bHideFromUser": False,
        "bBenchmark": False
    }
}

class menu():
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
    
    def selectGraphRepresentation():
        gVars.selectedRep = utils.validInputInList(["matrix", "list", "table"], " type> ", "Invalid representation! Expected: matrix, list or table.")
    
    def inputAndInitGraf():
        nodesCount = utils.validInputType("intpos", "nodes> ")

    def action():
        print("action> ", end = "")
        try:
            whatToDo = utils.safeInput()
            while whatToDo.lower() not in [i for i in commandsJson.keys() if not commandsJson[i]["bHideFromUser"]]:
                print("Unknown command. Try \"help\" for a list of commands\naction> ", end = "")
                whatToDo = utils.safeInput()
        except EOFError: whatToDo = "exit"
        callFunction(whatToDo.lower())
    
    def main():
        commandsJson["help"]["function"] = menu.help
        menu.selectGraphRepresentation()
        menu.inputAndInitGraf()
        while True: menu.action()

if __name__ == "__main__": menu.main()
