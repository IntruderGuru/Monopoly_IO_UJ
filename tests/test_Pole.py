import pygame
import pytest

from src.Pole import Pole, Vector2, KierunekPol


class TestPole:
    DOMYSLNY_NUMER_POLA = 10

    def setup_method(self):
        self.typ_pole = "test_typ"
        self.pole = Pole(TestPole.DOMYSLNY_NUMER_POLA, self.typ_pole)

    @pytest.mark.parametrize("maksymalna_liczba_pol", list(range(0, len(KierunekPol) * Pole.DLUGOSC_SCIANY_W_POLACH)))
    def test_oblicz_zwrot_naglowka_pola_rzuca_wyjatek_niepoprawna_maksymalna_liczba_pol_za_mala(self, maksymalna_liczba_pol):
        with pytest.raises(Exception):
            wynik = Pole.oblicz_zwrot_naglowka_pola(TestPole.DOMYSLNY_NUMER_POLA, Pole.DLUGOSC_SCIANY_W_POLACH, maksymalna_liczba_pol)


    dodatkowa_sztuczna_ilosc_pol = 10

    @pytest.mark.parametrize("maksymalna_liczba_pol", list(range(len(KierunekPol) * Pole.DLUGOSC_SCIANY_W_POLACH + 1, (len(KierunekPol) + dodatkowa_sztuczna_ilosc_pol) * Pole.DLUGOSC_SCIANY_W_POLACH)))
    def test_oblicz_zwrot_naglowka_pola_rzuca_wyjatek_niepoprawna_maksymalna_liczba_pol_za_duza(self, maksymalna_liczba_pol):
        with pytest.raises(Exception):
            wynik = Pole.oblicz_zwrot_naglowka_pola(TestPole.DOMYSLNY_NUMER_POLA, Pole.DLUGOSC_SCIANY_W_POLACH, maksymalna_liczba_pol)

    def test_oblicz_zwrot_naglowka_pola_niepoprawna_maksymalna_liczba_pol_dzielnie_zero(self):
        with pytest.raises(Exception):
            wynik = Pole.oblicz_zwrot_naglowka_pola(10, dlugosc_sciany_w_polach=0, maksymalna_liczba_pol=Pole.MAKSYMALNA_LICZBA_POL)

    def test_oblicz_zwrot_naglowka_pola_poprawna_maksymalna_liczba_pol_duze_wymiary(self):
        pass

    def test_oblicz_zwrot_naglowka_pola_poprawna_maksymalna_liczba_pol_male_wymiary(self):
        # Aby zwrocilo duze wymiary pola, numer pola musi byc wielokrotnoscia dlugosc_sciany_w_polach
        wynikowe_wymiary = Pole.oblicz_zwrot_naglowka_pola(len(KierunekPol) * Pole.DLUGOSC_SCIANY_W_POLACH, Pole.DLUGOSC_SCIANY_W_POLACH, Pole.MAKSYMALNA_LICZBA_POL)
        pass

    def test_oblicz_rozmiar_pola(self):
        pass

    def test_inicjalizacja_pozycji(self):
        pass

    def test_typ_zmiennych_konstruktora(self):
        assert isinstance(self.pole.numer, int)
        assert isinstance(self.pole.typ, str)
        assert isinstance(self.pole.wymiary, Vector2)
        assert isinstance(self.pole.kierunek_sciany, KierunekPol)
        assert isinstance(self.pole.pozycja, Vector2)
        assert isinstance(self.pole.sciezka_do_grafiki, str)

    @pytest.mark.skip(reason="Not yet implemented path checking")
    def test_sciezka_do_grafiki(self):
        pass

    def test_zwroc_info(self):
        przewidywany_tekst = f"Nazwa: {self.typ_pole}"
        zwrocony_tekst = self.pole.zwroc_info()

        assert przewidywany_tekst == zwrocony_tekst

