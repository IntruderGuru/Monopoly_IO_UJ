import copy
import pytest
import pygame
from typing import Collection

from src.Przycisk import Przycisk


class TestPrzycisk:
    PRZYCISK_POS_X = 100
    PRZYCISK_POS_Y = 100
    PRZYCISK_SZEROKOSC = 100
    PRZYCISK_WYSOKOSC = 100

    LEWO_GORA = (PRZYCISK_POS_X, PRZYCISK_POS_Y)
    LEWO_DOL = (PRZYCISK_POS_X, PRZYCISK_POS_Y + PRZYCISK_WYSOKOSC - 1)
    PRAWO_GORA = (PRZYCISK_POS_X + PRZYCISK_SZEROKOSC - 1, PRZYCISK_POS_Y)
    PRAWO_DOL = (PRZYCISK_POS_X + PRZYCISK_SZEROKOSC - 1, PRZYCISK_POS_Y + PRZYCISK_WYSOKOSC - 1)

    def setup_method(self):
        pygame.init()
        # pygame.font.init()

        self.screen = pygame.display.set_mode((1200, 800), pygame.RESIZABLE)

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
        pozycja_klikniecia = (TestPrzycisk.PRZYCISK_POS_X + TestPrzycisk.PRZYCISK_SZEROKOSC // 2,
                              TestPrzycisk.PRZYCISK_POS_Y + TestPrzycisk.PRZYCISK_WYSOKOSC // 2)
        result_click = self.przycisk.is_clicked(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {
            "button": 1,
            "pos": pozycja_klikniecia
        }))

        assert result_click is True

    def test_is_clicked_zewnatrz_przycisku(self):
        pozycja_klikniecia = (TestPrzycisk.PRZYCISK_POS_X - TestPrzycisk.PRZYCISK_SZEROKOSC // 2,
                              TestPrzycisk.PRZYCISK_POS_Y - TestPrzycisk.PRZYCISK_WYSOKOSC // 2)
        result_click = self.przycisk.is_clicked(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {
            "button": 1,
            "pos": pozycja_klikniecia
        }))

        assert result_click is False

    # odpowiednio: lewo-gora, prawo-dol, lewo-dol, prawo-gora
    @pytest.mark.parametrize("pozycja_klikniecia", [LEWO_GORA, LEWO_DOL, PRAWO_GORA, PRAWO_DOL])
    def test_is_clicked_na_granicach_przycisku(self, pozycja_klikniecia):
        result_click = self.przycisk.is_clicked(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {
            "button": 1,
            "pos": pozycja_klikniecia
        }))

        assert result_click is True

    # Zmiana w display na HIDDEN sprawia ze ten nie przechodzi, testowany na RESIZABLE
    def test_hover_kolor(self):
        kursor_pozycja_w_przycisku = (TestPrzycisk.PRZYCISK_POS_X + TestPrzycisk.PRZYCISK_SZEROKOSC // 2,
                                      TestPrzycisk.PRZYCISK_POS_Y + TestPrzycisk.PRZYCISK_WYSOKOSC // 2)

        pygame.mouse.set_pos(kursor_pozycja_w_przycisku)
        self.przycisk.draw(self.screen)

        przycisk_tlo_kolor = self.screen.get_at(kursor_pozycja_w_przycisku)

        assert (przycisk_tlo_kolor == self.przycisk.hover_color)

    @pytest.mark.parametrize("pozycja_kursora", [LEWO_GORA, LEWO_DOL, PRAWO_GORA, PRAWO_DOL])
    def test_kolor_brzegi_przycisku(self, pozycja_kursora: tuple):
        pygame.mouse.set_pos(pozycja_kursora)
        self.przycisk.draw(self.screen)

        przycisk_tlo_kolor = self.screen.get_at(pozycja_kursora)

        assert (przycisk_tlo_kolor == self.przycisk.hover_color)

    # Uwaga na wymiary, nie dawać wartości równych, defaultowych!
    @pytest.mark.parametrize("wymiary", [(10, 10), (110, 110)])
    def test_updateSize_zgodne_wymiary(self, wymiary: tuple):
        poprzednie_wymiary = self.przycisk.pobierz_wymiary()

        self.przycisk.updateSize(TestPrzycisk.PRZYCISK_POS_X,
                                 TestPrzycisk.PRZYCISK_POS_Y,
                                 wymiary[0], wymiary[1])

        nowe_wymiary = self.przycisk.pobierz_wymiary()

        assert poprzednie_wymiary.width != nowe_wymiary.width
        assert poprzednie_wymiary.height != nowe_wymiary.height
        assert wymiary[0] == nowe_wymiary.width
        assert wymiary[1] == nowe_wymiary.height

    @pytest.mark.parametrize("wymiary", [(0, 0), (-5, -10), (-2, 10), (20, -43)])
    def test_updateSize_niezgodne_wymiary(self, wymiary: tuple):
        poprzednie_wymiary = self.przycisk.pobierz_wymiary()

        self.przycisk.updateSize(TestPrzycisk.PRZYCISK_POS_X,
                                 TestPrzycisk.PRZYCISK_POS_Y,
                                 wymiary[0], wymiary[1])

        nowe_wymiary = self.przycisk.pobierz_wymiary()

        assert poprzednie_wymiary.width == nowe_wymiary.width
        assert poprzednie_wymiary.height == nowe_wymiary.height
        assert wymiary[0] != nowe_wymiary.width
        assert wymiary[1] != nowe_wymiary.height
