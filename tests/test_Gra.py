import os
import pytest
import pygame
from src.proxy.GraProxy import GraProxy
from src.Gra import Gra
from src.KontrolerWiadomosci import KontrolerWiadomosci


# Komenda aby uruchomic testy: python -m pytest ./tests
class TestGra:
    def setup_method(self):
        pygame.init()
        pygame.font.init()
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        self.font = pygame.font.Font(None, 20)
        self._kontroler_wiadomosci = KontrolerWiadomosci(self.font)
        self._screen = pygame.display.set_mode((1200, 800), pygame.RESIZABLE)
        self.gra = GraProxy(Gra(self._screen, self._kontroler_wiadomosci))

    # ten test powinien wyrzucić wyjątek, "out of index"
    # Podawany event w metodzie gra.aktualizacja_zdarzen(event), event= jest rowny None, poniewaz korzystamy z wewnetrznie zorganizowanej kolejki eventow
    def test_no_players_quantity_given(self):
        with pytest.raises(Exception):
            self.gra.dodaj_zdarzenie_do_kolejki(event=pygame.event.Event(pygame.KEYDOWN, {"unicode": 32, "key": pygame.K_SPACE}))
            self.gra.pozwol_wykonac_zdarzenie_z_kolejki()
            self.gra.aktualizacja_zdarzenia(event=None)
