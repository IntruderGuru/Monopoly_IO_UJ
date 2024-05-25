import random
import pygame

from src.Okno.AkcjaPolaOkno import Okno, AkcjaPolaOkno
from src.Plansza import Plansza
from src.Posiadlosc import *
from src.Pionek import Pionek
from src.KontrolerWiadomosci import KontrolerWiadomosci

KWOTA_POCZATKOWA = 10000
MIN_LICZBA_GRACZY = 2
MAX_LICZBA_GRACZY = 5
LICZBA_POL = 40


# Dodajemy listę kolorów dla pionków jako obiekty pygame.Color
PIECE_COLORS: [pygame.Color] = [
    pygame.Color("red"),
    pygame.Color("green"),
    pygame.Color("blue"),
    pygame.Color("yellow"),
    pygame.Color("purple"),
]


class StosOtwartychOkien:
    def __init__(self):
        self.stos: list[Okno] = list()
        self.rozmiar_stosu = 0

    def dodaj(self, okno: Okno):
        self.stos.append(okno)
        self.rozmiar_stosu += 1

    def usun(self):
        if self.rozmiar_stosu > 0:
            self.stos.pop()
            self.rozmiar_stosu -= 1

    def gora(self):
        return self.stos[self.rozmiar_stosu - 1]

    def czy_pusty(self):
        return self.rozmiar_stosu == 0

    def aktualizacja(self):
        if not self.czy_pusty():
            self.gora().aktualizacja()

    def aktualizacja_zdarzen(self, event: pygame.event.Event):
        if not self.czy_pusty():
            self.gora().aktulizacja_zdarzen(event)

    def wyswietl(self, okno: pygame.Surface):
        if not self.czy_pusty():
            self.gora().wyswietl(okno)


