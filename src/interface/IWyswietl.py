import pygame

from abc import ABC, abstractmethod


class IWyswietl(ABC):
    """
        Interfejs umozliwiajacy wyswietlanie obiektu na ekranie
    """

    @abstractmethod
    def wyswietl(self, okno: pygame.SurfaceType):
        pass
