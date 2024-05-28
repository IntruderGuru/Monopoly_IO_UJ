from src.okno.Okno import Okno
from src.Przycisk import Przycisk
import pygame


class AkcjaZastawOkno(Okno):

    def __init__(self, gra):

        self.H = 800
        self.W = 1200
        self.gra = gra
        self.pole_png = pygame.transform.scale(pygame.image.load("graphics/zastaw.jpg"), (0.28 * self.W, 0.64 * self.H))

        self.kolor_przycisku = (70, 70, 70)
        self.kolor_hovera = (150, 150, 150)

        self.przycisk_zastaw = Przycisk(self.W * 0.6, self.H * 0.2, self.W * 0.2, self.H * 0.15, self.kolor_przycisku, self.kolor_hovera, "zastaw", (255,255,255))
        self.wyjscie = Przycisk(self.W * 0.6, self.H * 0.4, self.W * 0.2, self.H * 0.15, self.kolor_przycisku, self.kolor_hovera, "wyjscie", (255,255,255))
        self.czy_zastaw = False

    def aktualizacja(self):
        pass

    def aktualizacja_zdarzen(self, event: pygame.event.Event):
        if self.czy_zastaw:
            if self.przycisk_zastaw.is_clicked(event):
                self.zastaw()
                #self.czy_zastaw = False
            elif self.wyjscie.is_clicked(event):
                self.czy_zastaw = False

    def wyswietl(self, screen: pygame.Surface):
        if self.czy_zastaw:
            self.pole_png = pygame.transform.scale(self.pole_png, (0.28 * self.W, 0.64 * self.H))
            screen.blit(self.pole_png, (self.W * 0.2, self.H * 0.15))
            self.przycisk_zastaw.updateSize(self.W * 0.6, self.H * 0.2, self.W * 0.2, self.H * 0.15)
            self.wyjscie.updateSize(self.W * 0.6, self.H * 0.4, self.W * 0.2, self.H * 0.15)
            self.przycisk_zastaw.draw(screen)
            self.wyjscie.draw(screen)

    def akcja_zastawiania(self, gracz):
        self.gracz = gracz
        
    def zastaw(self):
        self.gracz.zastaw_posiadlosci(self.gra)