class Gracz:
    def __init__(self, id, kwota, pionek):
        self.id = id
        self.kwota = kwota
        self.pionek = pionek
        self.pozycja = 0
        self.uwiezienie = False
        self.tury_w_wiezieniu = 0  # Licznik tur w więzieniu
        self.lista_posiadlosci

    def odczekajJednaTure(self):
        if self.uwiezienie:
            self.tury_w_wiezieniu += 1
            if self.tury_w_wiezieniu >= 2:
                self.uwiezienie = False
                self.tury_w_wiezieniu = 0
                print(f"Gracz {self.id} opuszcza więzienie po dwóch turach")


    def zastaw_nieruchomosci(self, gra):
        while True:
            for posiadlosc in self.lista_posiadlosci:
                if not posiadlosc.czy_zastawiona:
                    posiadlosc.wyswietl_info
            gra.messages.append("Wpisz numer posiadłości którą chcesz zastawić")
            #wczytanie numeru, sprawdzenie czy numer jest dobry
            x = 2
            self.lista_posiadlosci[x].czy_zastawiona = True
            self.kwota += self.lista_posiadlosci[x].zastaw_kwota

            gra.messages.append("Czy chcesz zastawić kolejną nieruchomość? t/n")
            if not gra.pobierz_info_tak_nie():
                return
