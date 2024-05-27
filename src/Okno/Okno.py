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

    @abstractmethod
    def aktualizuj_rozmiar_okna(self, width, height):
        pass

    @abstractmethod
    def zamknij(self):
        pass
