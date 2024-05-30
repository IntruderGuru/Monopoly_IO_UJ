import random
import pygame

from src.Okno.AkcjaPolaOkno import Okno, AkcjaPolaOkno
from src.Okno.AkcjaNieruchomosciOkno import AkcjaNieruchomosciOkno
from src.Okno.AkcjaKartOkno import AkcjaKartOkno
from src.Okno.AkcjaZastawOkno import AkcjaZastawOkno
from src.Okno.AkcjaZagadekOkno import AkcjaZagadekOkno
from src.Okno.AkcjaWiezieniaOkno import AkcjaWiezieniaOkno
from src.Wizualizator import Wizualizator
from src.Plansza import Plansza
from src.Posiadlosc import *
from src.Pionek import Pionek
from src.KontrolerWiadomosci import KontrolerWiadomosci


KWOTA_POCZATKOWA = 10000
MIN_LICZBA_GRACZY = 2
MAX_LICZBA_GRACZY = 5
LICZBA_POL = 40


# Dodajemy listę kolorów dla pionków jako obiekty pygame.Color
PIECE_COLORS: list[pygame.Color] = [
    pygame.Color("red"),
    pygame.Color("green"),
    pygame.Color("blue"),
    pygame.Color("yellow"),
    pygame.Color("purple"),
]


