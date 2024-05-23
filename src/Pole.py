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
    MALE_POLE_WYMIARY: Vector2 = Vector2(30, 50)
    # warning: najlepiej gdy DUZE_POLE_WYMIARY ma oba wymiary z MALE_POLE_WYMIARY.y
    DUZE_POLE_WYMIARY: Vector2 = Vector2(50, 50)
    KOLOR_TLA = pygame.color.THECOLORS["red"]
    OFF_SET: Vector2 = Vector2(100, 100)
    SPACING: int = 10
    MAKSYMALNA_LICZBA_POL: int = 40
    # dla sciany = ilosc malych pol + jedno duze pole
    DLUGOSC_SCIANY_W_POLACH = 10

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

    @staticmethod
    def inicjalizacja_pozycji(numer_pola, kierunek_sciany) -> Vector2:
        lewo = Pole.OFF_SET.x
        gora = Pole.OFF_SET.y

        # Uwaga na orientacje dlugosci i szerokosci pola, jako x i y, zawsze os pozioma to x, os pionowa to y, niezaleznie od orientacji pola, nieintuicyjne!
        match kierunek_sciany:
            case KierunekPol.Gora:
                lewo += ((Pole.DUZE_POLE_WYMIARY.x + Pole.SPACING) if numer_pola % 10 != 0 else 0)
                lewo += 0 if (numer_pola % 10 == 0) else (((numer_pola % 10) - 1) * (Pole.MALE_POLE_WYMIARY.x + Pole.SPACING))

            case KierunekPol.Prawo:
                lewo += 9 * (Pole.MALE_POLE_WYMIARY.x + Pole.SPACING) + Pole.DUZE_POLE_WYMIARY.x + Pole.SPACING
                gora += 0 if (numer_pola % 10 == 0) else (((numer_pola % 10) - 1) * (Pole.MALE_POLE_WYMIARY.x + Pole.SPACING))
                gora += ((Pole.DUZE_POLE_WYMIARY.y + Pole.SPACING) if numer_pola % 10 != 0 else 0)

            case KierunekPol.Dol:
                lewo += (9 - (numer_pola % 10)) * (Pole.MALE_POLE_WYMIARY.x + Pole.SPACING)
                lewo += (Pole.DUZE_POLE_WYMIARY.x + Pole.SPACING)       # Czemu dziala nie mam bladego pojecia
                gora += 9 * (Pole.MALE_POLE_WYMIARY.x + Pole.SPACING) + Pole.DUZE_POLE_WYMIARY.y + Pole.SPACING

            case KierunekPol.Lewo:
                gora += (9 - (numer_pola % 10)) * (Pole.MALE_POLE_WYMIARY.x + Pole.SPACING) + Pole.DUZE_POLE_WYMIARY.y + Pole.SPACING

        return Vector2(lewo, gora)

    def __init__(self, numer: int, typ: str):
        self.numer = numer
        self.typ = typ
        self.kolor_naglowka = pygame.color.THECOLORS["violet"]
        self.wymiary: Vector2 = self.oblicz_rozmiar_pola(self.numer, Pole.DLUGOSC_SCIANY_W_POLACH, Pole.MAKSYMALNA_LICZBA_POL)
        self.kierunek_sciany = self.oblicz_zwrot_naglowka_pola(self.numer, Pole.DLUGOSC_SCIANY_W_POLACH, Pole.MAKSYMALNA_LICZBA_POL)
        self.pozycja: Vector2 = self.inicjalizacja_pozycji(self.numer, self.kierunek_sciany)

    def wyswietl_info(self) :
        return (f"Nazwa: {self.typ}")

    def render(self, screen):
        szerokosc_aktualny_kierunek = self.wymiary.x if self.kierunek_sciany in (KierunekPol.Gora, KierunekPol.Dol) else self.wymiary.y
        wysokosc_aktualny_kierunek = self.wymiary.y if self.kierunek_sciany in (KierunekPol.Gora, KierunekPol.Dol) else self.wymiary.x

        my_font = pygame.font.SysFont('Arial', 15)
        text_surface = my_font.render(str(self.numer), False, pygame.color.THECOLORS["black"])
        screen.blit(text_surface, (self.pozycja.x, self.pozycja.y))
        
        pygame.draw.rect(screen, Pole.KOLOR_TLA, pygame.Rect(self.pozycja.x, self.pozycja.y, szerokosc_aktualny_kierunek, wysokosc_aktualny_kierunek), width=1)
