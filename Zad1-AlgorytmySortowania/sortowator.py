import subprocess
import sys
import os
import glob
import time
import random

sys.setrecursionlimit(2500000)
currentFolderProgramu = os.path.dirname(os.path.abspath(__file__))

def wyprintujTablice(tablica):
    for element in tablica:
        print(element, end = " ")
    print()

# Się wstawia się elementy do lewej "posortowanej" strony całe te
def sortowaniePrzezWstawianie(tablica, indexPoczatku = 0, przyrost = 1): 
    for i in range(indexPoczatku + przyrost, len(tablica), przyrost):
        wartoscPodI = tablica[i]
        j = i - przyrost
        while j >= indexPoczatku and tablica[j] > wartoscPodI:
            tablica[j + przyrost] = tablica[j]
            j -= przyrost
        tablica[j + przyrost] = wartoscPodI
    return tablica

# Tutaj elementy najwięjsze "wypływają" jak bąbelki do prawej strony i są w dobrym miejscu juz.
def sortowanieBabelkowe(tablica):
    for i in range(len(tablica) - 1):
        for j in range(len(tablica) - 1 - i):
            if tablica[j] > tablica[j + 1]:
                tablica[j], tablica[j + 1] = tablica[j + 1], tablica[j]
    return tablica

# Się wybiera się tutaj tym razem po prostu z czesci nieposortowanej najmniejszy element i
# siup do prawego konca czesci lewej posortowanej.
def sortowaniePrzezWybor(tablica):
    for i in range(len(tablica) - 1):
        indexNajmnElementu = i
        for j in range(i + 1, len(tablica)):
            if tablica[j] < tablica[indexNajmnElementu]:
                indexNajmnElementu = j
        tablica[i], tablica[indexNajmnElementu] = tablica[indexNajmnElementu], tablica[i]
    return tablica

# Do sortowania nizej
def getListaPrzyrostowShella(tablica):
    przyrosty = [1]
    for k in range(len(tablica)):
        przyrost = 4 ** (k + 1) + 3 * (2 ** k) + 1
        if przyrost > len(tablica) / 2: break
        przyrosty.append(przyrost)
    return przyrosty

# Takie jak przez wstawianie ale z przyrostem malejącym coraz niżej i tak dalej i tak dalej.
def sortowanieShella(tablica):
    przyrostyShella = getListaPrzyrostowShella(tablica)
    for i in range(len(przyrostyShella) - 1, -1, -1):
        przyrost = przyrostyShella[i]
        for j in range(przyrost):
            sortowaniePrzezWstawianie(tablica, j, przyrost)
    return tablica

# Zlicza wystąpienia potem modyfikacja tab. pomoc. i odpowiednie umiejscowienie tych tych.
def stabilneSortowaniePrzezZliczanie(tablica):
    maksElement = max(tablica)
    tablicaPomocniczaB = [0] * (maksElement + 1)
    for element in tablica:
        tablicaPomocniczaB[element] += 1
    for i in range(1, maksElement + 1):
        tablicaPomocniczaB[i] += tablicaPomocniczaB[i - 1]
    tablicaWyjsciowaC = [0] * len(tablica)
    for i in range(len(tablica) - 1, -1, -1):
        tablicaWyjsciowaC[tablicaPomocniczaB[tablica[i]] - 1] = tablica[i] # ten minus jeden tutaj zeby na poprawnej pozycji w tablicy wyjsciowej dalo
        tablicaPomocniczaB[tablica[i]] -= 1
    return tablicaWyjsciowaC

# Dzieli i zwycięża i gotowe
def sortowaniePrzezScalanie(tablica, i = None, j = None):
    if i == j == None: i, j = [0, len(tablica) - 1]
    srodek = (j - i) // 2 + i
    if j - i > 0:
        sortowaniePrzezScalanie(tablica, i, srodek)
        sortowaniePrzezScalanie(tablica, srodek + 1, j)
        tempTablica = []
        x, y = [i, srodek + 1]
        while x <= srodek and y <= j:
            if tablica[x] <= tablica[y]:
                tempTablica.append(tablica[x])
                x += 1
            else:
                tempTablica.append(tablica[y])
                y += 1
        while x <= srodek:
            tempTablica.append(tablica[x])
            x += 1
        while y <= j:
            tempTablica.append(tablica[y])
            y += 1
        iKopia = i
        for element in tempTablica:
            tablica[iKopia] = element
            iKopia += 1
    return tablica

