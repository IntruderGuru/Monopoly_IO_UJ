import random


class KartaSzansy:
    def __init__(self):
        self.karty = [
            "Otrzymujesz 200 zł",
            "Płacisz 100 zł",
            "Idź na Start",
            "Idź do więzienia",
            "Otrzymujesz 50 zł od każdego gracza",
            "Strata 50 zł na naprawy",
        ]
        random.shuffle(self.karty)
        self.current_index = 0
        self.akcje = {
            "Otrzymujesz 200 zł": self.otrzymujesz_200,
            "Płacisz 100 zł": self.placisz_100,
            "Idź na Start": self.idz_na_start,
            "Idź do więzienia": self.idz_do_wiezienia,
            "Otrzymujesz 50 zł od każdego gracza": self.otrzymujesz_50_od_kazdego,
            "Strata 50 zł na naprawy": self.strata_50_na_naprawy,
        }

    def nastepna_karta(self):
        karta = self.karty[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.karty)
        return karta

    def wykonaj_karte(self, gra, gracz, karta):
        self.akcje[karta](gra, gracz)

    def otrzymujesz_200(self, gra, gracz):
        gracz.kwota += 200
        gra.kontroler_wiadomosci.dodaj_wiadomosc(f"Gracz {gracz.id} otrzymuje 200 zł")

    def placisz_100(self, gra, gracz):
        gracz.kwota -= 100
        gra.kontroler_wiadomosci.dodaj_wiadomosc(f"Gracz {gracz.id} płaci 100 zł")

    def idz_na_start(self, gra, gracz):
        gra.przesun_gracza_bez_raportu(gracz, 0)
        gra.kontroler_wiadomosci.dodaj_wiadomosc(f"Gracz {gracz.id} idzie na Start")

    def idz_do_wiezienia(self, gra, gracz):
        gra.przesun_gracza_bez_raportu(gracz, 10)
        gracz.uwiezienie = True
        gra.kontroler_wiadomosci.dodaj_wiadomosc(f"Gracz {gracz.id} idzie do więzienia")

    def otrzymujesz_50_od_kazdego(self, gra, gracz):
        for g in gra._gracze:
            if g.id != gracz.id:
                g.kwota -= 50
                gracz.kwota += 50
        gra.kontroler_wiadomosci.dodaj_wiadomosc(f"Gracz {gracz.id} otrzymuje 50 zł od każdego gracza")

    def strata_50_na_naprawy(self, gra, gracz):
        gracz.kwota -= 50
        gra.kontroler_wiadomosci.dodaj_wiadomosc(f"Gracz {gracz.id} traci 50 zł na naprawy")
