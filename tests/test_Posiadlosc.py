import pygame
import pytest

from src.Posiadlosc import Posiadlosc
from src.Gracz import Gracz
from src.Gra import Gra
from src.KontrolerWiadomosci import KontrolerWiadomosci


#TODO: Zmiana typu z kolor: str na pygame.Color

class TestPosiadlosc:
    NUMER = 0
    NAZWA = "test"
    KOLOR = "czarny"
    CENA = 500
    CZYNSZ = 500
    ZASTAW = 500
    CENA_DOMU = 0

    def setup_method(self):
        pygame.init()

            # przepisz na mocki
        self.font = pygame.font.Font(None, 20)
        self.screen = pygame.display.set_mode((1200, 800), pygame.RESIZABLE)
        self._kontroler_wiadomosci = KontrolerWiadomosci(self.font)
        self._gra = Gra(self.screen, self._kontroler_wiadomosci)

        self.posiadlosc = Posiadlosc(TestPosiadlosc.NUMER, TestPosiadlosc.NAZWA, TestPosiadlosc.KOLOR,
                                     TestPosiadlosc.CENA, TestPosiadlosc.CZYNSZ, TestPosiadlosc.ZASTAW,
                                     TestPosiadlosc.CENA_DOMU)


    def test_inicjalizacja_typow(self):
        assert isinstance(self.posiadlosc.nazwa, str)
        assert isinstance(self.posiadlosc.kolor, str)
        assert isinstance(self.posiadlosc.cena, int)
        assert isinstance(self.posiadlosc.zastaw_kwota, int)
        assert isinstance(self.posiadlosc.cena_domu, int)
        assert isinstance(self.posiadlosc.wlasciciel, (None | Gracz)) is True
        assert isinstance(self.posiadlosc.czy_zastawiona, bool)
        assert isinstance(self.posiadlosc.liczba_domow, int)
        assert isinstance(self.posiadlosc.liczba_hoteli, int)

    @pytest.mark.parametrize("liczba_domow", (0, 1, 2))
    def test_zwroc_info(self, liczba_domow):
        self.posiadlosc.liczba_domow = liczba_domow

        zwrocone_info = self.posiadlosc.zwroc_info()
        przewidywane_info = \
            (f"Nazwa: {TestPosiadlosc.NAZWA} \n"
             f"Cena: {TestPosiadlosc.CENA}   Czynsz: {TestPosiadlosc.CZYNSZ}  Zastaw: {TestPosiadlosc.ZASTAW} "
             f"\nCena-dom: {TestPosiadlosc.CENA_DOMU}  Liczba domkow: {liczba_domow}") \
            if liczba_domow > 0 \
            else \
            (f"Nazwa: {TestPosiadlosc.NAZWA} \n"
             f"Cena: {TestPosiadlosc.CENA}   Czynsz: {TestPosiadlosc.CZYNSZ}  Zastaw: {TestPosiadlosc.ZASTAW} "
             f"\nCena-dom: {TestPosiadlosc.CENA_DOMU}")

        assert zwrocone_info == przewidywane_info

    def test_kup_posiadlosc_udany(self):
        self.posiadlosc.kup_posiadlosc()