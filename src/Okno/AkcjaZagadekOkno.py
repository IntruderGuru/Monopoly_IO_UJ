from src.Okno.Okno import Okno
from src.Przycisk import Przycisk
import pygame


class AkcjaZagadekOkno(Okno):

    def __init__(self, gra):

        self.H = 800
        self.W = 1200
        self.gra = gra

        self.kolor_przycisku = (70, 70, 70)
        self.kolor_hovera = (150, 150, 150)

        self.A = Przycisk(self.W * 0.42, self.H * 0.7, self.W * 0.2, self.H * 0.1, self.kolor_przycisku, self.kolor_hovera, "wyjscie", (255,255,255))
        self.B = Przycisk(self.W * 0.42, self.H * 0.7, self.W * 0.2, self.H * 0.1, self.kolor_przycisku, self.kolor_hovera, "wyjscie", (255,255,255))
        self.C = Przycisk(self.W * 0.42, self.H * 0.7, self.W * 0.2, self.H * 0.1, self.kolor_przycisku, self.kolor_hovera, "wyjscie", (255,255,255))
        self.czy_zagadka = False

        font = pygame.font.Font(None, 74)

    def aktualizacja(self):
        pass

    def aktualizacja_zdarzen(self, event: pygame.event.Event):
        pass
        # if self.wyjscie.is_clicked(event):
        #     self.czy_zagadka = False

    def wyswietl(self, screen: pygame.Surface):
        if self.czy_zagadka:
            screen.fill((255,255,255))
            screen.blit(self.tekst, (50, 250))
            # self.A.updateSize(self.W * 0.42, self.H * 0.7, self.W * 0.2, self.H * 0.1)
            # self.wyjscie.draw(screen)

    def przygotuj_tekst_zagadki(self):
        font = pygame.font.Font(None, 74)
        self.tekst_zagadki = "tu tekst z metody kuby"
        self.tekst = font.render(self.tekst_zagadki, True, (0,0,0))