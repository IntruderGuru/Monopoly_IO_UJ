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
        self.czy_zagadka = False

        self.A = Przycisk(self.W * 0.2, self.H * 0.5, self.H * 0.1, self.H * 0.1, self.kolor_przycisku, self.kolor_hovera, "A", (255,255,255))
        self.B = Przycisk(self.W * 0.2, self.H * 0.6, self.H * 0.1, self.H * 0.1, self.kolor_przycisku, self.kolor_hovera, "B", (255,255,255))
        self.C = Przycisk(self.W * 0.2, self.H * 0.7, self.H * 0.1, self.H * 0.1, self.kolor_przycisku, self.kolor_hovera, "C", (255,255,255))

        self.odpowiedz_A = "empty"
        self.odpowiedz_B = "empty"
        self.odpowiedz_C = "empty"

        self.skalar_czcionki = 22 #im wiekszy tym mniejsza czcionka
        self.font = pygame.font.Font(None, int(self.W / self.skalar_czcionki))
        self.informacja_o_podatku = "Zapłać podatek dochodowy o wartości x"
        self.informacja_o_zagadce = "odpowiedz poprawnie na pytanie aby zmniejszyć opłatę"
        self.tekst_zagadki = "empty"


    def aktualizacja(self):
        pass

    def aktualizacja_zdarzen(self, event: pygame.event.Event):
        pass
        # if self.wyjscie.is_clicked(event):
        #     self.czy_zagadka = False

    def wyswietl(self, screen: pygame.Surface):
        self.zaktualizuj_rozmiar_czcionki()

        if self.czy_zagadka:
            self.wyswietl_teksty(screen)
        
            self.A.updateSize(self.W * 0.2, self.H * 0.5, self.H * 0.1, self.H * 0.1)
            self.A.draw(screen)
            self.B.updateSize(self.W * 0.2, self.H * 0.62, self.H * 0.1, self.H * 0.1)
            self.B.draw(screen)
            self.C.updateSize(self.W * 0.2, self.H * 0.74, self.H * 0.1, self.H * 0.1)
            self.C.draw(screen)

    def przygotuj_tekst_zagadki(self):
        self.tekst_zagadki = "Ile to: (5 + 6) * 4 / 5"

    def zaktualizuj_rozmiar_czcionki(self):
        self.font = pygame.font.Font(None, int(self.W / self.skalar_czcionki))
        self.podatek = self.font.render(self.informacja_o_podatku, True, (0,0,0))
        self.font = pygame.font.Font(None, int(self.W / self.skalar_czcionki) - 15)
        self.info = self.font.render(self.informacja_o_zagadce, True, (0,0,0))
        self.zagadka = self.font.render(self.tekst_zagadki, True, (0,0,0))

        #odpowiedzi
        self.oA = self.font.render(self.odpowiedz_A, True, (0,0,0))
        self.oB = self.font.render(self.odpowiedz_B, True, (0,0,0))
        self.oC = self.font.render(self.odpowiedz_C, True, (0,0,0))

    def wyswietl_teksty(self, screen):
        screen.fill((255,255,255))
        screen.blit(self.podatek, (self.W * 0.2, self.H * 0.2))
        screen.blit(self.info, (self.W * 0.21, self.H * 0.27))
        screen.blit(self.zagadka, (self.W * 0.3, self.H * 0.4))

        #odpowiedzi
        screen.blit(self.oA, (self.W * 0.3, self.H * 0.54))
        screen.blit(self.oB, (self.W * 0.3, self.H * 0.66))
        screen.blit(self.oC, (self.W * 0.3, self.H * 0.78))

        

    def pobierz_odpowiedzi(self):
        self.odpowiedz_A = "6"
        self.odpowiedz_B = "7"
        self.odpowiedz_C = "-22"