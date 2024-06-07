
import pytest
from unittest.mock import MagicMock
from src.Pionek import Pionek


# Komenda aby uruchomic testy: python -m pytest ./tests
class TestPionek:
    def setup_method(self):
        self.pionek = MagicMock()
        self.pionek.numer_pola = 0
        self.pionek.przesun = Pionek.przesun
        # Pozniej dodaj "mock object"

    @pytest.mark.parametrize("liczba_pol", list(range(Pionek.MIN_LICZBA_OCZEK, Pionek.MAX_LICZBA_OCZEK)))
    def test_ruch_prawidlowa_ilosc_oczek(self, liczba_pol):
        assert self.pionek.przesun(self.pionek, liczba_pol) is True

    @pytest.mark.parametrize("liczba_pol", [-1, -2, -50, -100])
    def test_ruch_nieprawidlowa_ilosc_oczek(self, liczba_pol):
        assert self.pionek.przesun(self.pionek, liczba_pol) is False
