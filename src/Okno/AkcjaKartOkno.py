from src.Okno.Okno import Okno
from src.Przycisk import Przycisk
import pygame


class AkcjaKartOkno(Okno):

    def __init__(self, gra):

        self.H = 800
        self.W = 1200
        self.gra = gra
        self.szansa_png = pygame.transform.scale(pygame.image.load("graphics/karta_szansy.png"), (0.6 * self.W, 0.5 * self.H))

        self.kolor_przycisku = (70, 70, 70)
        self.kolor_hovera = (150, 150, 150)
        self.wyjscie = Przycisk(self.W * 0.42, self.H * 0.7, self.W * 0.2, self.H * 0.1, self.kolor_przycisku, self.kolor_hovera, "wyjście", (255,255,255))
        self.czy_szansa = False

    def aktualizacja(self):
        pass

    def aktualizacja_zdarzen(self, event: pygame.event.Event):
        if self.wyjscie.is_clicked(event):
            self.czy_szansa = False

    def wyswietl(self, screen: pygame.Surface):
        if self.czy_szansa:
            self.szansa_png = pygame.transform.scale(self.szansa_png, (0.64 * self.W, 0.5 * self.H))
            screen.blit(self.szansa_png, (self.W * 0.2, self.H * 0.15))
            self.wyjscie.updateSize(self.W * 0.42, self.H * 0.7, self.W * 0.2, self.H * 0.1)
            self.wyjscie.draw(screen)

