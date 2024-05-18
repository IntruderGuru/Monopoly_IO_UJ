from src.Pole import Pole
from src.Gracz import Gracz

class Posiadlosc(Pole):

    def __init__(self, numer: int, nazwa: str, cena: int, czynsz: int, zastaw: int, cena_domu: int):
        super().__init__(numer, "Posiadlosc")
        self.nazwa = nazwa
        self.cena = cena
        self.czynsz = czynsz
        self.zastaw_kwota = zastaw
        self.cena_domu = cena_domu
        self.IDwlasciciela = None 
        self.czy_zastawione = False
        self.liczba_domow = 0

    def wyswietl_info(self):
        if self.liczba_domow:
            return (f"Nazwa: {self.nazwa} \nCena: {self.cena}   Czynsz: {self.czynsz}  Zastaw: {self.zastaw_kwota} \nCena-dom: {self.cena_domu}  Liczba domkow: {self.liczba_domow}")
        return (f"Nazwa: {self.nazwa} \nCena: {self.cena}   Czynsz: {self.czynsz}  Zastaw: {self.zastaw_kwota} \nCena-dom: {self.cena_domu}")
    
    def kup_posiadlosc(self, gra, gracz):
        if(self.cena > gracz.kwota):
            gra.messages.append("Nie masz wystarczająco dużo pieniędzy. Czy chcesz zastawić którąś z nieruchmości? t/n")
            #if gra.pobierz_info_tak_nie():
                #gracz.wyswietl_posiadlosci()
        else:
            gracz.kwota -= self.cena
            self.IDwlasciciela = gracz.id
            gra.messages.append("Zakup się udał")
    
    def kup_dom(self, gra, gracz):
        if(self.czy_zastawione):
            gra.messages.append("Nie można kupić domku lub hotelu na zastawionej nieruchomości")

        elif(self.cena_domu > gracz.kwota):
            gra.messages.append("Nie masz wystarczająco dużo pieniędzy. Czy chcesz zastawić którąś z nieruchmości? t/n")
            #if gra.pobierz_info_tak_nie():
                #gracz.wyswietl_posiadlosci()
        else:
            gracz.kwota -= self.cena_domu
            self.liczba_domow += 1
            gra.messages.append("Zakup domu się udał")
        
    def sprzedaj(self, gra, gracz):
        if(self.czy_zastawione):
            gra.messages.append("Nie można sprzedać zastawionej nieruchomości")
        else:
            gracz.kwota = gracz.kwota + self.cena + (self.liczba_domow * self.cena_domu)
            self.IDwlasciciela = None
            self.liczba_domow = 0


            



class PosiadloscKolo(Pole):
    def __init__(self, numer: int, nazwa: str, cena: int, czynsz: int, zastaw: int):
        super().__init__(numer, "Posiadlosc-kolo")
        self.nazwa = nazwa
        self.cena = cena
        self.czynsz = czynsz
        self.zastaw = zastaw
        self.IDwlasciciela = None 

    def wyswietl_info(self):
        return (f"Nazwa: {self.nazwa}\nCena: {self.cena}   Czynsz: {self.czynsz}  Zastaw: {self.zastaw}")

class PosiadloscPozaWmii(Pole):
    def __init__(self, numer: int, nazwa: str, cena: int, czynsz: int, zastaw: int):
        super().__init__(numer, "Posiadlosc-pozaWmii")
        self.nazwa = nazwa
        self.cena = cena
        self.czynsz = czynsz
        self.zastaw = zastaw
        self.IDwlasciciela = None 

    def wyswietl_info(self) :
        return (f"Nazwa: {self.nazwa}\nCena: {self.cena}   Czynsz: {self.czynsz}  Zastaw: {self.zastaw}")
