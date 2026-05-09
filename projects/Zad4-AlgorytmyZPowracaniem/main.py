import sys
import argparse
import graf
import time
import utils
sys.setrecursionlimit(2500000)

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("--hamilton", action="store_true")
parser.add_argument("--non-hamilton", action="store_true")
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
    "help": {
        "function": None,
        "displayName": "Help",
        "description": "Shows this message.",
        "bHideFromUser": False,
        "bBenchmark": False
    },
    "print": {
        "function": graf.Print,
        "displayName": "Print",
        "description": "Prints the adjacency matrix of the Graph.",
        "bHideFromUser": False,
        "bBenchmark": False
    },
    "export": {
        "function": graf.export,
        "displayName": "Export",
        "description": "Exports the graph to tickzpicture.",
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
commandAliases = {}

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
    
    def inputAndInitGraf():
        utils.nodes = int(utils.inputs.validPositiveNumber("nodes> ", 11))
        if args.hamilton:
            utils.saturation = float(utils.inputs.validPositiveNumber("saturation> ", utils.getMinSaturation(utils.nodes), 100, float))
            graf.argGenerate(utils.nodes, utils.saturation, True)
        elif args.non_hamilton:
            graf.argGenerate(utils.nodes, 50, False)

    def action():
        print("action> ", end = "")
        try:
            whatToDo = utils.safeInput().lower()
            if whatToDo in commandAliases: whatToDo = commandAliases[whatToDo]
            while whatToDo not in [i for i in commandsJson.keys() if not commandsJson[i]["bHideFromUser"]]:
                print("Unknown command. Try \"help\" for a list of commands\naction> ", end = "")
                if whatToDo in commandAliases: whatToDo = commandAliases[whatToDo]
                whatToDo = utils.safeInput().lower()
        except EOFError: whatToDo = "exit"
        commandsJson[whatToDo]["function"]()

    def main():
        commandsJson["help"]["function"] = menu.help
        if (not args.hamilton) and (not args.non_hamilton): utils.exitProgram(1, "U forgor about a --hamilton or --non-hamilton flag.")
        menu.inputAndInitGraf()
        while True: menu.action()

if __name__ == "__main__": menu.main()
