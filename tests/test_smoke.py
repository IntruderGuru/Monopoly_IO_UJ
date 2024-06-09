import time

import pytest
import pygame

from Main import Main
from src.KontrolerWiadomosci import KontrolerWiadomosci
from src.Wizualizator import Wizualizator
from src.Gra import Gra


class MockMain(Main):
    def __init__(self):
        super()


class TestSmoke:
    def setup_method(self):
        pygame.init()
        pygame.font.init()

        time.sleep(3)

        self.wizualizator = Wizualizator()
        self._screen = pygame.display.set_mode((1200, 660), pygame.RESIZABLE)
        self._screen_info = pygame.display.Info()
        self._screen_width = self._screen_info.current_w
        self._screen_height = self._screen_info.current_h
        self.kontroler_wiadomosci = KontrolerWiadomosci(None, self.wizualizator)
        self.liczba_graczy = 2
        self.gracze = ["test_1", "test_2"]

        self.gra = Gra(self._screen, self.kontroler_wiadomosci, self.liczba_graczy, self.gracze, self.wizualizator, self._screen_width, self._screen_height, MockMain())

    def test_inicjalizacji(self):
        assert isinstance(self.gra._glowne_okno, (pygame.Surface, pygame.SurfaceType))
        assert isinstance(self.gra._gracze, list)
        assert isinstance(self.gra.wizualizator, Wizualizator)
        assert isinstance(self.gra._kontroler_wiadomosci, KontrolerWiadomosci)

    MIN_LICZBA_GRACZY = 2
    MAX_LICZBA_GRACZY_PRAWOSTRONNIE_OTWARTY = 6

    @pytest.mark.parametrize("liczba_graczy", list(range(MIN_LICZBA_GRACZY, MAX_LICZBA_GRACZY_PRAWOSTRONNIE_OTWARTY)))
    def test_liczba_graczy(self, liczba_graczy):
        nazwy_graczy = []

        gracz_id = 0
        while gracz_id < liczba_graczy:
            nazwy_graczy.append(str(f"test_{gracz_id}"))
            gracz_id += 1

        gra = Gra(self._screen, self.kontroler_wiadomosci, liczba_graczy, nazwy_graczy, self.wizualizator, self._screen_width, self._screen_height, MockMain())

        gra.tura()

    def test_tura_jednego_gracza(self):
        self.gra.tura()