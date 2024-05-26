from src.Okno.Okno import Okno
from src.Przycisk import Przycisk
import pygame


class AkcjaNieruchomosciOkno(Okno):

    def __init__(self, gra):

        self.H = 800
        self.W = 1200
        self.gra = gra
        self.pole_png = pygame.transform.scale(pygame.image.load("graphics/pole.png"), (0.28 * self.W, 0.64 * self.H))

        self.kolor_przycisku = (70, 70, 70)
        self.kolor_hovera = (150, 150, 150)
        self.nieruchomosc = "brak"

        self.wyjscie            = Przycisk(self.W * 0.6, self.H * 0.4, self.W * 0.2, self.H * 0.15, self.kolor_przycisku, self.kolor_hovera, "wyjscie", (255,255,255))
        self.przycisk_kup_hotel = Przycisk(self.W * 0.6, self.H * 0.2, self.W * 0.2, self.H * 0.15, self.kolor_przycisku, self.kolor_hovera, "kup hotel", (255,255,255))
        self.przycisk_kup_domek = Przycisk(self.W * 0.6, self.H * 0.2, self.W * 0.2, self.H * 0.15, self.kolor_przycisku, self.kolor_hovera, "kup domek", (255,255,255))

        self.przycisk = self.wyjscie
        self.ktore_kupno = 0
        self.czy_kupno = False


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

        if self.przycisk.is_clicked(event) and self.nieruchomosc == "domek":
            self.kup_domek()
            self.czy_kupno = False
        elif self.przycisk.is_clicked(event) and self.nieruchomosc == "hotel":
            self.kup_hotel()
            self.czy_kupno = False
        elif self.wyjscie.is_clicked(event):
            self.czy_kupno = False

    def wyswietl(self, screen: pygame.Surface):
        if self.czy_kupno:
            self.pole_png = pygame.transform.scale(self.pole_png, (0.28 * self.W, 0.64 * self.H))
            screen.blit(self.pole_png, (self.W * 0.2, self.H * 0.15))
            self.przycisk.updateSize(self.W * 0.6, self.H * 0.2, self.W * 0.2, self.H * 0.15)
            self.wyjscie.updateSize(self.W * 0.6, self.H * 0.4, self.W * 0.2, self.H * 0.15)
            self.przycisk.draw(screen)
            self.wyjscie.draw(screen)

    def akcja_kupowania(self, posiadlosc, gracz):
        self.posiadlosc_gracza = posiadlosc
        self.gracz = gracz
        self.ustaw_poprawny_przycisk_domek_hotel()
        

    def kup_domek(self):
        self.posiadlosc_gracza.kup_dom(self.gra, self.gracz, 1)

    def kup_hotel(self):
        self.posiadlosc_gracza.kup_dom(self.gra, self.gracz, 5)
