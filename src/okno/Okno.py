import pygame
from abc import abstractmethod


class Okno:
    @staticmethod
    def wysrodkuj_obraz(okno: pygame.Vector2, obraz: pygame.Vector2) -> pygame.Vector2:
        left = (okno.x // 2) - (obraz.x // 2)
        top = (okno.y // 2) - (obraz.y // 2)

        return pygame.Vector2(left, top)

    @abstractmethod
    def aktualizacja(self):
        pass

    @abstractmethod
    def aktualizacja_zdarzen(self, event: pygame.event.Event):
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
