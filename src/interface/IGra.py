import pygame
from abc import abstractmethod


class IGra:
    @abstractmethod
    def aktualizacja_zdarzenia(self, event: pygame.event.Event):
        pass

