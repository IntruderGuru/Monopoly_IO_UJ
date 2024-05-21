import pygame
from typing import NamedTuple
from src.Pionek import Kierunek


class Vector2(NamedTuple):
    x: int
    y: int


class Pole:
    WYMIAR_NAGLOWKA: Vector2 = Vector2(30, 50)
    MALE_POLE_WYMIARY: Vector2 = Vector2(30, 50)
    DUZE_POLE_WYMIARY: Vector2 = Vector2(50, 50)
    KOLOR_TLA = pygame.color.THECOLORS["red"]
    OFF_SET: Vector2 = Vector2(100, 100)
    SPACING: int = 10

    """
    numer_pola - nr. id pola [0, maksymalna_liczba_pol)
    dlugosc_sciany_w_polach - ilosc pol na jednym z czterech brzegow planszy, /*??odejmowana jest 1 do liczenia orientacji??*/, zakladamy ze plansza jest kwadratem 
    maksymalna_liczba_pol - ilosc pol na planszy
    """
    @staticmethod
    def oblicz_zwrot_naglowka_pola(numer_pola, dlugosc_sciany_w_polach, maksymalna_liczba_pol) -> Kierunek:
        if abs(maksymalna_liczba_pol / dlugosc_sciany_w_polach) != len(Kierunek):
            raise "Podano niepoprawne wymiary planszy!"

        return Kierunek((numer_pola % maksymalna_liczba_pol) // dlugosc_sciany_w_polach)

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

        lewo = Pole.OFF_SET.x
        gora = Pole.OFF_SET.y

        szerokosc_aktualny_kierunek = wymiary_pola.x if kierunek_sciany in (Kierunek.Gora, Kierunek.Dol) else wymiary_pola.y
        wysokosc_aktualny_kierunek = wymiary_pola.y if kierunek_sciany in (Kierunek.Gora, Kierunek.Dol) else wymiary_pola.x

        # szerokosc_przeciwny_kierunek = wymiary_pola.y if kierunek_sciany in (Kierunek.Gora, Kierunek.Dol) else wymiary_pola.x
        # wysokosc_przeciwny_kierunek = wymiary_pola.x if kierunek_sciany in (Kierunek.Gora, Kierunek.Dol) else wymiary_pola.y

        # Uwaga na orientacje dlugosci i szerokosci pola, jako x i y, zawsze os pozioma to x, os pionowa to y, niezaleznie od orientacji pola, nieintuicyjne!
        match kierunek_sciany:
            case Kierunek.Gora:
                lewo += ((self.numer % 10) * (Pole.MALE_POLE_WYMIARY.x + Pole.SPACING)
                         + (Pole.DUZE_POLE_WYMIARY.x if self.numer % 10 != 0 else 0))

            case Kierunek.Prawo:
                lewo += 9 * (Pole.MALE_POLE_WYMIARY.x + Pole.SPACING) + Pole.DUZE_POLE_WYMIARY.x
                gora += (self.numer % 10) * (Pole.MALE_POLE_WYMIARY.x + Pole.SPACING)

            case Kierunek.Dol:
                lewo += (10 - (self.numer % 10)) * (Pole.MALE_POLE_WYMIARY.x + Pole.SPACING) + (Pole.DUZE_POLE_WYMIARY.x if self.numer % 10 == 0 else 0)
                gora += 9 * (Pole.MALE_POLE_WYMIARY.x + Pole.SPACING) + Pole.DUZE_POLE_WYMIARY.y

            case Kierunek.Lewo:
                gora += (10 - (self.numer % 10)) * (Pole.MALE_POLE_WYMIARY.x + Pole.SPACING)

        pygame.draw.rect(screen, Pole.KOLOR_TLA, pygame.Rect(lewo, gora, szerokosc_aktualny_kierunek, wysokosc_aktualny_kierunek), width=1)
