import random
from src.Gracz import Gracz

KWOTA_POCZATKOWA = 10000
MIN_LICZBA_GRACZY = 2
MAX_LICZBA_GRACZY = 5


class Gra:
    def __init__(self):
        self.gracze = []        
        self._kwota_poczatkowa = KWOTA_POCZATKOWA
        self.liczbaGraczy = 0
        self.sumaOczek = 0
        self.kolejnyRzutKostka = False

    def przygotuj_graczy(self):
        while True:
            self.liczbaGraczy = int(input("Podaj liczbe graczy: "))
            if self.liczbaGraczy >= MIN_LICZBA_GRACZY and self.liczbaGraczy <= MAX_LICZBA_GRACZY:
                break
            else:
                print("niepoprawna ilosc graczy")

        self.aktualnyGracz = random.randint(1, self.liczbaGraczy)

        for i in range(1, self.liczbaGraczy + 1):
            gracz = Gracz(i, self._kwota_poczatkowa)
            self.gracze.append(gracz)


    def wybierzKolejnegoGracza(self):
        self.sumaOczek = 0
        while True:
            if not self.gracze[self.aktualnyGracz - 1].uwiezienie:
                break
            else:
                self.gracze[self.aktualnyGracz - 1].odczekajJednaTure()
                self.aktualnyGracz = (self.aktualnyGracz + 1) % self.liczbaGraczy
                self.sumaOczek = 0


    def analizujRzut(self, kostkaPierwsza, kostkaDruga):

        if(kostkaPierwsza + kostkaDruga == 7):
            self.kolejnyRzutKostka = True
            print("siodemka, rzuc jeszcze raz")
        else:
            self.kolejnyRzutKostka = False
            print("nastepny gracz")

        print()

        #koniec tury, gracz idzie do wiezienia
        if self.sumaOczek == 21:
            print("idziesz do wiezienia")
            self.gracze[self.aktualnyGracz - 1].uwiezienie = True
            self.kolejnyRzutKostka = False
            return



    def tura(self):

        #wybieranie nastepnego gracza w kolejce 
        if not self.kolejnyRzutKostka:
            self.wybierzKolejnegoGracza()
        
        print("ruch gracza:", self.aktualnyGracz)

        kostkaPierwsza = random.randint(1, 6)
        kostkaDruga = random.randint(1, 6)
        self.sumaOczek += (kostkaPierwsza + kostkaDruga)

        print("kostka pierwsza:", kostkaPierwsza, ", kostka druga:", kostkaDruga)
        print("suma:", self.sumaOczek)
        
        self.analizujRzut(kostkaPierwsza, kostkaDruga)

        #zapetlenie graczy
        if not self.kolejnyRzutKostka:
            self.aktualnyGracz += 1
            if self.aktualnyGracz == self.liczbaGraczy + 1:
                self.aktualnyGracz = 1

