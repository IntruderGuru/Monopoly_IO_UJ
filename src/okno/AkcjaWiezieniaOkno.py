from src.okno.Okno import Okno
from src.Przycisk import Przycisk
import pygame


class AkcjaWiezieniaOkno(Okno):

    def __init__(self, gra):
        self.W = 1200
        self.H = 800
        self.gra = gra

        self.zdjecie = pygame.transform.scale(
            pygame.image.load("graphics/wiezienie.png"), (0.45 * self.H, 0.45 * self.H)
        )

        self.wyjscie = Przycisk(
            self.W * 0.6,
            self.H * 0.3,
            self.W * 0.2,
            self.H * 0.15,
            self.gra.kolor_przycisku,
            self.gra.kolor_gdy_kursor,
            "wyjście",
            self.gra.kolor_tekstu,
        )
        self.czy_wiezienie = False

        self.skalar_czcionki = 24  # im wiekszy tym mniejsza czcionka
        self.font = pygame.font.Font(self.gra.czcionka, int(self.W / self.skalar_czcionki))
        self.informacja_o_wiezeniu = "idziesz do więzienia, stoisz 2 tury"

    def aktualizacja(self):
        pass

    def aktualizacja_zdarzen(self, event: pygame.event.Event):
        if self.wyjscie.is_clicked(event):
            self.zamknij()
            self.czy_wiezienie = False

    def wyswietl(self, screen: pygame.Surface):
        H = self.H
        W = self.W

        if self.czy_wiezienie:
            
            nakladka = pygame.Surface(screen.get_size())
            nakladka.set_alpha(self.gra.przezroczystosc_nakladki)  # Ustaw przezroczystość (0-255)
            nakladka.fill(self.gra.kolor_nakladki)
            screen.blit(nakladka, (0, 0))

            self.zaktualizuj_rozmiar_czcionki()
            self.wyswietl_teksty(screen)

            self.zdjecie = pygame.transform.scale(
                self.zdjecie, (0.45 * self.H, 0.45 * self.H)
            )
            screen.blit(self.zdjecie, (W * 0.2, H * 0.15))
            self.wyjscie.updateSize(W * 0.6, H * 0.3, W * 0.2, H * 0.15)
            self.wyjscie.draw(screen)

    def aktualizuj_rozmiar_okna(self, width, height):
        self.W = width
        self.H = height

    def zaktualizuj_rozmiar_czcionki(self):
        self.font = pygame.font.Font(self.gra.czcionka, int(self.W / self.skalar_czcionki))
        self.tekst = self.font.render(self.informacja_o_wiezeniu, True, (0, 0, 0))

    def wyswietl_teksty(self, screen):
        screen.blit(self.tekst, (self.W * 0.18, self.H * 0.7))

    def zamknij(self):
        self.gra.czy_akcja_zakonczona = True