class Gra:
    def __init__(
        self,
        glowne_okno: pygame.Surface,
        kontroler_wiadomosci: KontrolerWiadomosci,
        liczba_graczy: int,
        gracze: list[str],
        wizualizator,
        szerokosc_ekranu,
        wysokosc_ekranu,
    ):
        self._glowne_okno: pygame.Surface = glowne_okno
        self._gracze = [
            Gracz(name, KWOTA_POCZATKOWA, Pionek(0, PIECE_COLORS[i], "path"))
            for i, name in enumerate(gracze)
        ]
        self._plansza: Plansza = Plansza()
        self._kwota_poczatkowa = KWOTA_POCZATKOWA
        self._liczba_graczy = liczba_graczy
        self._suma_oczek = 0
        self._kolejny_rzut_kostka = False
        self._aktualny_gracz = 1
        self.messages = []
        self.aktualna_szerokosc_ekranu = szerokosc_ekranu
        self.aktualna_wysokosc_ekranu = wysokosc_ekranu
        self._kontroler_wiadomosci = kontroler_wiadomosci
        self.wizualizator = wizualizator

        # sekcja wizualna
        self.kolor_przycisku = self.wizualizator.kolor_przycisku
        self.kolor_gdy_kursor = self.wizualizator.kolor_gdy_kursor
        self.kolor_tekstu = self.wizualizator.kolor_czcionki_na_przycisku
        self.kolor_tla = self.wizualizator.kolor_tla
        self.kolor_czcionki = self.wizualizator.kolor_czcionki

        # sekcja okien
        self._plansza = Plansza()

        self.akcja_pola_okno = AkcjaPolaOkno(self)
        self.akcja_nieruchomosci_okno = AkcjaNieruchomosciOkno(self)
        self.akcja_kart_okno = AkcjaKartOkno(self)
        self.akcja_zastaw_okno = AkcjaZastawOkno(self)
        self.akcja_zagadek_okno = AkcjaZagadekOkno(self)
        self.akcja_wiezienie_okno = AkcjaWiezieniaOkno(self)
        self.czy_akcja_zakonczona = True

    def przygotuj_graczy(self):
        self._kontroler_wiadomosci.dodaj_wiadomosc(
            f"Liczba graczy: {self._liczba_graczy}"
        )
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
                if not self._gracze[self._aktualny_gracz - 1].uwiezienie:
                    self._kontroler_wiadomosci.dodaj_wiadomosc(
                        f"Gracz {self._aktualny_gracz} opuszcza więzienie po dwóch turach"
                    )
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
            self.przesun_gracza_bez_raportu(self._gracze[self._aktualny_gracz - 1], 10)
            self._gracze[self._aktualny_gracz - 1].uwiezienie = True
            self._gracze[self._aktualny_gracz - 1].tury_w_wiezieniu = 0
            self._kolejny_rzut_kostka = False
            self._suma_oczek = 0

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

    def przesun_gracza_bez_raportu(self, gracz, nowa_pozycja):
        stara_pozycja = gracz.pionek.numer_pola
        gracz.pionek.przesun(40 - stara_pozycja + nowa_pozycja) % LICZBA_POL

    def akcja_kupienia_nieruchomosci(self, gracz, posiadlosc, nr_pola=1):
        if posiadlosc.kolor == "kolo" or posiadlosc.kolor == "pozaWmii":
            return
        if not gracz.caly_kolor(posiadlosc.kolor):
            self._kontroler_wiadomosci.dodaj_wiadomosc(
                "Nie posiadasz wszystkich kart z koloru, dlatego nie możesz jeszcze kupić domku"
            )
            return
        if posiadlosc.czy_zastawiona:
            self._kontroler_wiadomosci.dodaj_wiadomosc(
                "Nie można kupić domku lub hotelu na zastawionej posiadłości"
            )
            return

        nieruchomosc = gracz.czy_cztery_domki(posiadlosc)
        if nieruchomosc == "nie":
            self._kontroler_wiadomosci.dodaj_wiadomosc(
                f"Masz już 4 domki na tej posiadłości, aby kupić hotel, musisz mieć 4 domki na każdej posiadłości w kolorze {posiadlosc.kolor}"
            )
            return

        self.akcja_nieruchomosci_okno.czy_kupno = True
        self.akcja_nieruchomosci_okno.nieruchomosc = nieruchomosc

    def wykup_z_wiezienia_rzutem(self):
        liczba_siodemek = 0
        for x in range(3):
            kostka_pierwsza = random.randint(1, 6)
            kostka_druga = random.randint(1, 6)
            suma += kostka_pierwsza + kostka_druga
            if suma == 7:
                liczba_siodemek += 1
            self._kontroler_wiadomosci.dodaj_wiadomosc(
                f"Kostka pierwsza: {kostka_pierwsza}, Kostka druga: {kostka_druga}"
            )
        if liczba_siodemek < 2:
            self._kontroler_wiadomosci.dodaj_wiadomosc(
                f"Niestety, wyrzuciłeś tylko {liczba_siodemek} siódemek. Nie udało Ci się wykupić z więzienia, musisz odsiedzieć wyrok"
            )
            return False
        self._kontroler_wiadomosci.dodaj_wiadomosc(
            f"Gratulacje! Wyrzuciłeś {liczba_siodemek} siódemek. Udało Ci się wykupić z więzienia"
        )
        return True

    def wykonaj_akcje_na_polu(self, gracz, pole):
        self._kontroler_wiadomosci.dodaj_wiadomosc(pole.zwroc_info())

        if pole.typ == "Podatek dochodowy":
            self.czy_akcja_zakonczona = False
            self.akcja_zagadek_okno.akcja_podatkowa(gracz, pole)
            self.akcja_zagadek_okno.przygotuj_zagadke()
            self.akcja_zagadek_okno.czy_zagadka = True

        elif pole.typ == "Szansa":
            self.czy_akcja_zakonczona = False
            self.akcja_kart_okno.czy_szansa = True
            karta = self._plansza.karty.nastepna_karta()
            karta.wyswietl_tresc(self)
            karta.wykonaj_akcje(self, gracz)

        elif pole.typ == "Wiezienie":
            self._kontroler_wiadomosci.dodaj_wiadomosc("Gracz odwiedza więzienie")

        # TODO: mozliwosc wykupienia sie z wiezienia za pomoca wyrzucenia 2 siodemek na 3 rzuty kostka
        elif pole.typ == "idz_do_wiezienia":
            self._kontroler_wiadomosci.dodaj_wiadomosc("Gracz idzie do więzienia")
            if self.wykup_z_wiezienia_rzutem():
                return
            if not gracz.liczba_kart_wyjdz_z_wiezienia:
                self.czy_akcja_zakonczona = False
                self.akcja_wiezienie_okno.czy_wiezienie = True
                gracz.uwiezienie = True
                self.przesun_gracza_bez_raportu(
                    self._gracze[self._aktualny_gracz - 1], 10
                )
            else:
                gracz.liczba_kart_wyjdz_z_wiezienia -= 1
                self._kontroler_wiadomosci.dodaj_wiadomosc(
                    "Wykorzystano kartę 'wyjdź bezpłatnie z więzienia'"
                )

        elif pole.typ == "Posiadlosc":
            if isinstance(pole, Posiadlosc):
                posiadlosc = pole
                posiadlosc.wyswietl_info(self)
                if posiadlosc.wlasciciel is None:
                    self.czy_akcja_zakonczona = False
                    self.akcja_pola_okno.czy_akcja_pola = True
                    self.akcja_pola_okno.akcja_kupowania(posiadlosc, gracz)
                elif posiadlosc.wlasciciel == gracz.id:
                    self.czy_akcja_zakonczona = False
                    self.akcja_kupienia_nieruchomosci(gracz, posiadlosc)
                    self.akcja_nieruchomosci_okno.akcja_kupowania(posiadlosc, gracz)
                else:
                    self._kontroler_wiadomosci.dodaj_wiadomosc("Gracz płaci czynsz")
                    gracz.zaplac_czynsz(self, posiadlosc)
            else:
                raise Exception("Błąd. Posiadłość jest innym polem")

    def tura(self):
        if not self._kolejny_rzut_kostka:
            self.wybierz_kolejnego_gracza()

        if not self._gracze[self._aktualny_gracz - 1].uwiezienie:
            self._kontroler_wiadomosci.dodaj_wiadomosc(
                f"Ruch gracza: {self._aktualny_gracz}"
            )

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
            self._kontroler_wiadomosci.dodaj_wiadomosc(
                f"Gracz {self._aktualny_gracz} jest w więzieniu."
            )
            self.wybierz_kolejnego_gracza()

        if not self._kolejny_rzut_kostka:
            self._aktualny_gracz = (self._aktualny_gracz % self._liczba_graczy) + 1
            self._kontroler_wiadomosci.dodaj_wiadomosc(
                f"Teraz tura gracza: {self._aktualny_gracz}"
            )

    def aktualizacja_zdarzenia(self, event: pygame.event.Event):
        if (
            event.type == pygame.KEYDOWN
            and event.key == pygame.K_SPACE
            and self.czy_akcja_zakonczona
        ):
            self.tura()

        self.akcja_pola_okno.aktualizacja_zdarzen(event)
        self.akcja_nieruchomosci_okno.aktualizacja_zdarzen(event)
        self.akcja_kart_okno.aktualizacja_zdarzen(event)
        self.akcja_zastaw_okno.aktualizacja_zdarzen(event)
        self.akcja_zagadek_okno.aktualizacja_zdarzen(event)
        self.akcja_wiezienie_okno.aktualizacja_zdarzen(event)

    def wyswietl(self):

        self.aktualizuj_rozmiar_okien()
        self._plansza.render(self._glowne_okno)

        for gracz in self._gracze:
            gracz.pionek.wyswietl(self._glowne_okno)

        self.akcja_pola_okno.wyswietl(self._glowne_okno)
        self.akcja_nieruchomosci_okno.wyswietl(self._glowne_okno)
        self.akcja_kart_okno.wyswietl(self._glowne_okno)
        self.akcja_zastaw_okno.wyswietl(self._glowne_okno)
        self.akcja_zagadek_okno.wyswietl(self._glowne_okno)
        self.akcja_wiezienie_okno.wyswietl(self._glowne_okno)

    def aktualizuj_rozmiar_okien(self):
        self.akcja_pola_okno.aktualizuj_rozmiar_okna(
            self.aktualna_szerokosc_ekranu, self.aktualna_wysokosc_ekranu
        )
        self.akcja_nieruchomosci_okno.aktualizuj_rozmiar_okna(
            self.aktualna_szerokosc_ekranu, self.aktualna_wysokosc_ekranu
        )
        self.akcja_kart_okno.aktualizuj_rozmiar_okna(
            self.aktualna_szerokosc_ekranu, self.aktualna_wysokosc_ekranu
        )
        self.akcja_zagadek_okno.aktualizuj_rozmiar_okna(
            self.aktualna_szerokosc_ekranu, self.aktualna_wysokosc_ekranu
        )
        self.akcja_wiezienie_okno.aktualizuj_rozmiar_okna(
            self.aktualna_szerokosc_ekranu, self.aktualna_wysokosc_ekranu
        )
        self.akcja_zastaw_okno.aktualizuj_rozmiar_okna(
            self.aktualna_szerokosc_ekranu, self.aktualna_wysokosc_ekranu
        )
