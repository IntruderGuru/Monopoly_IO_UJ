import pygame
import pytest

from src.Gracz import Gracz
from src.Gra import Gra
from src.okno.AkcjaZastawOkno import AkcjaZastawOkno
from unittest.mock import MagicMock


class TestAkcjaZastawOkno:
    def setup_method(self):
        pygame.init()

        self.akcja_zastaw_okno = AkcjaZastawOkno(MagicMock())

    def test_typ_zmiennych_zainicjalizowanych(self):
        assert isinstance(self.akcja_zastaw_okno.gracz, (type(None), Gracz))
        assert isinstance(self.akcja_zastaw_okno.czy_zastaw, bool)
        assert isinstance(self.akcja_zastaw_okno.pole_png, (pygame.Surface | pygame.SurfaceType))

    def test_akcja_zastawienia(self):
        mock_gracz = MagicMock()
        mock_gracz.id = "fake_id"

        self.akcja_zastaw_okno.akcja_zastawiania(mock_gracz)

        assert mock_gracz == self.akcja_zastaw_okno.gracz

    @pytest.mark.xfail(reason="Po ustawieniu gracza, gracz nie moze byc typu None")
    def test_czy_gracz_null(self):
        self.akcja_zastaw_okno.akcja_zastawiania(None)

        assert self.akcja_zastaw_okno.gracz is not None

    @pytest.mark.xfail(reason="Gracz nie moze byc typu None, podczas wykonywania akcja na nim")
    def test_zastaw_gracz_none(self):
        self.akcja_zastaw_okno.gracz = None
        self.akcja_zastaw_okno.gracz.zastaw_posiadlosci()

    @pytest.mark.skip
    def test_klik_event_zastaw(self):
        # magic mock here
        pass