import random
import pygame
import sys
from src.Gracz import Gracz
from src.Pole import Pole
from src.Plansza import Plansza
from src.Posiadlosc import *
from src.Pionek import Pionek
from src.Przycisk import Przycisk

KWOTA_POCZATKOWA = 10000
MIN_LICZBA_GRACZY = 2
MAX_LICZBA_GRACZY = 5
LICZBA_POL = 40

aktualna_szerokosc_ekranu = 1200
aktualna_wysokosc_ekranu = 800

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
        self.glowne_okno = glowne_okno
        self.gracze: list[Gracz] = []
        self._kwota_poczatkowa = KWOTA_POCZATKOWA
        self._liczba_graczy = 0
        self._suma_oczek = 0
        self._kolejny_rzut_kostka = False
        self._aktualny_gracz = 0
        self.board = self.stworz_plansze()
        self.messages = []

        # Refactor def akcja_dostepnego_pola() - Piter
        self.board_png = pygame.transform.scale(
            pygame.image.load("graphics/pole.png"), (0.28 * aktualna_szerokosc_ekranu, 0.64 * aktualna_wysokosc_ekranu)
        )

        self.kolor_przycisku = (70, 70, 70)
        self.kolor_hovera = (150, 150, 150)

        self.zakup = Przycisk(aktualna_szerokosc_ekranu * 0.6, aktualna_wysokosc_ekranu * 0.2, aktualna_szerokosc_ekranu * 0.2, aktualna_wysokosc_ekranu * 0.15, self.kolor_przycisku, self.kolor_hovera, "kupuje", (255,255,255))
        self.licytacja = Przycisk(aktualna_szerokosc_ekranu * 0.6, aktualna_wysokosc_ekranu * 0.4, aktualna_szerokosc_ekranu * 0.2, aktualna_wysokosc_ekranu * 0.15, self.kolor_przycisku, self.kolor_hovera, "licytacja", (255,255,255))
        self.ktora_akcja = 0
        self.czy_dostep = False

        # Refactor def pobierz_info_tak_nie() - Piter
        self.kolor_tak = (51, 204, 51)
        self.kolor_nie = (255, 77, 77)
        self.kolor_hovera_nie = (255, 102, 102)
        self.kolor_hovera_tak = (71, 209, 71)

        self.font = pygame.font.Font(None, 36)
        self.text = self.font.render("test", True, (0,0,0))
        self.text_rect = self.text.get_rect(center=(aktualna_szerokosc_ekranu * 0.5, aktualna_wysokosc_ekranu * 0.4,))

        self.tak = Przycisk(aktualna_wysokosc_ekranu * 0.3, aktualna_wysokosc_ekranu * 0.45, aktualna_wysokosc_ekranu * 0.15, aktualna_wysokosc_ekranu * 0.11, self.kolor_tak, self.kolor_hovera_tak, "tak", (255,255,255))
        self.nie = Przycisk(aktualna_wysokosc_ekranu * 0.5, aktualna_wysokosc_ekranu * 0.45, aktualna_wysokosc_ekranu * 0.15, aktualna_wysokosc_ekranu * 0.11, self.kolor_nie, self.kolor_hovera_nie, "nie", (255,255,255))

        self.tak_klik = False
        self.nie_klik = True
        self.czy_info = False

        # Refactor def akcja_kupienia_nieruchomosci() - Piter
        self.nieruchomosc = "wyjscie"
        self.wyjscie = Przycisk(aktualna_szerokosc_ekranu * 0.6, aktualna_wysokosc_ekranu * 0.4, aktualna_szerokosc_ekranu * 0.2, aktualna_wysokosc_ekranu * 0.15, self.kolor_przycisku, self.kolor_hovera, "brak ruchu", (255,255,255))
        self.przycisk_kup_hotel = Przycisk(aktualna_szerokosc_ekranu * 0.6, aktualna_wysokosc_ekranu * 0.2, aktualna_szerokosc_ekranu * 0.2, aktualna_wysokosc_ekranu * 0.15, self.kolor_przycisku, self.kolor_hovera, "kup hotel", (255,255,255))
        self.przycisk_kup_domek = Przycisk(aktualna_szerokosc_ekranu * 0.6, aktualna_wysokosc_ekranu * 0.2, aktualna_szerokosc_ekranu * 0.2, aktualna_wysokosc_ekranu * 0.15, self.kolor_przycisku, self.kolor_hovera, "kup domek", (255,255,255))
        self.ktore_kupno = 0
        self.czy_kupno = False

    def stworz_plansze(self):
        board = []
        board.append(Pole(0, "Start"))
        board.append(Posiadlosc(1, "Automat z kawą", 600, 20, 300, 500))
        board.append(Pole(2, "Szansa"))
        board.append(Posiadlosc(3, "Bistro \"Świetlica\"", 600, 40, 300, 500))
        board.append(Pole(4, "Podatek dochodowy"))
        board.append(PosiadloscKolo(5, "KNRSI", 2000, 250, 1000))
        board.append(Posiadlosc(6, "Parking", 1000, 60, 500, 500))
        board.append(Pole(7, "Szansa"))
        board.append(Posiadlosc(8, "Winda", 1000, 60, 500, 500))
        board.append(Posiadlosc(9, "Szatnia", 1200, 80, 500, 500))
        board.append(Pole(10, "Wiezienie"))
        board.append(Posiadlosc(11,"Sala 1073 (sieci)", 1400, 100, 700, 1000))
        board.append(PosiadloscPozaWmii(12,"Drążki za wydziałem", 1500, 0, 750))
        board.append(Posiadlosc(13, "Sala 0056 (laby)", 1400, 100, 700, 1000))
        board.append(Posiadlosc(14, "Sala 1072 (macbooki)", 1600, 120, 800, 1000))
        board.append(PosiadloscKolo(15, "KNMF", 2000, 250, 1000))
        board.append(Posiadlosc(16, "Ślimak", 1800, 140, 900, 1000))
        board.append(Pole(17, "Szansa"))
        board.append(Posiadlosc(18, "Serwerownia", 1800, 140, 900, 1000))
        board.append(Posiadlosc(19, "Pokój samorządu", 2000, 160, 1000, 1000))
        board.append(Pole(20, "Parking"))
        board.append(Posiadlosc(21, "Recepcja", 2200, 180, 1100, 1500))
        board.append(Pole(22, "Szansa"))
        board.append(Posiadlosc(23, "Dziekanat", 2200, 180, 1100, 1500))
        board.append(Posiadlosc(24, "Muzeum komputerów", 2400, 200, 1200, 1500))
        board.append(PosiadloscKolo(25, "KMS", 2000, 250, 1000))
        board.append(Posiadlosc(26, "Mural", 2600, 220, 1300, 1500))
        board.append(Posiadlosc(27, "Pomnik Kopernika", 2600, 220, 1300, 1500))
        board.append(PosiadloscPozaWmii(28,"Przejście przez WZIKS", 1500, 0, 750))
        board.append(Posiadlosc(29, "Fontanna", 2800, 240, 1400, 1500))
        board.append(Pole(30, "Idz do wiezienia"))
        board.append(Posiadlosc(31, "Ping-pong", 3000, 260, 1500, 2000))
        board.append(Posiadlosc(32, "Bilard", 3000, 260, 1500, 2000))
        board.append(Pole(33, "Szansa"))
        board.append(Posiadlosc(34, "Piłkarzyki", 3200, 280, 1600, 2000))
        board.append(PosiadloscKolo(35, "KSI", 2000, 250, 1000))
        board.append(Pole(36, "Szansa"))
        board.append(Posiadlosc(37, "sala 0004", 3500, 350, 1750, 2000))
        board.append(Pole(38, "Podatek dochodowy"))
        board.append(Posiadlosc(39, "sala 0089", 4000, 500, 2000, 2000))

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

    def wybierz_kolejnego_gracza(self):
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

    def analizuj_rzut(self, kostka_pierwsza, kostka_druga):
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
        # gracz.pionek.numer_pola = nowa_pozycja
        gracz.pionek.przesun(ruch)
        gracz.czy_przeszedl_przez_start(self, stara_pozycja)

        self.messages.append(
            f"Gracz {gracz.id} przesunął się z pozycji {stara_pozycja} na {nowa_pozycja}"
        )

        pole = self.board[nowa_pozycja]
        self.wykonaj_akcje_na_polu(gracz, pole)

    def pobierz_info_tak_nie(self, text):
        self.czy_info = True

            # for event in pygame.event.get():
            #     if event.type == pygame.QUIT:
            #         pygame.quit()
            #         sys.exit()
            #     elif tak.is_clicked(event):
            #         return True
            #     elif nie.is_clicked(event):
            #         return False

    def akcja_dostepnego_pola(self, gracz, pole, nr_pola = 1):
        self.czy_dostep = True

            # for event in pygame.event.get():
            #     if event.type == pygame.QUIT:
            #         pygame.quit()
            #         sys.exit()
            #     elif self.zakup.is_clicked(event):
            #         return 1
            #     elif self.licytacja.is_clicked(event):
            #         return 2

    def aktualizuj_zdarzenia(self, event: pygame.event.Event):
        self.tak_klik = False
        self.nie_klik = True

        if self.zakup.is_clicked(event):
            self.ktore_kupno = 1
            self.czy_dostep = False
            # return 1
        elif self.licytacja.is_clicked(event):
            self.ktore_kupno = 2
            self.czy_dostep = False
            # return 2

        elif self.tak.is_clicked(event):
            self.tak_klik = True
            self.czy_info = False
            # return True
        elif self.nie.is_clicked(event):
            self.nie_klik = False
            self.czy_info = False
            # return False

        elif self.przycisk_kup_domek.is_clicked(event) and self.nieruchomosc == "domek":
            self.czy_kupno = False
        elif self.przycisk_kup_hotel.is_clicked(event) and self.nieruchomosc == "hotel":
            self.czy_kupno = False
        elif self.wyjscie.is_clicked(event) and self.nieruchomosc == "wyjscie":
            self.czy_kupno = False

    def wyswietlaj(self):
        if self.czy_dostep:
            self.glowne_okno.blit(self.board_png, (aktualna_szerokosc_ekranu * 0.2, aktualna_wysokosc_ekranu * 0.15))
            self.zakup.draw(self.glowne_okno)
            self.licytacja.draw(self.glowne_okno)

        if self.czy_info:
            self.glowne_okno.blit(self.text, self.text_rect)
            self.tak.draw(self.glowne_okno)
            self.nie.draw(self.glowne_okno)

        if self.czy_kupno:
            self.przycisk_kup_domek.draw(self.glowne_okno)
            self.przycisk_kup_hotel.draw(self.glowne_okno)
            self.wyjscie.draw(self.glowne_okno)

    def akcja_kupienia_nieruchomosci(self, gracz, posiadlosc, nr_pola = 1):
        self.czy_kupno = True

        if posiadlosc.liczba_domow < 4:
            self.nieruchomosc = "domek"
        else:
            self.nieruchomosc = "hotel"

    def wykonaj_akcje_na_polu(self, gracz, pole):
        self.messages.append(pole.wyswietl_info())

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
                akcja = self.ktora_akcja
                #akcja 1 to zakup posiadlosci
                if akcja == 1:
                    posiadlosc.kup_posiadlosc(self, gracz)
                #akcja 2 to licytacja
                if akcja == 2:
                    pass

            elif posiadlosc.IDwlasciciela == gracz.id:
                self.akcja_kupienia_nieruchomosci(gracz, posiadlosc)
                akcja = self.ktora_akcja

                if akcja == 1:
                    posiadlosc.kup_dom(self, gracz)
                elif akcja == 2:
                    #nie jest zaimplementowane kupowanie hotelu
                    #posiadlosc.kup_hotel(self, gracz)
                    pass

            else:
                pass


    def tura(self):

        if not self._kolejny_rzut_kostka:
            self.wybierz_kolejnego_gracza()

        if not self.gracze[self._aktualny_gracz - 1].uwiezienie:
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
                self.gracze[self._aktualny_gracz - 1], kostka_pierwsza + kostka_druga
            )
        else:
            self.messages.append(f"Gracz {self._aktualny_gracz} jest width więzieniu.")

        if not self._kolejny_rzut_kostka:
            self._aktualny_gracz = (self._aktualny_gracz % self._liczba_graczy) + 1


    def get_messages(self):
        messages = self.messages.copy()
        self.messages.clear()
        return messages
