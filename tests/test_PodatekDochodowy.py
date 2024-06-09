import pygame
import pytest

from src.PodatekDochodowy import PodatekDochodowy


class TestPodatekDochodowy:
    DOMYSLNA_KWOTA = 1000

    def setup_method(self):
        self.podatek_dochodowy = PodatekDochodowy(0, TestPodatekDochodowy.DOMYSLNA_KWOTA)

    def test_typ_zmiennych(self):
        assert isinstance(self.podatek_dochodowy.podatek, int)
        assert self.podatek_dochodowy.typ == "Podatek dochodowy"

    def test_wyswietl_info(self):
        informacja_zwrotna = self.podatek_dochodowy.wyswietl_info()
        oczekiwany_tekst = f"Stanąłeś na polu podatek dochodowy. Musisz zapłacić podatek w wysokości {TestPodatekDochodowy.DOMYSLNA_KWOTA}"

        assert oczekiwany_tekst == informacja_zwrotna

    @pytest.mark.skip
    def test_zaplac_podatek_poprawna_odpowiedz_wystarczajaca_kwota(self):
        pass
