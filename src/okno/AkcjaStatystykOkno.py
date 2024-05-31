from src.okno.Okno import Okno
from src.Statystyka import Statystyka
import pygame


MAKSYMALNA_DLUGOSC_NAZWY_GRACZA = 10

class AkcjaStatystykOkno(Okno):
    def __init__(self, gra):
        self.W = 1200
        self.H = 800
        self.gra = gra
        self.czy_akcja_statystyk = True

        self.skalar_czcionki = 22  # im wiekszy tym mniejsza czcionka
        self.font = pygame.font.Font(None, int(self.W / self.skalar_czcionki))

        self.odleglosc_pionowa = 0.1
        self.odleglosc_pozioma = 0.1
        self.mnoznik_wysokosci = 0.1
        self.mnoznik_szerokosci = 0.6

    def aktualizacja(self):
        pass

    def aktualizacja_zdarzen(self, event: pygame.event.Event):
        pass

    def wyswietl(self, screen: pygame.Surface):

        if self.czy_akcja_statystyk:
            
            i = 0
            for gracz in self.gra._gracze:
                self.zaktualizuj_tekst_i_rozmiar(gracz)

                screen.blit(self.nazwa, (self.W * (self.mnoznik_szerokosci + (self.odleglosc_pozioma * 1)), self.H * (self.mnoznik_wysokosci + (i * self.odleglosc_pionowa))))
                screen.blit(self.pieniadze, (self.W * (self.mnoznik_szerokosci + (self.odleglosc_pozioma * 2)), self.H * (self.mnoznik_wysokosci + (i * self.odleglosc_pionowa))))
                screen.blit(self.posiadlosci, (self.W * (self.mnoznik_szerokosci + (self.odleglosc_pozioma * 3)), self.H * (self.mnoznik_wysokosci + (i * self.odleglosc_pionowa))))
                screen.blit(self.domki, (self.W * (self.mnoznik_szerokosci + (self.odleglosc_pozioma * 4)), self.H * (self.mnoznik_wysokosci + (i * self.odleglosc_pionowa))))
                screen.blit(self.hotele, (self.W * (self.mnoznik_szerokosci + (self.odleglosc_pozioma * 5)), self.H * (self.mnoznik_wysokosci + (i * self.odleglosc_pionowa))))
                i += 1


    def aktualizuj_rozmiar_okna(self, width, height):
        self.W = width
        self.H = height

    def zamknij(self):
        self.gra.czy_akcja_zakonczona = True


    def sprawdz_czy_nazwa_gracza_nie_za_dluga(self, nazwa):
        if len(nazwa) > MAKSYMALNA_DLUGOSC_NAZWY_GRACZA:
            return (nazwa[:MAKSYMALNA_DLUGOSC_NAZWY_GRACZA - 3] + "...")
        else:
            return nazwa
        
    def zaktualizuj_tekst_i_rozmiar(self, gracz):
        self.font = pygame.font.Font(None, int(self.W / self.skalar_czcionki))

        self.nazwa = self.font.render(
            str(gracz.statystyka.nazwa_gracza), True, self.gra.kolor_czcionki
        )
        self.pieniadze = self.font.render(
            str(gracz.statystyka.pieniadze), True, self.gra.kolor_czcionki
        )
        self.posiadlosci = self.font.render(
            str(gracz.statystyka.ilosc_posiadlosci), True, self.gra.kolor_czcionki
        )
        self.domki = self.font.render(
            str(gracz.statystyka.ilosc_domkow), True, self.gra.kolor_czcionki
        )
        self.hotele = self.font.render(
            str(gracz.statystyka.ilosc_hoteli), True, self.gra.kolor_czcionki
        )
        