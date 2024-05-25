from src.Okno.Okno import Okno
from src.Przycisk import Przycisk
import pygame
from enum import Enum


class AkcjaZakupu(Enum):
    Nic = 0
    Posiadlosc = 1
    Hotel = 2


class AkcjaPolaOkno(Okno):
    def __init__(self):
        self.aktualna_szerokosc_ekranu = 1200
        self.aktualna_wysokosc_ekranu = 800

        self.board_png = pygame.transform.scale(
            pygame.image.load("graphics/pole.png"), (0.28 * self.aktualna_szerokosc_ekranu, 0.64 * self.aktualna_wysokosc_ekranu)
        )

        self.kolor_przycisku = (70, 70, 70)
        self.kolor_hovera = (150, 150, 150)

        # self.zakup = Przycisk(self.aktualna_szerokosc_ekranu * 0.6, self.aktualna_wysokosc_ekranu * 0.2, self.aktualna_szerokosc_ekranu * 0.2, self.aktualna_wysokosc_ekranu * 0.15, self.kolor_przycisku, self.kolor_hovera, "kupuje", (255,255,255))
        # self.licytacja = Przycisk(self.aktualna_szerokosc_ekranu * 0.6, self.aktualna_wysokosc_ekranu * 0.4, self.aktualna_szerokosc_ekranu * 0.2, self.aktualna_wysokosc_ekranu * 0.15, self.kolor_przycisku, self.kolor_hovera, "licytacja", (255,255,255))
        # self.czy_akcja_pola = False

        OFF_SET = 20
        self.przycisk_kup_domek = Przycisk(self.aktualna_szerokosc_ekranu * 0.6, self.aktualna_wysokosc_ekranu * 0.2, self.aktualna_szerokosc_ekranu * 0.2, self.aktualna_wysokosc_ekranu * 0.15, self.kolor_przycisku, self.kolor_hovera, "kup domek", (255,255,255))

        przycisk_offset = self.przycisk_kup_domek.pobierz_wymiary().height + OFF_SET
        self.przycisk_kup_hotel = Przycisk(self.aktualna_szerokosc_ekranu * 0.6, self.aktualna_wysokosc_ekranu * 0.2 + przycisk_offset, self.aktualna_szerokosc_ekranu * 0.2, self.aktualna_wysokosc_ekranu * 0.15, self.kolor_przycisku, self.kolor_hovera, "kup hotel", (255,255,255))

        przycisk_offset = self.przycisk_kup_hotel.pobierz_wymiary().height + OFF_SET
        self.wyjscie = Przycisk(self.aktualna_szerokosc_ekranu * 0.6, self.aktualna_wysokosc_ekranu * 0.4 + przycisk_offset, self.aktualna_szerokosc_ekranu * 0.2, self.aktualna_wysokosc_ekranu * 0.15, self.kolor_przycisku, self.kolor_hovera, "brak ruchu", (255,255,255))

        self.ktora_akcja_zakupu: AkcjaZakupu = AkcjaZakupu.Nic
        self.czy_zakup = False

    def okno_kup_nieruchomosc(self, gracz, pole_posiadlosc):
        self.czy_zakup = True

        id_wlasciciela_posiadlosci = pole_posiadlosc.pobierz_id_wlasciciela()
        if id_wlasciciela_posiadlosci is None or id_wlasciciela_posiadlosci == gracz.id:
            match self.ktora_akcja_zakupu:
                case AkcjaZakupu.Posiadlosc:
                    pole_posiadlosc.kup_posiadlosc(self, gracz)

                case AkcjaZakupu.Hotel:
                    pass

    def czy_koniec_zakupu(self) -> bool:
        return self.czy_zakup

    def aktualizacja(self):
        pass

    def aktulizacja_zdarzen(self, event: pygame.event.Event):
        # if self.zakup.is_clicked(event):
        #     self.czy_akcja_pola = False
        #
        # elif self.licytacja.is_clicked(event):
        #     self.czy_akcja_pola = False

        if self.przycisk_kup_domek.is_clicked(event):
            self.ktora_akcja_zakupu = AkcjaZakupu.Posiadlosc

        elif self.przycisk_kup_hotel.is_clicked(event):
            self.ktora_akcja_zakupu = AkcjaZakupu.Hotel

        elif self.wyjscie.is_clicked(event):
            self.czy_zakup = False

    def wyswietl(self, screen: pygame.Surface):
        H = self.aktualna_wysokosc_ekranu
        W = self.aktualna_szerokosc_ekranu

        # if self.czy_akcja_pola:
        #     self.board_png = pygame.transform.scale(self.board_png, (0.28 * W, 0.64 * H))
        #     screen.blit(self.board_png, (W * 0.2, H * 0.15))
        #     self.zakup.updateSize(W * 0.6, H * 0.2, W * 0.2, H * 0.15)
        #     self.licytacja.updateSize(W * 0.6, H * 0.4, W * 0.2, H * 0.15)
        #     self.zakup.draw(screen)
        #     self.licytacja.draw(screen)

        if self.czy_zakup:
            self.przycisk_kup_domek.draw(screen)
            self.przycisk_kup_hotel.draw(screen)
            self.wyjscie.draw(screen)
