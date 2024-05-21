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
        self.czy_zastawiona = False
        self.liczba_domow = 0

    def wyswietl_info(self):
        if self.liczba_domow:
            return (f"Nazwa: {self.nazwa} \nCena: {self.cena}   Czynsz: {self.czynsz}  Zastaw: {self.zastaw_kwota} \nCena-dom: {self.cena_domu}  Liczba domkow: {self.liczba_domow}")
        return (f"Nazwa: {self.nazwa} \nCena: {self.cena}   Czynsz: {self.czynsz}  Zastaw: {self.zastaw_kwota} \nCena-dom: {self.cena_domu}")
    
    def kup_posiadlosc(self, gra, gracz):
        if(self.cena > gracz.kwota):
            if gra.tak_kilk == True:
                print("Nie masz wystarczająco dużo pieniędzy. Czy chcesz zastawić którąś z nieruchmości? ")
                #gracz.zastaw_posiadlosci()
                pass
            elif gra.nie_klik == False:
                gra.messages.append("Zakup zakończony niepowodzeniem")
                return
            
        gracz.kwota -= self.cena
        gracz.lista_posiadlosci.append(self)
        self.IDwlasciciela = gracz.id
        gra.messages.append("Zakup się udał")
    
    def kup_dom(self, gra, gracz):
        if(self.czy_zastawiona):
            gra.messages.append("Nie można kupić domku lub hotelu na zastawionej nieruchomości")
            return
        while True:
            if(self.cena_domu > gracz.kwota):
                if gra.tak_klik == True:
                    print("Nie masz wystarczająco dużo pieniędzy. Czy chcesz zastawić którąś z nieruchmości?")
                    #gracz.zastaw_posiadlosci()
                    pass
                elif gra.nie_klik == False:
                    gra.messages.append("Zakup zakończony niepowodzeniem")
                    return
            gracz.kwota -= self.cena_domu
            self.liczba_domow += 1
            gra.messages.append("Zakup domu się udał")
            if gra.nie_klik == False:
                print("Czy chcesz zastawić kolejną nieruchomość?")
                return
        
    def sprzedaj_posiadlosc(self, gra, gracz):
        if(self.czy_zastawiona):
            gra.messages.append("Nie można sprzedać zastawionej nieruchomości")
        else:
            #80% wartości posiadłości
            gracz.kwota = gracz.kwota + (self.cena + (self.liczba_domow * self.cena_domu))*0.8
            self.IDwlasciciela = None
            self.liczba_domow = 0
            gracz.lista_posiadlosci.remove(self)

    def sprzedaj_dom(self, gra, gracz):
        if(self.czy_zastawiona):
            gra.messages.append("Nie można sprzedać zastawionej nieruchomości")
        else:
            #80% wartości
            gra.messages.append("Ile domków chcesz sprzedać?")
            #wczytanie do x, sprawdzenie czy x <= self.liczba_domow
            x=2
            gracz.kwota = gracz.kwota + (x * self.cena_domu * 0.8)
            self.liczba_domow -= x


            



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
