class Gra:
    def __init__(self):
        self.gracze = []
        
class Plansza:
    def __init__(self):
        self.Pola = []
        
class Gracz:
    def __init__(self, Id: int, pionek: Pionek, kartaSzansy: KartaSzansy, liczbaPostojow: int, uwiezienie: bool):
        self.Id = Id
        self.pionek = pionek
        self.kartaSzansy = kartaSzansy
        self.liczbaPostojow = liczbaPostojow
        self.uwiezienie = uwiezienie
        
class Posiadlosc(Pole):
    def __init__(self, cena: int, czynsz: int, cenaDomu: int, cenaHotelu: int, IDwlasciciela: int):
        self.cena = cena
        self.czynsz = czynsz
        self.cenaDomu = cenaDomu
        self.cenaHotelu = cenaHotelu
        self.IDwlasciciela = IDwlasciciela        

class Pole:
    def __init__(self, numer: int, grafika: Graphic):
        self.numer = numer
        self.grafika = grafika

class PoleWykonywalne(Pole):
    def __init__(self):

class PoleSpecjalne(Pole):
    def __init__(self):
        
class KartaSzansy:
    def __init__(self, trescKarty: str):
        self.trescKarty = trescKarty
        
class Pionek:
    def __init__(self, numerPola: int, color: Color, grafika: Graphic):
        self.numerPola = numerPola
        self.color = color
        self.grafika = grafika

    def zmienGrafike(self) -> bool:

    def zmienPozycje(self, nowaPozycja: int) -> bool:

class Statystyki:
    def __init__(self):
        self.statystyki = []

    def zaktualizujStatystykiGracza(self, gracz: Gracz): 
        
class Statystyka:
    def __init__(self, IDgracza: int, majatek: int, iloscPosiadlosci: int, iloscDomow: int, iloscHoteli: int):
        self.IDgracza = IDgracza
        self.majatek = majatek
        self.iloscPosiadlosci = iloscPosiadlosci
        self.iloscDomow = iloscDomow
        self.iloscHoteli = iloscHoteli

    def zmienWartosc(self):       
        
class Tutorial:
    def __init__(self, ukonczony: bool):
        self.ukonczony = ukonczony

    def rozpocznij(self):        


class Czas:
    def __init__(self, czasGry: float, czasTury: float):
        self.czasGry = czasGry
        self.czasTury = czasTury


class Zagadki:
    def __init__(self, trescZagadki: str, poprawnaOdpowiedz: int):
        self.trescZagadki = trescZagadki
        self.poprawnaOdpowiedz = poprawnaOdpowiedz

    def sprawdzOdpowiedz(self) -> bool:
















