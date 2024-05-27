from src.Okno.Okno import Okno
from src.Przycisk import Przycisk
import pygame
from enum import Enum


class AkcjaZakupu(Enum):
    Nic = 0
    Posiadlosc = 1
    Hotel = 2


class AkcjaPolaOkno(Okno):
    def __init__(self, gra):
        self.W = 1200
        self.H = 800
        self.gra = gra
        
        self.zakup = Przycisk(self.W * 0.6, self.H * 0.2, self.W * 0.2, self.H * 0.15, self.gra.kolor_przycisku, self.gra.kolor_gdy_kursor, "kupuję", self.gra.kolor_tekstu)
        self.licytacja = Przycisk(self.W * 0.6, self.H * 0.4, self.W * 0.2, self.H * 0.15, self.gra.kolor_przycisku, self.gra.kolor_gdy_kursor, "licytacja", self.gra.kolor_tekstu)
        self.czy_akcja_pola = False
        
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

#     def aktulizacja_zdarzen(self, event: pygame.event.Event):
#         if self.przycisk_kup_domek.is_clicked(event):
#             self.ktora_akcja_zakupu = AkcjaZakupu.Posiadlosc

#         elif self.przycisk_kup_hotel.is_clicked(event):
#             self.ktora_akcja_zakupu = AkcjaZakupu.Hotel

#         elif self.wyjscie.is_clicked(event):
#             self.czy_zakup = False

    def aktualizacja_zdarzen(self, event: pygame.event.Event):
        if self.zakup.is_clicked(event):
            self.kup_pole()
            self.czy_akcja_pola = False
            self.zamknij()
        elif self.licytacja.is_clicked(event):
            self.czy_akcja_pola = False
            self.zamknij()
            pass

    def wyswietl(self, screen: pygame.Surface):
        if self.czy_zakup:
            self.przycisk_kup_domek.draw(screen)
            self.przycisk_kup_hotel.draw(screen)
            self.wyjscie.draw(screen)

    def akcja_kupowania(self, posiadlosc, gracz):
        self.posiadlosc_do_zakupu = posiadlosc
        self.gracz_majacy_mozliwosc_zakupu = gracz
        self.board_png = pygame.transform.scale(pygame.image.load(self.posiadlosc_do_zakupu.sciezka_do_grafiki), (0.28 * self.W, 0.64 * self.H))

    def kup_pole(self):
        self.posiadlosc_do_zakupu.kup_posiadlosc(self.gra, self.gracz_majacy_mozliwosc_zakupu)
        
    def aktualizuj_rozmiar_okna(self, width, height):
        self.W = width
        self.H = height

    def zamknij(self):
        self.gra.czy_akcja_zakonczona = True
