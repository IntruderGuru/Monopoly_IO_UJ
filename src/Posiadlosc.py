from src.Pole import Pole

class Posiadlosc(Pole):

    def __init__(self, numer: int, nazwa: str, cena: int, czynsz: int, zastaw: int, cena_domu: int):
        super().__init__(numer, "Posiadlosc")
        self.nazwa = nazwa
        self.cena = cena
        self.czynsz = czynsz
        self.zastaw = zastaw
        self.cena_domu = cena_domu
        self.IDwlasciciela = None 

    def wyswietl_info(self) :
        return (f"Nazwa: {self.nazwa} \nCena: {self.cena}   Czynsz: {self.czynsz}  Zastaw: {self.zastaw} \nCena-dom: {self.cena_domu}")


class PosiadloscKolo(Pole):
    def __init__(self, numer: int, nazwa: str, cena: int, czynsz: int, zastaw: int):
        super().__init__(numer, "Posiadlosc-kolo")
        self.nazwa = nazwa
        self.cena = cena
        self.czynsz = czynsz
        self.zastaw = zastaw
        self.IDwlasciciela = None 

    def wyswietl_info(self) :
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
