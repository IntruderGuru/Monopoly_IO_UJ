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

    MALE_POLE_WYMIARY: Vector2 = Vector2(44, 70)
    # warning: najlepiej, gdy DUZE_POLE_WYMIARY ma oba wymiary z MALE_POLE_WYMIARY.y
    DUZE_POLE_WYMIARY: Vector2 = Vector2(70, 70)
    OFF_SET: Vector2 = Vector2(12, 12)
    SPACING: int = 10
    MAKSYMALNA_LICZBA_POL: int = 40
    # dla sciany = ilosc malych pol + jedno duze pole
    DLUGOSC_SCIANY_W_POLACH = 10

    def __init__(self, numer_pola: int, color: pygame.color, grafika: str, W, H, il):
        self.numer_pola = numer_pola
        self.color = color
        self.sciezka_do_grafiki = grafika
        self.szerokosc_ratio = 1
        self.wysokosc_ratio = 1
        self.W = W
        self.H = H
        self.kierunek: KierunekPol = KierunekPol.Gora
        self.wymiary: Vector2 = Vector2(20, 20)
        self.pozycja: Vector2 = self.oblicz_nowa_pozycje(self.numer_pola, self.kierunek)
        self.zdjecie_pionek = pygame.transform.scale(
            pygame.image.load(self.sciezka_do_grafiki), (self.wymiary.x, self.wymiary.y)
        )
        self.ilosc_graczy_na_polu = il
        
    def oblicz_nowa_pozycje(self, numer_pola, kierunek_sciany) -> Vector2:
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

        return Vector2(lewo * self.szerokosc_ratio, gora * self.wysokosc_ratio)

    def przesun(self, liczba_pol: int, gra) -> bool:
        if liczba_pol <= 0:
            return False
        gra._plansza.plansza[self.numer_pola].ilosc_graczy_na_polu -= 1
        self.numer_pola = (self.numer_pola + liczba_pol) % Pionek.LICZBA_POL
        gra._plansza.plansza[self.numer_pola].ilosc_graczy_na_polu += 1
        self.kierunek = KierunekPol(self.numer_pola // Pionek.DLUGOSC_SCIANKI_W_POLACH)
        self.pozycja = self.oblicz_nowa_pozycje(self.numer_pola, self.kierunek)

        return True


    def aktualizacja_rozmiaru(self, szerokosc, wysokosc):
        szerokosc_ekranu = 1200
        wysokosc_ekranu = 660
        self.W = szerokosc
        self.H = wysokosc

        self.szerokosc_ratio = szerokosc / szerokosc_ekranu
        self.wysokosc_ratio = wysokosc / wysokosc_ekranu

        print(self.pozycja)
        self.pozycja = self.oblicz_nowa_pozycje(self.numer_pola, self.kierunek)
        print(self.pozycja)

    def wyswietl(self, okno: pygame.Surface, gra):
        skalar = 35
        
        self.zdjecie_pionek = pygame.transform.scale(
            pygame.image.load(self.sciezka_do_grafiki), (self.W / skalar, self.W / skalar)
        )
        self.ilosc_graczy_na_polu = gra._plansza.plansza[self.numer_pola].ilosc_graczy_na_polu
        if self.ilosc_graczy_na_polu > 1:
            self.maska = pygame.transform.scale(
                pygame.image.load(f"graphics/pionek/pionek{self.ilosc_graczy_na_polu}mask.png"), (self.W / skalar, self.W / skalar)
            )
        # zdjecie_pionek_transformed = pygame.transform.scale(self.zdjecie_pionek, (self.wymiary.x * self.szerokosc_ratio, self.wymiary.y * self.wysokosc_ratio))
        okno.blit(self.zdjecie_pionek, (self.pozycja.x, self.pozycja.y))
        if self.ilosc_graczy_na_polu > 1:
            okno.blit(self.maska, (self.pozycja.x, self.pozycja.y))
