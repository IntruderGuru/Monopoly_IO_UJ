class Statystyka:

    def __init__(self, kwota_startowa, nazwa_gracza):
        self.nazwa_gracza = nazwa_gracza
        self.pieniadze = kwota_startowa
        self.ilosc_posiadlosci = 0
        self.ilosc_domkow = 0
        self.ilosc_hoteli = 0

    def aktualizuj_statystyke(self, pieniadze, kupil_posiadlosc, kupil_dom, kupil_hotel):
        self.pieniadze = pieniadze
        self.ilosc_posiadlosci += kupil_posiadlosc
        self.ilosc_domkow += kupil_dom
        self.ilosc_hoteli += kupil_hotel
    