import random
from src.Gracz import Gracz
from src.Pole import Pole

KWOTA_POCZATKOWA = 10000
MIN_LICZBA_GRACZY = 2
MAX_LICZBA_GRACZY = 5
LICZBA_POL = 40


class Gra:
    def __init__(self):
        self.gracze = []
        self._kwota_poczatkowa = KWOTA_POCZATKOWA
        self._liczba_graczy = 0
        self._suma_oczek = 0
        self._kolejny_rzut_kostka = False
        self._aktualny_gracz = 0
        self.board = self.stworz_plansze()

    def stworz_plansze(self):

        # Create the board with properties and other special positions

        board = []

        typy_pol = [
            "start",
            "posiadlosc_brazowa",
            "karta_szansy",
            "posiadlosc_brazowa",
            "podatek_dochodowy",
            "pojedyncza_posiadlosc",
            "posiadlosc_niebieska",
            "karta_szansy",
            "posiadlosc_niebieska",
            "posiadlosc_niebieska",
            "wiezienie",
            "posiadlosc_rozowa",
            "inna_posiadlosc",
            "posiadlosc_rozowa",
            "posiadlosc_rozowa",
            "pojedyncza_posiadlosc",
            "posiadlosc_pomaranczowa",
            "karta_szansy",
            "posiadlosc_pomaranczowa",
            "posiadlosc_pomaranczowa",
            "parking",
            "posiadlosc_czerwona",
            "karta_szansy",
            "posiadlosc_czerwona",
            "posiadlosc_czerwona",
            "pojedyncza_posiadlosc",
            "posiadlosc_zolta",
            "posiadlosc_zolta",
            "inna_posiadlosc",
            "idz_na_10",
            "posiadlosc_zolta",
            "posiadlosc_zielona",
            "posiadlosc_zielona",
            "karta_szansy",
            "posiadlosc_zielona",
            "pojedyncza_posiadlosc",
            "karta_szansy",
            "posiadlosc_niebieska",
            "podatek_dochodowy",
            "posiadlosc_niebieska",
        ]

        for numer, typ in enumerate(typy_pol):

            board.append(Pole(numer, typ))

        return board

    def przygotuj_graczy(self):
        while True:
            self._liczba_graczy = int(input("Podaj liczbe graczy: "))
            if (
                self._liczba_graczy >= MIN_LICZBA_GRACZY
                and self._liczba_graczy <= MAX_LICZBA_GRACZY
            ):
                break
            else:
                print("niepoprawna ilosc graczy")

        self._aktualny_gracz = random.randint(1, self._liczba_graczy)

        for i in range(1, self._liczba_graczy + 1):
            gracz = Gracz(i, self._kwota_poczatkowa)
            gracz.pozycja = 0
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

        if kostka_pierwsza + kostka_druga == 7:
            self._kolejny_rzut_kostka = True
            print("siodemka, rzuc jeszcze raz")
        else:
            self._kolejny_rzut_kostka = False

        # koniec tury, gracz idzie do wiezienia
        if self._suma_oczek == 21:
            print("idziesz do wiezienia")
            self._aktualny_gracz.pozycja = 10
            self.gracze[self._aktualny_gracz - 1].uwiezienie = True
            self._kolejny_rzut_kostka = False
            return

    def przesun_gracza(self, gracz, ruch):

        stara_pozycja = gracz.pozycja

        nowa_pozycja = (stara_pozycja + ruch) % LICZBA_POL

        gracz.pozycja = nowa_pozycja

        print(
            f"Gracz {gracz.Id} przesunął się z pozycji {stara_pozycja} na {nowa_pozycja}"
        )

        pole = self.board[nowa_pozycja]

        self.wykonaj_akcje_na_polu(gracz, pole)
        print("nastepny gracz")
        print()

    def wykonaj_akcje_na_polu(self, gracz, pole):
        print(f"Pole {pole.typ}")
        if pole.typ == "wiezienie":

            print("Gracz idzie do więzienia")

            gracz.uwiezienie = True

        elif pole.typ == "idz_na_10":

            print("Gracz musi iść na pole 10 (więzienie)")

            gracz.pozycja = 10

            gracz.uwiezienie = True

        # Tutaj implementacje kolejnych pol itd.

    def tura(self):

        # wybieranie nastepnego gracza w kolejce
        if not self._kolejny_rzut_kostka:
            self.wybierzKolejnegoGracza()

        print("ruch gracza:", self._aktualny_gracz)

        kostka_pierwsza = random.randint(1, 6)
        kostka_druga = random.randint(1, 6)
        self._suma_oczek += kostka_pierwsza + kostka_druga

        print("kostka pierwsza:", kostka_pierwsza, ", kostka druga:", kostka_druga)
        print("suma:", self._suma_oczek)

        self.analizujRzut(kostka_pierwsza, kostka_druga)
        self.przesun_gracza(
            self.gracze[self._aktualny_gracz - 1], kostka_pierwsza + kostka_druga
        )
        # zapetlenie graczy
        if not self._kolejny_rzut_kostka:
            self._aktualny_gracz += 1
            if self._aktualny_gracz == self._liczba_graczy + 1:
                self._aktualny_gracz = 1
