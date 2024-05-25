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

    def wyswietl_info(self, gra):
        if self.liczba_domow:
            gra.messages.append(f"Nazwa: {self.nazwa} \nCena: {self.cena}   Czynsz: {self.czynsz}  Zastaw: {self.zastaw_kwota} \nCena-dom: {self.cena_domu}  Liczba domkow: {self.liczba_domow}")
        else:
            gra.messages.append(f"Nazwa: {self.nazwa} \nCena: {self.cena}   Czynsz: {self.czynsz}  Zastaw: {self.zastaw_kwota} \nCena-dom: {self.cena_domu}")
    
    def oblicz_czynsz(self):
        if(self.kolor == 'brazowy'):
            pass
    
    def kup_posiadlosc(self, gra, gracz):
        x = gracz.wykonaj_oplate(gra, self.cena)
        if x == 1:
            gracz.lista_posiadlosci.append(self)
            self.IDwlasciciela = gracz.id
            gra.messages.append(f"Gratulacje, dokonałeś zakupu {self.nazwa}!")
            gra.akcja_pola_okno.czy_akcja_pola = False
        elif not gra.akcja_zastaw_okno.czy_zastaw:
            gra.messages.append("Wycofałeś się z zakupu")  
            gra.akcja_pola_okno.czy_akcja_pola = False  
        return

    
    def kup_dom(self, gra, gracz):
        if(self.czy_zastawiona):
            gra.messages.append("Nie można kupić domku lub hotelu na zastawionej posiadłości")
            return
        
        if(gracz.wykonaj_oplate(gra, self.cena_domu)):
            self.liczba_domow += 1
            gra.messages.append("Zakup domu się udał")
        else:
            gra.messages.append("Wycofałeś się z zakupu")    
        

        
    def sprzedaj_posiadlosc(self, gra, gracz):
        if(self.czy_zastawiona):
            gra.messages.append("Nie można sprzedać zastawionej posiadłości")
        else:
            #80% wartości posiadłości
            gracz.kwota = gracz.kwota + (self.cena + (self.liczba_domow * self.cena_domu))*0.8
            self.IDwlasciciela = None
            self.liczba_domow = 0
            gracz.lista_posiadlosci.remove(self)

    def sprzedaj_dom(self, gra, gracz):
        if(self.czy_zastawiona):
            gra.messages.append("Nie można sprzedać zastawionej posiadłości")
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

    def wyswietl_info(self, gra):
        gra.messages.append(f"Nazwa: {self.nazwa}\nCena: {self.cena}   Czynsz: {self.czynsz}  Zastaw: {self.zastaw}")


class PosiadloscPozaWmii(Pole):
    def __init__(self, numer: int, nazwa: str, cena: int, czynsz: int, zastaw: int):
        super().__init__(numer, "Posiadlosc-pozaWmii")
        self.nazwa = nazwa
        self.cena = cena
        self.czynsz = czynsz
        self.zastaw = zastaw
        self.IDwlasciciela = None 

    def wyswietl_info(self, gra) :
        gra.messages.append(f"Nazwa: {self.nazwa}\nCena: {self.cena}   Czynsz: {self.czynsz}  Zastaw: {self.zastaw}")