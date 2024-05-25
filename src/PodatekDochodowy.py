from src.Pole import Pole
from src.Gracz import Gracz
from src.Gra import Gra


class Zagadka():
    def __init__(self, tresc_zagadki: str, odpowiedz_a: str, odpowiedz_b: str, odpowiedz_c: str, poprawna: int):
        self.tresc_zagadki = tresc_zagadki
        self.odpowiedz_a = odpowiedz_a
        self.odpowiedz_b = odpowiedz_b
        self.odpowiedz_c = odpowiedz_c
        self.poprawna = poprawna
    
    def zadaj_zagadke(self, gra: Gra) -> bool:
        gra.messages.append(f"{self.tresc_zagadki} \na. {self.odpowiedz_a} \nb. {self.odpowiedz_b} \nc. {self.odpowiedz_c}")
        #dodac przyciski na wybieranie odpowiedzi

class PodatekDochodowy(Pole):

    def __init__(self, numer: int, podatek: int):
        super().__init__(numer, "Podatek Dochodowy")
        self.podatek = podatek

    def wyswietl_info(self):
        return (f"Stanąłeś na polu podatek dochodowy. Musisz zapłacić podatek w wysokości {self.podatek}")

    def zaplac_podatek(self, gra: Gra, gracz: Gracz):
        #cos zagadki wybor i jej zadanie
        czy_dobra = True
        if(czy_dobra):
            return
        if(self.podatek > gracz.kwota):
            if gra.pobierz_info_tak_nie("Nie masz wystarczająco dużo pieniędzy, aby zapłacić podatek. Czy chcesz zastawić którąś z nieruchmości? Jeśli tego nie zrobisz przegrywasz."):
                gracz.zastaw_nieruchomosci()
            else: 
                gra.messages.append("Bankrutujesz")
                return
        gracz.kwota -= self.podatek
        gra.messages.append("Podatek został zapłacony")