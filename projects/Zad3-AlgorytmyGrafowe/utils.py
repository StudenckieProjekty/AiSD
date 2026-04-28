import sys

def exitProgram(statusCode = 0, message = ""):
    print(f"\n{f'{message}\n' if message else ''}Program exited with status: {statusCode}")
    sys.exit()

def safeInput(string = ""):
    try: whatToDo = input(string)
    except EOFError: exitProgram()
    return whatToDo

def validInputInList(validValues, inputMessage = "", errorMessage = ""):
    if inputMessage: print(inputMessage, end = "")
    whatToDo = input().lower()
    while whatToDo.lower() not in validValues:
        if errorMessage: print(errorMessage)
        if inputMessage: print(inputMessage, end = "")
        whatToDo = input().lower()
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
