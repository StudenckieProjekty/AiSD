import sys
import argparse
import backpack
import time
import utils
sys.setrecursionlimit(2500000)

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("--dynamic", action="store_true")
parser.add_argument("--brute-force", action="store_true")
parser.add_argument("--benchmark", action="store_true")
args = parser.parse_args()

def callFunctionWithBenchmark(function, functionArg, displayName):
    if args.benchmark:
        startTime = time.perf_counter()
        result = function(functionArg)
        endTime = time.perf_counter()
        execTime = endTime - startTime
        print(f"{displayName} benchmarked time: ({execTime:.6f} s)")
    else: result = function(functionArg)
    return result

def backpackProblem():
    datasetJson = utils.readDataset()
    if not datasetJson: return
    for i in range(len(datasetJson)):
        dataset = datasetJson[i]
        if args.dynamic: result = callFunctionWithBenchmark(backpack.bpDynamic, dataset, "Dynamic Programming")
        else: result = callFunctionWithBenchmark(backpack.bpBruteForce, dataset, "Brute force")
        print(f"Items in result for dataset #{i + 1} (Backpack capacity = {dataset["backpackCapacity"]}):")
        totalWeight = 0
        totalValue = 0
        for j in range(dataset["itemsCount"]):
            if ((result >> j) & 1) == 0: continue
            weight = dataset["items"][j]["weight"]
            totalWeight += weight
            value = dataset["items"][j]["value"]
            totalValue += value
            print(f"Item #{j + 1}: weight = {weight}, value = {value}")
        print(f"Total weight: {totalWeight}, Total value: {totalValue}")
        print()
    print("Done!")

commandsJson = {
    "help": {
        "function": None,
        "displayName": "Help",
        "description": "Shows this message."
    },
    "createdataset": {
        "function": utils.createDataset,
        "displayName": "CreateDataset",
        "description": "Generates custom datasets."
    },
    "backpack": {
        "function": backpackProblem,
        "displayName": "Backpack",
        "description": "Starts the chosen Backpack Problem algorithm on datasets."
    },
    "exit": {
        "function": utils.exitProgram,
        "displayName": "Exit",
        "description": "Exits the program (same as CTRL+D)."
    }
}
commandAliases = {
    "dataset": "createdataset",
    "create": "createdataset"
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
            print(f"{commandsJson[command]['displayName']}{' ' * (spacesCount - len(command))}{commandsJson[command]['description']}")

    def action():
        print("action> ", end = "")
        try:
            whatToDo = utils.safeInput().lower()
            if whatToDo in commandAliases: whatToDo = commandAliases[whatToDo]
            while whatToDo not in commandsJson.keys():
                print("Unknown command. Try \"help\" for a list of commands\naction> ", end = "")
                whatToDo = utils.safeInput().lower()
                if whatToDo in commandAliases: whatToDo = commandAliases[whatToDo]
        except EOFError: whatToDo = "exit"
        commandsJson[whatToDo]["function"]()

    def main():
        commandsJson["help"]["function"] = menu.help
        if (not args.dynamic) and (not args.brute_force): utils.exitProgram(1, "U forgor about a --dynamic or --brute-force flag.")
        while True: menu.action()

if __name__ == "__main__": menu.main()
