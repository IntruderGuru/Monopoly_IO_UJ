import pygame
import pytest

from src.Wizualizator import Wizualizator
from src.Gracz import Gracz
from src.okno.AkcjaZastawOkno import AkcjaZastawOkno
from unittest.mock import MagicMock


class TestAkcjaZastawOkno:
    def setup_method(self):
        pygame.init()

        mock_gra = MagicMock()
        mock_gra.wizualizator = Wizualizator()

        self.akcja_zastaw_okno = AkcjaZastawOkno(gra=mock_gra)

    def test_typ_zmiennych_zainicjalizowanych(self):
        assert isinstance(self.akcja_zastaw_okno.gracz, (type(None), Gracz))
        assert isinstance(self.akcja_zastaw_okno.czy_zastaw, bool)
        assert isinstance(self.akcja_zastaw_okno.zastaw_png, (pygame.Surface | pygame.SurfaceType))

    @pytest.mark.xfail(reason="Po ustawieniu gracza, gracz nie moze byc typu None")
    def test_czy_gracz_null(self):
        event = pygame.event.Event(type=pygame.MOUSEBUTTONDOWN)
        self.akcja_zastaw_okno.aktualizacja_zdarzen(event)

        assert self.akcja_zastaw_okno.gracz is not None

    @pytest.mark.xfail(reason="Gracz nie moze byc typu None, podczas wykonywania akcja na nim")
    def test_zastaw_gracz_none(self):
        self.akcja_zastaw_okno.gracz = None
        self.akcja_zastaw_okno.gracz.zastaw_posiadlosci()

    @pytest.mark.skip
    def test_klik_event_zastaw(self):
        # magic mock here
        pass