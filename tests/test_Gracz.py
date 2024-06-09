import pytest

import Gracz
from src.Gracz import Gracz, UMIEJETNOSC_ZMIEJSZENIA_CZYNSZU_O
from src.Gra import Gra
from unittest.mock import MagicMock, patch


class MockKontrolerWiadomosci:
    def dodaj_wiadomosc(self):
        pass


class MockWlasciciel:
    def dodaj_pieniadze(self, gra, czynsz):
        pass


class MockPosiadlosc:
    NAZWA = "mock_posiadlosc"
    DOMYSLNA_ZASTAW_KWOTA = 2_000
    DOMYSLNA_CZYNSZ_KWOTA = 1_000

    def __init__(self):
        self.cz_zastawiona: bool
        self.zastaw_kwota = MockPosiadlosc.DOMYSLNA_ZASTAW_KWOTA
        self.nazwa = MockPosiadlosc.NAZWA
        self.wlasciciel = MockWlasciciel()

    def oblicz_czynsz(self, czynsz):
        return MockPosiadlosc.DOMYSLNA_CZYNSZ_KWOTA


class MockAkcjaZastawOkno:
    def __init__(self):
        self.czy_zdejmij_zestaw: bool


class TestGracz:
    DOMYSLNE_ID = 0
    DOMYSLNA_KWOTA = 10_000
    DOMYSLNA_UMIEJETNOSC = "none"

    def setup_method(self):
        self.gracz = Gracz(TestGracz.DOMYSLNE_ID, TestGracz.DOMYSLNA_KWOTA, MagicMock(), TestGracz.DOMYSLNA_UMIEJETNOSC)

    def test_umiejetnosc_wiecej_pieniedzy_na_start(self):
        umiejetnosc = "wiecej_pieniedzy_na_start"
        gracz = Gracz(0, TestGracz.DOMYSLNA_KWOTA, MagicMock(), umiejetnosc)

        nowa_kwota = gracz.kwota

        assert TestGracz.DOMYSLNA_KWOTA < nowa_kwota

    def test_umiejetnosc_karta_wyjscia_z_wiezienia(self):
        umiejetnosc = "karta_wyjscia_z_wiezienia"
        gracz = Gracz(0, TestGracz.DOMYSLNA_KWOTA, MagicMock(), umiejetnosc)

        stara_liczba_kart_wyjdz_z_wiezienia = 0
        nowa_liczba_kart_wyjdz_z_wiezienia = gracz.liczba_kart_wyjdz_z_wiezienia

        assert stara_liczba_kart_wyjdz_z_wiezienia < nowa_liczba_kart_wyjdz_z_wiezienia

    def test_zastaw_posiadlosc(self):
        mock_gra = MagicMock()
        mock_posiadlosc = MockPosiadlosc()

        self.gracz.lista_posiadlosci.append(mock_posiadlosc)
        numer_ostatniej_posiadlosci = len(self.gracz.lista_posiadlosci) - 1

        with patch.object(mock_gra, '_kontroler_wiadomosci', new=MockKontrolerWiadomosci):
            przewidywana_nowa_liczba_zastawionych = 1
            przewidywana_nowa_kwota = self.gracz.kwota

            self.gracz.zastaw_posiadlosci(mock_gra, numer_ostatniej_posiadlosci)

            przewidywana_nowa_kwota += MockPosiadlosc.DOMYSLNA_ZASTAW_KWOTA

            nowa_kwota_gracza = self.gracz.kwota
            nowa_liczba_zastawionych_gracza = self.gracz.liczba_zastawionych

            assert przewidywana_nowa_liczba_zastawionych == nowa_liczba_zastawionych_gracza
            assert przewidywana_nowa_kwota == nowa_kwota_gracza

    def test_zdejmij_zastaw_liczba_zastawionych_zero(self):
        mock_gra = MagicMock()

        with (patch.object(mock_gra, '_kontroler_wiadomosci', new=MockKontrolerWiadomosci),
              patch.object(mock_gra, 'akcja_zastaw_okno', new=MockAkcjaZastawOkno)):
            self.gracz.zdejmij_zastaw_posiadlosci(mock_gra)

            assert mock_gra.akcja_zastaw_okno.czy_zdejmij_zastaw is False

    def test_zdejmij_zastaw_liczba_zastawionych_rozna_od_zera(self):
        mock_gra = MagicMock()

        with (patch.object(mock_gra, '_kontroler_wiadomosci', new=MockKontrolerWiadomosci),
              patch.object(mock_gra, 'akcja_zastaw_okno', new=MockAkcjaZastawOkno)):
            mock_posiadlosc = MockPosiadlosc()

            self.gracz.lista_posiadlosci.append(mock_posiadlosc)
            numer_ostatniej_posiadlosci = len(self.gracz.lista_posiadlosci) - 1

            self.gracz.zastaw_posiadlosci(mock_gra, numer_ostatniej_posiadlosci)
            self.gracz.zdejmij_zastaw_posiadlosci(mock_gra)

        przewidywana_kwota_gracza = MockPosiadlosc.DOMYSLNA_ZASTAW_KWOTA + TestGracz.DOMYSLNA_KWOTA - MockPosiadlosc.DOMYSLNA_ZASTAW_KWOTA * 1.2
        nowa_kwota_gracza = self.gracz.kwota

        assert nowa_kwota_gracza == przewidywana_kwota_gracza

    def test_zaplac_czynsz_posiada_umiejetnosc_placi_mniejsze_czynsze(self):
        umiejetnosci = "placi_mniejsze_czynsze"
        gracz = Gracz(TestGracz.DOMYSLNE_ID, TestGracz.DOMYSLNA_KWOTA, MagicMock(), umiejetnosci)

        mock_gra = MagicMock()

        with patch.object(mock_gra, '_kontroler_wiadomosci', new=MockKontrolerWiadomosci):
            gracz.zaplac_czynsz(mock_gra, MockPosiadlosc())

            przewidywana_nowa_kwota_gracza = TestGracz.DOMYSLNA_KWOTA - (MockPosiadlosc.oblicz_czynsz(MockPosiadlosc, None) - UMIEJETNOSC_ZMIEJSZENIA_CZYNSZU_O)

            assert przewidywana_nowa_kwota_gracza == gracz.kwota

    @pytest.mark.parametrize("kwota_dodana", [5_000, -5_000, 0, 1, -1, -0])
    def test_dodaj_pieniadze_dodatnia(self, kwota_dodana):
        mock_gra = MagicMock()

        with patch.object(mock_gra, '_kontroler_wiadomosci', new=MockKontrolerWiadomosci):
            self.gracz.dodaj_pieniadze(mock_gra, kwota_dodana)

            przewidywana_nowa_kwota_gracza = TestGracz.DOMYSLNA_KWOTA + kwota_dodana

            assert self.gracz.kwota == przewidywana_nowa_kwota_gracza

    def test_czy_przeszedl_przez_start_posiada_umiejetnosc_dostaje_wiecej_za_przejscie_przez_start(self):
        mock_gra = MagicMock()

        with patch.object(mock_gra, '_kontroler_wiadomosci', new=MockKontrolerWiadomosci):
            mock_pionek = MagicMock()
            mock_pionek.numer_pola = 10
            stara_pozycja = 20
            umiejetnosc = "dostaje_wiecej_za_przejscie_przez_start"

            gracz = Gracz(TestGracz.DOMYSLNE_ID, TestGracz.DOMYSLNA_KWOTA, mock_pionek, umiejetnosc)
            stara_kwota_gracza = gracz.kwota

            gracz.czy_przeszedl_przez_start(mock_gra, stara_pozycja)

            assert stara_kwota_gracza + 2200 == gracz.kwota

    def test_czy_przeszedl_przez_start_nie_posiada_umiejetnosc_dostaje_wiecej_za_przejscie_przez_start(self):
        mock_gra = MagicMock()

        with patch.object(mock_gra, '_kontroler_wiadomosci', new=MockKontrolerWiadomosci):
            mock_pionek = MagicMock()
            mock_pionek.numer_pola = 10
            stara_pozycja = 20
            umiejetnosc = "none"

            gracz = Gracz(TestGracz.DOMYSLNE_ID, TestGracz.DOMYSLNA_KWOTA, mock_pionek, umiejetnosc)
            stara_kwota_gracza = gracz.kwota

            gracz.czy_przeszedl_przez_start(mock_gra, stara_pozycja)

            assert stara_kwota_gracza + 2000 == gracz.kwota

    def test_czy_przeszedl_przez_start_nie_przeszedl(self):
        mock_gra = MagicMock()

        with patch.object(mock_gra, '_kontroler_wiadomosci', new=MockKontrolerWiadomosci):
            mock_pionek = MagicMock()
            mock_pionek.numer_pola = 10
            self.gracz.pionek = mock_pionek

            stara_pozycja = 5

            stara_kwota_gracza = self.gracz.kwota
            self.gracz.czy_przeszedl_przez_start(mock_gra, stara_pozycja)

            assert stara_kwota_gracza == self.gracz.kwota