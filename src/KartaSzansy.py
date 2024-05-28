import random

class KartaSzansy:
    def __init__(self, typ, tresc, wartosc=0):
        self.typ = typ
        self.tresc = tresc
        self.wartosc = wartosc
        
    def wyswietl_tresc(self, gra):
        gra.kontroler_wiadomosci.dodaj_wiadomosc(self.tresc)
        
    def wykonaj_akcje(self, gra, gracz):
        if self.typ == "pobierz":
            gracz.dodaj_pieniadze(gra, self.wartosc)
            
        elif self.typ == "pobierz_od_graczy":
            for g in gra._gracze:
                if g.id != gracz.id:
                    g.wykonaj_oplate(gra, self.wartosc)
                    gracz.dodaj_pieniadze(gra, self.wartosc)
            gra.kontroler_wiadomosci.dodaj_wiadomosc(f"Gracz {gracz.id} otrzymuje {self.wartosc} zł od każdego gracza")
            
        elif self.typ == "oplata":
            gracz.wykonaj_oplate(gra, self.wartosc)
            
        elif self.typ == "oplata_za_domki":
            pass
            
        elif self.typ == "przejdz_na_pole":
            gra.przesun_gracza(self, gracz, self.wartosc)
            
        #brak poboru oplaty za przejscie przez start 
        elif self.typ == "cofnij_na_pole":
            gra.przesun_gracza_bez_raportu(self, gracz, self.wartosc)
            
        elif self.typ == "cofnij_do_wiezienia":
            gracz.uwiezienie = True
            gra.przesun_gracza_bez_raportu(gra._gracze[gra._aktualny_gracz - 1], 10)
        
        elif self.typ == "karta_wyjscie_z_wiezienia":
            pass
            

class Karty:
    def __init__(self):
        self.karty = self.wczytaj_karty("data/karty.txt")
        random.shuffle(self.karty)
        self.current_index = 0

    def wczytaj_karty(self, plik: str) -> list[KartaSzansy]:
        karty = []
        with open(plik, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            i = 0
            while i < len(lines):
                if i + 2 >= len(lines):
                    raise ValueError(f"Unexpected end of file at line {i}. Each card must have exactly 3 lines.")
                typ = lines[i].strip()
                tresc = lines[i + 1].strip()
                wartosc = int(lines[i + 2].strip())
                karta = KartaSzansy(typ, tresc, wartosc)
                karty.append(karta)
                i += 3
        return karty

    def nastepna_karta(self):
        karta = self.karty[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.karty)
        return karta


    def idz_na_start(self, gra, gracz):
        gra.przesun_gracza_bez_raportu(gracz, 0)
        gra.kontroler_wiadomosci.dodaj_wiadomosc(f"Gracz {gracz.id} idzie na Start")


    def otrzymujesz_50_od_kazdego(self, gra, gracz):
        for g in gra._gracze:
            if g.id != gracz.id:
                g.kwota -= 50
                gracz.kwota += 50
        gra.kontroler_wiadomosci.dodaj_wiadomosc(f"Gracz {gracz.id} otrzymuje 50 zł od każdego gracza")

    def strata_50_na_naprawy(self, gra, gracz):
        gracz.kwota -= 50
        gra.kontroler_wiadomosci.dodaj_wiadomosc(f"Gracz {gracz.id} traci 50 zł na naprawy")
