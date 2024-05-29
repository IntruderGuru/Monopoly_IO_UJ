import pygame
from src.Wizualizator import Wizualizator


class KontrolerWiadomosci:
    MAKSYMALNA_ILOSC_WIADOMOSCI = 15

    def __init__(self, font, wizualizator):
        self.wiadomosci: list[str] = list()
        self.ilosc_wiadomosci = 0
        self.ostatnia_pozycyjnie_wiadomosc_index = 0
        self.font: pygame.font.Font = font
        self.wizualizator = wizualizator

    def _render_text(self, text: str, pos, okno: pygame.Surface):
        text_surface = self.font.render(text, True, self.wizualizator.kolor_czcionki)
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

    def wyswietl(self, okno: pygame.Surface, szerokosc_okna):
        y_offset = 10

        wiadomosc_index = self.ostatnia_pozycyjnie_wiadomosc_index
        wiadomosc_index_end = (
            (self.ostatnia_pozycyjnie_wiadomosc_index - 1)
            % KontrolerWiadomosci.MAKSYMALNA_ILOSC_WIADOMOSCI
            if self.ilosc_wiadomosci == KontrolerWiadomosci.MAKSYMALNA_ILOSC_WIADOMOSCI
            else self.ilosc_wiadomosci - 1
        )

        while wiadomosc_index != wiadomosc_index_end:
            wiadomosc = self.wiadomosci[wiadomosc_index]

            if isinstance(wiadomosc, str | bytes):
                self._render_text(wiadomosc, (szerokosc_okna - 400, y_offset), okno)
                y_offset += 40

            wiadomosc_index = (
                wiadomosc_index + 1
            ) % KontrolerWiadomosci.MAKSYMALNA_ILOSC_WIADOMOSCI

        # for message in self.wiadomosci[-15:]:  # Wyświetla ostatnie 15 komunikatów
        #     if isinstance(message, str | bytes):
        #         self._render_text(message, (szerokosc_okna - 400, y_offset), okno)
        #         y_offset += 40
