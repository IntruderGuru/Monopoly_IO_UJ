import pygame
from abc import abstractmethod


class Okno:
    @abstractmethod
    def aktualizacja(self):
        pass

    @abstractmethod
    def aktulizacja_zdarzen(self, event: pygame.event.Event):
        pass

    @abstractmethod
    def wyswietl(self, screen: pygame.Surface):
        pass
