from src.okno.Okno import Okno
from src.Przycisk import Przycisk
import pygame
from enum import Enum


class AkcjaPolaOkno(Okno):
    def __init__(self, gra):
        self.W = 1200
        self.H = 800
        self.gra = gra

        self.zakup = Przycisk(
            self.W * 0.6,
            self.H * 0.2,
            self.W * 0.2,
            self.H * 0.15,
            self.gra.kolor_przycisku,
            self.gra.kolor_gdy_kursor,
            "kupuję",
            self.gra.kolor_tekstu,
        )
        self.licytacja = Przycisk(
            self.W * 0.6,
            self.H * 0.4,
            self.W * 0.2,
            self.H * 0.15,
            self.gra.kolor_przycisku,
            self.gra.kolor_gdy_kursor,
            "licytacja",
            self.gra.kolor_tekstu,
        )
        self.wyjscie = Przycisk(
            self.W * 0.6,
            self.H * 0.6,
            self.W * 0.2,
            self.H * 0.15,
            self.gra.kolor_przycisku,
            self.gra.kolor_gdy_kursor,
            "wyjscie",
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

        self.pole_png= None
        self.najechano_na_pole = False

        self.czy_akcja_pola = False
        self.gracz_majacy_mozliwosc_zakupu = None
        self.posiadlosc_do_zakupu = None

        self.skalar_czcionki = 60  # im wiekszy tym mniejsza czcionka
        self.font = pygame.font.Font(None, int(self.W / self.skalar_czcionki))

    def aktualizacja(self):
        pass

    def aktualizacja_zdarzen(self, event: pygame.event.Event):
        if self.zakup.is_clicked(event):
            self.kup_pole()
            self.czy_akcja_pola = False
            self.zamknij()
        elif self.licytacja.is_clicked(event):
            self.czy_akcja_pola = False
            self.zamknij()
            pass
        elif self.wyjscie.is_clicked(event):
            self.czy_akcja_pola = False
            self.zamknij()

        if self.czy_akcja_pola:
            if self.karta.czy_najechano():
                self.pole_png = pygame.transform.scale(
                pygame.image.load("graphics/pola/pole_tyl_karty.png"),
                (0.24 * self.W, 0.64 * self.H),
                )
                self.najechano_na_pole = True
            else:
                self.pole_png = pygame.transform.scale(
                pygame.image.load(self.posiadlosc_do_zakupu.sciezka_do_grafiki),
                (0.24 * self.W, 0.64 * self.H),
                )
                self.najechano_na_pole = False



    def wyswietl(self, screen: pygame.Surface):

        self.zaktualizuj_tekst_i_rozmiar()

        if self.czy_akcja_pola:
            self.zakup.updateSize(
                self.W * 0.6,
                self.H * 0.2,
                self.W * 0.2,
                self.H * 0.15
            )
            self.licytacja.updateSize(
                self.W * 0.6,
                self.H * 0.4,
                self.W * 0.2,
                self.H * 0.15,
            )
            self.wyjscie.updateSize(
                self.W * 0.6,
                self.H * 0.6,
                self.W * 0.2,
                self.H * 0.15,
            )

            self.karta.updateSize(
                self.W * 0.2,
                self.H * 0.15,
                0.24 * self.W, 
                0.64 * self.H
            )

            self.zakup.draw(screen)
            self.licytacja.draw(screen)
            self.wyjscie.draw(screen)

            pole_png_wyswietlane = pygame.transform.scale(
                self.pole_png, (0.24 * self.W, 0.64 * self.H)
            )
            screen.blit(pole_png_wyswietlane, (self.W * 0.2, self.H * 0.15))

            self.odleglosc_pionowa = 0.03
            self.wysokosc_napisow = 0.42
            if self.najechano_na_pole:
                screen.blit(self.czynsz_bez_nieruchomosci, (self.W * 0.23, self.H * (self.wysokosc_napisow + (0 * self.odleglosc_pionowa))))
                screen.blit(self.wzrost_czynszu_dom, (self.W * 0.23, self.H * (self.wysokosc_napisow + (1 * self.odleglosc_pionowa))))
                screen.blit(self.wzrost_czynszu_hotel, (self.W * 0.23, self.H * (self.wysokosc_napisow + (2 * self.odleglosc_pionowa))))


    def akcja_kupowania(self, posiadlosc, gracz):
        self.posiadlosc_do_zakupu = posiadlosc
        self.gracz_majacy_mozliwosc_zakupu = gracz
        self.pole_png = pygame.transform.scale(
            pygame.image.load(self.posiadlosc_do_zakupu.sciezka_do_grafiki),
            (0.24 * self.W, 0.64 * self.H),
        )

    def kup_pole(self):
        self.posiadlosc_do_zakupu.kup_posiadlosc(
            self.gra, self.gracz_majacy_mozliwosc_zakupu
        )

    def aktualizuj_rozmiar_okna(self, width, height):
        self.W = width
        self.H = height

    def zamknij(self):
        self.gra.czy_akcja_zakonczona = True

    def zaktualizuj_tekst_i_rozmiar(self):
        self.font = pygame.font.Font(None, int(self.W / self.skalar_czcionki))

        self.czynsz_bez_nieruchomosci = self.font.render(
            "Czynsz bez nieruchomości: " + str(100), True, self.gra.kolor_czcionki_tyl_karty
        )
        self.wzrost_czynszu_dom = self.font.render(
            "Wzrost czynszu (domek +) " + str(70), True, self.gra.kolor_czcionki_tyl_karty
        )
        self.wzrost_czynszu_hotel = self.font.render(
            "Wzrost czynszu (hotel +) " + str(100), True, self.gra.kolor_czcionki_tyl_karty
        )