from src.okno.Okno import Okno
from src.Przycisk import Przycisk
import pygame


class AkcjaKartOkno(Okno):

    def __init__(self, gra):
        self.H = 660
        self.W = 1200
        self.gra = gra
        self.czy_szansa = False
        self.szansa_png = pygame.transform.scale(
            pygame.image.load("graphics/karta_szansy.png"), (0.6 * self.W, 0.5 * self.H)
        )

        self.wyjscie = Przycisk(
            self.W * 0.42,
            self.H * 0.7,
            self.W * 0.2,
            self.H * 0.1,
            self.gra.kolor_przycisku,
            self.gra.kolor_gdy_kursor,
            "wyjście",
            self.gra.kolor_tekstu,
        )

        self.skalar_czcionki = 28  # im wiekszy tym mniejsza czcionka
        self.font = pygame.font.Font(
            self.gra.czcionka, int(self.W / self.skalar_czcionki)
        )
        self.karta = None
        self.tresc_karty = "empty"

    def aktualizacja(self):
        pass

    def aktualizacja_zdarzen(self, event: pygame.event.Event):
        if self.czy_szansa:
            if self.wyjscie.is_clicked(event):
                if self.karta:
                    self.gra._plansza.karty.aktualna_karta.wykonaj_akcje(
                        self.gra, self.gra._gracze[self.gra._indeks_aktualnego_gracza]
                    )
                self.czy_szansa = False
                self.zamknij()

    def wyswietl(self, screen: pygame.Surface):
        self.zaktualizuj_rozmiar_czcionki()

        self.wyjscie.updateSize(self.W * 0.42, self.H * 0.7, self.W * 0.2, self.H * 0.1)

        if self.czy_szansa:
            nakladka = pygame.Surface(screen.get_size())
            nakladka.set_alpha(
                self.gra.przezroczystosc_nakladki
            )  # Ustaw przezroczystość (0-255)
            nakladka.fill(self.gra.kolor_nakladki)
            screen.blit(nakladka, (0, 0))

            self.wyjscie.draw(screen)

            szansa_png_wyswietlane = pygame.transform.scale(
                self.szansa_png, (0.64 * self.W, 0.5 * self.H)
            )
            screen.blit(szansa_png_wyswietlane, (self.W * 0.2, self.H * 0.15))
            self.wyswietl_lamana_tresc_karty(
                screen, self.tresc_karty, self.W * 0.5, self.H * 0.3
            )

    def przygotuj_karte(self):
        self.karta = self.gra._plansza.karty.nastepna_karta()
        self.tresc_karty = self.karta.tresc

    def zaktualizuj_rozmiar_czcionki(self):
        self.font = pygame.font.Font(
            self.gra.czcionka, int(self.W / self.skalar_czcionki) - 15
        )
        self.karta = self.font.render(self.tresc_karty, True, self.gra.kolor_czcionki)

    def wyswietl_lamana_tresc_karty(
        self, screen, tekst: str, start_x, start_y
    ) -> float:
        """
        :param screen: ekran na ktory jest rysowany tekst
        :param tekst: tekst poddany lamaniu i wyswietleniu juz polamanym
        :param start_x: offset x do wyswietlania tekstu
        :param start_y: offset y do wyswietlania tekstu
        :return: procentowa ilosc zajetego ekranu przez linijki tekstu w porownaniu do calego ekranu
        """
        wyrazy = [wyraz.split(" ") for wyraz in tekst.splitlines()]
        szerokosc_spacji = self.font.size(" ")[0]

        maksymalna_szerokosc = int(self.gra.aktualna_szerokosc_ekranu * 0.8)
        x, y = start_x, start_y
        # ze stacka xD
        for line in wyrazy:
            for word in line:
                word_surface = self.font.render(word, 0, self.gra.kolor_czcionki)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= maksymalna_szerokosc:
                    x = start_x  # Reset the x.
                    y += word_height  # Start on new row.
                screen.blit(word_surface, (x, y))
                x += word_width + szerokosc_spacji
            x = start_x  # Reset the x.
            y += word_height  # Start on new row.

        return (y - start_y) / self.gra.aktualna_wysokosc_ekranu

    def aktualizuj_rozmiar_okna(self, width, height):
        self.W = width
        self.H = height

    def zamknij(self):
        self.gra.czy_akcja_zakonczona = True
