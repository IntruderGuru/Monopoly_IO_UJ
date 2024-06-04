import pygame
from typing import NamedTuple
from enum import Enum


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
    MALE_POLE_WYMIARY: Vector2 = Vector2(44, 70)
    # warning: najlepiej, gdy DUZE_POLE_WYMIARY ma oba wymiary z MALE_POLE_WYMIARY.y
    DUZE_POLE_WYMIARY: Vector2 = Vector2(70, 70)
    KOLOR_TLA = pygame.Color(28,28,30,255)
    OFF_SET: Vector2 = Vector2(12, 12)
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
        if abs(maksymalna_liczba_pol / dlugosc_sciany_w_polach) != len(KierunekPol):
            raise "Podano niepoprawne wymiary planszy!"

        return Pole.DUZE_POLE_WYMIARY if (numer_pola % dlugosc_sciany_w_polach) == 0 else Pole.MALE_POLE_WYMIARY

    # def inicjalizacja_pozycji(self, numer_pola, kierunek_sciany) -> Vector2:
    #     lewo = Pole.OFF_SET.x
    #     gora = Pole.OFF_SET.y
    #
    #     # Uwaga na orientacje dlugosci i szerokosci pola, jako x i y, zawsze os pozioma to x, os pionowa to y, niezaleznie od orientacji pola, nieintuicyjne!
    #     match kierunek_sciany:
    #         case KierunekPol.Gora:
    #             lewo += ((Pole.DUZE_POLE_WYMIARY.x * self.szerokosc_ratio + Pole.SPACING) if numer_pola % 10 != 0 else 0)
    #             lewo += 0 if (numer_pola % 10 == 0) else (((numer_pola % 10) - 1) * (Pole.MALE_POLE_WYMIARY.x * self.szerokosc_ratio + Pole.SPACING))
    #
    #         case KierunekPol.Prawo:
    #             lewo += 9 * (Pole.MALE_POLE_WYMIARY.x * self.szerokosc_ratio + Pole.SPACING) + Pole.DUZE_POLE_WYMIARY.x * self.szerokosc_ratio + Pole.SPACING
    #             gora += 0 if (numer_pola % 10 == 0) else (((numer_pola % 10) - 1) * (Pole.MALE_POLE_WYMIARY.x * self.wysokosc_ratio + Pole.SPACING))
    #             gora += ((Pole.DUZE_POLE_WYMIARY.y * self.wysokosc_ratio + Pole.SPACING) if numer_pola % 10 != 0 else 0)
    #
    #         case KierunekPol.Dol:
    #             lewo += (9 - (numer_pola % 10)) * (Pole.MALE_POLE_WYMIARY.x * self.szerokosc_ratio + Pole.SPACING)
    #             lewo += (Pole.DUZE_POLE_WYMIARY.x * self.szerokosc_ratio + Pole.SPACING)       # Czemu dziala nie mam bladego pojecia
    #             gora += 9 * (Pole.MALE_POLE_WYMIARY.x * self.wysokosc_ratio + Pole.SPACING) + Pole.DUZE_POLE_WYMIARY.y * self.wysokosc_ratio + Pole.SPACING
    #
    #         case KierunekPol.Lewo:
    #             gora += (9 - (numer_pola % 10)) * (Pole.MALE_POLE_WYMIARY.x * self.wysokosc_ratio + Pole.SPACING) + Pole.DUZE_POLE_WYMIARY.y * self.wysokosc_ratio + Pole.SPACING
    #
    #     return Vector2(lewo, gora)

    def inicjalizacja_pozycji(self, numer_pola, kierunek_sciany) -> Vector2:
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

        return Vector2(lewo * self.szerokosc_ratio, gora * self.wysokosc_ratio)

    def __init__(self, numer: int, typ: str):
        self.numer = numer
        self.typ = typ
        self.szerokosc_ratio = 1
        self.wysokosc_ratio = 1
        self.kupione_przez = 0 #jesli 0 to nie kupione
        self.kolor_naglowka = pygame.color.THECOLORS["violet"]
        self.wymiary: Vector2 = self.oblicz_rozmiar_pola(self.numer, Pole.DLUGOSC_SCIANY_W_POLACH, Pole.MAKSYMALNA_LICZBA_POL)
        self.kierunek_sciany = self.oblicz_zwrot_naglowka_pola(self.numer, Pole.DLUGOSC_SCIANY_W_POLACH, Pole.MAKSYMALNA_LICZBA_POL)
        self.pozycja: Vector2 = self.inicjalizacja_pozycji(self.numer, self.kierunek_sciany)
        self.sciezka_do_grafiki = "..."

    def zwroc_info(self) -> str:
        return f"Nazwa: {self.typ}"

    def aktualizacja_rozmiaru(self, szerokosc, wysokosc):
        szerokosc_ekranu = 1200
        wysokosc_ekranu = 660

        self.szerokosc_ratio = szerokosc / szerokosc_ekranu
        self.wysokosc_ratio = wysokosc / wysokosc_ekranu

        # print((szerokosc, wysokosc))

        self.pozycja = self.inicjalizacja_pozycji(self.numer, self.kierunek_sciany)

    def render(self, screen):
        szerokosc_aktualny_kierunek = self.wymiary.x if self.kierunek_sciany in (KierunekPol.Gora, KierunekPol.Dol) else self.wymiary.y
        wysokosc_aktualny_kierunek = self.wymiary.y if self.kierunek_sciany in (KierunekPol.Gora, KierunekPol.Dol) else self.wymiary.x

        szerokosc_aktualny_kierunek *= self.szerokosc_ratio
        wysokosc_aktualny_kierunek *= self.wysokosc_ratio

        test_wymiary = Pole.DUZE_POLE_WYMIARY if self.numer in (0, 10, 20, 30) else Pole.MALE_POLE_WYMIARY
        nowa_szerokosc = test_wymiary.x
        nowa_wysokosc = test_wymiary.y

        obrot = 0
        match self.kierunek_sciany:
            case KierunekPol.Dol:
                nowa_szerokosc *= self.szerokosc_ratio
                nowa_wysokosc *= self.wysokosc_ratio
                obrot = 0
            case KierunekPol.Lewo:
                nowa_szerokosc *= self.wysokosc_ratio
                nowa_wysokosc *= self.szerokosc_ratio
                obrot = 270
            case KierunekPol.Gora:
                nowa_szerokosc *= self.szerokosc_ratio
                nowa_wysokosc *= self.wysokosc_ratio
                obrot = 180
            case KierunekPol.Prawo:
                nowa_szerokosc *= self.wysokosc_ratio
                nowa_wysokosc *= self.szerokosc_ratio
                obrot = 90

        pole_surface = pygame.transform.scale(pygame.image.load(self.sciezka_do_grafiki), (nowa_szerokosc, nowa_wysokosc))
        pole_surface = pygame.transform.rotate(pole_surface, obrot)

        self.renderuj_otoczke(screen, szerokosc_aktualny_kierunek, wysokosc_aktualny_kierunek)
        screen.blit(pole_surface, (self.pozycja.x, self.pozycja.y))
        

    def renderuj_otoczke(self, screen, szerokosc_aktualny_kierunek, wysokosc_aktualny_kierunek):
        
        color = (0, 0, 0)
        

        if self.kupione_przez == 0:
            return
        elif self.kupione_przez == 1:
            color = (255, 0, 0)
        elif self.kupione_przez == 2:
            color = (0, 255, 0)
        elif self.kupione_przez == 3:
            color = (0, 0, 255)
        elif self.kupione_przez == 4:
            color = (255, 255, 0)
        elif self.kupione_przez == 5:
            color = (184, 3, 255)

        pygame.draw.rect(screen, color, pygame.Rect(self.pozycja.x- 2.5, self.pozycja.y - 2.5, szerokosc_aktualny_kierunek + 5, wysokosc_aktualny_kierunek + 5), width = 100)