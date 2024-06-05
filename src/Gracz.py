from src.Statystyka import Statystyka

class Gracz:
    def __init__(self, id, kwota, pionek):
        self.id = id
        self.kwota = kwota
        self.pionek = pionek
        self.pozycja = 0
        self.tury_w_wiezieniu = 0  # Licznik tur w więzieniu
        self.liczba_kart_wyjdz_z_wiezienia = 0
        self.lista_posiadlosci = []
        self.liczba_zastawionych = 0
        self.statystyka = Statystyka(kwota, self.id)  

    # TODO: wczytanie numeru zastawianej posiadlosci
    def zastaw_posiadlosci(self, gra):
        if self.liczba_zastawionych >= len(self.lista_posiadlosci):
            gra._kontroler_wiadomosci.dodaj_wiadomosc(
                "Nie masz już posiadłości, które mógłbyś zastawić"
            )
            gra.akcja_zastaw_okno.czy_zastaw = False
            return

        gra._kontroler_wiadomosci.dodaj_wiadomosc(
            "To wszystkie Twoje posiadłości, które możesz zastawić:"
        )
        for posiadlosc in self.lista_posiadlosci:
            if not posiadlosc.czy_zastawiona:
                #posiadlosc.wyswietl_info(gra)
                gra._kontroler_wiadomosci.dodaj_wiadomosc(f"({posiadlosc.nazwa}")

        # wczytanie numeru, sprawdzenie czy numer jest dobry
        x = 0
        self.lista_posiadlosci[x].czy_zastawiona = True
        self.liczba_zastawionych += 1
        self.kwota += self.lista_posiadlosci[x].zastaw_kwota
        self.statystyka.aktualizuj_stan_pieniedzy(self.kwota)

    def zdejmij_zastaw_posiadlosci(self, gra):
        if self.liczba_zastawionych == 0:
            gra._kontroler_wiadomosci.dodaj_wiadomosc(
                "Nie masz zastawionych posiadlosci"
            )
            gra.akcja_zastaw_okno.czy_zdejmij_zastaw = False
            return

        gra._kontroler_wiadomosci.dodaj_wiadomosc(
            "To wszystkie Twoje posiadłości, które masz zastawione:"
        )
        for posiadlosc in self.lista_posiadlosci:
            if posiadlosc.czy_zastawiona:
                #posiadlosc.wyswietl_info(gra)
                gra._kontroler_wiadomosci.dodaj_wiadomosc(f"({posiadlosc.nazwa}")

        # wczytanie numeru, sprawdzenie czy numer jest dobry
        x = 0
        cena = self.lista_posiadlosci[x].zastaw_kwota * 1.2
        if self.kwota >= cena:
            self.lista_posiadlosci[x].czy_zastawiona = False
            self.liczba_zastawionych -= 1
            self.kwota -= cena
        else:
            gra._kontroler_wiadomosci.dodaj_wiadomosc(
                "Nie masz wystarczająco dużo pieniędzy, aby zdjąć zastaw z posiadłości"
            )
        self.statystyka.aktualizuj_stan_pieniedzy(self.kwota)

    def zaplac_czynsz(self, gra, posiadlosc):
        czynsz = posiadlosc.oblicz_czynsz(gra)
        self.wykonaj_oplate(gra, czynsz)
        posiadlosc.wlasciciel.dodaj_pieniadze(gra, czynsz)

    def ile_w_kolorze(self, kolor):
        liczba_w_kolorze = 0
        for posiadlosc in self.lista_posiadlosci:
            if not posiadlosc.kolor == kolor:
                liczba_w_kolorze += 1
        return liczba_w_kolorze

    def caly_kolor(self, kolor):
        if kolor == "brazowy" or kolor == "granatowy" or kolor == "pozaWmii":
            return self.ile_w_kolorze(kolor) == 2
        else:
            return self.ile_w_kolorze(kolor) == 3

    def czy_cztery_domki(self, posiadlosc):
        if posiadlosc.liczba_domow < 4:
            return "domek"

        liczba_domkow_w_kolorze = 0
        for pole in self.lista_posiadlosci:
            if not pole.kolor == pole.kolor:
                liczba_domkow_w_kolorze += pole.liczba_domow

        if posiadlosc.kolor == "brazowy" or posiadlosc.kolor == "granatowy":
            if liczba_domkow_w_kolorze < 8:
                return "nie"
            return "hotel"
        else:
            if liczba_domkow_w_kolorze < 12:
                return "nie"
            return "hotel"

    def wykonaj_oplate(self, gra, cena):
        if cena > self.kwota:
            gra._kontroler_wiadomosci.dodaj_wiadomosc(
                f"Brakuje Ci {cena - self.kwota} pieniędzy. Czy chcesz zastawić którąś z posiadłości?"
            )
            gra.akcja_zastaw_okno.czy_zastaw = True
            gra.akcja_zastaw_okno.akcja_zastawiania(self)
        else:
            self.kwota -= cena
            self.statystyka.aktualizuj_stan_pieniedzy(self.kwota)
            return 1
        
        self.statystyka.aktualizuj_stan_pieniedzy(self.kwota)
        return 0

    def dodaj_pieniadze(self, gra, cena):
        self.kwota += cena
        gra._kontroler_wiadomosci.dodaj_wiadomosc(
            f"Gracz {self.id} otrzymał {cena} pieniędzy"
        )
        self.statystyka.aktualizuj_stan_pieniedzy(self.kwota)

    def czy_przeszedl_przez_start(self, gra, stara_pozycja):
        if self.pionek.numer_pola < stara_pozycja and self.tury_w_wiezieniu == 0:
            self.dodaj_pieniadze(gra, 2000)
