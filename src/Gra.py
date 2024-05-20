import random
import pygame
import sys
from src.Gracz import Gracz
from src.Pole import Pole
from src.Posiadlosc import *
from src.Pionek import Pionek

KWOTA_POCZATKOWA = 10000
MIN_LICZBA_GRACZY = 2
MAX_LICZBA_GRACZY = 5
LICZBA_POL = 40

# Dodajemy listę kolorów dla pionków jako obiekty pygame.Color
PIECE_COLORS = [
    pygame.Color("red"),
    pygame.Color("green"),
    pygame.Color("blue"),
    pygame.Color("yellow"),
    pygame.Color("purple"),
]


class Gra:
    def __init__(self):
        self.gracze = []
        self._kwota_poczatkowa = KWOTA_POCZATKOWA
        self._liczba_graczy = 0
        self._suma_oczek = 0
        self._kolejny_rzut_kostka = False
        self._aktualny_gracz = 0
        self.board = self.stworz_plansze()
        self.messages = []

    def stworz_plansze(self):
        board = []
        board.append(Pole(0, "Start"))
        board.append(Posiadlosc(1, "Automat z kawą", 600, 20, 300, 500))
        board.append(Pole(2, "Szansa"))
        board.append(Posiadlosc(3, "Bistro \"Świetlica\"", 600, 40, 300, 500))
        board.append(Pole(4, "Podatek dochodowy"))
        board.append(PosiadloscKolo(5, "KNRSI", 2000, 250, 1000))
        board.append(Posiadlosc(6, "Parking", 1000, 60, 500, 500))
        board.append(Pole(7, "Szansa"))
        board.append(Posiadlosc(8, "Winda", 1000, 60, 500, 500))
        board.append(Posiadlosc(9, "Szatnia", 1200, 80, 500, 500))
        board.append(Pole(10, "Wiezienie"))
        board.append(Posiadlosc(11,"Sala 1073 (sieci)", 1400, 100, 700, 1000))
        board.append(PosiadloscPozaWmii(12,"Drążki za wydziałem", 1500, 0, 750))
        board.append(Posiadlosc(13, "Sala 0056 (laby)", 1400, 100, 700, 1000))
        board.append(Posiadlosc(14, "Sala 1072 (macbooki)", 1600, 120, 800, 1000))
        board.append(PosiadloscKolo(15, "KNMF", 2000, 250, 1000))
        board.append(Posiadlosc(16, "Ślimak", 1800, 140, 900, 1000))
        board.append(Pole(17, "Szansa"))
        board.append(Posiadlosc(18, "Serwerownia", 1800, 140, 900, 1000))
        board.append(Posiadlosc(19, "Pokój samorządu", 2000, 160, 1000, 1000))
        board.append(Pole(20, "Parking"))
        board.append(Posiadlosc(21, "Recepcja", 2200, 180, 1100, 1500))
        board.append(Pole(22, "Szansa"))
        board.append(Posiadlosc(23, "Dziekanat", 2200, 180, 1100, 1500))
        board.append(Posiadlosc(24, "Muzeum komputerów", 2400, 200, 1200, 1500))
        board.append(PosiadloscKolo(25, "KMS", 2000, 250, 1000))
        board.append(Posiadlosc(26, "Mural", 2600, 220, 1300, 1500))
        board.append(Posiadlosc(27, "Pomnik Kopernika", 2600, 220, 1300, 1500))
        board.append(PosiadloscPozaWmii(28,"Przejście przez WZIKS", 1500, 0, 750))
        board.append(Posiadlosc(29, "Fontanna", 2800, 240, 1400, 1500))
        board.append(Pole(30, "Idz do wiezienia"))
        board.append(Posiadlosc(31, "Ping-pong", 3000, 260, 1500, 2000))
        board.append(Posiadlosc(32, "Bilard", 3000, 260, 1500, 2000))
        board.append(Pole(33, "Szansa"))
        board.append(Posiadlosc(34, "Piłkarzyki", 3200, 280, 1600, 2000))
        board.append(PosiadloscKolo(35, "KSI", 2000, 250, 1000))
        board.append(Pole(36, "Szansa"))
        board.append(Posiadlosc(37, "sala 0004", 3500, 350, 1750, 2000))
        board.append(Pole(38, "Podatek dochodowy"))
        board.append(Posiadlosc(39, "sala 0089", 4000, 500, 2000, 2000))

        return board

    def przygotuj_graczy(self):
        self.messages.append(f"Liczba graczy: {self._liczba_graczy}")
        for i in range(1, self._liczba_graczy + 1):
            pionek = Pionek(0, PIECE_COLORS[i - 1], "path")
            gracz = Gracz(i, self._kwota_poczatkowa, pionek)
            gracz.pozycja = 0
            self.gracze.append(gracz)
            color = PIECE_COLORS[i - 1]
            self.messages.append(
                f"Gracz {i} gotowy z pionkiem w kolorze {color.r}, {color.g}, {color.b}"
            )

    def wybierzKolejnegoGracza(self):
        self._suma_oczek = 0
        poczatkowy_gracz = self._aktualny_gracz

        while True:
            if not self.gracze[self._aktualny_gracz - 1].uwiezienie:
                break
            else:
                self.gracze[self._aktualny_gracz - 1].odczekajJednaTure()
                self._aktualny_gracz = (self._aktualny_gracz % self._liczba_graczy) + 1
                self._suma_oczek = 0
                if self._aktualny_gracz == poczatkowy_gracz:
                    self.messages.append(
                        "Wszyscy gracze są w więzieniu. Przechodzimy do następnej tury."
                    )
                    break

    def analizujRzut(self, kostka_pierwsza, kostka_druga):
        if kostka_pierwsza + kostka_druga == 7:
            self._kolejny_rzut_kostka = True
            self.messages.append("Siódemka, rzuć jeszcze raz")
        else:
            self._kolejny_rzut_kostka = False

        if self._suma_oczek == 21:
            self.messages.append("Idziesz do więzienia")
            self.gracze[self._aktualny_gracz - 1].pozycja = 10
            self.gracze[self._aktualny_gracz - 1].uwiezienie = True
            self._kolejny_rzut_kostka = False

    def przesun_gracza(self, gracz, ruch):
        stara_pozycja = gracz.pionek.numer_pola
        nowa_pozycja = (stara_pozycja + ruch) % LICZBA_POL
        # gracz.pozycja = nowa_pozycja
        gracz.pionek.numer_pola = nowa_pozycja
        gracz.pionek.przesun(ruch)
        gracz.czy_przeszedl_przez_start(self, stara_pozycja)

        self.messages.append(
            f"Gracz {gracz.id} przesunął się z pozycji {stara_pozycja} na {nowa_pozycja}"
        )

        pole = self.board[nowa_pozycja]
        self.wykonaj_akcje_na_polu(gracz, pole)

    def stworz_przycisk(self, text, x, y, w, h, color, hover_color, screen, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(screen, hover_color, (x, y, w, h))
            if click[0] == 1 and action is not None:
                return action
        else:
            pygame.draw.rect(screen, color, (x, y, w, h))

        font = pygame.font.Font(None, 36)
        text_surface = font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=((x + (w / 2)), (y + (h / 2))))
        screen.blit(text_surface, text_rect)

        return None

    def pobierz_info_tak_nie(self, text):
        clock = pygame.time.Clock()
        res = (720,720) 
        screen = pygame.display.set_mode(res) 
        color_true = (0, 255, 0) #zielony
        color_false = (255, 0, 0) #czerwony
        button_color = (170,170,170) #szary

        window_size = (300, 200)
        pygame.display.set_caption('Wybierz opcję')

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            screen.fill((255, 255, 255))

            font = pygame.font.Font(None, 36)
            text_surface = font.render(text, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(window_size[0], 30))
            screen.blit(text_surface, text_rect)

            true_action = self.stworz_przycisk("Tak", 50, 70, 80, 50, button_color, color_true, screen, "True")
            false_action = self.stworz_przycisk("Nie", 170, 70, 80, 50, button_color, color_false, screen, "False")

            if true_action:
                return True
            if false_action:
                return False

            pygame.display.flip()
            pygame.display.update()
            clock.tick(30)
            pygame.display.set_mode((1200, 800), pygame.RESIZABLE)


    
    def wykonaj_akcje_na_polu(self, gracz, pole):
        self.messages.append(pole.wyswietl_info())
        if pole.typ == "wiezienie":
            self.messages.append("Gracz idzie do więzienia")
            gracz.uwiezienie = True

        elif pole.typ == "idz_do_wiezienia":
            self.messages.append("Gracz musi iść na pole 30 (więzienie)")
            # gracz.pozycja = 30
            gracz.uwiezienie = True
            #  pole = self.board[30],
        
        elif "Posiadlosc" == pole.typ:
            if isinstance(pole, Posiadlosc):
               posiadlosc = pole
            if posiadlosc.IDwlasciciela is None:
                if self.pobierz_info_tak_nie(f"Czy chcesz kupić miejsce {posiadlosc.nazwa}?"):
                    posiadlosc.kup_posiadlosc(self, gracz)
            elif posiadlosc.IDwlasciciela == gracz.id:
                if self.pobierz_info_tak_nie(f"Czy chcesz kupić dom na {posiadlosc.nazwa}?"):
                    posiadlosc.kup_dom(self, gracz)

            #czynsz - posiadlosc nalezy do innego gracza
            #else:


    def tura(self):
        if not self._kolejny_rzut_kostka:
            self.wybierzKolejnegoGracza()

        if not self.gracze[self._aktualny_gracz - 1].uwiezienie:
            self.messages.append(f"Ruch gracza: {self._aktualny_gracz}")

            kostka_pierwsza = random.randint(1, 6)
            kostka_druga = random.randint(1, 6)
            self._suma_oczek += kostka_pierwsza + kostka_druga

            self.messages.append(
                f"Kostka pierwsza: {kostka_pierwsza}, Kostka druga: {kostka_druga}"
            )
            self.messages.append(f"Suma: {self._suma_oczek}")

            self.analizujRzut(kostka_pierwsza, kostka_druga)
            self.przesun_gracza(
                self.gracze[self._aktualny_gracz - 1], kostka_pierwsza + kostka_druga
            )
        else:
            self.messages.append(f"Gracz {self._aktualny_gracz} jest width więzieniu.")

        if not self._kolejny_rzut_kostka:
            self._aktualny_gracz = (self._aktualny_gracz % self._liczba_graczy) + 1

    def get_messages(self):
        messages = self.messages.copy()
        self.messages.clear()
        return messages
