import sys

grafInMatrix = []
grafInList = [[]]
grafInTable = []

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

    def validPositiveNumber(inputMessage = None, minValue = None, maxValue = None, type = int):
        if inputMessage: print(inputMessage, end = "")
        whatToDo = safeInput()
        bIsAllGood = False
        while not bIsAllGood:
            bIsAllGood = True
            if not whatToDo.isdecimal(): bIsAllGood = False
            whatToDo = type(whatToDo)
            if not type(whatToDo) > 0: bIsAllGood = False
            if minValue and whatToDo < minValue: bIsAllGood = False
            if maxValue and whatToDo > maxValue: bIsAllGood = False
            if not bIsAllGood:
                print(f"A positive {f'integer' if type == int else 'float'}{f' that is >= {round(minValue, 2)}' if minValue else ''}{f' and <= {round(maxValue, 2)}' if maxValue else ''} is expected here. Try again")
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
                liczba = liczba.replace("-", "")
                if not liczba.isdecimal():
                    bIsAllGood = False; break
                liczba = int(liczba)
                if liczba <= 0 or (maxValue and liczba > maxValue):
                    bIsAllGood = True; break
            if not bIsAllGood:
                print(f"An empty or space seperated list of positive integers{f' that are <= {round(maxValue, 2)}' if maxValue else ''} is expected here. Try again")
                if inputMessage: print(inputMessage, end = "")
                whatToDo = safeInput()
        return whatToDo

def getMinSaturation(nodes):
    return 100 * (2/nodes)
