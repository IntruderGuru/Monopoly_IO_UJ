import pygame
from enum import Enum
from typing import NamedTuple


class KierunekPol(Enum):
    Gora = 0
    Prawo = 1
    Dol = 2
    Lewo = 3


class Vector2(NamedTuple):
    x: int
    y: int


class Pionek:
    MIN_LICZBA_OCZEK = 2
    MAX_LICZBA_OCZEK = 12
    DLUGOSC_SCIANKI_W_POLACH = 10
    LICZBA_POL = 40

    MALE_POLE_WYMIARY: Vector2 = Vector2(30, 50)
    # warning: najlepiej gdy DUZE_POLE_WYMIARY ma oba wymiary z MALE_POLE_WYMIARY.y
    DUZE_POLE_WYMIARY: Vector2 = Vector2(50, 50)
    OFF_SET: Vector2 = Vector2(100, 100)
    SPACING: int = 10
    MAKSYMALNA_LICZBA_POL: int = 40
    # dla sciany = ilosc malych pol + jedno duze pole
    DLUGOSC_SCIANY_W_POLACH = 10

    @staticmethod
    def oblicz_nowa_pozycje(numer_pola, kierunek_sciany) -> Vector2:
        lewo = Pionek.OFF_SET.x
        gora = Pionek.OFF_SET.y

        # Uwaga na orientacje dlugosci i szerokosci pola, jako x i y, zawsze os pozioma to x, os pionowa to y, niezaleznie od orientacji pola, nieintuicyjne!
        match kierunek_sciany:
            case KierunekPol.Gora:
                lewo += ((Pionek.DUZE_POLE_WYMIARY.x + Pionek.SPACING) if numer_pola % 10 != 0 else 0)
                lewo += 0 if (numer_pola % 10 == 0) else (((numer_pola % 10) - 1) * (Pionek.MALE_POLE_WYMIARY.x + Pionek.SPACING))

            case KierunekPol.Prawo:
                lewo += 9 * (Pionek.MALE_POLE_WYMIARY.x + Pionek.SPACING) + Pionek.DUZE_POLE_WYMIARY.x + Pionek.SPACING
                gora += 0 if (numer_pola % 10 == 0) else (((numer_pola % 10) - 1) * (Pionek.MALE_POLE_WYMIARY.x + Pionek.SPACING))
                gora += ((Pionek.DUZE_POLE_WYMIARY.y + Pionek.SPACING) if numer_pola % 10 != 0 else 0)

            case KierunekPol.Dol:
                lewo += (9 - (numer_pola % 10)) * (Pionek.MALE_POLE_WYMIARY.x + Pionek.SPACING)
                lewo += (Pionek.DUZE_POLE_WYMIARY.x + Pionek.SPACING)       # Czemu dziala nie mam bladego pojecia
                gora += 9 * (Pionek.MALE_POLE_WYMIARY.x + Pionek.SPACING) + Pionek.DUZE_POLE_WYMIARY.y + Pionek.SPACING

            case KierunekPol.Lewo:
                gora += (9 - (numer_pola % 10)) * (Pionek.MALE_POLE_WYMIARY.x + Pionek.SPACING) + Pionek.DUZE_POLE_WYMIARY.y + Pionek.SPACING

        return Vector2(lewo, gora)

    def __init__(self, numer_pola: int, color: pygame.color, grafika: str):
        self.numer_pola = numer_pola
        self.color = color
        self.grafika = grafika
        self.kierunek: KierunekPol = KierunekPol.Gora
        self.wymiary: Vector2 = Vector2(20, 20)
        self.pozycja: Vector2 = self.oblicz_nowa_pozycje(self.numer_pola, self.kierunek)

    def przesun(self, liczba_pol: int) -> bool:
        if Pionek.MIN_LICZBA_OCZEK <= liczba_pol <= Pionek.MAX_LICZBA_OCZEK:
            self.numer_pola = (self.numer_pola + liczba_pol) % Pionek.LICZBA_POL
            self.kierunek = KierunekPol(self.numer_pola // Pionek.DLUGOSC_SCIANKI_W_POLACH)
            self.pozycja = self.oblicz_nowa_pozycje(self.numer_pola, self.kierunek)

            return True

        return False

    def wyswietl(self, okno: pygame.Surface):
        pygame.draw.rect(okno, self.color, pygame.Rect(self.pozycja.x, self.pozycja.y, self.wymiary.x, self.wymiary.y))

