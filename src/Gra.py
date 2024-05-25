import random
import pygame

from src.Okno.AkcjaPolaOkno import AkcjaPolaOkno
from src.Okno.AkcjaNieruchomosciOkno import AkcjaNieruchomosciOkno
from src.Okno.AkcjaKartOkno import AkcjaKartOkno
from src.Okno.AkcjaZagadekOkno import AkcjaZagadekOkno
from src.Plansza import Plansza
from src.Posiadlosc import *
from src.Pionek import Pionek

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


class Gra:
    def __init__(self, glowne_okno: pygame.Surface):
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

        self._plansza = Plansza()
        self.akcja_pola_okno = AkcjaPolaOkno(self)
        self.akcja_nieruchomosci_okno = AkcjaNieruchomosciOkno(self)
        self.akcja_kart_okno = AkcjaKartOkno(self)
        self.akcja_zagadek_okno = AkcjaZagadekOkno(self)


    def przygotuj_graczy(self):
        self.messages.append(f"Liczba graczy: {self._liczba_graczy}")
        for i in range(1, self._liczba_graczy + 1):
            pionek = Pionek(0, PIECE_COLORS[i - 1], "path")
            gracz = Gracz(i, self._kwota_poczatkowa, pionek)
            gracz.pozycja = 0
            self._gracze.append(gracz)
            color = PIECE_COLORS[i - 1]
            self.messages.append(
                f"Gracz {i} gotowy z pionkiem w kolorze {color.r}, {color.g}, {color.b}"
            )

    def wybierz_kolejnego_gracza(self):
        self._suma_oczek = 0
        poczatkowy_gracz = self._aktualny_gracz

        while True:
            if not self._gracze[self._aktualny_gracz - 1].uwiezienie:
                break
            else:
                self._gracze[self._aktualny_gracz - 1].odczekajJednaTure()
                self._aktualny_gracz = (self._aktualny_gracz % self._liczba_graczy) + 1
                self._suma_oczek = 0
                if self._aktualny_gracz == poczatkowy_gracz:
                    self.messages.append(
                        "Wszyscy gracze są w więzieniu. Przechodzimy do następnej tury."
                    )
                    break

    def analizuj_rzut(self, kostka_pierwsza, kostka_druga):
        if kostka_pierwsza + kostka_druga == 7:
            self._kolejny_rzut_kostka = True
            self.messages.append("Siódemka, rzuć jeszcze raz")
        else:
            self._kolejny_rzut_kostka = False

        if self._suma_oczek == 21:
            self.messages.append("Idziesz do więzienia")
            self._gracze[self._aktualny_gracz - 1].pozycja = 10
            self._gracze[self._aktualny_gracz - 1].uwiezienie = True
            self._kolejny_rzut_kostka = False

    def przesun_gracza(self, gracz, ruch):
        stara_pozycja = gracz.pionek.numer_pola
        nowa_pozycja = (stara_pozycja + ruch) % LICZBA_POL
        gracz.pionek.przesun(ruch)
        gracz.czy_przeszedl_przez_start(self, stara_pozycja)

        self.messages.append(
            f"Gracz {gracz.id} przesunął się z pozycji {stara_pozycja} na {nowa_pozycja}"
        )

        pole = self._plansza.pobierz_pole(nowa_pozycja)
        self.wykonaj_akcje_na_polu(gracz, pole)

    def akcja_dostepnego_pola(self, gracz, pole, nr_pola = 1):
        self.akcja_pola_okno.czy_akcja_pola = True

    def akcja_kupienia_nieruchomosci(self, gracz, posiadlosc, nr_pola = 1):
        self.akcja_nieruchomosci_okno.czy_kupno = True

        if posiadlosc.liczba_domow < 4:
            self.akcja_nieruchomosci_okno.nieruchomosc = "domek"
        else:
            self.akcja_nieruchomosci_okno.nieruchomosc = "hotel"


    def wykonaj_akcje_na_polu(self, gracz, pole):
        self.messages.append(pole.wyswietl_info())

        if pole.typ == "Podatek dochodowy":
            self.akcja_zagadek_okno.przygotuj_tekst_zagadki()
            self.akcja_zagadek_okno.czy_zagadka = True

        if pole.typ == "Szansa":
            self.akcja_kart_okno.czy_szansa = True

        if pole.typ == "wiezienie":
            self.messages.append("Gracz idzie do więzienia")
            gracz.uwiezienie = True

        elif pole.typ == "idz_do_wiezienia":
            self.messages.append("Gracz musi iść na pole 30 (więzienie)")
            gracz.uwiezienie = True

        elif pole.typ == "Posiadlosc":

            if isinstance(pole, Posiadlosc):
                posiadlosc = pole

            if posiadlosc.IDwlasciciela is None:
                self.akcja_dostepnego_pola(gracz, posiadlosc)
                self.akcja_pola_okno.akcja_kupowania(posiadlosc, gracz)
            elif posiadlosc.IDwlasciciela == gracz.id:
                self.akcja_kupienia_nieruchomosci(gracz, posiadlosc)
                self.akcja_nieruchomosci_okno.akcja_kupowania(posiadlosc, gracz)
            else:
                pass

    def tura(self):

        if not self._kolejny_rzut_kostka:
            self.wybierz_kolejnego_gracza()

        if not self._gracze[self._aktualny_gracz - 1].uwiezienie:
            self.messages.append(f"Ruch gracza: {self._aktualny_gracz}")

            kostka_pierwsza = random.randint(1, 6)
            kostka_druga = random.randint(1, 6)
            self._suma_oczek += kostka_pierwsza + kostka_druga

            self.messages.append(
                f"Kostka pierwsza: {kostka_pierwsza}, Kostka druga: {kostka_druga}"
            )
            self.messages.append(f"Suma: {self._suma_oczek}")

            self.analizuj_rzut(kostka_pierwsza, kostka_druga)
            self.przesun_gracza(
                self._gracze[self._aktualny_gracz - 1], kostka_pierwsza + kostka_druga
            )
        else:
            self.messages.append(f"Gracz {self._aktualny_gracz} jest width więzieniu.")

        if not self._kolejny_rzut_kostka:
            self._aktualny_gracz = (self._aktualny_gracz % self._liczba_graczy) + 1

    def get_messages(self):
        messages = self.messages.copy()
        self.messages.clear()
        return messages

    def aktualizuj_zdarzenia(self, event: pygame.event.Event):
        self.akcja_pola_okno.aktualizacja_zdarzen(event)
        self.akcja_nieruchomosci_okno.aktualizacja_zdarzen(event)
        self.akcja_kart_okno.aktualizacja_zdarzen(event)
        self.akcja_zagadek_okno.aktualizacja_zdarzen(event)

    def wyswietl(self):
        self._plansza.render(self._glowne_okno)

        for gracz in self._gracze:
            gracz.pionek.wyswietl(self._glowne_okno)

        self.akcja_pola_okno.wyswietl(self._glowne_okno)
        self.akcja_nieruchomosci_okno.wyswietl(self._glowne_okno)
        self.akcja_kart_okno.wyswietl(self._glowne_okno)
        self.akcja_zagadek_okno.wyswietl(self._glowne_okno)