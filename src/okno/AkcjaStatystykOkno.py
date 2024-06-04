from src.okno.Okno import Okno
from src.Statystyka import Statystyka
import pygame


MAKSYMALNA_DLUGOSC_NAZWY_GRACZA = 12

class AkcjaStatystykOkno(Okno):
    def __init__(self, gra):
        self.W = 1200
        self.H = 660
        self.gra = gra
        self.czy_akcja_statystyk = True

        self.skalar_czcionki = 40 # im wiekszy tym mniejsza czcionka
        self.font = pygame.font.Font(self.gra.czcionka, int(self.W / self.skalar_czcionki))

        self.odleglosc_pionowa = 0.06
        self.mnoznik_wysokosci = 0.1
        self.mnoznik_szerokosci = 0.62

    def aktualizacja(self):
        pass

    def aktualizacja_zdarzen(self, event: pygame.event.Event):
        pass

    def wyswietl(self, screen: pygame.Surface):

        if self.czy_akcja_statystyk:
            
            i = 0
            self.ramka = pygame.transform.scale(
                pygame.image.load("graphics/tlo_do_statystyk.png"),
                (self.W * 0.43, self.H * 0.36)
            )
            screen.blit(self.ramka, (self.W * (self.mnoznik_szerokosci - 0.06), self.H * (self.mnoznik_wysokosci - 0.08)))

            self.tlo_wiad = pygame.transform.scale(
                pygame.image.load("graphics/tlo_do_wiadomosci.png"),
                (self.W * 0.43, self.H * 0.56)
            )
            screen.blit(self.tlo_wiad, (self.W * (self.mnoznik_szerokosci - 0.06), self.H * (self.mnoznik_wysokosci + 0.28)))

            self.tlo_glowna = pygame.transform.scale(
                pygame.image.load("graphics/tlo_do_glownej_wiadomosci.png"),
                (self.W * 0.43, self.H * 0.05)
            )
            screen.blit(self.tlo_glowna, (self.W * (self.mnoznik_szerokosci - 0.06), self.H * (self.mnoznik_wysokosci + 0.755)))
            
            for gracz in self.gra._gracze:

                nazwa_gracza = self.sprawdz_czy_nazwa_gracza_nie_za_dluga(gracz.id)
                self.zaktualizuj_tekst_i_rozmiar(gracz, nazwa_gracza)

                self.zdjecie_pionek = pygame.transform.scale(
                    pygame.image.load(gracz.pionek.sciezka_do_grafiki), (0.02 * self.W, 0.02 * self.W)
                )

                screen.blit(self.zdjecie_pionek, (self.W * (self.mnoznik_szerokosci - 0.03), self.H * (self.mnoznik_wysokosci + (i * self.odleglosc_pionowa - 0.005))))

                screen.blit(self.nazwa, (self.W * (self.mnoznik_szerokosci), self.H * (self.mnoznik_wysokosci + (i * self.odleglosc_pionowa))))
                screen.blit(self.pieniadze, (self.W * (self.mnoznik_szerokosci + 0.12), self.H * (self.mnoznik_wysokosci + (i * self.odleglosc_pionowa))))
                screen.blit(self.posiadlosci, (self.W * (self.mnoznik_szerokosci + 0.22), self.H * (self.mnoznik_wysokosci + (i * self.odleglosc_pionowa))))
                screen.blit(self.domki, (self.W * (self.mnoznik_szerokosci + 0.26), self.H * (self.mnoznik_wysokosci + (i * self.odleglosc_pionowa))))
                screen.blit(self.hotele, (self.W * (self.mnoznik_szerokosci + 0.3), self.H * (self.mnoznik_wysokosci + (i * self.odleglosc_pionowa))))
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
        
    def zaktualizuj_tekst_i_rozmiar(self, gracz, nazwa_gracza):
        self.font = pygame.font.Font(self.gra.czcionka, int(self.W / self.skalar_czcionki))

        self.nazwa = self.font.render(
            str(nazwa_gracza), True, self.gra.kolor_czcionki
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
        