def podzielAbyZwyciezyc(tablica, bLosowyIndex, x, y):
    i, j = [x, y]
    pivot = tablica[random.randint(x, y)] if bLosowyIndex else tablica[x]
    while i <= j:
        while tablica[i] < pivot: i += 1
        while tablica[j] > pivot: j -= 1
        if i <= j:
            tablica[i], tablica[j] = tablica[j], tablica[i]
            i += 1
            j -= 1
    return j

def quickSort(tablica, bLosowyIndex = True, x = None, y = None):
    if x == y == None: x, y = [0, len(tablica) - 1]
    if x < y:
        podzielenie = podzielAbyZwyciezyc(tablica, bLosowyIndex, x, y)
        if podzielenie < x: podzielenie = x # gdy tego nie bylo to wywalało recursion bo czsami podzielenie moze wyjsc -1
        quickSort(tablica, bLosowyIndex, x, podzielenie)
        quickSort(tablica, bLosowyIndex, podzielenie + 1, y)
    return tablica

def quickSortLewyIndex(tablica):
    return quickSort(tablica, False)

def quickSortLosowyIndex(tablica):
    return quickSort(tablica, True)

def naprawKopiec(tablica, indexRodzica, indexKonca):
    indexLewegoSyna = 2 * indexRodzica if 2 * indexRodzica <= indexKonca else -1
    indexPrawegoSyna = 2 * indexRodzica + 1 if 2 * indexRodzica + 1 <= indexKonca else -1
    indexDoZamiany = -1
    if indexLewegoSyna != -1 and tablica[indexLewegoSyna] > tablica[indexRodzica]:
        if indexDoZamiany == -1 or tablica[indexDoZamiany] < tablica[indexLewegoSyna]:
            indexDoZamiany = indexLewegoSyna
    if indexPrawegoSyna != -1 and tablica[indexPrawegoSyna] > tablica[indexRodzica]:
        if indexDoZamiany == -1 or tablica[indexDoZamiany] < tablica[indexPrawegoSyna]:
            indexDoZamiany = indexPrawegoSyna
    if indexDoZamiany != -1:
        tablica[indexRodzica], tablica[indexDoZamiany] = tablica[indexDoZamiany], tablica[indexRodzica]
        naprawKopiec(tablica, indexDoZamiany, indexKonca)

def utworzKopiecPoczatkowy(tablica):
    tablica = [0] + tablica
    i, j = [1, len(tablica) - 1]
    indexOstatniegoRodzica = j // 2
    for i in range(indexOstatniegoRodzica, 0, -1):
        naprawKopiec(tablica, i, j)
    return tablica

def sortowaniePrzezKopcowanie(tablica):
    tablica = utworzKopiecPoczatkowy(tablica)
    for j in range(len(tablica) - 1, 1, -1):
        tablica[1], tablica[j] = tablica[j], tablica[1]
        naprawKopiec(tablica, 1, j - 1)
    return tablica

