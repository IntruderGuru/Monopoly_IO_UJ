from typing import Collection

import pytest
import pygame

from src.Przycisk import Przycisk


class TestPrzycisk:
    PRZYCISK_POS_X = 100
    PRZYCISK_POS_Y = 100
    PRZYCISK_SZEROKOSC = 100
    PRZYCISK_WYSOKOSC = 100

    def setup_method(self):
        pygame.font.init()

        self.przycisk = Przycisk(TestPrzycisk.PRZYCISK_POS_X, TestPrzycisk.PRZYCISK_POS_Y,
                                 TestPrzycisk.PRZYCISK_SZEROKOSC, TestPrzycisk.PRZYCISK_WYSOKOSC,
                                 pygame.color.THECOLORS["green"],
                                 pygame.color.THECOLORS["violet"],
                                 "TestPrzycisk",
                                 pygame.color.THECOLORS["black"])

    def test_inicjalizacja_typow_zmiennych(self):
        assert type(self.przycisk.rect) is pygame.Rect
        assert isinstance(self.przycisk.color, (pygame.color.Color, Collection)) is True
        assert isinstance(self.przycisk.hover_color, (pygame.color.Color, Collection)) is True
        assert type(self.przycisk.font) is pygame.font.Font

    def test_is_clicked_wewnatrz_przycisku(self):
        pozycja_klikniecia = (150, 150)
        result_click = self.przycisk.is_clicked(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {
            "button": 1,
            "pos": pozycja_klikniecia
        }))

        assert result_click is True

    def test_is_clicked_zewnatrz_przycisku(self):
        pozycja_klikniecia = (250, 250)
        result_click = self.przycisk.is_clicked(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {
            "button": 1,
            "pos": pozycja_klikniecia
        }))

        assert result_click is False

    # odpowiednio: lewo-gora, prawo-dol, lewo-dol, prawo-gora
    @pytest.mark.parametrize("pozycja_klikniecia", [(100, 100), (199, 199), (100, 199), (199, 100)])
    def test_is_clicked_na_granicach_przycisku(self, pozycja_klikniecia):
        result_click = self.przycisk.is_clicked(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {
            "button": 1,
            "pos": pozycja_klikniecia
        }))

        assert result_click is True
