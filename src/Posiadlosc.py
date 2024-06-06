from src.Pole import Pole
from src.Gracz import Gracz
import math

KOSZT_SPRZEDAZY = 0.8


class Posiadlosc(Pole):

    def __init__(self, numer, nazwa, kolor, cena, czynsz, zastaw, cena_domu=0):
        super().__init__(numer, "Posiadlosc")
        self.nazwa = nazwa
        self.kolor = kolor
        self.cena = cena
        self.czynsz = czynsz
        self.zastaw_kwota = zastaw
        self.cena_domu = cena_domu
        self.wlasciciel = None
        self.czy_zastawiona = False
        self.liczba_domow = 0
        self.liczba_hoteli = 0

    def zwroc_info(self):
        if self.liczba_domow:
            return f"Nazwa: {self.nazwa} \nCena: {self.cena}   Czynsz: {self.czynsz}  Zastaw: {self.zastaw_kwota} \nCena-dom: {self.cena_domu}  Liczba domkow: {self.liczba_domow}"
        return f"Nazwa: {self.nazwa} \nCena: {self.cena}   Czynsz: {self.czynsz}  Zastaw: {self.zastaw_kwota} \nCena-dom: {self.cena_domu}"

    def pobierz_id_wlasciciela(self):
        return self.wlasciciel

    def wyswietl_info(self, gra):
        czynsz = self.czynsz
        if self.wlasciciel:
            czynsz = self.oblicz_czynsz(gra)

        if self.kolor != "pozaWmii" and self.kolor != "kolo":
            gra._kontroler_wiadomosci.dodaj_wiadomosc(f"Nazwa: {self.nazwa}")
            gra._kontroler_wiadomosci.dodaj_wiadomosc(
                f"Cena: {self.cena}   Czynsz: {czynsz}  Zastaw: {self.zastaw_kwota}"
            )
            gra._kontroler_wiadomosci.dodaj_wiadomosc(
                f"Cena-dom: {self.cena_domu}  Liczba domkow: {self.liczba_domow}"
            )
        else:
            gra._kontroler_wiadomosci.dodaj_wiadomosc(f"Nazwa: {self.nazwa}")
            gra._kontroler_wiadomosci.dodaj_wiadomosc(
                f"Cena: {self.cena}   Czynsz: {czynsz}  Zastaw: {self.zastaw_kwota}"
            )

    def oblicz_czynsz(self, gra):
        liczba_w_kolorze = self.wlasciciel.ile_w_kolorze(self.kolor)
        if self.kolor == "pozaWmii":
            if liczba_w_kolorze == 2:
                return gra._suma_oczek * 10 * 10
            else:
                return gra._suma_oczek * 4 * 10
        elif self.kolor == "kolo":
            if liczba_w_kolorze == 1:
                return 250
            elif liczba_w_kolorze == 2:
                return 500
            elif liczba_w_kolorze == 3:
                return 1000
            else:
                return 2000
        else:
            if liczba_w_kolorze < 3:
                return self.czynsz
            if liczba_w_kolorze == 3 and self.liczba_domow == 0:
                return 2 * self.czynsz

            cena = 0
            if self.liczba_domow == 1:
                cena = 5 * self.czynsz
            elif self.liczba_domow == 2:
                cena = 15 * self.czynsz
            elif self.liczba_domow == 3:
                cena = 45 * self.czynsz
            elif self.liczba_domow == 4:
                cena = 80 * self.czynsz

            cena += self.czynsz * 125 * self.liczba_hoteli
            return cena

    def aktualizuj_czynsz(self):
        if self.wlasciciel:
            liczba_posiadlosci = len(self.wlasciciel.lista_posiadlosci)
            self.czynsz *= 1 + 0.05 * liczba_posiadlosci
            self.czynsz = math.ceil(self.czynsz)

    def kup_posiadlosc(self, gra, gracz):
        x = gracz.wykonaj_oplate(gra, self.cena)
        if x == 1:
            gracz.lista_posiadlosci.append(self)
            self.wlasciciel = gracz
            self.kupione_przez = int(gracz.pionek.sciezka_do_grafiki[27])
            gra._kontroler_wiadomosci.dodaj_wiadomosc(
                f"Gratulacje, dokonałeś zakupu {self.nazwa}!"
            )
            gracz.statystyka.dodaj_posiadlosc()
            gra.akcja_pola_okno.czy_akcja_pola = False

            for posiadlosc in gracz.lista_posiadlosci:
                posiadlosc.aktualizuj_czynsz()
        elif not gra.akcja_zastaw_okno.czy_zastaw:
            gra._kontroler_wiadomosci.dodaj_wiadomosc("Wycofałeś się z zakupu")
            gra.akcja_pola_okno.czy_akcja_pola = False
        return

    def kup_dom(self, gra, gracz, ile_domow):
        if gracz.wykonaj_oplate(gra, self.cena_domu * ile_domow):
            self.liczba_domow += ile_domow
            gracz.statystyka.dodaj_dom(ile_domow)
            while self.liczba_domow >= 5:
                self.liczba_domow -= 5
                gracz.statystyka.odejmij_dom(5)
                self.liczba_hoteli += 1
                gracz.statystyka.dodaj_hotel(1)
            gra._kontroler_wiadomosci.dodaj_wiadomosc(
                f"Zakup domu się udał posiadasz {self.liczba_domow} domów i {self.liczba_hoteli} hoteli"
            )
        else:
            gra._kontroler_wiadomosci.dodaj_wiadomosc("Wycofałeś się z zakupu")

    def sprzedaj_dom(self, gra, gracz):
        if self.liczba_domow > 0:
            gracz.kwota = gracz.kwota + self.cena_domu * KOSZT_SPRZEDAZY
            self.liczba_domow -= 1
            gracz.statystyka.odejmij_dom(1)

    def sprzedaj_hotel(self, gra, gracz):
        if self.liczba_hoteli > 0:
            gracz.kwota = (
                gracz.kwota
                + (self.liczba_hoteli * 5 * self.cena_domu) * KOSZT_SPRZEDAZY
            )
            self.liczba_hoteli -= 1
            gracz.statystyka.odejmij_hotel(1)
