from src.Pole import Pole
from src.Gracz import Gracz
from src.Gra import Gra
from numpy import random
from enum import Enum


class Odpowiedz(Enum):
    Odpowiedz_A = 0
    Odpowiedz_B = 1
    Odpowiedz_C = 2

class Zagadka():
    def __init__(self, tresc_zagadki: str, odpowiedz_a: str, odpowiedz_b: str, odpowiedz_c: str, poprawna: Odpowiedz) -> None:
        self.tresc_zagadki = tresc_zagadki
        self.odpowiedz_a = odpowiedz_a
        self.odpowiedz_b = odpowiedz_b
        self.odpowiedz_c = odpowiedz_c
        self.poprawna = poprawna
    
class Zagadki:
    lista_zagadek = [
        Zagadka()
    ]

    def __init__(self) -> None:
        self.permutacja = random.permutation(self.lista_zagadek)
        self.ind = 0

    def nastepna_zagadka(self) -> Zagadka:
        curr = self.ind
        self.ind = (self.ind + 1) % len(self.lista_zagadek)
        return self.permutacja[curr]

class PodatekDochodowy(Pole):

    def __init__(self, numer: int, podatek: int) -> None:
        super().__init__(numer, "Podatek Dochodowy")
        self.podatek = podatek

    def wyswietl_info(self) -> str:
        return (f"Stanąłeś na polu podatek dochodowy. Musisz zapłacić podatek w wysokości {self.podatek}")

    def zaplac_podatek(self, gra: Gra, gracz: Gracz, czy_dobra: bool) -> None:
        do_zaplaty = self.podatek
        if(czy_dobra):
            do_zaplaty /= 2
        
        if(do_zaplaty > gracz.kwota):
            if gra.pobierz_info_tak_nie("Nie masz wystarczająco dużo pieniędzy, aby zapłacić podatek. Czy chcesz zastawić którąś z nieruchmości? Jeśli tego nie zrobisz przegrywasz."):
                gracz.zastaw_nieruchomosci()
        if(do_zaplaty > gracz.kwota):
            gra.messages.append("Bankrutujesz")
        gracz.kwota -= do_zaplaty
        gra.messages.append("Podatek został zapłacony")