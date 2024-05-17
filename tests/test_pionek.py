import pytest
import pygame
from src.Pionek import Pionek


# Komenda aby uruchomic testy: python -m pytest ./tests
class TestPionek:
    def setup_method(self):
        self.pionek = Pionek(0, pygame.color.THECOLORS["black"], "graphics")
        # Pozniej dodaj "mock object"

    @pytest.mark.parametrize("liczba_pol", list(range(Pionek.MIN_LICZBA_OCZEK, Pionek.MAX_LICZBA_OCZEK)))
    def test_ruch_prawidlowa_ilosc_oczek(self, liczba_pol):
        assert self.pionek.przesun(liczba_pol) is True

    @pytest.mark.parametrize("liczba_pol", [-1, 0, 1, 13, 14])
    def test_ruch_nieprawidlowa_ilosc_oczek(self, liczba_pol):
        assert self.pionek.przesun(liczba_pol) is False
