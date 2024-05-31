class Statystyka:

    def __init__(self, kwota_startowa, nazwa_gracza):
        self.nazwa_gracza = nazwa_gracza
        self.pieniadze = kwota_startowa
        self.ilosc_posiadlosci = 0
        self.ilosc_domkow = 0
        self.ilosc_hoteli = 0

    def aktualizuj_stan_pieniedzy(self, pieniadze):
        self.pieniadze = pieniadze

    def dodaj_posiadlosc(self):
        self.ilosc_posiadlosci += 1

    def dodaj_hotel(self, ile):
        self.ilosc_hoteli += ile

    def dodaj_domek(self, ile):
        self.ilosc_domkow += ile

    def odejmij_domek(self, ile):
        self.ilosc_domkow -= ile

    