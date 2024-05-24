from Okno.Okno import Okno
from src.Przycisk import Przycisk
import pygame


class AkcjaPolaOkno(Okno):

    def __init__(self):
        self.aktualna_szerokosc_ekranu = 1200
        self.aktualna_wysokosc_ekranu = 800

        self.board_png = pygame.transform.scale(
            pygame.image.load("graphics/pole.png"), (0.28 * self.aktualna_szerokosc_ekranu, 0.64 * self.aktualna_wysokosc_ekranu)
        )

        self.kolor_przycisku = (70, 70, 70)
        self.kolor_hovera = (150, 150, 150)

        self.zakup = Przycisk(self.aktualna_szerokosc_ekranu * 0.6, self.aktualna_wysokosc_ekranu * 0.2, self.aktualna_szerokosc_ekranu * 0.2, self.aktualna_wysokosc_ekranu * 0.15, self.kolor_przycisku, self.kolor_hovera, "kupuje", (255,255,255))
        self.licytacja = Przycisk(self.aktualna_szerokosc_ekranu * 0.6, self.aktualna_wysokosc_ekranu * 0.4, self.aktualna_szerokosc_ekranu * 0.2, self.aktualna_wysokosc_ekranu * 0.15, self.kolor_przycisku, self.kolor_hovera, "licytacja", (255,255,255))
        self.ktora_akcja = 0
        self.czy_akcja_pola = False

        self.nieruchomosc = "wyjscie"
        self.wyjscie = Przycisk(self.aktualna_szerokosc_ekranu * 0.6, self.aktualna_wysokosc_ekranu * 0.4, self.aktualna_szerokosc_ekranu * 0.2, self.aktualna_wysokosc_ekranu * 0.15, self.kolor_przycisku, self.kolor_hovera, "brak ruchu", (255,255,255))
        self.przycisk_kup_hotel = Przycisk(self.aktualna_szerokosc_ekranu * 0.6, self.aktualna_wysokosc_ekranu * 0.2, self.aktualna_szerokosc_ekranu * 0.2, self.aktualna_wysokosc_ekranu * 0.15, self.kolor_przycisku, self.kolor_hovera, "kup hotel", (255,255,255))
        self.przycisk_kup_domek = Przycisk(self.aktualna_szerokosc_ekranu * 0.6, self.aktualna_wysokosc_ekranu * 0.2, self.aktualna_szerokosc_ekranu * 0.2, self.aktualna_wysokosc_ekranu * 0.15, self.kolor_przycisku, self.kolor_hovera, "kup domek", (255,255,255))
        self.ktore_kupno = 0
        self.czy_kupno = False

    def aktualizacja(self):
        pass

    def aktulizacja_zdarzen(self, event: pygame.event.Event):
        if self.zakup.is_clicked(event):
            self.ktore_kupno = 1
            self.czy_akcja_pola = False
            # return 1
        elif self.licytacja.is_clicked(event):
            self.ktore_kupno = 2
            self.czy_akcja_pola = False
            # return 2
        elif self.przycisk_kup_domek.is_clicked(event) and self.nieruchomosc == "domek":
            self.czy_kupno = False
        elif self.przycisk_kup_hotel.is_clicked(event) and self.nieruchomosc == "hotel":
            self.czy_kupno = False
        elif self.wyjscie.is_clicked(event) and self.nieruchomosc == "wyjscie":
            self.czy_kupno = False

    def wyswietl(self, screen: pygame.Surface):
        H = self.aktualna_wysokosc_ekranu
        W = self.aktualna_szerokosc_ekranu

        if self.czy_akcja_pola:
            self.board_png = pygame.transform.scale(self.board_png, (0.28 * W, 0.64 * H))
            screen.blit(self.board_png, (W * 0.2, H * 0.15))
            self.zakup.updateSize(W * 0.6, H * 0.2, W * 0.2, H * 0.15)
            self.licytacja.updateSize(W * 0.6, H * 0.4, W * 0.2, H * 0.15)
            self.zakup.draw(screen)
            self.licytacja.draw(screen)

        if self.czy_kupno:
            self.przycisk_kup_domek.draw(screen)
            self.przycisk_kup_hotel.draw(screen)
            self.wyjscie.draw(screen)