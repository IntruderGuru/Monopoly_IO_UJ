import os
import pytest
import pygame

from src.Wizualizator import Wizualizator
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
        self.wizualizator = Wizualizator()

        self._kontroler_wiadomosci = KontrolerWiadomosci(self.font, self.wizualizator)
        self._screen = pygame.display.set_mode((1200, 800), pygame.RESIZABLE)

        liczba_graczy = 2
        lista_nazw_graczy = ["test1", "test2"]
        self.gra = GraProxy(
            Gra(
                self._screen,
                self._kontroler_wiadomosci,
                liczba_graczy,
                lista_nazw_graczy,
                self.wizualizator,
                1200,
                800,
                self,
            )
        )

    # ten test powinien wyrzucić wyjątek, "out of index"
    # Podawany event w metodzie gra.aktualizacja_zdarzen(event), event= jest rowny None, poniewaz korzystamy z wewnetrznie zorganizowanej kolejki eventow
    # python -m pytest ./tests -k "test_no_players_quantity_given"
    def test_brak_podanej_ilosci_graczy(self):
        try:
            self.gra.dodaj_zdarzenie_do_kolejki(
                event=pygame.event.Event(
                    pygame.KEYDOWN, {"unicode": 32, "key": pygame.K_SPACE}
                )
            )
            self.gra.pozwol_wykonac_zdarzenie_z_kolejki()
            self.gra.aktualizacja_zdarzenia(event=None)
        except Exception as e:
            pytest.fail(
                f"Test nie powinien rzucac wyjatku, problem ze spacja na poczatku gry! {e}"
            )
