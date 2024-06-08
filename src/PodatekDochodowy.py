from src.Pole import Pole
from src.Gracz import Gracz
from numpy import random


class Zagadka:
    def __init__(
        self,
        tresc_zagadki: str,
        odpowiedz_a: str,
        odpowiedz_b: str,
        odpowiedz_c: str,
        poprawna: str,
    ) -> None:
        self.tresc_zagadki = tresc_zagadki
        self.odpowiedz_a = odpowiedz_a
        self.odpowiedz_b = odpowiedz_b
        self.odpowiedz_c = odpowiedz_c
        self.poprawna = poprawna


class Zagadki:

    def __init__(self) -> None:
        self.lista_zagadek = self.wczytaj_zagadki("data/zagadki.txt")
        self.permutacja = random.permutation(self.lista_zagadek)
        self.ind = 0

    def nastepna_zagadka(self) -> Zagadka:
        curr = self.ind
        self.ind = (self.ind + 1) % len(self.lista_zagadek)
        return self.permutacja[curr]

    def wczytaj_zagadki(self, plik: str) -> list[Zagadka]:
        zagadki = []
        with open(plik, "r", encoding="utf-8") as file:
            lines = file.readlines()
            i = 0
            while i < len(lines):
                if i + 4 >= len(lines):
                    raise ValueError(
                        f"Problem w linii {i}. Każda zagadka powinna mieć 5 linii danych."
                    )
                tresc = lines[i].strip()
                odpowiedz_a = lines[i + 1].strip()
                odpowiedz_b = lines[i + 2].strip()
                odpowiedz_c = lines[i + 3].strip()
                poprawna = lines[i + 4].strip()
                zagadka = Zagadka(
                    tresc, odpowiedz_a, odpowiedz_b, odpowiedz_c, poprawna
                )
                zagadki.append(zagadka)
                i += 6
        return zagadki


class PodatekDochodowy(Pole):

    def __init__(self, numer: int, podatek: int) -> None:
        super().__init__(numer, "Podatek dochodowy")
        self.podatek = podatek

    def zaplac_podatek(self, gra, gracz: Gracz, czy_dobra: bool) -> None:
        do_zaplaty = self.podatek
        if czy_dobra:
            gra._kontroler_wiadomosci.dodaj_wiadomosc(
                f"Udzieliłeś/udzieliłaś poprawnej odpowiedzi, koszt zostaje pomniejszony")
            do_zaplaty //= 2

        if gracz.wykonaj_oplate(gra, do_zaplaty):
            gra._kontroler_wiadomosci.dodaj_wiadomosc(
                "Podatek został zapłacony, zapłacono: " + str(do_zaplaty)
            )
        else:
            gra._kontroler_wiadomosci.dodaj_wiadomosc("Bankrutujesz")
