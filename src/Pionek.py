import pygame
from enum import Enum


class Kierunek(Enum):
    Prawo = 0
    Dol = 1
    Lewo = 2
    Gora = 3


class Pionek:
    MIN_LICZBA_OCZEK = 1
    MAX_LICZBA_OCZEK = 12
    DLUGOSC_SCIANKI_W_POLACH = 10
    LICZBA_POL = 40

    def __init__(self, numer_pola: int, color: pygame.Color, grafika: str):
        self.numer_pola = numer_pola
        self.color = color
        self.grafika = grafika
        self.wymiary: pygame.Rect = pygame.Rect(100.0, 100.0, 35.0, 35.0)
        self.kierunek: Kierunek = Kierunek.Prawo

    def _zmien_left_top(self, left, top):
        self.wymiary.left = left
        self.wymiary.top = top

    def _ktore_pole_w_rzedzie(self):
        return ((self.numer_pola % 10) + 1) * 76.8

    def _zmien_pozycje(self):
        match self.kierunek:
            case Kierunek.Prawo:
                self._zmien_left_top(
                    23.2 + self._ktore_pole_w_rzedzie(), self.wymiary.top
                )

            case Kierunek.Dol:
                self._zmien_left_top(
                    self.wymiary.left, 23.2 + self._ktore_pole_w_rzedzie()
                )

            case Kierunek.Lewo:
                self._zmien_left_top(
                    868.0 - self._ktore_pole_w_rzedzie(), self.wymiary.top
                )

            case Kierunek.Gora:
                self._zmien_left_top(
                    self.wymiary.left, 868.0 - self._ktore_pole_w_rzedzie()
                )

    def przesun(self, liczba_pol: int) -> bool:
        if Pionek.MIN_LICZBA_OCZEK <= liczba_pol <= Pionek.MAX_LICZBA_OCZEK:
            self.numer_pola = (self.numer_pola + liczba_pol) % Pionek.LICZBA_POL
            self.kierunek = list(Kierunek)[
                self.numer_pola // Pionek.DLUGOSC_SCIANKI_W_POLACH
            ]
            self._zmien_pozycje()

            return True

        return False

    def wyswietlaj(self, window: pygame.Surface):
        pygame.draw.rect(window, self.color, self.wymiary)
