import pygame
from typing import NamedTuple
from enum import Enum
from src.Pionek import Kierunek


# TODO: Do usuniecia, korzystanie z jednego enuma z Pionka, problem z kolejnoscia wystepowania
# TODO: atrybutow w enumie w Pionku, zla kolejnosc, poprawna ponizej
class KierunekPol(Enum):
    Gora = 0
    Prawo = 1
    Dol = 2
    Lewo = 3


class Vector2(NamedTuple):
    x: int
    y: int


class Pole:
    WYMIAR_NAGLOWKA: Vector2 = Vector2(30, 50)
    # warning: najlepiej gdy DUZE_POLE_WYMIARY ma oba wymiary z MALE_POLE_WYMIARY.y
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
    def oblicz_zwrot_naglowka_pola(numer_pola, dlugosc_sciany_w_polach, maksymalna_liczba_pol) -> KierunekPol:
        if abs(maksymalna_liczba_pol / dlugosc_sciany_w_polach) != len(KierunekPol):
            raise "Podano niepoprawne wymiary planszy!"

        return KierunekPol((numer_pola % maksymalna_liczba_pol) // dlugosc_sciany_w_polach)

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

    # TODO: inicjalizacja tych wartosci w konstruktorze, aby za kazdym razem ich nie liczyc w metodzie render
    def render(self, screen):
        kierunek_sciany = self.oblicz_zwrot_naglowka_pola(self.numer, 10, 40)
        wymiary_pola = self.oblicz_rozmiar_pola(self.numer, 10, 40)

        lewo = Pole.OFF_SET.x
        gora = Pole.OFF_SET.y

        szerokosc_aktualny_kierunek = wymiary_pola.x if kierunek_sciany in (KierunekPol.Gora, KierunekPol.Dol) else wymiary_pola.y
        wysokosc_aktualny_kierunek = wymiary_pola.y if kierunek_sciany in (KierunekPol.Gora, KierunekPol.Dol) else wymiary_pola.x

        # Uwaga na orientacje dlugosci i szerokosci pola, jako x i y, zawsze os pozioma to x, os pionowa to y, niezaleznie od orientacji pola, nieintuicyjne!
        match kierunek_sciany:
            case KierunekPol.Gora:
                lewo += ((Pole.DUZE_POLE_WYMIARY.x + Pole.SPACING) if self.numer % 10 != 0 else 0)
                lewo += 0 if (self.numer % 10 == 0) else (((self.numer % 10) - 1) * (Pole.MALE_POLE_WYMIARY.x + Pole.SPACING))

            case KierunekPol.Prawo:
                lewo += 9 * (Pole.MALE_POLE_WYMIARY.x + Pole.SPACING) + Pole.DUZE_POLE_WYMIARY.x + Pole.SPACING
                gora += 0 if (self.numer % 10 == 0) else (((self.numer % 10) - 1) * (Pole.MALE_POLE_WYMIARY.x + Pole.SPACING))
                gora += ((Pole.DUZE_POLE_WYMIARY.y + Pole.SPACING) if self.numer % 10 != 0 else 0)

            case KierunekPol.Dol:
                lewo += (9 - (self.numer % 10)) * (Pole.MALE_POLE_WYMIARY.x + Pole.SPACING)
                lewo += (Pole.DUZE_POLE_WYMIARY.x + Pole.SPACING)       # Czemu dziala nie mam bladego pojecia
                gora += 9 * (Pole.MALE_POLE_WYMIARY.x + Pole.SPACING) + Pole.DUZE_POLE_WYMIARY.y + Pole.SPACING

            case KierunekPol.Lewo:
                gora += (9 - (self.numer % 10)) * (Pole.MALE_POLE_WYMIARY.x + Pole.SPACING) + Pole.DUZE_POLE_WYMIARY.y + Pole.SPACING

        my_font = pygame.font.SysFont('Arial', 30)
        text_surface = my_font.render(str(self.numer), False, pygame.color.THECOLORS["black"])
        screen.blit(text_surface, (lewo, gora))
        pygame.draw.rect(screen, Pole.KOLOR_TLA, pygame.Rect(lewo, gora, szerokosc_aktualny_kierunek, wysokosc_aktualny_kierunek), width=1)
