from src.okno.Okno import Okno
from src.Przycisk import Przycisk
import pygame


class AkcjaNieruchomosciOkno(Okno):

    def __init__(self, gra):

        self.H = 800
        self.W = 1200
        self.gra = gra
        self.nieruchomosc = "brak"

        self.wyjscie = Przycisk(
            self.W * 0.6,
            self.H * 0.4,
            self.W * 0.2,
            self.H * 0.15,
            self.gra.kolor_przycisku,
            self.gra.kolor_gdy_kursor,
            "wyjscie",
            self.gra.kolor_tekstu,
        )
        self.przycisk_kup_hotel = Przycisk(
            self.W * 0.6,
            self.H * 0.2,
            self.W * 0.2,
            self.H * 0.15,
            self.gra.kolor_przycisku,
            self.gra.kolor_gdy_kursor,
            "kup hotel",
            self.gra.kolor_tekstu,
        )
        self.przycisk_kup_domek = Przycisk(
            self.W * 0.6,
            self.H * 0.2,
            self.W * 0.2,
            self.H * 0.15,
            self.gra.kolor_przycisku,
            self.gra.kolor_gdy_kursor,
            "kup domek",
            self.gra.kolor_tekstu,
        )

        self.karta = Przycisk(
            self.W * 0.6,
            self.H * 0.6,
            self.W * 0.2,
            self.H * 0.15,
            self.gra.kolor_przycisku,
            self.gra.kolor_gdy_kursor,
            "",
            self.gra.kolor_tekstu,
        )

        self.pole_png = None
        self.najechano_na_pole = False

        self.przycisk = self.wyjscie
        self.ktore_kupno = 0
        self.czy_kupno = False

        self.skalar_czcionki = 60  # im wiekszy tym mniejsza czcionka
        self.font = pygame.font.Font(
            self.gra.czcionka, int(self.W / self.skalar_czcionki)
        )

    def ustaw_poprawny_przycisk_domek_hotel(self):

        if self.nieruchomosc == "domek":
            self.przycisk = self.przycisk_kup_domek
        elif self.nieruchomosc == "hotel":
            self.przycisk = self.przycisk_kup_hotel
        else:
            self.przycisk = self.wyjscie

    def aktualizacja(self):
        pass

    def aktualizacja_zdarzen(self, event: pygame.event.Event):

        if self.czy_kupno:
            if self.przycisk.is_clicked(event) and self.nieruchomosc == "domek":
                self.kup_domek()
                self.czy_kupno = False
                self.zamknij()
            elif self.przycisk.is_clicked(event) and self.nieruchomosc == "hotel":
                self.kup_hotel()
                self.czy_kupno = False
                self.zamknij()
            elif self.wyjscie.is_clicked(event):
                self.czy_kupno = False
                self.zamknij()

            if self.czy_kupno:
                if self.karta.czy_najechano():
                    self.pole_png = pygame.transform.scale(
                        pygame.image.load("graphics/pola/pole_tyl_karty.png"),
                        (0.24 * self.W, 0.64 * self.H),
                    )
                    self.najechano_na_pole = True
                else:
                    self.pole_png = pygame.transform.scale(
                        pygame.image.load(self.posiadlosc_gracza.sciezka_do_grafiki),
                        (0.24 * self.W, 0.64 * self.H),
                    )
                    self.najechano_na_pole = False

    def wyswietl(self, screen: pygame.Surface):


        if self.czy_kupno:
            self.zaktualizuj_tekst_i_rozmiar()
            nakladka = pygame.Surface(screen.get_size())
            nakladka.set_alpha(self.gra.przezroczystosc_nakladki)  # Ustaw przezroczystość (0-255)
            nakladka.fill(self.gra.kolor_nakladki)
            screen.blit(nakladka, (0, 0))

            self.pole_png = pygame.transform.scale(
                self.pole_png, (0.24 * self.W, 0.64 * self.H)
            )
            screen.blit(self.pole_png, (self.W * 0.2, self.H * 0.15))
            self.przycisk.updateSize(
                self.W * 0.6, self.H * 0.2, self.W * 0.2, self.H * 0.15
            )
            self.wyjscie.updateSize(
                self.W * 0.6, self.H * 0.4, self.W * 0.2, self.H * 0.15
            )
            self.karta.updateSize(
                self.W * 0.2, self.H * 0.15, 0.24 * self.W, 0.64 * self.H
            )
            self.przycisk.draw(screen)
            self.wyjscie.draw(screen)

            pole_png_wyswietlane = pygame.transform.scale(
                self.pole_png, (0.24 * self.W, 0.64 * self.H)
            )
            screen.blit(pole_png_wyswietlane, (self.W * 0.2, self.H * 0.15))

            self.odleglosc_pionowa = 0.03
            self.wysokosc_napisow = 0.42
            if self.najechano_na_pole:
                screen.blit(
                    self.czynsz_bez_nieruchomosci,
                    (
                        self.W * 0.23,
                        self.H * (self.wysokosc_napisow + (0 * self.odleglosc_pionowa)),
                    ),
                )
                screen.blit(
                    self.wzrost_czynszu_dom,
                    (
                        self.W * 0.23,
                        self.H * (self.wysokosc_napisow + (1 * self.odleglosc_pionowa)),
                    ),
                )
                screen.blit(
                    self.wzrost_czynszu_hotel,
                    (
                        self.W * 0.23,
                        self.H * (self.wysokosc_napisow + (2 * self.odleglosc_pionowa)),
                    ),
                )

    def akcja_kupowania(self, posiadlosc, gracz):
        self.posiadlosc_gracza = posiadlosc
        self.gracz = gracz
        self.ustaw_poprawny_przycisk_domek_hotel()
        self.pole_png = pygame.transform.scale(
            pygame.image.load(self.posiadlosc_gracza.sciezka_do_grafiki),
            (0.28 * self.W, 0.64 * self.H),
        )

    def kup_domek(self):
        self.posiadlosc_gracza.kup_dom(self.gra, self.gracz, 1)

    def kup_hotel(self):
        self.posiadlosc_gracza.kup_dom(self.gra, self.gracz, 5)

    def aktualizuj_rozmiar_okna(self, width, height):
        self.W = width
        self.H = height

    def zamknij(self):
        self.gra.czy_akcja_zakonczona = True

    def zaktualizuj_tekst_i_rozmiar(self):
        self.font = pygame.font.Font(
            self.gra.czcionka, int(self.W / self.skalar_czcionki)
        )

        if self.posiadlosc_gracza is None:
            self.czynsz_bez_nieruchomosci = self.font.render(
                "Czynsz bez nieruchomości: " + str(100),
                True,
                self.gra.kolor_czcionki_tyl_karty,
            )
        else:
            self.czynsz_bez_nieruchomosci = self.font.render(
                "Czynsz bez nieruchomości: " + str(self.posiadlosc_gracza.czynsz),
                True,
                self.gra.kolor_czcionki_tyl_karty,
            )
        self.wzrost_czynszu_dom = self.font.render(
            "Wzrost czynszu (domek +): " + str(70),
            True,
            self.gra.kolor_czcionki_tyl_karty,
        )
        self.wzrost_czynszu_hotel = self.font.render(
            "Wzrost czynszu (hotel +): " + str(100),
            True,
            self.gra.kolor_czcionki_tyl_karty,
        )