class Gra:
    def __init__(self, glowne_okno: pygame.Surface, kontroler_wiadomosci: KontrolerWiadomosci):
        self._glowne_okno: pygame.Surface = glowne_okno
        self._gracze: list[Gracz] = []
        self._plansza: Plansza = Plansza()
        self._kwota_poczatkowa = KWOTA_POCZATKOWA
        self._liczba_graczy = 0
        self._suma_oczek = 0
        self._kolejny_rzut_kostka = False
        self._aktualny_gracz = 0
        self.messages = []
        self.aktualna_szerokosc_ekranu = 1200
        self.aktualna_wysokosc_ekranu = 800
        self._kontroler_wiadomosci = kontroler_wiadomosci

        self._plansza = Plansza()
        self._akcja_pola_okno = AkcjaPolaOkno()

        #
        self._czy_gracz_ma_ture = False
        self._stos_otwartych_okien = StosOtwartychOkien()

    def przygotuj_graczy(self):
        self._kontroler_wiadomosci.dodaj_wiadomosc(f"Liczba graczy: {self._liczba_graczy}")
        for i in range(1, self._liczba_graczy + 1):
            pionek = Pionek(0, PIECE_COLORS[i - 1], "path")
            gracz = Gracz(i, self._kwota_poczatkowa, pionek)
            gracz.pozycja = 0
            self._gracze.append(gracz)
            color = PIECE_COLORS[i - 1]
            self._kontroler_wiadomosci.dodaj_wiadomosc(
                f"Gracz {i} gotowy z pionkiem w kolorze {color.r}, {color.g}, {color.b}"
            )

    def wybierz_kolejnego_gracza(self):
        self._suma_oczek = 0
        poczatkowy_gracz = self._aktualny_gracz

        while True:
            if not self._gracze[self._aktualny_gracz - 1].uwiezienie:
                self._czy_gracz_ma_ture = True
                break
            else:
                self._gracze[self._aktualny_gracz - 1].odczekajJednaTure()
                self._aktualny_gracz = (self._aktualny_gracz % self._liczba_graczy) + 1
                self._suma_oczek = 0
                if self._aktualny_gracz == poczatkowy_gracz:
                    self._kontroler_wiadomosci.dodaj_wiadomosc(
                        "Wszyscy gracze są w więzieniu. Przechodzimy do następnej tury."
                    )
                    break

    def analizuj_rzut(self, kostka_pierwsza, kostka_druga):
        if kostka_pierwsza + kostka_druga == 7:
            self._kolejny_rzut_kostka = True
            self._kontroler_wiadomosci.dodaj_wiadomosc("Siódemka, rzuć jeszcze raz")
        else:
            self._kolejny_rzut_kostka = False

        if self._suma_oczek == 21:
            self._kontroler_wiadomosci.dodaj_wiadomosc("Idziesz do więzienia")
            self._gracze[self._aktualny_gracz - 1].pozycja = 10
            self._gracze[self._aktualny_gracz - 1].uwiezienie = True
            self._kolejny_rzut_kostka = False

    def przesun_gracza(self, gracz, ruch):
        stara_pozycja = gracz.pionek.numer_pola
        nowa_pozycja = (stara_pozycja + ruch) % LICZBA_POL
        gracz.pionek.przesun(ruch)
        gracz.czy_przeszedl_przez_start(self, stara_pozycja)

        self._kontroler_wiadomosci.dodaj_wiadomosc(
            f"Gracz {gracz.id} przesunął się z pozycji {stara_pozycja} na {nowa_pozycja}"
        )

        pole = self._plansza.pobierz_pole(nowa_pozycja)
        self.wykonaj_akcje_na_polu(gracz, pole)

    def wykonaj_akcje_na_polu(self, gracz, pole):
        self._kontroler_wiadomosci.dodaj_wiadomosc(pole.zwroc_info())

        if pole.typ == "wiezienie":
            self._kontroler_wiadomosci.dodaj_wiadomosc("Gracz idzie do więzienia")
            gracz.uwiezienie = True

        elif pole.typ == "idz_do_wiezienia":
            self._kontroler_wiadomosci.dodaj_wiadomosc("Gracz musi iść na pole 30 (więzienie)")
            gracz.uwiezienie = True

        elif pole.typ == "Posiadlosc":
            if isinstance(pole, Posiadlosc):
                self._akcja_pola_okno.okno_kup_nieruchomosc(gracz, pole)
                self._stos_otwartych_okien.dodaj(self._akcja_pola_okno)

    def tura(self):
        if not self._kolejny_rzut_kostka:
            self.wybierz_kolejnego_gracza()

        if not self._gracze[self._aktualny_gracz - 1].uwiezienie:
            self._kontroler_wiadomosci.dodaj_wiadomosc(f"Ruch gracza: {self._aktualny_gracz}")

            kostka_pierwsza = random.randint(1, 6)
            kostka_druga = random.randint(1, 6)
            self._suma_oczek += kostka_pierwsza + kostka_druga

            self._kontroler_wiadomosci.dodaj_wiadomosc(
                f"Kostka pierwsza: {kostka_pierwsza}, Kostka druga: {kostka_druga}"
            )
            self._kontroler_wiadomosci.dodaj_wiadomosc(f"Suma: {self._suma_oczek}")

            self.analizuj_rzut(kostka_pierwsza, kostka_druga)
            self.przesun_gracza(
                self._gracze[self._aktualny_gracz - 1], kostka_pierwsza + kostka_druga
            )
        else:
            self._kontroler_wiadomosci.dodaj_wiadomosc(f"Gracz {self._aktualny_gracz} jest w więzieniu.")

        if not self._kolejny_rzut_kostka:
            self._aktualny_gracz = (self._aktualny_gracz % self._liczba_graczy) + 1

    def get_messages(self):
        messages = self.messages.copy()
        self.messages.clear()
        return messages

    def aktualizacja(self):
        if not self._stos_otwartych_okien.czy_pusty():
            self._stos_otwartych_okien.gora().aktualizacja()

        if not self._akcja_pola_okno.czy_koniec_zakupu():
            self._czy_gracz_ma_ture = False
            self._stos_otwartych_okien.usun()

    def aktualizacja_zdarzenia(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not self._czy_gracz_ma_ture:
            self._czy_gracz_ma_ture = True
            self.tura()

        # self._akcja_pola_okno.aktulizacja_zdarzen(event)
        if not self._stos_otwartych_okien.czy_pusty():
            self._stos_otwartych_okien.gora().aktulizacja_zdarzen(event)

    def wyswietl(self):
        self._plansza.render(self._glowne_okno)

        for gracz in self._gracze:
            gracz.pionek.wyswietl(self._glowne_okno)

        # self._akcja_pola_okno.wyswietl(self._glowne_okno)
        if not self._stos_otwartych_okien.czy_pusty():
            self._stos_otwartych_okien.gora().wyswietl(self._glowne_okno)
