from src.Pole import Pole
from src.Gracz import Gracz
from src.Gra import Gra




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