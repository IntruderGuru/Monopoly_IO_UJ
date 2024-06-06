import pytest
from src.Statystyka import Statystyka


class TestStatystyka:
    def setup_method(self):
        self.statystyka = Statystyka(1000, "test1")

    def test_aktualizuj_stan_pieniedzy_poprawna_kwota(self):
        nowy_stan_pieniedzy = 2000

        self.statystyka.aktualizuj_stan_pieniedzy(nowy_stan_pieniedzy)

        stan_pieniedzy_po_aktualziacji = self.statystyka.pieniadze

        assert nowy_stan_pieniedzy == stan_pieniedzy_po_aktualziacji

    def test_aktualizuj_stan_pieniedzy_kwota_ujemna(self):
        nowy_stan_pieniedzy = -2000

        self.statystyka.aktualizuj_stan_pieniedzy(nowy_stan_pieniedzy)

        stan_pieniedzy_po_aktualziacji = self.statystyka.pieniadze

        assert (nowy_stan_pieniedzy == stan_pieniedzy_po_aktualziacji)

    def test_dodaj_posiadlosc(self):
        ilosc_posiadlosci_przed_dodaniem = self.statystyka.ilosc_posiadlosci

        self.statystyka.dodaj_posiadlosc()

        ilosc_posiadlosci_po_dodaniu = self.statystyka.ilosc_posiadlosci
        przewidywana_ilosc_posiadlosci = ilosc_posiadlosci_przed_dodaniem + 1

        assert przewidywana_ilosc_posiadlosci == ilosc_posiadlosci_po_dodaniu

    def test_dodaj_hotel_poprawna_ilosc(self):
        ilosc_hoteli_przed_dodaniem = self.statystyka.ilosc_hoteli
        ilosc_nowych_hoteli = 2

        self.statystyka.dodaj_hotel(ilosc_nowych_hoteli)

        ilsoc_hoteli_po_dodaniu = self.statystyka.ilosc_hoteli
        przewidywana_ilosc_hoteli = ilosc_hoteli_przed_dodaniem + ilosc_nowych_hoteli

        assert przewidywana_ilosc_hoteli == ilsoc_hoteli_po_dodaniu

    def test_dodaj_hotel_ujemna_ilosc(self):
        ilosc_hoteli_przed_dodaniem = self.statystyka.ilosc_hoteli
        ilosc_nowych_hoteli_niewlasciwa = -2

        self.statystyka.dodaj_hotel(ilosc_nowych_hoteli_niewlasciwa)

        niepoprawna_ilsoc_hoteli_po_dodaniu = self.statystyka.ilosc_hoteli
        przewidywana_ilosc_hoteli = ilosc_hoteli_przed_dodaniem

        assert przewidywana_ilosc_hoteli != niepoprawna_ilsoc_hoteli_po_dodaniu

    def test_dodaj_domek_poprawna_ilosc(self):
        ilosc_domkow_przed_dodaniem = self.statystyka.ilosc_domkow
        ilosc_nowych_domkow = 2

        self.statystyka.dodaj_domek(ilosc_nowych_domkow)

        ilsoc_domkow_po_dodaniu = self.statystyka.ilosc_domkow
        przewidywana_ilosc_hoteli = ilosc_domkow_przed_dodaniem + ilosc_nowych_domkow

        assert przewidywana_ilosc_hoteli == ilsoc_domkow_po_dodaniu

    def test_dodaj_domek_ujemna_ilosc(self):
        ilosc_domkow_przed_dodaniem = self.statystyka.ilosc_domkow
        ilosc_nowych_domkow_niewlasciwa = -2

        self.statystyka.dodaj_domek(ilosc_nowych_domkow_niewlasciwa)

        niepoprawna_ilsoc_domkow_po_dodaniu = self.statystyka.ilosc_domkow
        przewidywana_ilosc_hoteli = ilosc_domkow_przed_dodaniem

        assert przewidywana_ilosc_hoteli != niepoprawna_ilsoc_domkow_po_dodaniu

    def test_odejmij_domek_poprawna_ilosc(self):
        startowa_ilosc_domkow = 4
        self.statystyka.ilosc_domkow = startowa_ilosc_domkow

        ilosc_domkow_przed_odjeciem = self.statystyka.ilosc_domkow
        ilosc_odjetych_domkow = 2

        self.statystyka.odejmij_domek(ilosc_odjetych_domkow)

        ilsoc_domkow_po_odjeciu = self.statystyka.ilosc_domkow
        przewidywana_ilosc_domkow = ilosc_domkow_przed_odjeciem - ilosc_odjetych_domkow

        assert przewidywana_ilosc_domkow == ilsoc_domkow_po_odjeciu

    def test_odejmij_domek_ujemna_wartosc_domkow(self):
        startowa_ilosc_domkow = 0
        self.statystyka.ilosc_domkow = startowa_ilosc_domkow

        ilosc_domkow_przed_odjeciem = self.statystyka.ilosc_domkow
        ilosc_odjetych_domkow = 2

        self.statystyka.odejmij_domek(ilosc_odjetych_domkow)

        niepoprawna_ilsoc_domkow_po_odjeciu = self.statystyka.ilosc_domkow
        przewidywana_ilosc_domkow = ilosc_domkow_przed_odjeciem

        assert przewidywana_ilosc_domkow != niepoprawna_ilsoc_domkow_po_odjeciu

    def test_odejmij_domek_minusowa_ilosc_odejmowanych(self):
        startowa_ilosc_domkow = 0
        self.statystyka.ilosc_domkow = startowa_ilosc_domkow

        ilosc_domkow_przed_odjeciem = self.statystyka.ilosc_domkow
        ilosc_odjetych_domkow = -2

        self.statystyka.odejmij_domek(ilosc_odjetych_domkow)

        niepoprawna_ilsoc_domkow_po_odjeciu = self.statystyka.ilosc_domkow
        przewidywana_ilosc_domkow = ilosc_domkow_przed_odjeciem

        assert przewidywana_ilosc_domkow != niepoprawna_ilsoc_domkow_po_odjeciu
