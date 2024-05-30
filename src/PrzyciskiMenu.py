from src.Przycisk import Przycisk
from src.Wizualizator import Wizualizator


class PrzyciskiMenu:

    def __init__(self, H, W, wizualizator):

        self.wizualizator = wizualizator

        self.nowa_gra = Przycisk(
            W * 0.35,
            H * 0.4,
            W * 0.3,
            H * 0.1,
            self.wizualizator.kolor_przycisku,
            self.wizualizator.kolor_gdy_kursor,
            "Nowa gra",
            self.wizualizator.kolor_czcionki_na_przycisku,
        )

        self.wczytaj_gre = Przycisk(
            W * 0.35,
            H * 0.52,
            W * 0.3,
            H * 0.1,
            self.wizualizator.kolor_przycisku,
            self.wizualizator.kolor_gdy_kursor,
            "Wczytaj zapis",
            self.wizualizator.kolor_czcionki_na_przycisku,
        )

        self.wyjscie = Przycisk(
            W * 0.35,
            H * 0.64,
            W * 0.3,
            H * 0.1,
            self.wizualizator.kolor_przycisku,
            self.wizualizator.kolor_gdy_kursor,
            "Wyjscie",
            self.wizualizator.kolor_czcionki_na_przycisku,
        )

        self.two = Przycisk(
            W * 0.3,
            H * 0.5,
            H * 0.1,
            H * 0.1,
            self.wizualizator.kolor_przycisku,
            self.wizualizator.kolor_gdy_kursor,
            "2",
            self.wizualizator.kolor_czcionki_na_przycisku,
        )

        self.three = Przycisk(
            W * 0.4,
            H * 0.5,
            H * 0.1,
            H * 0.1,
            self.wizualizator.kolor_przycisku,
            self.wizualizator.kolor_gdy_kursor,
            "3",
            self.wizualizator.kolor_czcionki_na_przycisku,
        )

        self.four = Przycisk(
            W * 0.5,
            H * 0.5,
            H * 0.1,
            H * 0.1,
            self.wizualizator.kolor_przycisku,
            self.wizualizator.kolor_gdy_kursor,
            "4",
            self.wizualizator.kolor_czcionki_na_przycisku,
        )

        self.five = Przycisk(
            W * 0.6,
            H * 0.5,
            H * 0.1,
            H * 0.1,
            self.wizualizator.kolor_przycisku,
            self.wizualizator.kolor_gdy_kursor,
            "5",
            self.wizualizator.kolor_czcionki_na_przycisku,
        )

    def aktualizuj_rozmiar(self, W, H):
        # skalowanie do jakiejsc czesci, testowo
        MIN_W = 500
        MIN_H = 400
        W = max(W, MIN_W)
        H = max(H, MIN_H)

        self.nowa_gra.updateSize(W * 0.35,
            H * 0.4,
            W * 0.3,
            H * 0.1)
        self.wyjscie.updateSize(W * 0.35,
            H * 0.64,
            W * 0.3,
            H * 0.1)
        self.wczytaj_gre.updateSize(W * 0.35,
            H * 0.52,
            W * 0.3,
            H * 0.1)
        self.two.updateSize(W * 0.3,
            H * 0.5,
            H * 0.1,
            H * 0.1)
        self.three.updateSize(W * 0.4,
            H * 0.5,
            H * 0.1,
            H * 0.1)
        self.four.updateSize(W * 0.5,
            H * 0.5,
            H * 0.1,
            H * 0.1)
        self.five.updateSize(W * 0.6,
            H * 0.5,
            H * 0.1,
            H * 0.1)
