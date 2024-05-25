from src.Okno.Okno import Okno
from src.Przycisk import Przycisk
from src.Odpowiedz import Odpowiedz
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
        self.informacja_o_podatku = "Zapłać podatek dochodowy o wartości "
        self.informacja_o_zagadce = "odpowiedz poprawnie na pytanie aby zmniejszyć opłatę"
        self.tekst_zagadki = "empty"


    def aktualizacja(self):
        pass

    def aktualizacja_zdarzen(self, event: pygame.event.Event):

        if self.A.is_clicked(event) :
            self.pole.zaplac_podatek(self.gra, self.gracz, (self.poprawna_odpowiedz == Odpowiedz.Odpowiedz_A))
            self.czy_zagadka = False
        elif self.B.is_clicked(event):
            self.pole.zaplac_podatek(self.gra, self.gracz, (self.poprawna_odpowiedz == Odpowiedz.Odpowiedz_B))
            self.czy_zagadka = False
        elif self.C.is_clicked(event):
            self.pole.zaplac_podatek(self.gra, self.gracz, (self.poprawna_odpowiedz == Odpowiedz.Odpowiedz_C))
            self.czy_zagadka = False


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

    def przygotuj_zagadke(self):

        zagadka = self.gra._plansza.zagadki.nastepna_zagadka()
        self.tekst_zagadki = zagadka.tresc_zagadki

        self.odpowiedz_A = zagadka.odpowiedz_a
        self.odpowiedz_B = zagadka.odpowiedz_b
        self.odpowiedz_C = zagadka.odpowiedz_c
        self.poprawna_odpowiedz = zagadka.poprawna

        self.informacja_o_podatku += str(self.pole.podatek)

    def akcja_podatkowa(self, gracz, pole):
        self.gracz = gracz
        self.pole = pole



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
        screen.blit(self.podatek, (self.W * 0.18, self.H * 0.2))
        screen.blit(self.info, (self.W * 0.19, self.H * 0.27))
        screen.blit(self.zagadka, (self.W * 0.2, self.H * 0.4))

        #odpowiedzi
        screen.blit(self.oA, (self.W * 0.3, self.H * 0.54))
        screen.blit(self.oB, (self.W * 0.3, self.H * 0.66))
        screen.blit(self.oC, (self.W * 0.3, self.H * 0.78))

    def aktualizuj_rozmiar_okna(self, width, height):
        self.W = width
        self.H = height