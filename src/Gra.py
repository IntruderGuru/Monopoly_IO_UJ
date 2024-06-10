import random
import pygame
import pickle

from src.okno.AkcjaPolaOkno import AkcjaPolaOkno
from src.okno.AkcjaNieruchomosciOkno import AkcjaNieruchomosciOkno
from src.okno.AkcjaKartOkno import AkcjaKartOkno
from src.okno.AkcjaZastawOkno import AkcjaZastawOkno
from src.okno.AkcjaZagadekOkno import AkcjaZagadekOkno
from src.okno.AkcjaWiezieniaOkno import AkcjaWiezieniaOkno
from src.okno.AkcjaStatystykOkno import AkcjaStatystykOkno
from src.Wizualizator import Wizualizator
from src.Plansza import Plansza
from src.Posiadlosc import *
from src.Pionek import Pionek
from src.KontrolerWiadomosci import KontrolerWiadomosci
from src.interface.IGra import IGra
from src.Przycisk import Przycisk


KWOTA_POCZATKOWA = 16000
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

umiejetnosci = [
    "wiecej_pieniedzy_na_start",
    "porusza_sie_o_1_pole_wiecej",
    "karta_wyjscia_z_wiezienia",
    "sprzedaje_nieruchomosci_za_oryginalna_ceny",
    "dostaje_wiecej_za_przejscie_przez_start",
    "placi_mniejsze_czynsze",
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
        main_ref,
    ):
        random.shuffle(umiejetnosci)
        self._glowne_okno: pygame.Surface = glowne_okno
        self._kwota_poczatkowa = KWOTA_POCZATKOWA
        self._liczba_graczy = liczba_graczy
        self._suma_oczek = 0
        self._kolejny_rzut_kostka = False
        self._indeks_aktualnego_gracza = 0
        self.messages = []
        self.aktualna_szerokosc_ekranu = szerokosc_ekranu
        self.aktualna_wysokosc_ekranu = wysokosc_ekranu
        self._kontroler_wiadomosci = kontroler_wiadomosci
        self.wizualizator = wizualizator
        self._gracze = self.stworz_graczy(gracze)
        self.main = main_ref

        # sekcja wizualna
        self.kolor_przycisku = self.wizualizator.kolor_przycisku
        self.kolor_gdy_kursor = self.wizualizator.kolor_gdy_kursor
        self.kolor_tekstu = self.wizualizator.kolor_czcionki_na_przycisku
        self.kolor_tla = self.wizualizator.kolor_tla
        self.kolor_czcionki = self.wizualizator.kolor_czcionki
        self.kolor_czcionki_tyl_karty = self.wizualizator.kolor_czcionki_tyl_karty
        self.czcionka = self.wizualizator.czcionka
        self.kolor_nakladki = self.wizualizator.kolor_nakladki
        self.przezroczystosc_nakladki = self.wizualizator.przezroczystosc_nakladki
        self.font = pygame.font.Font(self.czcionka, 20)
        self.end_game_flag = 1

        # sekcja okien
        self._plansza = Plansza()
        self._plansza.aktualizacja_rozmiaru(
            self.aktualna_szerokosc_ekranu, self.aktualna_wysokosc_ekranu
        )

        self.akcja_pola_okno = AkcjaPolaOkno(self)
        self.akcja_nieruchomosci_okno = AkcjaNieruchomosciOkno(self)
        self.akcja_kart_okno = AkcjaKartOkno(self)
        self.akcja_zastaw_okno = AkcjaZastawOkno(self)
        self.akcja_zagadek_okno = AkcjaZagadekOkno(self)
        self.akcja_wiezienie_okno = AkcjaWiezieniaOkno(self)
        self.akcja_statystyk_okno = AkcjaStatystykOkno(self)
        self.czy_akcja_zakonczona = True

        # Załaduj obrazy kostek
        self.dice_images = []
        for i in range(1, 7):
            image_path = f"graphics/dice/dice{i}.png"
            image = pygame.image.load(image_path)
            self.dice_images.append(pygame.transform.scale(image, (100, 100)))

        # feature_testingMechanism
        self.input_text = ""
        print("HELLO from Gra")
        self._plansza.plansza[0].ilosc_graczy_na_polu = liczba_graczy

        # nowa tura
        self.nastepna_tura = Przycisk(
            szerokosc_ekranu * 0.3,
            wysokosc_ekranu * 0.7,
            szerokosc_ekranu * 0.2,
            wysokosc_ekranu * 0.15,
            self.wizualizator.kolor_przycisku_tury,
            self.wizualizator.kolor_przycisku_tury_gdy_kursor,
            "tura",
            self.wizualizator.kolor_czcionki,
            26,
        )
        self.zapisz_wyjdz = Przycisk(
            szerokosc_ekranu * 0.3,
            wysokosc_ekranu * 0.75,
            szerokosc_ekranu * 0.2,
            wysokosc_ekranu * 0.15,
            self.wizualizator.kolor_przycisku_tury,
            self.wizualizator.kolor_przycisku_tury_gdy_kursor,
            "Zapisz i wyjdz",
            self.wizualizator.kolor_czcionki,
            8,
        )

        self.gracz_poprzedniej_tury = -1
        self.zwyciezca = -1
        self.waiter = 4

    def stworz_graczy(self, nazwy_graczy) -> list[Gracz]:
        lista_graczy = [
            Gracz(
                name,
                KWOTA_POCZATKOWA,
                Pionek(
                    0,
                    PIECE_COLORS[i],
                    "graphics/pionek/PionekColor" + str(i + 1) + ".png",
                    self.aktualna_szerokosc_ekranu,
                    self.aktualna_wysokosc_ekranu,
                    self._liczba_graczy,
                ),
                umiejetnosci[i],
            )
            for i, name in enumerate(nazwy_graczy)
        ]

        return lista_graczy

    def analizuj_rzut(self, kostka_pierwsza, kostka_druga, bonus):
        self._kolejny_rzut_kostka = False

        if kostka_pierwsza + kostka_druga == 7:
            self._kolejny_rzut_kostka = True
            self._kontroler_wiadomosci.dodaj_wiadomosc(
                "Siódemka, otrzymujesz dodatkową turę"
            )

        if self._suma_oczek == 21:
            self._kontroler_wiadomosci.dodaj_wiadomosc(
                "Uzyskałeś logarytmiczne przyspieszenie. Idziesz do więzienia"
            )
            self.przesun_gracza_bez_raportu(
                self._gracze[self._indeks_aktualnego_gracza], 10
            )
            self._gracze[self._indeks_aktualnego_gracza].tury_w_wiezieniu = 2
            self.akcja_wiezienie_okno.czy_wiezienie = True
            self._kolejny_rzut_kostka = False
        else:
            self.przesun_gracza(
                self._gracze[self._indeks_aktualnego_gracza],
                kostka_pierwsza + kostka_druga + bonus,
            )

    def wyswietl_kostki(self, screen, dice1, dice2):
        # im wieksze tym mniejszy odstep
        oddalenie_kostek_od_siebie = 8.1
        self.aktualizuj_rozmiar_kostek()
        dice_x = self.aktualna_szerokosc_ekranu * 0.213
        dice_y = self.aktualna_wysokosc_ekranu * 0.38
        screen.blit(self.dice_images[dice1 - 1], (dice_x, dice_y))
        screen.blit(
            self.dice_images[dice2 - 1],
            (
                dice_x + (self.aktualna_wysokosc_ekranu / oddalenie_kostek_od_siebie),
                dice_y,
            ),
        )

    def aktualizuj_rozmiar_kostek(self):
        # im wiekszy tym mniejsze kostki
        skalar_kostek = 10

        for i in range(1, 7):
            image_path = f"graphics/dice/dice{i}.png"
            image = pygame.image.load(image_path)
            self.dice_images[i - 1] = pygame.transform.scale(
                image,
                (
                    self.aktualna_wysokosc_ekranu / skalar_kostek,
                    self.aktualna_wysokosc_ekranu / skalar_kostek,
                ),
            )

    def symuluj_rzut(self):
        liczba_klatek = 5  # Liczba klatek animacji
        for _ in range(liczba_klatek):
            # Losowe wartości dla obu kostek
            dice1 = random.randint(1, 6)
            dice2 = random.randint(1, 6)
            self.wyswietl_kostki(self._glowne_okno, dice1, dice2)
            pygame.display.update()
            pygame.time.wait(75)  # Czas oczekiwania między klatkami animacji

        # Ostateczne wartości kostek
        kostka_1 = random.randint(1, 6)
        kostka_2 = random.randint(1, 6)
        return kostka_1, kostka_2

    def przesun_gracza(self, gracz, ruch):
        stara_pozycja = gracz.pionek.numer_pola
        nowa_pozycja = (stara_pozycja + ruch) % LICZBA_POL
        gracz.pionek.przesun(ruch, self)
        gracz.czy_przeszedl_przez_start(self, stara_pozycja)

        self._kontroler_wiadomosci.dodaj_wiadomosc(
            f"Gracz {gracz.id} przesunął się z pozycji {stara_pozycja} na {nowa_pozycja}"
        )
        gracz.pionek.wyswietl(self._glowne_okno, self)
        pole = self._plansza.pobierz_pole(nowa_pozycja)
        self.wykonaj_akcje_na_polu(gracz, pole)

    def przesun_gracza_bez_raportu(self, gracz, nowa_pozycja):
        stara_pozycja = gracz.pionek.numer_pola
        gracz.pionek.przesun((nowa_pozycja - stara_pozycja) % LICZBA_POL, self)
        gracz.pionek.wyswietl(self._glowne_okno, self)

    def akcja_kupienia_nieruchomosci(self, gracz, posiadlosc, nr_pola=1):
        if posiadlosc.kolor == "kolo" or posiadlosc.kolor == "pozaWmii":
            return
        if not gracz.caly_kolor(posiadlosc.kolor):
            self._kontroler_wiadomosci.dodaj_wiadomosc(
                "Nie posiadasz wszystkich kart z koloru"
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
                f"Masz już 4 domki na tym polu. Kup domy na innych polach {posiadlosc.kolor}"
            )
            return

        self.akcja_nieruchomosci_okno.czy_kupno = True
        self.akcja_nieruchomosci_okno.nieruchomosc = nieruchomosc
        self.czy_akcja_zakonczona = False

    def wykup_z_wiezienia_rzutem(self):
        liczba_siodemek = 0
        for x in range(3):
            kostka_pierwsza, kostka_druga = self.symuluj_rzut()
            suma = kostka_pierwsza + kostka_druga
            if suma == 7:
                liczba_siodemek += 1
            self._kontroler_wiadomosci.dodaj_wiadomosc(
                f"Kostka pierwsza: {kostka_pierwsza}, Kostka druga: {kostka_druga}"
            )
            self.wyswietl_kostki(self._glowne_okno, kostka_pierwsza, kostka_druga)
            pygame.display.update()  # Aktualizuj ekran po wyświetleniu kostek
            pygame.time.wait(1000)

        if liczba_siodemek < 2:
            self._kontroler_wiadomosci.dodaj_wiadomosc(
                f"Wyrzuciłeś {liczba_siodemek} siódemek. Idziesz do więzienia"
            )
            return False
        self._kontroler_wiadomosci.dodaj_wiadomosc(
            f"Wyrzuciłeś {liczba_siodemek} siódemek. Unikasz więzienia"
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
            self.akcja_kart_okno.przygotuj_karte(gracz)

        elif pole.typ == "Wiezienie":
            self._kontroler_wiadomosci.dodaj_wiadomosc("Gracz odwiedza więzienie")

        elif pole.typ == "Idz do wiezienia":
            self._kontroler_wiadomosci.dodaj_wiadomosc("Gracz idzie do więzienia")
            if self.wykup_z_wiezienia_rzutem():
                self.czy_akcja_zakonczona = True
                return
            if gracz.liczba_kart_wyjdz_z_wiezienia > 0:
                gracz.liczba_kart_wyjdz_z_wiezienia -= 1
                self._kontroler_wiadomosci.dodaj_wiadomosc(
                    "Wykorzystano kartę 'wyjdź bezpłatnie z więzienia'"
                )
            else:
                self.akcja_wiezienie_okno.czy_wiezienie = True
                self.czy_akcja_zakonczona = False
                gracz.tury_w_wiezieniu = 2
                self.przesun_gracza_bez_raportu(
                    self._gracze[self._indeks_aktualnego_gracza], 10
                )

        elif pole.typ == "Posiadlosc":
            if isinstance(pole, Posiadlosc):
                posiadlosc = pole
                # posiadlosc.wyswietl_info(self)
                if posiadlosc.wlasciciel is None:
                    self.czy_akcja_zakonczona = False
                    self.akcja_pola_okno.czy_akcja_pola = True
                    self.akcja_pola_okno.akcja_kupowania(posiadlosc, gracz)
                elif posiadlosc.wlasciciel == gracz:
                    self.akcja_kupienia_nieruchomosci(gracz, posiadlosc)
                    self.akcja_nieruchomosci_okno.akcja_kupowania(posiadlosc, gracz)
                else:
                    if posiadlosc.czy_zastawiona:
                        return
                    self._kontroler_wiadomosci.dodaj_wiadomosc("Gracz płaci czynsz")
                    gracz.zaplac_czynsz(self, posiadlosc)
            else:
                raise Exception("Błąd. Posiadłość jest innym polem")

    def tura(self):

        if self.gracz_poprzedniej_tury != self._indeks_aktualnego_gracza:
            self._kontroler_wiadomosci.usun_wszystkie_wiadomosci()
        self.gracz_poprzedniej_tury = self._indeks_aktualnego_gracza

        self._kontroler_wiadomosci.dodaj_wiadomosc(
            f"Teraz tura gracza: {self._gracze[self._indeks_aktualnego_gracza].id}"
        )

        if self._gracze[self._indeks_aktualnego_gracza].tury_w_wiezieniu:
            self._gracze[self._indeks_aktualnego_gracza].tury_w_wiezieniu -= 1
            if self._gracze[self._indeks_aktualnego_gracza].tury_w_wiezieniu == 0:
                self._kontroler_wiadomosci.dodaj_wiadomosc(
                    f"Gracz {self._indeks_aktualnego_gracza + 1} opuszcza więzienie"
                )
            else:
                self._kontroler_wiadomosci.dodaj_wiadomosc(
                    f"{self._gracze[self._indeks_aktualnego_gracza].id} jest w więzieniu. Zostało {self._gracze[self._indeks_aktualnego_gracza].tury_w_wiezieniu} tur."
                )

        else:
            kostka_pierwsza, kostka_druga = self.symuluj_rzut()

            self._kontroler_wiadomosci.dodaj_wiadomosc(
                f"Kostka pierwsza: {kostka_pierwsza}"
            )
            self._kontroler_wiadomosci.dodaj_wiadomosc(f"Kostka druga: {kostka_druga}")

            #
            # kostka_druga = 6
            # kostka_pierwsza = 6
            #
            self._suma_oczek += kostka_pierwsza + kostka_druga
            umiejetnosc = 0
            if (
                self._gracze[self._indeks_aktualnego_gracza].umiejetnosc
                == "porusza_sie_o_1_pole_wiecej"
            ):
                umiejetnosc = 1
                self._kontroler_wiadomosci.dodaj_wiadomosc(
                    f"Korzystasz z umiejętności: ruch +1"
                )

            # Wyświetl kostki
            self.wyswietl_kostki(self._glowne_okno, kostka_pierwsza, kostka_druga)
            pygame.display.update()  # Aktualizuj ekran po wyświetleniu kostek
            pygame.time.wait(1000)

            self.analizuj_rzut(kostka_pierwsza, kostka_druga, umiejetnosc)

        # self._gracze[self._indeks_aktualnego_gracza].kwota -= 1000
        # self._gracze[self._indeks_aktualnego_gracza].statystyka.aktualizuj_stan_pieniedzy(self._gracze[self._indeks_aktualnego_gracza].kwota)
        self.kto_zbankrutowal()

        if self._gracze[self._indeks_aktualnego_gracza].czy_aktywny == False:
            self.zamknij_wszystkie_okna()

        if self.czy_zwyciezca():
            self._kontroler_wiadomosci.dodaj_wiadomosc(
                f"Zwycięża: {self._gracze[self.zwyciezca].id}"
            )

        if (not self._kolejny_rzut_kostka) and self.zwyciezca == -1:

            while True:
                self._indeks_aktualnego_gracza = (
                    self._indeks_aktualnego_gracza + 1
                ) % self._liczba_graczy
                self._suma_oczek = 0

                if self._gracze[self._indeks_aktualnego_gracza].czy_aktywny == True:
                    break
                # zapetla sie gdy bedzie 1 gracz i zbankrutuje (wtedy powinno sie pokazac info o wygranej)

        self.main.turn_start_time = pygame.time.get_ticks()

    def get_messages(self):
        messages = self.messages.copy()
        self.messages.clear()
        return messages

    # override
    def aktualizacja(self):
        pass
        # if not self._stos_otwartych_okien.czy_pusty():
        #     self._stos_otwartych_okien.gora().aktualizacja()

        # if not self.akcja_pola_okno.czy_koniec_zakupu():
        #     self._czy_gracz_ma_ture = False
        #     self._stos_otwartych_okien.usun()

    def process_input(self, input_text):
        self._kontroler_wiadomosci.dodaj_wiadomosc(f"Wprowadzono: {input_text}")
        if input_text.isdigit():
            liczba_graczy = int(input_text)
            if liczba_graczy >= 2 and liczba_graczy <= 5:
                self._liczba_graczy = liczba_graczy
                self._kontroler_wiadomosci.dodaj_wiadomosc(
                    f"Ustaw liczbe graczy na {liczba_graczy}"
                )
                self.przygotuj_graczy()
                self._kontroler_wiadomosci.dodaj_wiadomosc(
                    "Naciśnij spację, aby rzucić kostką"
                )
            else:
                self._kontroler_wiadomosci.dodaj_wiadomosc(
                    "Nieprawidłowa liczba graczy."
                )
        else:
            self._kontroler_wiadomosci.dodaj_wiadomosc(
                f"Nieznana komenda: {input_text}"
            )

    # metoda pomocnicza w celu wykonania pojdynczego zdarzenia
    # oddzielona od aktualizacja_zdarzenia, na rzecz architektury i wykorzystania klasy GraProxy(event injection, tracking)
    def wykonaj_zdarzenie(self, event: pygame.event.Event):
        if (
            event.type == pygame.KEYDOWN
            and event.key == pygame.K_SPACE
            and self.czy_akcja_zakonczona
            and self.zwyciezca == -1
        ):
            self.tura()
        if (
            self.nastepna_tura.is_clicked(event)
            and self.czy_akcja_zakonczona
            and self.zwyciezca == -1
        ):
            self.tura()
        if (
            self.zapisz_wyjdz.is_clicked(event)
            and self.czy_akcja_zakonczona
            and self.zwyciezca == -1
        ):
            self.input_text = ""
            self.zapisz_gre()
            pygame.quit()
        elif event.type == pygame.KEYDOWN and self.zwyciezca == -1:
            if event.key == pygame.K_RETURN:
                # self.process_input(self.input_text)
                self.input_text = ""
            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            elif event.key == pygame.K_s:
                self.input_text = ""
                self.zapisz_gre()
                pygame.quit()
            else:
                self.input_text += event.unicode
        elif event.type == pygame.VIDEORESIZE:
            self.aktualna_szerokosc_ekranu = event.w
            self.aktualna_wysokosc_ekranu = event.h

            # Rozmiar nie moze byc mniejszy niz 500 na 500
            # if event.w > 1000 and event.h > 550:
            self._plansza.aktualizacja_rozmiaru(
                self.aktualna_szerokosc_ekranu, self.aktualna_wysokosc_ekranu
            )

            for gracz in self._gracze:
                gracz.pionek.aktualizacja_rozmiaru(
                    self.aktualna_szerokosc_ekranu, self.aktualna_wysokosc_ekranu
                )

        self.akcja_pola_okno.aktualizacja_zdarzen(event)
        self.akcja_nieruchomosci_okno.aktualizacja_zdarzen(event)
        self.akcja_kart_okno.aktualizacja_zdarzen(event)
        self.akcja_zastaw_okno.aktualizacja_zdarzen(event)
        self.akcja_zagadek_okno.aktualizacja_zdarzen(event)
        self.akcja_wiezienie_okno.aktualizacja_zdarzen(event)

    # override
    def aktualizacja_zdarzenia(self, event: pygame.event.Event):
        self.wykonaj_zdarzenie(event)

    def zamknij_wszystkie_okna(self):
        self.akcja_pola_okno.czy_akcja_pola = False
        self.akcja_pola_okno.zamknij()

        self.akcja_nieruchomosci_okno.czy_kupno = False
        self.akcja_nieruchomosci_okno.zamknij()

        if self.akcja_kart_okno.czy_szansa:
            self._plansza.karty.aktualna_karta.wykonaj_akcje(
                self, self._gracze[self._indeks_aktualnego_gracza]
            )
        self.akcja_kart_okno.czy_szansa = False
        self.akcja_kart_okno.zamknij()

        self.akcja_zastaw_okno.czy_zastaw = False
        self.akcja_zastaw_okno.zamknij()

        if self.akcja_zagadek_okno.czy_zagadka:
            print(self._gracze[self._indeks_aktualnego_gracza].kwota)
            if 1500 > self._gracze[self._indeks_aktualnego_gracza].kwota:
                if self.pobierz_info_tak_nie(
                    "Nie masz wystarczająco dużo pieniędzy, aby zapłacić podatek. Czy chcesz zastawić którąś z nieruchmości? Jeśli tego nie zrobisz przegrywasz."
                ):
                    self._gracze[self._indeks_aktualnego_gracza].zastaw_nieruchomosci()
            if 1500 > self._gracze[self._indeks_aktualnego_gracza].kwota:
                self.messages.append("Bankrutujesz")
            self._gracze[self._indeks_aktualnego_gracza].kwota -= 1500
            self._kontroler_wiadomosci.dodaj_wiadomosc(
                "Kara za nie wybranie odpowiedzi, zapłacono: " + str(1500)
            )
            self._gracze[
                self._indeks_aktualnego_gracza
            ].statystyka.aktualizuj_stan_pieniedzy(
                self._gracze[self._indeks_aktualnego_gracza].kwota
            )
        self.akcja_zagadek_okno.czy_zagadka = False
        self.akcja_zagadek_okno.zamknij_bez_wiadomosci()

        self.akcja_wiezienie_okno.czy_wiezienie = False
        self.akcja_wiezienie_okno.zamknij()

    def render_text(self, text, pos):
        text_surface = self.font.render(text, True, (0, 0, 0))
        self._glowne_okno.blit(text_surface, pos)

    def render_game_time(self):

        self.font1 = pygame.font.Font(
            self.czcionka, int(self.aktualna_szerokosc_ekranu / 80)
        )

        pozostaly_czas_gry = self.main.LIMIT_CZASU_GRY - int(
            self.main.uplyniety_czas_gry
        )
        game_time_text = f"Czas gry: {int(self.main.uplyniety_czas_gry // 60):02}:{int(self.main.uplyniety_czas_gry % 60):02}"
        if pozostaly_czas_gry <= 300:
            text_color = pygame.Color("red")
            if self.end_game_flag == 1:
                self._kontroler_wiadomosci.dodaj_wiadomosc(
                    "Zostało mniej niż 5 minut do końca gry"
                )
                self.end_game_flag = 0
        else:
            text_color = self.wizualizator.kolor_napisu_gracz_tury

        tekst = self.font1.render(game_time_text, True, text_color)
        self._glowne_okno.blit(
            tekst,
            (
                self.aktualna_szerokosc_ekranu * 0.078,
                self.aktualna_wysokosc_ekranu * 0.85,
            ),
        )

    def render_turn_time(self):
        if self.main.LIMIT_CZASU_TURY != 999:
            self.font1 = pygame.font.Font(
                self.czcionka, int(self.aktualna_szerokosc_ekranu / 80)
            )

            pozostaly_czas_tury = self.main.LIMIT_CZASU_TURY - int(
                self.main.uplyniety_czas_tury
            )
            turn_time_text = f"Czas tury: {pozostaly_czas_tury:02}"
            if pozostaly_czas_tury <= 10:
                text_color = pygame.Color("red")
            else:
                text_color = self.wizualizator.kolor_napisu_gracz_tury

            tekst = self.font1.render(turn_time_text, True, text_color)
            self._glowne_okno.blit(
                tekst,
                (
                    self.aktualna_szerokosc_ekranu * 0.418,
                    self.aktualna_wysokosc_ekranu * 0.85,
                ),
            )

    # override
    def wyswietl(self, okno: pygame.Surface, W, H):

        self.aktualizuj_rozmiar_okien()

        if self.zwyciezca != -1 and self.waiter < 0:
            self.wyswietl_zwyciezce()
            return

        self.render_text(
            self.input_text,
            (self.aktualna_szerokosc_ekranu - 400, self.aktualna_wysokosc_ekranu - 50),
        )

        self._plansza.render(self._glowne_okno)
        self.nastepna_tura.draw(self._glowne_okno)
        self.zapisz_wyjdz.draw(self._glowne_okno)

        for gracz in self._gracze:
            if gracz.czy_aktywny:
                gracz.pionek.wyswietl(self._glowne_okno, self)

        self.wypisz_nazwe_gracza_tury()
        self.akcja_statystyk_okno.wyswietl(self._glowne_okno)
        self._kontroler_wiadomosci.wyswietl(okno, W, H)
        self.akcja_wiezienie_okno.wyswietl(self._glowne_okno)
        self.akcja_pola_okno.wyswietl(self._glowne_okno)
        self.akcja_nieruchomosci_okno.wyswietl(self._glowne_okno)
        self.akcja_kart_okno.wyswietl(self._glowne_okno)
        self.akcja_zastaw_okno.wyswietl(self._glowne_okno)
        self.akcja_zagadek_okno.wyswietl(self._glowne_okno)

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
        self.akcja_statystyk_okno.aktualizuj_rozmiar_okna(
            self.aktualna_szerokosc_ekranu, self.aktualna_wysokosc_ekranu
        )

        self.nastepna_tura.updateSize(
            self.aktualna_szerokosc_ekranu * 0.218,
            self.aktualna_wysokosc_ekranu * 0.64,
            self.aktualna_szerokosc_ekranu * 0.12,
            self.aktualna_wysokosc_ekranu * 0.08,
        )

        self.zapisz_wyjdz.updateSize(
            self.aktualna_szerokosc_ekranu * 0.245,
            self.aktualna_wysokosc_ekranu * 0.74,
            self.aktualna_szerokosc_ekranu * 0.06,
            self.aktualna_wysokosc_ekranu * 0.05,
        )

    def wypisz_nazwe_gracza_tury(self):
        self.render_game_time()  # Wyświetlanie czasu gry
        self.render_turn_time()  # Wyświetlanie czasu tury

        napis = "Tura gracza:"
        sciezka_do_pionka = self._gracze[
            self._indeks_aktualnego_gracza
        ].pionek.sciezka_do_grafiki

        self.skalar_czcionki = 40  # im wiekszy tym mniejsza czcionka
        self.font = pygame.font.Font(
            self.czcionka, int(self.aktualna_szerokosc_ekranu / self.skalar_czcionki)
        )

        self.zdjecie_pionek = pygame.transform.scale(
            pygame.image.load(sciezka_do_pionka),
            (
                0.03 * self.aktualna_szerokosc_ekranu,
                0.03 * self.aktualna_szerokosc_ekranu,
            ),
        )

        self._glowne_okno.blit(
            self.zdjecie_pionek,
            (
                self.aktualna_szerokosc_ekranu * 0.32,
                self.aktualna_wysokosc_ekranu * 0.285,
            ),
        )

        tekst = self.font.render(napis, True, self.wizualizator.kolor_napisu_gracz_tury)
        self._glowne_okno.blit(
            tekst,
            (
                self.aktualna_szerokosc_ekranu * 0.21,
                self.aktualna_wysokosc_ekranu * 0.3,
            ),
        )

    def zapisz_gre(self):
        with open("save/gracze.pickle", "wb") as handle:
            pickle.dump(self._gracze, handle, protocol=pickle.HIGHEST_PROTOCOL)

        with open("save/liczba_graczy.pickle", "wb") as handle:
            pickle.dump(self._liczba_graczy, handle, protocol=pickle.HIGHEST_PROTOCOL)

        with open("save/indeks_aktualnego_gracza.pickle", "wb") as handle:
            pickle.dump(
                self._indeks_aktualnego_gracza, handle, protocol=pickle.HIGHEST_PROTOCOL
            )

        with open("save/messages.pickle", "wb") as handle:
            pickle.dump(self.messages, handle, protocol=pickle.HIGHEST_PROTOCOL)

        with open("save/plansza.pickle", "wb") as handle:
            pickle.dump(self._plansza, handle, protocol=pickle.HIGHEST_PROTOCOL)

        with open("save/gracz_poprzedniej_tury.pickle", "wb") as handle:
            pickle.dump(
                self.gracz_poprzedniej_tury, handle, protocol=pickle.HIGHEST_PROTOCOL
            )
        with open("save/zwyciezca.pickle", "wb") as handle:
            pickle.dump(self.zwyciezca, handle, protocol=pickle.HIGHEST_PROTOCOL)
        with open("save/waiter.pickle", "wb") as handle:
            pickle.dump(self.waiter, handle, protocol=pickle.HIGHEST_PROTOCOL)
        with open("save/czas_gry.pickle", "wb") as handle:
            pickle.dump(
                self.main.uplyniety_czas_gry, handle, protocol=pickle.HIGHEST_PROTOCOL
            )
        with open("save/limit_gra.pickle", "wb") as handle:
            pickle.dump(
                self.main.LIMIT_CZASU_GRY, handle, protocol=pickle.HIGHEST_PROTOCOL
            )
        with open("save/limit_tura.pickle", "wb") as handle:
            pickle.dump(
                self.main.LIMIT_CZASU_TURY, handle, protocol=pickle.HIGHEST_PROTOCOL
            )

        self.main._running = False

    def wczytaj_gre(self):
        with open("save/gracze.pickle", "rb") as handle:
            self._gracze = pickle.load(handle)
        with open("save/liczba_graczy.pickle", "rb") as handle:
            self._liczba_graczy = pickle.load(handle)
        with open("save/indeks_aktualnego_gracza.pickle", "rb") as handle:
            self._indeks_aktualnego_gracza = pickle.load(handle)
        with open("save/messages.pickle", "rb") as handle:
            self.messages = pickle.load(handle)
        with open("save/plansza.pickle", "rb") as handle:
            self._plansza = pickle.load(handle)
        with open("save/gracz_poprzedniej_tury.pickle", "rb") as handle:
            self.gracz_poprzedniej_tury = pickle.load(handle)
        with open("save/zwyciezca.pickle", "rb") as handle:
            self.zwyciezca = pickle.load(handle)
        with open("save/waiter.pickle", "rb") as handle:
            self.waiter = pickle.load(handle)
        with open("save/czas_gry.pickle", "rb") as handle:
            self.main.uplyniety_czas_gry = pickle.load(handle)
        with open("save/limit_gra.pickle", "rb") as handle:
            self.main.LIMIT_CZASU_GRY = pickle.load(handle)
        with open("save/limit_tura.pickle", "rb") as handle:
            self.main.LIMIT_CZASU_TURY = pickle.load(handle)

    def kto_zbankrutowal(self):
        for gracz in self._gracze:
            if gracz.kwota > 0:
                continue
            else:
                if (
                    len(gracz.lista_posiadlosci) == 0
                    or len(gracz.lista_posiadlosci) == gracz.liczba_zastawionych
                ) and gracz.czy_aktywny == True:
                    gracz.czy_aktywny = False
                    self._kontroler_wiadomosci.dodaj_wiadomosc(
                        f"Gracz {gracz.id} bankrutuje"
                    )

    def czy_zwyciezca(self):
        licznik = 0
        licznik_indeksu = 0
        zwyciezca = -1
        for gracz in self._gracze:
            if gracz.czy_aktywny:
                licznik += 1
                zwyciezca = licznik_indeksu
            licznik_indeksu += 1

        if licznik == 1:
            self.zwyciezca = zwyciezca
            return True
        else:
            return False

    def wyswietl_zwyciezce(self):

        self.skalar_czcionki = 15  # im wiekszy tym mniejsza czcionka
        self.font = pygame.font.Font(
            self.czcionka, int(self.aktualna_szerokosc_ekranu / self.skalar_czcionki)
        )
        zwyciezca_tekst = self.font.render(
            f"Zwycięstwo", True, self.wizualizator.kolor_zlotego_napisu
        )

        self.font = pygame.font.Font(
            self.czcionka,
            int(self.aktualna_szerokosc_ekranu / (self.skalar_czcionki + 5)),
        )
        nazwa_gracza = self.font.render(
            self._gracze[self.zwyciezca].id, True, self.kolor_czcionki
        )

        grafika_zwyciezcy = pygame.transform.scale(
            pygame.image.load(self._gracze[self.zwyciezca].pionek.sciezka_do_grafiki),
            (
                0.15 * self.aktualna_szerokosc_ekranu,
                0.15 * self.aktualna_szerokosc_ekranu,
            ),
        )

        self._glowne_okno.fill(self.wizualizator.kolor_tla)
        self._glowne_okno.blit(
            zwyciezca_tekst,
            (
                self.aktualna_szerokosc_ekranu * 0.25,
                self.aktualna_wysokosc_ekranu * 0.3,
            ),
        )
        self._glowne_okno.blit(
            grafika_zwyciezcy,
            (
                self.aktualna_szerokosc_ekranu * 0.55,
                self.aktualna_wysokosc_ekranu * 0.2,
            ),
        )
        self._glowne_okno.blit(
            nazwa_gracza,
            (
                self.aktualna_szerokosc_ekranu * 0.35,
                self.aktualna_wysokosc_ekranu * 0.5,
            ),
        )

    def aktualizuj(self, czas):
        if self.zwyciezca != -1:
            self.waiter -= czas
