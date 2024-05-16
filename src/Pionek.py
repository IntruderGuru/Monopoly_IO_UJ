import pygame


class Pionek:
    MIN_LICZBA_OCZEK = 2
    MAX_LICZBA_OCZEK = 12

    def __init__(self, numer_pola: int, color: pygame.color.THECOLORS, grafika: str):
        self.numer_pola = numer_pola
        self.color = color
        self.grafika = grafika

    def zmien_grafike(self) -> bool:
        pass

    def przesun(self, liczba_pol: int) -> bool:
        if Pionek.MIN_LICZBA_OCZEK <= liczba_pol <= Pionek.MAX_LICZBA_OCZEK:
            self.numer_pola += liczba_pol
            return True

        return False

    def wyswietlaj(self, window: pygame.Surface):
        pygame.draw.rect(window, self.color, )