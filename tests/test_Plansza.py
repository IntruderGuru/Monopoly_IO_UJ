import pygame
import pytest

from src.Pole import Pole
from src.Plansza import Plansza


class TestPlansza:
    def setup_method(self):
        pygame.init()

        self.plansza = Plansza()

    def test_typow_klasy_plansza(self):
        assert isinstance(self.plansza.plansza, list)

    @pytest.mark.parametrize("numer_pola", list(range(0, 40)))
    def test_pobierz_pole_poprawny_zakres(self, numer_pola):
        rezultat_pole = self.plansza.pobierz_pole(numer_pola)

        assert isinstance(rezultat_pole, Pole)

    @pytest.mark.parametrize("numer_pola", [-2, -1, -100, 41, 42, 50, 100, 1000])
    def test_pobierz_pole_niepoprawny_zakres(self, numer_pola):
        with pytest.raises(Exception):
            rezultat = self.plansza.pobierz_pole(numer_pola)

    def test_wczytaj_grafiki(self):
        path = "graphics/pola/pole_"
        extension = ".png"
        nr_pola = 0

        self.plansza.wczytaj_grafiki()

        for pole in self.plansza.plansza:
            tekst_sciezki = (path + str(nr_pola) + extension)
            nr_pola += 1

            assert pole.sciezka_do_grafiki == tekst_sciezki
