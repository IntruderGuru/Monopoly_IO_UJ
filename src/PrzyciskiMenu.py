from src.Przycisk import Przycisk
from src.Wizualizator import Wizualizator


class PrzyciskiMenu:

    def __init__(self, H, W, wizualizator):

        self.wizualizator = wizualizator

        self.nowa_gra = Przycisk(
            W * 0.35,
            H * 0.4,
            W * 0.3,
            H * 0.1,
            self.wizualizator.kolor_przycisku,
            self.wizualizator.kolor_gdy_kursor,
            "Nowa gra",
            self.wizualizator.kolor_czcionki_na_przycisku,
        )

        self.wczytaj_gre = Przycisk(
            W * 0.35,
            H * 0.52,
            W * 0.3,
            H * 0.1,
            self.wizualizator.kolor_przycisku,
            self.wizualizator.kolor_gdy_kursor,
            "Wczytaj zapis",
            self.wizualizator.kolor_czcionki_na_przycisku,
        )

        self.wyjscie = Przycisk(
            W * 0.35,
            H * 0.64,
            W * 0.3,
            H * 0.1,
            self.wizualizator.kolor_przycisku,
            self.wizualizator.kolor_gdy_kursor,
            "Wyjscie",
            self.wizualizator.kolor_czcionki_na_przycisku,
        )

        self.trzydziesci_minut = Przycisk(
            W * 0.25,
            H * 0.5,
            H * 0.1,
            H * 0.1,
            self.wizualizator.kolor_przycisku,
            self.wizualizator.kolor_gdy_kursor,
            "30",
            self.wizualizator.kolor_czcionki_na_przycisku,
        )

        self.szescdziesiat_minut = Przycisk(
            W * 0.35,
            H * 0.5,
            H * 0.1,
            H * 0.1,
            self.wizualizator.kolor_przycisku,
            self.wizualizator.kolor_gdy_kursor,
            "60",
            self.wizualizator.kolor_czcionki_na_przycisku,
        )

        self.dziewiecdziesiat_minut = Przycisk(
            W * 0.45,
            H * 0.5,
            H * 0.1,
            H * 0.1,
            self.wizualizator.kolor_przycisku,
            self.wizualizator.kolor_gdy_kursor,
            "90",
            self.wizualizator.kolor_czcionki_na_przycisku,
        )

        self.jedna_minuta = Przycisk(
            W * 0.25,
            H * 0.5,
            H * 0.1,
            H * 0.1,
            self.wizualizator.kolor_przycisku,
            self.wizualizator.kolor_gdy_kursor,
            "60",
            self.wizualizator.kolor_czcionki_na_przycisku,
            28
        )

        self.dwie_minuty = Przycisk(
            W * 0.35,
            H * 0.5,
            H * 0.1,
            H * 0.1,
            self.wizualizator.kolor_przycisku,
            self.wizualizator.kolor_gdy_kursor,
            "120",
            self.wizualizator.kolor_czcionki_na_przycisku,
            28
        )

        self.trzy_minuty = Przycisk(
            W * 0.45,
            H * 0.5,
            H * 0.1,
            H * 0.1,
            self.wizualizator.kolor_przycisku,
            self.wizualizator.kolor_gdy_kursor,
            "180",
            self.wizualizator.kolor_czcionki_na_przycisku,
            28
        )

        self.bez_ograniczen = Przycisk(
            W * 0.55,
            H * 0.5,
            W * 0.2,
            H * 0.1,
            self.wizualizator.kolor_przycisku,
            self.wizualizator.kolor_gdy_kursor,
            "Bez limitu",
            self.wizualizator.kolor_czcionki_na_przycisku,
            25,
        )

        self.two = Przycisk(
            W * 0.3,
            H * 0.5,
            H * 0.1,
            H * 0.1,
            self.wizualizator.kolor_przycisku,
            self.wizualizator.kolor_gdy_kursor,
            "2",
            self.wizualizator.kolor_czcionki_na_przycisku,
        )

        self.three = Przycisk(
            W * 0.4,
            H * 0.5,
            H * 0.1,
            H * 0.1,
            self.wizualizator.kolor_przycisku,
            self.wizualizator.kolor_gdy_kursor,
            "3",
            self.wizualizator.kolor_czcionki_na_przycisku,
        )

        self.four = Przycisk(
            W * 0.5,
            H * 0.5,
            H * 0.1,
            H * 0.1,
            self.wizualizator.kolor_przycisku,
            self.wizualizator.kolor_gdy_kursor,
            "4",
            self.wizualizator.kolor_czcionki_na_przycisku,
        )

        self.five = Przycisk(
            W * 0.6,
            H * 0.5,
            H * 0.1,
            H * 0.1,
            self.wizualizator.kolor_przycisku,
            self.wizualizator.kolor_gdy_kursor,
            "5",
            self.wizualizator.kolor_czcionki_na_przycisku,
        )

        self.poprzedni = Przycisk(
            W * 0.2,
            H * 0.5,
            W * 0.1,
            H * 0.1,
            self.wizualizator.kolor_przycisku,
            self.wizualizator.kolor_gdy_kursor,
            "poprzedni",
            self.wizualizator.kolor_czcionki_na_przycisku,
        )

        self.nastepny = Przycisk(
            W * 0.3,
            H * 0.5,
            W * 0.1,
            H * 0.1,
            self.wizualizator.kolor_przycisku,
            self.wizualizator.kolor_gdy_kursor,
            "nastepny",
            self.wizualizator.kolor_czcionki_na_przycisku,
        )

        self.poprzedni_szary = Przycisk(
            W * 0.2,
            H * 0.5,
            W * 0.1,
            H * 0.1,
            self.wizualizator.kolor_niedzialajcego_przycisku,
            self.wizualizator.kolor_niedzialajcego_przycisku,
            "poprzedni",
            self.wizualizator.kolor_czcionki_na_przycisku,
        )

        self.nastepny_szary = Przycisk(
            W * 0.3,
            H * 0.5,
            W * 0.1,
            H * 0.1,
            self.wizualizator.kolor_niedzialajcego_przycisku,
            self.wizualizator.kolor_niedzialajcego_przycisku,
            "nastepny",
            self.wizualizator.kolor_czcionki_na_przycisku,
        )

        self.graj = Przycisk(
            W * 0.4,
            H * 0.5,
            W * 0.1,
            H * 0.1,
            self.wizualizator.kolor_przycisku_graj,
            self.wizualizator.kolor_gdy_kursor_przycisku_graj,
            "graj",
            (40, 40, 40),
        )

        self.personalizacja = Przycisk(
            W * 0.5,
            H * 0.5,
            W * 0.1,
            H * 0.1,
            self.wizualizator.kolor_przycisku,
            self.wizualizator.kolor_gdy_kursor,
            "Dodaj karte",
            self.wizualizator.kolor_czcionki_na_przycisku,
            20,
        )

        # cofnij na pole. karta wyjście z więznienia

        self.pobierz = Przycisk(
            W * 0.15,
            H * 0.3,
            W * 0.2,
            H * 0.1,
            self.wizualizator.kolor_przycisku,
            self.wizualizator.kolor_gdy_kursor,
            "pobierz",
            self.wizualizator.kolor_czcionki_na_przycisku,
            20,
        )
        self.pobierz_od_graczy = Przycisk(
            W * 0.15,
            H * 0.5,
            W * 0.25,
            H * 0.1,
            self.wizualizator.kolor_przycisku,
            self.wizualizator.kolor_gdy_kursor,
            "pobierz od graczy",
            self.wizualizator.kolor_czcionki_na_przycisku,
            20,
        )
        self.oplata = Przycisk(
            W * 0.15,
            H * 0.7,
            W * 0.25,
            H * 0.1,
            self.wizualizator.kolor_przycisku,
            self.wizualizator.kolor_gdy_kursor,
            "oplata",
            self.wizualizator.kolor_czcionki_na_przycisku,
            20,
        )
        self.oplata_za_domki = Przycisk(
            W * 0.5,
            H * 0.3,
            W * 0.25,
            H * 0.1,
            self.wizualizator.kolor_przycisku,
            self.wizualizator.kolor_gdy_kursor,
            "oplata za domki",
            self.wizualizator.kolor_czcionki_na_przycisku,
            20,
        )
        self.przejdz_na_pole = Przycisk(
            W * 0.5,
            H * 0.5,
            W * 0.25,
            H * 0.1,
            self.wizualizator.kolor_przycisku,
            self.wizualizator.kolor_gdy_kursor,
            "przejdz na pole",
            self.wizualizator.kolor_czcionki_na_przycisku,
            20,
        )
        self.cofnij_do_wiezienia = Przycisk(
            W * 0.5,
            H * 0.7,
            W * 0.25,
            H * 0.1,
            self.wizualizator.kolor_przycisku,
            self.wizualizator.kolor_gdy_kursor,
            "cofnij do wiezienia",
            self.wizualizator.kolor_czcionki_na_przycisku,
            20,
        )

        self.powrot = Przycisk(
            W * 0.8,
            H * 0.8,
            W * 0.2,
            H * 0.1,
            self.wizualizator.kolor_przycisku,
            self.wizualizator.kolor_gdy_kursor,
            "powrot",
            self.wizualizator.kolor_czcionki_na_przycisku,
        )

        self.zaakceptuj = Przycisk(
            W * 0.8,
            H * 0.8,
            W * 0.2,
            H * 0.1,
            self.wizualizator.kolor_akceptacji_nazwy_gracza,
            self.wizualizator.kolor_gdy_kursor_przycisku_graj,
            "zaakceptuj",
            (40, 40, 40)
        )

    def aktualizuj_rozmiar(self, W, H):
        # skalowanie do jakiejsc czesci, testowo
        MIN_W = 500
        MIN_H = 400
        W = max(W, MIN_W)
        H = max(H, MIN_H)

        self.nowa_gra.updateSize(W * 0.35, H * 0.5, W * 0.3, H * 0.1)
        self.wczytaj_gre.updateSize(W * 0.35, H * 0.62, W * 0.3, H * 0.1)
        self.wyjscie.updateSize(W * 0.35, H * 0.74, W * 0.3, H * 0.1)
        self.two.updateSize(W * 0.3, H * 0.5, H * 0.1, H * 0.1)
        self.three.updateSize(W * 0.4, H * 0.5, H * 0.1, H * 0.1)
        self.four.updateSize(W * 0.5, H * 0.5, H * 0.1, H * 0.1)
        self.five.updateSize(W * 0.6, H * 0.5, H * 0.1, H * 0.1)

        self.trzydziesci_minut.updateSize(W * 0.25, H * 0.5, H * 0.1, H * 0.1)
        self.szescdziesiat_minut.updateSize(W * 0.35, H * 0.5, H * 0.1, H * 0.1)
        self.dziewiecdziesiat_minut.updateSize(W * 0.45, H * 0.5, H * 0.1, H * 0.1)

        self.jedna_minuta.updateSize(W * 0.25, H * 0.5, H * 0.1, H * 0.1)
        self.dwie_minuty.updateSize(W * 0.35, H * 0.5, H * 0.1, H * 0.1)
        self.trzy_minuty.updateSize(W * 0.45, H * 0.5, H * 0.1, H * 0.1)

        self.bez_ograniczen.updateSize(W * 0.55, H * 0.5, W * 0.2, H * 0.1)

        self.nastepny.updateSize(W * 0.4, H * 0.8, W * 0.2, H * 0.1)
        self.poprzedni.updateSize(W * 0.15, H * 0.8, W * 0.2, H * 0.1)
        self.graj.updateSize(W * 0.65, H * 0.8, W * 0.2, H * 0.1)
        self.nastepny_szary.updateSize(W * 0.4, H * 0.8, W * 0.2, H * 0.1)
        self.poprzedni_szary.updateSize(W * 0.15, H * 0.8, W * 0.2, H * 0.1)
        self.nowa_gra.updateSize(W * 0.35, H * 0.5, W * 0.3, H * 0.1)
        self.wczytaj_gre.updateSize(W * 0.35, H * 0.62, W * 0.3, H * 0.1)
        self.wyjscie.updateSize(W * 0.35, H * 0.74, W * 0.3, H * 0.1)
        self.two.updateSize(W * 0.3, H * 0.5, H * 0.1, H * 0.1)
        self.three.updateSize(W * 0.4, H * 0.5, H * 0.1, H * 0.1)
        self.four.updateSize(W * 0.5, H * 0.5, H * 0.1, H * 0.1)
        self.five.updateSize(W * 0.6, H * 0.5, H * 0.1, H * 0.1)

        self.nastepny.updateSize(W * 0.28, H * 0.8, W * 0.2, H * 0.1)
        self.poprzedni.updateSize(W * 0.05, H * 0.8, W * 0.2, H * 0.1)
        self.graj.updateSize(W * 0.51, H * 0.8, W * 0.2, H * 0.1)
        self.personalizacja.updateSize(
            W * 0.75,
            H * 0.8,
            W * 0.2,
            H * 0.1,
        )
        self.nastepny_szary.updateSize(W * 0.28, H * 0.8, W * 0.2, H * 0.1)
        self.poprzedni_szary.updateSize(W * 0.05, H * 0.8, W * 0.2, H * 0.1)

        #karty szansy
        self.pobierz.updateSize(W * 0.2, H * 0.3, W * 0.25, H * 0.1)
        self.pobierz_od_graczy.updateSize(W * 0.2, H * 0.45, W * 0.25, H * 0.1)
        self.oplata.updateSize(W * 0.2, H * 0.6, W * 0.25, H * 0.1)

        self.oplata_za_domki.updateSize(W * 0.55, H * 0.3, W * 0.25, H * 0.1)
        self.przejdz_na_pole.updateSize(W * 0.55, H * 0.45, W * 0.25, H * 0.1)
        self.cofnij_do_wiezienia.updateSize(W * 0.55, H * 0.6, W * 0.25, H * 0.1)

        self.powrot.updateSize(W * 0.4, H * 0.77, W * 0.2, H * 0.1)
        self.zaakceptuj.updateSize(W * 0.378, H * 0.4, W * 0.25, H * 0.15)
