import pygame
from src.Wizualizator import Wizualizator


class KontrolerWiadomosci:
    MAKSYMALNA_ILOSC_WIADOMOSCI = 8

    def __init__(self, font, wizualizator):
        self.wiadomosci: list[str] = list()
        self.ilosc_wiadomosci = 0
        self.ostatnia_pozycyjnie_wiadomosc_index = 0
        # self.font: pygame.font.Font = font
        self.wizualizator = wizualizator
        self.W = 1200
        self.H = 800
        self.skalar_czcionki = 60 # im wiekszy tym mniejsza czcionka
        self.font = pygame.font.Font(self.wizualizator.czcionka, int(self.W / self.skalar_czcionki))
        self.koordynaty_ostatniej_wiadomosci = 0

    def _render_text(self, text: str, pos, okno: pygame.Surface, ostatnia_wiadomosc):

        if ostatnia_wiadomosc:
            self.font = pygame.font.Font(self.wizualizator.czcionka, int(self.W / (self.skalar_czcionki - 15)))
            text_surface = self.font.render(text, True, self.wizualizator.kolor_ostatniej_wiadomosci)
        else:
            self.font = pygame.font.Font(self.wizualizator.czcionka, int(self.W / self.skalar_czcionki))
            text_surface = self.font.render(text, True, self.wizualizator.kolor_wiadomosci)
        okno.blit(text_surface, pos)

    def dodaj_wiadomosc(self, tresc: str):

        if self.ilosc_wiadomosci < KontrolerWiadomosci.MAKSYMALNA_ILOSC_WIADOMOSCI:
            self.ilosc_wiadomosci += 1
            self.wiadomosci.append(tresc)
        else:
            self.wiadomosci[self.ostatnia_pozycyjnie_wiadomosc_index] = tresc
            self.ostatnia_pozycyjnie_wiadomosc_index = (
                self.ostatnia_pozycyjnie_wiadomosc_index + 1
            ) % KontrolerWiadomosci.MAKSYMALNA_ILOSC_WIADOMOSCI

    def usun_wszystkie_wiadomosci(self):
        self.wiadomosci.clear()
        self.ilosc_wiadomosci = 0
        self.ostatnia_pozycyjnie_wiadomosc_index = 0

    def wyswietl(self, okno: pygame.Surface, W, H):

        self.H = H
        self.W = W

        y_offset = 0.06

        wiadomosc_index = self.ostatnia_pozycyjnie_wiadomosc_index
        wiadomosc_index_end = (
            (self.ostatnia_pozycyjnie_wiadomosc_index - 1)
            % KontrolerWiadomosci.MAKSYMALNA_ILOSC_WIADOMOSCI
            if self.ilosc_wiadomosci == KontrolerWiadomosci.MAKSYMALNA_ILOSC_WIADOMOSCI
            else self.ilosc_wiadomosci - 1
        )

        wiadomosc_number = 0
        i = 0
        ostatnia_wiadomosc = False
        while wiadomosc_number < self.ilosc_wiadomosci:
            if wiadomosc_number == self.ilosc_wiadomosci - 1:
                ostatnia_wiadomosc = True

            # while wiadomosc_index != wiadomosc_index_end:
            wiadomosc = self.wiadomosci[wiadomosc_index]

            if isinstance(wiadomosc, str | bytes):
                self._render_text(wiadomosc, (W * 0.595, H * (0.48 + (i * y_offset))), okno, ostatnia_wiadomosc)
                if ostatnia_wiadomosc:
                    self.koordynaty_ostatniej_wiadomosci = (H * (0.467 + (i * y_offset)))

            wiadomosc_index = (
                wiadomosc_index + 1
            ) % KontrolerWiadomosci.MAKSYMALNA_ILOSC_WIADOMOSCI
            wiadomosc_number += 1
            i += 1