import pygame
from typing import NamedTuple
from src.Pionek import Kierunek


class Vector2(NamedTuple):
    x: int
    y: int


class Pole:
    WYMIAR_NAGLOWKA: Vector2 = (30, 50)
    MALE_POLE_WYMIARY: Vector2 = (30, 50)
    DUZE_POLE_WYMIARY: Vector2 = (50, 50)
    KOLOR_TLA = pygame.color.THECOLORS["white"]
    OFF_SET: Vector2 = (100, 100)

    """
    numer_pola - nr. id pola [0, maksymalna_liczba_pol)
    dlugosc_sciany_w_polach - ilosc pol na jednym z czterech brzegow planszy, /*??odejmowana jest 1 do liczenia orientacji??*/, zakladamy ze plansza jest kwadratem 
    maksymalna_liczba_pol - ilosc pol na planszy
    """
    @staticmethod
    def oblicz_zwrot_naglowka_pola(numer_pola, dlugosc_sciany_w_polach, maksymalna_liczba_pol) -> Kierunek:
        if abs(maksymalna_liczba_pol / dlugosc_sciany_w_polach) != len(Kierunek):
            raise "Podano niepoprawne wymiary planszy!"

        return Kierunek((numer_pola % maksymalna_liczba_pol) // (dlugosc_sciany_w_polach))

    @staticmethod
    def oblicz_rozmiar_pola(numer_pola, dlugosc_sciany_w_polach, maksymalna_liczba_pol) -> Vector2:
        if abs(maksymalna_liczba_pol / dlugosc_sciany_w_polach) != len(Kierunek):
            raise "Podano niepoprawne wymiary planszy!"

        return Pole.DUZE_POLE_WYMIARY if (numer_pola % dlugosc_sciany_w_polach) == 0 else Pole.MALE_POLE_WYMIARY

    def __init__(self, numer: int, typ: str):
        self.numer = numer
        self.typ = typ
        self.kolor_naglowka = pygame.color.THECOLORS["violet"]

    def wyswietl_info(self) :
        return (f"Nazwa: {self.typ}")

    def render(self, screen):
        kierunek_sciany = self.oblicz_zwrot_naglowka_pola(self.numer, 10, 40)
        wymiary_pola = self.oblicz_rozmiar_pola(self.numer, 10, 40)

        left = Pole.OFF_SET.x
        top = Pole.OFF_SET.y

        match kierunek_sciany:
            case Kierunek.Gora:
                left += (self.numer % 10) * wymiary_pola.x

            case Kierunek.Prawo:
                left += 10 * wymiary_pola.y
                top += (self.numer % 10) * wymiary_pola.y

            case Kierunek.Dol:
                left += 10 - (self.numer % 10) * wymiary_pola.x

            case Kierunek.Lewo:
                top += 10 - (self.numer % 10) * wymiary_pola.y


        pygame.draw.rect(screen, Pole.KOLOR_TLA, pygame.Rect())
