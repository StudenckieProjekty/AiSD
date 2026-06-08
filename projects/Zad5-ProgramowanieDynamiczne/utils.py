import sys
from pathlib import Path
import random
import json
import os

def exitProgram(statusCode = 0, message = ""):
    print(f"\n{f'{message}\n' if message else ''}Program exited with status: {statusCode}")
    sys.exit()

def safeInput(string = ""):
    try: whatToDo = input(string)
    except EOFError: exitProgram()
    return whatToDo

class inputs:
    def validInList(validValues, inputMessage = "", errorMessage = ""):
        if inputMessage: print(inputMessage, end = "")
        whatToDo = safeInput().lower()
        while whatToDo.lower() not in validValues:
            if errorMessage: print(errorMessage)
            if inputMessage: print(inputMessage, end = "")
            whatToDo = safeInput().lower()
        return whatToDo

    def validPositiveNumber(inputMessage = None, minValue = None, maxValue = None, dataType = int):
        if inputMessage: print(inputMessage, end = "")
        whatToDo = safeInput()
        bIsAllGood = False
        while not bIsAllGood:
            bIsAllGood = True
            try: whatToDo = dataType(whatToDo)
            except ValueError: bIsAllGood = False
            if bIsAllGood:
                if not dataType(whatToDo) > 0: bIsAllGood = False
                if minValue and whatToDo < minValue: bIsAllGood = False
                if maxValue and whatToDo > maxValue: bIsAllGood = False
            if not bIsAllGood:
                print(f"A positive {f'integer' if dataType == int else 'float'}{f' that is >= {round(minValue, 2)}' if minValue else ''}{f' and <= {round(maxValue, 2)}' if maxValue else ''} is expected here. Try again")
                if inputMessage: print(inputMessage, end = "")
                whatToDo = safeInput()
        return whatToDo

    def validListOrEmpty(inputMessage = None, maxValue = None):
        if inputMessage: print(inputMessage, end = "")
        whatToDo = safeInput()
        if not whatToDo: return whatToDo
        bIsAllGood = False
        while not bIsAllGood:
            bIsAllGood = True
            for liczba in whatToDo.split():
                try: liczba = int(liczba)
                except: bIsAllGood = False
                if bIsAllGood:
                    if liczba <= 0 or (maxValue and liczba > maxValue): bIsAllGood = False
            if not bIsAllGood:
                print(f"An empty or space seperated list of positive integers{f' that are <= {round(maxValue, 2)}' if maxValue else ''} is expected here. Try again")
                if inputMessage: print(inputMessage, end = "")
                whatToDo = safeInput()
        return whatToDo

def getDatasetPath():
    if getattr(sys, "frozen", False) or "__compiled__" in globals():
        return Path(sys.executable).parent.resolve() / "dataset.json"
    return Path(__file__).parent.resolve() / "dateset.json"

def createDataset():
    print("How many datasets do you want to make?")
    datasetsCount = inputs.validPositiveNumber("datasets> ", 1)
    print("How many items (n) do you want each dataset to have?")
    itemsCount = inputs.validPositiveNumber("items> ", 3)
    print("What should the max capacity (C) of the backapck be?")
    backpackCapacity = inputs.validPositiveNumber("capacity> ", 10)
    datasetJson = {
        "backpackCapacity": backpackCapacity,
        "itemsCount": itemsCount,
        "datasets": []
    }
    for i in range(datasetsCount):
        items = []
        for j in range(itemsCount):
            item = {
                "weight": random.randint(1, backpackCapacity),
                "value": random.randint(1, 2 * backpackCapacity)
            }
            items.append(item)
        datasetJson["datasets"].append(items)
    with open(getDatasetPath(), "w", encoding="utf-8") as fileToSave:
        json.dump(datasetJson, fileToSave, indent=2, ensure_ascii=False)
    print("Successfully created and saved to dataset.json")

def readDataset():
    datasetPath = getDatasetPath()
    if not os.path.exists(datasetPath):
        print("Generate some datasets first using the \"CreateDataset\" command.")
        return None
    bSuccessfullyRead = True
    try:
        with open(datasetPath, "r", encoding="utf-8") as fileToRead:
            datasetJson = json.loads(fileToRead.read())
    except: bSuccessfullyRead = False
    for object in ["backpackCapacity", "itemsCount", "datasets"]:
        if not object in datasetJson:
            bSuccessfullyRead = False
            break
    if not bSuccessfullyRead:
        print("Could not read the datasets.json file. Make a new one using the \"CreateDataset\" command.")
        return None
    return datasetJson
