from src.okno.Okno import Okno
from src.Przycisk import Przycisk
import pygame


class AkcjaZagadekOkno(Okno):

    def __init__(self, gra):

        self.H = 800
        self.W = 1200
        self.gra = gra
        self.czy_zagadka = False

        self.A = Przycisk(
            self.W * 0.2,
            self.H * 0.5,
            self.H * 0.1,
            self.H * 0.1,
            self.gra.kolor_przycisku,
            self.gra.kolor_gdy_kursor,
            "A",
            self.gra.kolor_tekstu,
        )
        self.B = Przycisk(
            self.W * 0.2,
            self.H * 0.6,
            self.H * 0.1,
            self.H * 0.1,
            self.gra.kolor_przycisku,
            self.gra.kolor_gdy_kursor,
            "B",
            self.gra.kolor_tekstu,
        )
        self.C = Przycisk(
            self.W * 0.2,
            self.H * 0.7,
            self.H * 0.1,
            self.H * 0.1,
            self.gra.kolor_przycisku,
            self.gra.kolor_gdy_kursor,
            "C",
            self.gra.kolor_tekstu,
        )

        self.odpowiedz_A = "empty"
        self.odpowiedz_B = "empty"
        self.odpowiedz_C = "empty"
        self.poprawna_odpowiedz = "empty"

        self.skalar_czcionki = 28  # im wiekszy tym mniejsza czcionka
        self.font = pygame.font.Font(
            self.gra.czcionka, int(self.W / self.skalar_czcionki))
        self.informacja_o_podatku = "Zapłać podatek dochodowy o wartości "
        self.informacja_o_podatku_z_cena = self.informacja_o_podatku + "x"
        self.informacja_o_zagadce = ""
        self.tekst_zagadki = "empty"

    def aktualizacja(self):
        pass

    def aktualizacja_zdarzen(self, event: pygame.event.Event):

        if self.czy_zagadka:

            if self.A.is_clicked(event):
                self.pole.zaplac_podatek(
                    self.gra, self.gracz, (self.poprawna_odpowiedz == "A")
                )
                self.czy_zagadka = False
                self.zamknij()
            elif self.B.is_clicked(event):
                self.pole.zaplac_podatek(
                    self.gra, self.gracz, (self.poprawna_odpowiedz == "B")
                )
                self.czy_zagadka = False
                self.zamknij()
            elif self.C.is_clicked(event):
                self.pole.zaplac_podatek(
                    self.gra, self.gracz, (self.poprawna_odpowiedz == "C")
                )
                self.czy_zagadka = False
                self.zamknij()

    def wyswietl(self, screen: pygame.Surface):
        self.zaktualizuj_rozmiar_czcionki()

        if self.czy_zagadka:
            screen.fill(self.gra.kolor_tla)
            screen.blit(self.podatek, (self.W * 0.18, self.H * 0.2))
            screen.blit(self.info, (self.W * 0.19, self.H * 0.27))
            offset_height_percent = self.wyswietl_lamana_tresc_zagadki(
                screen, self.tekst_zagadki, self.W * 0.2, self.H * 0.4)

            # odpowiedzi
            offset_height_percent -= 0.05
            screen.blit(self.oA, (self.W * 0.3, self.H *
                        (0.54 + offset_height_percent)))
            screen.blit(self.oB, (self.W * 0.3, self.H *
                        (0.66 + offset_height_percent)))
            screen.blit(self.oC, (self.W * 0.3, self.H *
                        (0.78 + offset_height_percent)))

            self.wyswietl_przyciski(screen, offset_height_percent)

    def przygotuj_zagadke(self):
        zagadka = self.gra._plansza.zagadki.nastepna_zagadka()
        self.tekst_zagadki = zagadka.tresc_zagadki

        self.odpowiedz_A = zagadka.odpowiedz_a
        self.odpowiedz_B = zagadka.odpowiedz_b
        self.odpowiedz_C = zagadka.odpowiedz_c
        self.poprawna_odpowiedz = zagadka.poprawna

        self.informacja_o_podatku_z_cena = self.informacja_o_podatku + str(
            self.pole.podatek
        )
        self.informacja_o_zagadce = "Odpowiedz poprawnie na pytanie aby zmniejszyć opłatę i zapłacić tylko " + str(
            (self.pole.podatek // 2)
        )

    def akcja_podatkowa(self, gracz, pole):
        self.gracz = gracz
        self.pole = pole

    def zaktualizuj_rozmiar_czcionki(self):
        self.font = pygame.font.Font(
            self.gra.czcionka, int(self.W / self.skalar_czcionki))
        self.podatek = self.font.render(
            self.informacja_o_podatku_z_cena, True, self.gra.kolor_czcionki
        )
        self.font = pygame.font.Font(self.gra.czcionka, int(
            self.W / self.skalar_czcionki) - 15)
        self.info = self.font.render(
            self.informacja_o_zagadce, True, self.gra.kolor_czcionki)
        self.zagadka = self.font.render(
            self.tekst_zagadki, True, self.gra.kolor_czcionki)

        # odpowiedzi
        self.oA = self.font.render(
            self.odpowiedz_A, True, self.gra.kolor_czcionki)
        self.oB = self.font.render(
            self.odpowiedz_B, True, self.gra.kolor_czcionki)
        self.oC = self.font.render(
            self.odpowiedz_C, True, self.gra.kolor_czcionki)

    def wyswietl_lamana_tresc_zagadki(self, screen, tekst: str, start_x, start_y) -> float:
        """
            :param screen: ekran na ktory jest rysowany tekst
            :param tekst: tekst poddany lamaniu i wyswietleniu juz polamanym
            :param start_x: offset x do wyswietlania tekstu
            :param start_y: offset y do wyswietlania tekstu
            :return: procentowa ilosc zajetego ekranu przez linijki tekstu w porownaniu do calego ekranu
        """
        wyrazy = [wyraz.split(' ') for wyraz in tekst.splitlines()]
        szerokosc_spacji = self.font.size(' ')[0]

        maksymalna_szerokosc = self.gra.aktualna_szerokosc_ekranu
        x, y = start_x, start_y
        # ze stacka xD
        for line in wyrazy:
            for word in line:
                word_surface = self.font.render(
                    word, 0, self.gra.kolor_czcionki)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= maksymalna_szerokosc:
                    x = start_x         # Reset the x.
                    y += word_height    # Start on new row.
                screen.blit(word_surface, (x, y))
                x += word_width + szerokosc_spacji
            x = start_x         # Reset the x.
            y += word_height    # Start on new row.

        return (y - start_y) / self.gra.aktualna_wysokosc_ekranu

    def wyswietl_przyciski(self, screen, offset_height_percent):
        self.A.updateSize(self.W * 0.2, self.H * (0.5 +
                          offset_height_percent), self.H * 0.1, self.H * 0.1)
        self.A.draw(screen)
        self.B.updateSize(self.W * 0.2, self.H * (0.62 +
                          offset_height_percent), self.H * 0.1, self.H * 0.1)
        self.B.draw(screen)
        self.C.updateSize(self.W * 0.2, self.H * (0.74 +
                          offset_height_percent), self.H * 0.1, self.H * 0.1)
        self.C.draw(screen)

    def aktualizuj_rozmiar_okna(self, width, height):
        self.W = width
        self.H = height

    def zamknij(self):
        self.gra._kontroler_wiadomosci.dodaj_wiadomosc(
            f"Poprawna odpowiedz to: {self.poprawna_odpowiedz}"
        )
        self.gra.czy_akcja_zakonczona = True
