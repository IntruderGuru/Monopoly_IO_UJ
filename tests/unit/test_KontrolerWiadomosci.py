import pytest
import pygame

from unittest.mock import MagicMock

from src.Wizualizator import Wizualizator
from src.KontrolerWiadomosci import KontrolerWiadomosci


class TestKontrolerWiadomosci:
    def setup_method(self):
        pygame.font.init()

        self.kontroler = KontrolerWiadomosci(MagicMock(), Wizualizator())

    podwojna_ilosc_maksymalnych_wiadomosci = KontrolerWiadomosci.MAKSYMALNA_ILOSC_WIADOMOSCI * 2

    @staticmethod
    def _dodaj_nowe_wiadomosci_do_kontrolera(kontroler: KontrolerWiadomosci, liczba_wiadomosc: int):
        numer = 0

        while numer < liczba_wiadomosc:
            kontroler.dodaj_wiadomosc(str(numer))
            numer += 1

    def test_typy_zmiennych_zainicjalizowane(self):
        assert isinstance(self.kontroler.wizualizator, Wizualizator)
        assert isinstance(self.kontroler.wiadomosci, list)
        assert isinstance(self.kontroler.font, pygame.font.Font)

    @pytest.mark.parametrize("numer_wiadomosci", list(range(0, podwojna_ilosc_maksymalnych_wiadomosci)))
    def test_dodaj_wiadomosc_ilosc_wiadomosci(self, numer_wiadomosci):
        self._dodaj_nowe_wiadomosci_do_kontrolera(self.kontroler, numer_wiadomosci)

        przewidywana_ilosc_wiadomosci = min(numer_wiadomosci, KontrolerWiadomosci.MAKSYMALNA_ILOSC_WIADOMOSCI)
        ilosc_wiadomosci_w_kontrolerze = self.kontroler.ilosc_wiadomosci

        assert przewidywana_ilosc_wiadomosci == ilosc_wiadomosci_w_kontrolerze

    poczworna_ilosc_maksymalnych_wiadomosci = KontrolerWiadomosci.MAKSYMALNA_ILOSC_WIADOMOSCI * 2

    @pytest.mark.parametrize("numer_wiadomosci", list(range(0, poczworna_ilosc_maksymalnych_wiadomosci)))
    def test_dodaj_wiadomosc_index_ostatniej_wiadomosci(self, numer_wiadomosci):
        self._dodaj_nowe_wiadomosci_do_kontrolera(self.kontroler, numer_wiadomosci)

        przewidywany_index_ostatniej_wiadomosci = numer_wiadomosci % KontrolerWiadomosci.MAKSYMALNA_ILOSC_WIADOMOSCI if self.kontroler.ilosc_wiadomosci >= KontrolerWiadomosci.MAKSYMALNA_ILOSC_WIADOMOSCI else 0
        rzeczywisty_ostatni_index_wiadomosci = self.kontroler.ostatnia_pozycyjnie_wiadomosc_index

        assert przewidywany_index_ostatniej_wiadomosci == rzeczywisty_ostatni_index_wiadomosci

    @pytest.mark.parametrize("numer_wiadomosci", list(range(0, podwojna_ilosc_maksymalnych_wiadomosci)))
    def test_usun_wszystkie_wiadomosci(self, numer_wiadomosci):
        self._dodaj_nowe_wiadomosci_do_kontrolera(self.kontroler, numer_wiadomosci)

        self.kontroler.usun_wszystkie_wiadomosci()

        ilosc_wiadomosci_w_liscie = len(self.kontroler.wiadomosci)
        ilosc_wiadomosci_atrybut = self.kontroler.ilosc_wiadomosci
        index_ostatniej_wiadomosci = self.kontroler.ostatnia_pozycyjnie_wiadomosc_index

        przewidywana_wartosc_dla_wszystkich = 0

        # symbol "\" powoduje możliwość zapisu zmiennej w nowej linijce
        assert ilosc_wiadomosci_w_liscie == ilosc_wiadomosci_atrybut == index_ostatniej_wiadomosci ==\
               przewidywana_wartosc_dla_wszystkich
