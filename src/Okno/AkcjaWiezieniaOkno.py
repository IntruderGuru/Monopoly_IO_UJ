from src.Okno.Okno import Okno
from src.Przycisk import Przycisk
import pygame


class AkcjaWiezieniaOkno(Okno):

    def __init__(self, gra):
        self.W = 1200
        self.H = 800
        self.gra = gra

        self.zdjecie = pygame.transform.scale(
            pygame.image.load("graphics/wiezienie.png"), (0.5 * self.W, 0.5 * self.W)
        )

        self.kolor_przycisku = (70, 70, 70)
        self.kolor_hovera = (150, 150, 150)

        self.wyjscie = Przycisk(self.W * 0.6, self.H * 0.2, self.W * 0.2, self.H * 0.15, self.kolor_przycisku, self.kolor_hovera, "wyjście", (255,255,255))
        self.czy_wiezienie = False
    
    def aktualizacja(self):
        pass

    def aktualizacja_zdarzen(self, event: pygame.event.Event):
        if self.wyjscie.is_clicked(event):
            self.czy_wiezienie = False


    def wyswietl(self, screen: pygame.Surface):
        H = self.H
        W = self.W

        if self.czy_wiezienie:
            self.zdjecie = pygame.transform.scale(self.zdjecie, (0.28 * W, 0.64 * H))
            screen.blit(self.zdjecie, (W * 0.2, H * 0.15))
            self.wyjscie.updateSize(W * 0.6, H * 0.2, W * 0.2, H * 0.15)
            self.wyjscie.draw(screen)

    def aktualizuj_rozmiar_okna(self, width, height):
        self.W = width
        self.H = height