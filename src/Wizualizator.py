class Wizualizator:

    def __init__(self):

        # przycisk
        self.kolor_przycisku = (70, 70, 70)
        self.kolor_gdy_kursor = (150, 150, 150)
        self.kolor_czcionki_na_przycisku = (200, 200, 200)
        self.kolor_przycisku_graj = (96, 247, 134)
        self.kolor_gdy_kursor_przycisku_graj = (76, 227, 114)
        self.kolor_niedzialajcego_przycisku = (50, 50, 50)

        # inne kolory
        self.kolor_akceptacji_nazwy_gracza = (96, 247, 134)
        self.kolor_tla = (119, 119, 175)
        self.kolor_napisu_gracz_tury = (255, 255, 255)
        self.kolor_czcionki = (255, 255, 255)
        self.kolor_czcionki_tyl_karty = (255, 255, 255)
        self.kolor_nakladki = (77, 77, 115)
        self.przezroczystosc_nakladki = 100

        #kolory wypisywania komunikatow
        self.kolor_wiadomosci = (255, 255, 255)
        self.kolor_ostatniej_wiadomosci = (255, 255, 255)

        #czcionka
        #self.czcionka = "fonts/Lato-Black.ttf"
        self.czcionka = None
        self.czcionka_przycisku = "fonts/Gameplay.ttf"
