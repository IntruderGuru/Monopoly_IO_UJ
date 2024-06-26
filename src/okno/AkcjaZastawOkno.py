from src.okno.Okno import Okno
from src.Przycisk import Przycisk
from src.Wizualizator import Wizualizator
import pygame


class AkcjaZastawOkno(Okno):

    def __init__(self, gra):
        self.stan = "czy_chcesz_zastawic"
        self.wizualizator: Wizualizator = gra.wizualizator
        self.font = pygame.font.Font(self.wizualizator.czcionka, 32)

        self.H = 800
        self.W = 1200
        self.gra = gra
        self.gracz = None
        self.cena = 0
        self.czy_zastaw = False
        self.wczytana_posiadlosc = ""
        self.ile_do_zastawienia = 0

        self.przycisk_zastaw = Przycisk(
            self.W * 0.35,
            self.H * 0.4,
            self.W * 0.3,
            self.H * 0.1,
            self.wizualizator.kolor_przycisku,
            self.wizualizator.kolor_gdy_kursor,
            "Zastaw",
            self.wizualizator.kolor_czcionki_na_przycisku,
            )
        self.przycisk_wyjscie = Przycisk(
            self.W * 0.35,
            self.H * 0.64,
            self.W * 0.3,
            self.H * 0.1,
            self.wizualizator.kolor_przycisku,
            self.wizualizator.kolor_gdy_kursor,
            "Wyjscie",
            self.wizualizator.kolor_czcionki_na_przycisku,
            )

        self.skalar_czcionki = 40  # im wiekszy tym mniejsza czcionka
        self.font = pygame.font.Font(
            self.wizualizator.czcionka, int(self.W / self.skalar_czcionki)
        )

    def aktualizacja(self):
        pass

    def aktualizacja_zdarzen(self, event: pygame.event.Event):
        if self.czy_zastaw:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.stan == "czy_chcesz_zastawic":
                    if self.przycisk_zastaw.is_clicked(event):
                        self.stan = "wybierz_numer"
                        self.wczytana_posiadlosc = ""
                if self.przycisk_wyjscie.is_clicked(event):
                    self.zamknij()

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    self.zamknij()

                if self.stan == "wybierz_numer":
                    if event.key == pygame.K_RETURN:
                        if self.wczytana_posiadlosc == "":
                            self.stan = "blad"
                            self.wczytana_posiadlosc = ""
                        else:
                            self.wczytana_posiadlosc = int(self.wczytana_posiadlosc)
                            if (
                                self.wczytana_posiadlosc > 0
                                and self.wczytana_posiadlosc <= self.ile_do_zastawienia
                            ):
                                self.gracz.zastaw_posiadlosci(
                                    self.gra, self.wczytana_posiadlosc - 1
                                )
                                self.stan = "zastawiono"
                            else:
                                self.stan = "blad"
                                self.wczytana_posiadlosc = ""
                    elif event.key == pygame.K_BACKSPACE:
                        if len(self.wczytana_posiadlosc) > 0:
                            self.wczytana_posiadlosc = self.wczytana_posiadlosc[:-1]
                    elif event.unicode.isdigit():
                        self.wczytana_posiadlosc += event.unicode
                elif self.stan == "zastawiono":
                    self.stan = "czy_chcesz_zastawic"
                elif self.stan == "blad":
                    self.stan = "wybierz_numer"
                    self.wczytana_posiadlosc = ""
                elif self.stan == "wyjscie":
                    self.zamknij()

    def wyswietl(self, screen: pygame.Surface):

        self.font = pygame.font.Font(
            self.gra.czcionka, int(self.W / self.skalar_czcionki)
        )

        if self.czy_zastaw:
            screen.fill(self.gra.kolor_tla)

            if (
                    self.stan == "czy_chcesz_zastawic"
                    and self.gracz.liczba_zastawionych >= len(self.gracz.lista_posiadlosci)
            ):
                self.przycisk_wyjscie.updateSize(
                    self.W * 0.6, self.H * 0.4, self.W * 0.2, self.H * 0.15
                )

                text = self.font.render(
                    "Nie masz już posiadłości, które mógłbyś zastawić",
                    True,
                    self.wizualizator.kolor_czcionki,
                )
                screen.blit(text, (self.W * 0.1, self.H * 0.1))
                self.stan = "wyjscie"
                pygame.display.update()
                pygame.time.wait(2000)
                self.zamknij()

            elif self.stan == "czy_chcesz_zastawic":
                self.przycisk_zastaw.updateSize(
                    self.W * 0.6, self.H * 0.2, self.W * 0.2, self.H * 0.15
                )
                self.przycisk_wyjscie.updateSize(
                    self.W * 0.6, self.H * 0.4, self.W * 0.2, self.H * 0.15
                )
                self.przycisk_zastaw.draw(screen)
                self.przycisk_wyjscie.draw(screen)

                if self.cena - self.gracz.kwota <= 0:
                    tekst = "Masz już wystarczającą ilość pieniędzy. Czy chcesz zastawić posiadłość? Masz poniższe do wyboru"
                else:
                    tekst = f"Brakuje Ci {self.cena - self.gracz.kwota}. Czy chcesz zastawić jakąś posiadłość? Masz poniższe do wyboru"

                text = self.font.render(
                    tekst,
                    True,
                    self.wizualizator.kolor_czcionki,
                )
                screen.blit(text, (self.W * 0.1, self.H * 0.1))
                self.wyswietl_do_zastawu(screen)

            elif self.stan == "wybierz_numer":
                text = self.font.render(
                    f"Wpisz numer posiadłości",
                    True,
                    self.wizualizator.kolor_czcionki,
                )
                screen.blit(text, (self.W * 0.1, self.H * 0.1))
                self.wyswietl_do_zastawu(screen)
                text = self.font.render(
                    str(self.wczytana_posiadlosc),
                    True,
                    self.wizualizator.kolor_czcionki,
                )
                screen.blit(text, (self.W * 0.1, self.H * 0.8))

            elif self.stan == "blad":
                text = self.font.render(
                    f"Wpisano zły numer",
                    True,
                    self.wizualizator.kolor_czcionki,
                )
                screen.blit(text, (self.W * 0.1, self.H * 0.1))

            elif self.stan == "zastawiono":
                text = self.font.render(
                    f"Zastawiono posiadłość",
                    True,
                    self.wizualizator.kolor_czcionki,
                )
                screen.blit(text, (self.W * 0.1, self.H * 0.1))

    def wyswietl_do_zastawu(self, screen):
        odstep = 0.25
        x = 1
        for posiadlosc in self.gracz.lista_posiadlosci:
            if not posiadlosc.czy_zastawiona:
                text = self.font.render(
                    f"{x}: {posiadlosc.nazwa}, kwota zastawu: {posiadlosc.zastaw_kwota}",
                    True,
                    self.wizualizator.kolor_czcionki,
                )
                screen.blit(text, (self.W * 0.1, self.H * odstep))
                odstep += 0.05
            x += 1
        self.ile_do_zastawienia = x - 1

    def ustaw_gracza(self, gracz, cena):
        self.stan = "czy_chcesz_zastawic"
        self.wczytana_posiadlosc = ""
        self.gracz = gracz
        self.cena = cena

    def aktualizuj_rozmiar_okna(self, width, height):
        self.W = width
        self.H = height

    def zamknij(self):
        self.wczytana_posiadlosc = ""
        self.czy_zastaw = False
