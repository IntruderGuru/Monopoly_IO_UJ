import random
import pygame
from src.Gracz import Gracz
from src.Pole import Pole
from src.Pionek import Pionek

KWOTA_POCZATKOWA = 10000
MIN_LICZBA_GRACZY = 2
MAX_LICZBA_GRACZY = 5
LICZBA_POL = 40

# Dodajemy listę kolorów dla pionków jako obiekty pygame.Color
PIECE_COLORS = [
    pygame.Color("red"),
    pygame.Color("green"),
    pygame.Color("blue"),
    pygame.Color("yellow"),
    pygame.Color("purple"),
]


class Gra:
    def __init__(self):
        self.gracze = []
        self._kwota_poczatkowa = KWOTA_POCZATKOWA
        self._liczba_graczy = 0
        self._suma_oczek = 0
        self._kolejny_rzut_kostka = False
        self._aktualny_gracz = 0
        self.board = self.stworz_plansze()
        self.messages = []

    def stworz_plansze(self):
        board = []
        typy_pol = [
            "start",  # 0
            "posiadlosc_czerwona",  # 1
            "karta_szansy",  # 2
            "posiadlosc_czerwona",  # 3
            "posiadlosc_czerwona",  # 4
            "pojedyncza_posiadlosc",  # 5
            "posiadlosc_zolta",  # 6
            "posiadlosc_zolta",  # 7
            "inna_posiadlosc",  # 8
            "idz_do_wiezienia",  # 9
            "posiadlosc_zolta",  # 10
            "posiadlosc_zielona",  # 11
            "posiadlosc_zielona",  # 12
            "karta_szansy",  # 13
            "posiadlosc_zielona",  # 14
            "pojedyncza_posiadlosc",  # 15
            "karta_szansy",  # 16
            "posiadlosc_niebieska",  # 17
            "podatek_dochodowy",  # 18
            "posiadlosc_niebieska",  # 19
            "parking",  # 20
            "posiadlosc_brazowa",  # 21
            "karta_szansy",  # 22
            "posiadlosc_brazowa",  # 23
            "podatek_dochodowy",  # 24
            "pojedyncza_posiadlosc",  # 25
            "posiadlosc_niebieska",  # 26
            "karta_szansy",  # 27
            "posiadlosc_niebieska",  # 28
            "posiadlosc_niebieska",  # 29
            "wiezienie",  # 30
            "posiadlosc_rozowa",  # 31
            "inna_posiadlosc",  # 32
            "posiadlosc_rozowa",  # 33
            "posiadlosc_rozowa",  # 34
            "pojedyncza_posiadlosc",  # 35
            "posiadlosc_pomaranczowa",  # 36
            "karta_szansy",  # 37
            "posiadlosc_pomaranczowa",  # 38
            "posiadlosc_pomaranczowa",  # 39
        ]

        for numer, typ in enumerate(typy_pol):
            board.append(Pole(numer, typ))

        return board

    def przygotuj_graczy(self):
        self.messages.append(f"Liczba graczy: {self._liczba_graczy}")
        for i in range(1, self._liczba_graczy + 1):
            pionek = Pionek(0, PIECE_COLORS[i - 1], "path")
            gracz = Gracz(i, self._kwota_poczatkowa, pionek)
            gracz.pozycja = 0
            self.gracze.append(gracz)
            color = PIECE_COLORS[i - 1]
            self.messages.append(
                f"Gracz {i} gotowy z pionkiem w kolorze {color.r}, {color.g}, {color.b}"
            )

    def wybierzKolejnegoGracza(self):
        self._suma_oczek = 0
        poczatkowy_gracz = self._aktualny_gracz

        while True:
            if not self.gracze[self._aktualny_gracz - 1].uwiezienie:
                break
            else:
                self.gracze[self._aktualny_gracz - 1].odczekajJednaTure()
                self._aktualny_gracz = (self._aktualny_gracz % self._liczba_graczy) + 1
                self._suma_oczek = 0
                if self._aktualny_gracz == poczatkowy_gracz:
                    self.messages.append(
                        "Wszyscy gracze są w więzieniu. Przechodzimy do następnej tury."
                    )
                    break

    def analizujRzut(self, kostka_pierwsza, kostka_druga):
        if kostka_pierwsza + kostka_druga == 7:
            self._kolejny_rzut_kostka = True
            self.messages.append("Siódemka, rzuć jeszcze raz")
        else:
            self._kolejny_rzut_kostka = False

        if self._suma_oczek == 21:
            self.messages.append("Idziesz do więzienia")
            self.gracze[self._aktualny_gracz - 1].pozycja = 10
            self.gracze[self._aktualny_gracz - 1].uwiezienie = True
            self._kolejny_rzut_kostka = False

    def przesun_gracza(self, gracz, ruch):
        stara_pozycja = gracz.pionek.numer_pola
        nowa_pozycja = (stara_pozycja + ruch) % LICZBA_POL
        # gracz.pozycja = nowa_pozycja
        gracz.pionek.numer_pola = nowa_pozycja
        gracz.pionek.przesun(ruch)

        self.messages.append(
            f"Gracz {gracz.id} przesunął się z pozycji {stara_pozycja} na {nowa_pozycja}"
        )

        pole = self.board[nowa_pozycja]
        self.wykonaj_akcje_na_polu(gracz, pole)

    def wykonaj_akcje_na_polu(self, gracz, pole):
        self.messages.append(f"Pole {pole.typ}")
        if pole.typ == "wiezienie":
            self.messages.append("Gracz idzie do więzienia")
            gracz.uwiezienie = True

        elif pole.typ == "idz_do_wiezienia":
            self.messages.append("Gracz musi iść na pole 30 (więzienie)")
            # gracz.pozycja = 30
            gracz.uwiezienie = True
            # pole = self.board[30]

    def tura(self):
        if not self._kolejny_rzut_kostka:
            self.wybierzKolejnegoGracza()

        if not self.gracze[self._aktualny_gracz - 1].uwiezienie:
            self.messages.append(f"Ruch gracza: {self._aktualny_gracz}")

            kostka_pierwsza = random.randint(1, 6)
            kostka_druga = random.randint(1, 6)
            self._suma_oczek += kostka_pierwsza + kostka_druga

            self.messages.append(
                f"Kostka pierwsza: {kostka_pierwsza}, Kostka druga: {kostka_druga}"
            )
            self.messages.append(f"Suma: {self._suma_oczek}")

            self.analizujRzut(kostka_pierwsza, kostka_druga)
            self.przesun_gracza(
                self.gracze[self._aktualny_gracz - 1], kostka_pierwsza + kostka_druga
            )
        else:
            self.messages.append(f"Gracz {self._aktualny_gracz} jest w więzieniu.")

        if not self._kolejny_rzut_kostka:
            self._aktualny_gracz = (self._aktualny_gracz % self._liczba_graczy) + 1

    def get_messages(self):
        messages = self.messages.copy()
        self.messages.clear()
        return messages
