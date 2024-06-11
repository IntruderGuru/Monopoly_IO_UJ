import pytest
import pygame
import os
import itertools

from Main import Main
from src.Gracz import Gracz
from src.Gra import Gra
from src.interface.IGra import IGra
from src.proxy.GraProxy import GraProxy
from src.Wizualizator import Wizualizator
from src.KontrolerWiadomosci import KontrolerWiadomosci

from unittest.mock import MagicMock


class MockMain(Main):
    def __init__(self):
        super()


class TestScenariuszowy:
    def setup_method(self):
        self.mock_main = MockMain()

        pygame.init()
        pygame.font.init()

        os.environ["SDL_VIDEO_CENTERED"] = "1"

        self.font = pygame.font.Font(None, 20)
        self.wizualizator = Wizualizator()

        self.kontroler_wiadomosci = KontrolerWiadomosci(self.font, self.wizualizator)
        self.okno = pygame.display.set_mode((1200, 800), pygame.RESIZABLE)

        self.liczba_graczy = 2
        self.lista_nazw_graczy = ["test1", "test2"]

        self.szerokosc = 1200
        self.wysokosc = 800

        self.gra = GraProxy(
            Gra(
                self.okno,
                self.kontroler_wiadomosci,
                self.liczba_graczy,
                self.lista_nazw_graczy,
                self.wizualizator,
                self.szerokosc,
                self.wysokosc,
                self.mock_main
            )
        )

    def test_kolejnosc_gracz(self):
        lista_graczy_z_gry: Gracz = self.gra.pobierz_instancje_gry()._gracze
        lista_graczy_z_konstruktora: [str] = self.lista_nazw_graczy

        for (gracz_z_gry, gracz_z_listy) in zip(lista_graczy_z_gry, lista_graczy_z_konstruktora):
            assert gracz_z_gry.id is gracz_z_listy

    # Scenariusz 1
    @pytest.mark.skip
    def test_scenariusz_jeden(self):
        pass
        event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_SPACE})

        self.gra.dodaj_zdarzenie_do_kolejki(event)