class menu():
    nrWybranegoAlgoStr = None
    jsonConfigu = {
        "wartosci": {
            "bSkipujSortowaniaKwadratoweDlaDuzychCiagow": True,
            "bSkipujSortowanieSzybkieDlaDlaDuzychCiagow": True,
            "bPokazujTablicePrzedOrazPoSortowaniu": True
        },
        "opcje": {
            "1": {
                "nazwa": "Skipuj sortowania o złożoności kwadratowej dla dużych ciągów",
                "opcja": "bSkipujSortowaniaKwadratoweDlaDuzychCiagow"
            },
            "2": {
                "nazwa": "Skipuj sortowanie szybkie dla dużych ciągów",
                "opcja": "bSkipujSortowanieSzybkieDlaDlaDuzychCiagow"
            },
            "3": {
                "nazwa": "Pokazuj tablice przed oraz po sortowaniu",
                "opcja": "bPokazujTablicePrzedOrazPoSortowaniu"
            }
        }
    }
    jsonAlgorytmow = {
        "1": {
            "nazwa": "Sortowanie przez wstawianie",
            "funkcja": sortowaniePrzezWstawianie
        },
        "2": {
            "nazwa": "Sortowanie bąbelkowe",
            "funkcja": sortowanieBabelkowe
        },
        "3": {
            "nazwa": "Sortowanie przez wybór",
            "funkcja": sortowaniePrzezWybor
        },
        "4": {
            "nazwa": "Sortowanie Shella",
            "funkcja": sortowanieShella
        },
        "5": {
            "nazwa": "Sortowanie przez zliczanie",
            "funkcja": stabilneSortowaniePrzezZliczanie
        },
        "6": {
            "nazwa": "Sortowanie przez scalanie",
            "funkcja": sortowaniePrzezScalanie
        },
        "7": {
            "nazwa": "Sortowanie szybkie (pivot skrajnie lewy)",
            "funkcja": quickSortLewyIndex
        },
        "8": {
            "nazwa": "Sortowanie szybkie (pivot losowy)",
            "funkcja": quickSortLosowyIndex
        },
        "9": {
            "nazwa": "Sortowanie przez kopcowanie",
            "funkcja": sortowaniePrzezKopcowanie
        },
        "10": {
            "nazwa": "Po co mam wybierać, najlepiej zabrać wszystkie"
        }
    }

    def startTesta():
        global currentFolderProgramu
        if not menu.nrWybranegoAlgoStr:
            print("Przed użyciem zapoznaj się z treścią listy algorytmów dołączonej do programu i se wybierz jakiś.\n")
            return
        folderBenchmarka = os.path.join(currentFolderProgramu, "benchmark")
        if not os.path.exists(folderBenchmarka):
            print("Chwila! Najpierw wygeneruj ciągi w menu. Bo ni ma czego sortować.\n")
            return
        pliki = glob.glob(os.path.join(folderBenchmarka, "*.txt"))
        if not pliki:
            print("Zara, zara! Folder benchmarków jest ale ni ma tam plików. Co się stało się?\nWygeneruj je tu w menu.\n")
            return
        print("Rozpoczynanie sortowania...")
        with open("wynikiBenchmarku.csv", "w", encoding="utf-8-sig") as plikBenchmarku:
            plikBenchmarku.write("Algorytm,Typ Ciągu,Rozmiar Ciągu,Czas\n")
            algoDoUruchomienia = []
            if menu.nrWybranegoAlgoStr == "10":
                algoDoUruchomienia = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
            else:
                algoDoUruchomienia = [menu.nrWybranegoAlgoStr]
            for plik in sorted(pliki):
                with open(plik, "r") as plik2: dane = [int(x) for x in plik2.read().split()]
                nazwaPliku = os.path.basename(plik)
                rozmiarTablicy = dane[0]
                tablica = dane[1:]
                typTablicy = nazwaPliku.rsplit("_", 1)[0] 
                for nrAlgo in algoDoUruchomienia:
                    nazwaAlgo = menu.jsonAlgorytmow[nrAlgo]["nazwa"]
                    funkcjaSortowania = menu.jsonAlgorytmow[nrAlgo]["funkcja"]
                    if (menu.jsonConfigu["wartosci"]["bSkipujSortowaniaKwadratoweDlaDuzychCiagow"] and nrAlgo in ["1", "2", "3"]\
                        or menu.jsonConfigu["wartosci"]["bSkipujSortowanieSzybkieDlaDlaDuzychCiagow"] and nrAlgo in ["7", "8"])\
                        and rozmiarTablicy > 16384:
                        print(f"Testowanie: {nazwaAlgo} jest skipowane dla rozmairu {rozmiarTablicy}")
                        continue
                    tablicaKopia = tablica.copy()
                    if menu.jsonConfigu["wartosci"]["bPokazujTablicePrzedOrazPoSortowaniu"] and rozmiarTablicy <= 32: wyprintujTablice(tablica)
                    print(f"Testowanie: {nazwaAlgo} dla pliku {nazwaPliku} ... ", end="")
                    sys.stdout.flush() # Tutj zeby od razu pokazało printa w konsoli
                    startCzas = time.perf_counter()
                    tablicaKopia = funkcjaSortowania(tablicaKopia)
                    endCzas = time.perf_counter()
                    czasWykonania = endCzas - startCzas
                    print(f"Gotowe! ({czasWykonania:.6f} s)")
                    if menu.jsonConfigu["wartosci"]["bPokazujTablicePrzedOrazPoSortowaniu"] and rozmiarTablicy <= 32: wyprintujTablice(tablicaKopia)
                    plikBenchmarku.write(f"{nazwaAlgo},{typTablicy},{rozmiarTablicy},{czasWykonania:.6f}\n")
        print()

    def wygenerujCiagi():
        global currentFolderProgramu
        print("Generowanie, proszę czekać...")
        subprocess.run([sys.executable, "generate.py"], cwd=currentFolderProgramu) # cwd zeby w current folderze .py sie uruchomil
        print()

    def wyboruAlgo():
        while True:
            if menu.nrWybranegoAlgoStr: print(f"Obecnie wybrano {menu.jsonAlgorytmow[menu.nrWybranegoAlgoStr]['nazwa']}.")
            print("Dostępne algorytmy sortowania:")
            for index in menu.jsonAlgorytmow:
                print(f"{index}: {menu.jsonAlgorytmow[index]['nazwa']}")
            print("Wprowadź numer przy wybranym algorytmie albo wprowadź 0, by pójść wstecz i wciśnij ENTER.")
            wybor = input()
            while not wybor in list(menu.jsonAlgorytmow.keys()) + ["0"]:
                wybor = input("\nWprowadzono niepoprawną wartość. Spróbuj raz jeszcze.\n")
            print()
            if wybor == "0": break
            menu.nrWybranegoAlgoStr = wybor
            print(f"Wybrano {menu.jsonAlgorytmow[wybor]['nazwa']}.\n")
            break
    
    def configu():
        while True:
            print("Dostępne opcje configu:")
            for indexOpcji in menu.jsonConfigu["opcje"]:
                opcja = menu.jsonConfigu["opcje"][indexOpcji]
                print(f"{indexOpcji}: {opcja['nazwa']} ({menu.jsonConfigu['wartosci'][opcja['opcja']]})")
            print("Aby przestawić jakąś opcję z True na False lub na odwrót, wprowadź odpowiedni numer i wciśnij ENTER.\nAby pójść wstecz, wprowadż 0 i wciśnij ENTER.")
            wybor = input()
            while not wybor in list(menu.jsonConfigu["opcje"].keys()) + ["0"]:
                wybor = input("\nWprowadzono niepoprawną wartość. Spróbuj raz jeszcze.\n")
            print()
            if wybor == "0": break
            wybranaOpcjaStr = menu.jsonConfigu["opcje"][wybor]["opcja"]
            menu.jsonConfigu["wartosci"][wybranaOpcjaStr] = not menu.jsonConfigu["wartosci"][wybranaOpcjaStr]

    def glowne():
        while True:
            print("Sortowator v1.0.0\nWpisz 1, aby uruchomić sortowanie i wciśnij ENTER.\nWpisz 2, aby wybrać algorytm sortowania i wciśnij ENTER.\nWpisz 3, aby wygenerować ciągi wejściowe i wsiśnij ENTER.\nWpisz 4, aby dostosować konfiguracje i wciśnij ENTER.\nAby zamknąć program nic nie wpisuj i wciśnij ENTER.")
            wybor = input()
            print()
            if not wybor: break
            elif wybor == "1": menu.startTesta()
            elif wybor == "2": menu.wyboruAlgo()
            elif wybor == "3": menu.wygenerujCiagi()
            elif wybor == "4": menu.configu()

if __name__ == "__main__": menu.glowne()
