import pygame
from interface.IGra import IGra
from src.Gra import Gra


class Kolejka:
    def __init__(self):
        self._kolejka: list[pygame.event.Event] = list()

    def rozmiar(self):
        return len(self._kolejka)

    def dodaj(self, element: pygame.event.Event):
        self._kolejka.append(element)

    def pobierz(self) -> pygame.event.Event | None:
        if len(self._kolejka) > 0:
            return self._kolejka.pop(0)

        return None


class GraProxy(IGra):
    def __init__(self, gra: Gra):
        self._kolejka_test_zdarzen: Kolejka = Kolejka()
        self._instancja_gra: Gra = gra
        self._czy_moze_wykonac_nastepne_zdarzenie = False

    def _zablokuj_wykonywanie_zdarzen(self):
        self._czy_moze_wykonac_nastepne_zdarzenie = False

    # override
    def aktualizacja_zdarzenia(self, event: pygame.event.Event):
        if self._czy_moze_wykonac_nastepne_zdarzenie is True:
            nastepne_zdarzenie = self._kolejka_test_zdarzen.pobierz()

            if nastepne_zdarzenie is not None:
                self._instancja_gra.wykonaj_zdarzenie(nastepne_zdarzenie)

            self._zablokuj_wykonywanie_zdarzen()

    def wykonaj_zdarzenie_z_kolejki(self):
        self._czy_moze_wykonac_nastepne_zdarzenie = True

    def dodaj_zdarzenie_do_kolejki(self, event: pygame.event.Event):
        self._kolejka_test_zdarzen.dodaj(event)

    def pobierz_instancje_gry(self) -> Gra:
        return self._instancja_gra
