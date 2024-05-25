from src.Pole import Pole
from src.Gracz import Gracz
from numpy import random
from src.Odpowiedz import Odpowiedz


class Zagadka():
    def __init__(self, tresc_zagadki: str, odpowiedz_a: str, odpowiedz_b: str, odpowiedz_c: str, poprawna: Odpowiedz) -> None:
        self.tresc_zagadki = tresc_zagadki
        self.odpowiedz_a = odpowiedz_a
        self.odpowiedz_b = odpowiedz_b
        self.odpowiedz_c = odpowiedz_c
        self.poprawna = poprawna
    
class Zagadki:
    lista_zagadek = [
        Zagadka("Co lubi jeść Nemo?", "glony", "ryby", "plankton", Odpowiedz.Odpowiedz_C)
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
        super().__init__(numer, "Podatek dochodowy")
        self.podatek = podatek

    def wyswietl_info(self) -> str:
        return (f"Stanąłeś na polu podatek dochodowy. Musisz zapłacić podatek w wysokości {self.podatek}")

    def zaplac_podatek(self, gra, gracz: Gracz, czy_dobra: bool) -> None:
        do_zaplaty = self.podatek
        if(czy_dobra):
            do_zaplaty /= 2
        
        if(do_zaplaty > gracz.kwota):
            if gra.pobierz_info_tak_nie("Nie masz wystarczająco dużo pieniędzy, aby zapłacić podatek. Czy chcesz zastawić którąś z nieruchmości? Jeśli tego nie zrobisz przegrywasz."):
                gracz.zastaw_nieruchomosci()
        if(do_zaplaty > gracz.kwota):
            gra.messages.append("Bankrutujesz")
        gracz.kwota -= do_zaplaty
        gra.messages.append("Podatek został zapłacony, zapłacono: " + str(do_zaplaty))