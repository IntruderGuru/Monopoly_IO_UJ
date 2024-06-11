import pygame

from abc import ABC, abstractmethod


class IAktualizacjaZdarzenia(ABC):
    """
        Interfejs umozliwiajacy aktualizacje nadchodzacego zdarzenia
    """

    @abstractmethod
    def aktualizacja_zdarzenia(self, event: pygame.event.EventType):
        pass
