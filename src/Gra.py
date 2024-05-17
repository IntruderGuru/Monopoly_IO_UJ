import random
from src.Gracz import Gracz

KWOTA_POCZATKOWA = 10000
MIN_LICZBA_GRACZY = 2
MAX_LICZBA_GRACZY = 5


class Gra:
    def __init__(self):
        self.gracze = []        
        self._kwota_poczatkowa = KWOTA_POCZATKOWA
        self._liczba_graczy = 0
        self._suma_oczek = 0
        self._kolejny_rzut_kostka = False

    def przygotuj_graczy(self):
        while True:
            self._liczba_graczy = int(input("Podaj liczbe graczy: "))
            if self._liczba_graczy >= MIN_LICZBA_GRACZY and self._liczba_graczy <= MAX_LICZBA_GRACZY:
                break
            else:
                print("niepoprawna ilosc graczy")

        self._aktualny_gracz = random.randint(1, self._liczba_graczy)

        for i in range(1, self._liczba_graczy + 1):
            gracz = Gracz(i, self._kwota_poczatkowa)
            self.gracze.append(gracz)


    def wybierzKolejnegoGracza(self):
        self._suma_oczek = 0
        while True:
            if not self.gracze[self._aktualny_gracz - 1].uwiezienie:
                break
            else:
                self.gracze[self._aktualny_gracz - 1].odczekajJednaTure()
                self._aktualny_gracz = (self._aktualny_gracz + 1) % self._liczba_graczy
                self._suma_oczek = 0


    def analizujRzut(self, kostka_pierwsza, kostka_druga):

        if(kostka_pierwsza + kostka_druga == 7):
            self._kolejny_rzut_kostka = True
            print("siodemka, rzuc jeszcze raz")
        else:
            self._kolejny_rzut_kostka = False
            print("nastepny gracz")

        print()

        #koniec tury, gracz idzie do wiezienia
        if self._suma_oczek == 21:
            print("idziesz do wiezienia")
            self.gracze[self._aktualny_gracz - 1].uwiezienie = True
            self._kolejny_rzut_kostka = False
            return



    def tura(self):

        #wybieranie nastepnego gracza w kolejce 
        if not self._kolejny_rzut_kostka:
            self.wybierzKolejnegoGracza()
        
        print("ruch gracza:", self._aktualny_gracz)

        kostka_pierwsza = random.randint(1, 6)
        kostka_druga = random.randint(1, 6)
        self._suma_oczek += (kostka_pierwsza + kostka_druga)

        print("kostka pierwsza:", kostka_pierwsza, ", kostka druga:", kostka_druga)
        print("suma:", self._suma_oczek)
        
        self.analizujRzut(kostka_pierwsza, kostka_druga)

        #zapetlenie graczy
        if not self._kolejny_rzut_kostka:
            self._aktualny_gracz += 1
            if self._aktualny_gracz == self._liczba_graczy + 1:
                self._aktualny_gracz = 1

