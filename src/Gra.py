import pygame
import os
import random
from PIL import Image
from Gracz import Gracz


KWOTA_POCZATKOWA = 10000
MIN_LICZBA_GRACZY = 2
MAX_LICZBA_GRACZY = 5


class Gra:
    def __init__(self):
        self.gracze = []        
        self.kwotaPoczatkowa = KWOTA_POCZATKOWA
        self.liczbaGraczy = 0
        self.sumaOczek = 0
        self.kolejnyRzutKostka = False

    def przygotuj_graczy(self):
        while True:
            self.liczbaGraczy = int(input("Podaj liczbe graczy: "))
            if self.liczbaGraczy >= MIN_LICZBA_GRACZY and self.liczbaGraczy <= MAX_LICZBA_GRACZY:
                break
            else:
                print("niepoprawna ilosc graczy")

        self.aktualnyGracz = random.randint(1, self.liczbaGraczy)

        for i in range(1, self.liczbaGraczy + 1):
            gracz = Gracz(i, self.kwotaPoczatkowa)
            self.gracze.append(gracz)


    def wybierzKolejnegoGracza(self):
        self.sumaOczek = 0
        while True:
            if not self.gracze[self.aktualnyGracz - 1].uwiezienie:
                break
            else:
                self.gracze[self.aktualnyGracz - 1].odczekajJednaTure()
                self.aktualnyGracz = (self.aktualnyGracz + 1) % self.liczbaGraczy
                self.sumaOczek = 0


    def analizujRzut(self, kostkaPierwsza, kostkaDruga):

        if(kostkaPierwsza + kostkaDruga == 7):
            self.kolejnyRzutKostka = True
            print("siodemka, rzuc jeszcze raz")
        else:
            self.kolejnyRzutKostka = False
            print("nastepny gracz")

        print()

        #koniec tury, gracz idzie do wiezienia
        if self.sumaOczek == 21:
            print("idziesz do wiezienia")
            self.gracze[self.aktualnyGracz - 1].uwiezienie = True
            self.kolejnyRzutKostka = False
            return



    def tura(self):

        #wybieranie nastepnego gracza w kolejce 
        if not self.kolejnyRzutKostka:
            self.wybierzKolejnegoGracza()
        
        print("ruch gracza:", self.aktualnyGracz)

        kostkaPierwsza = random.randint(1, 6)
        kostkaDruga = random.randint(1, 6)
        self.sumaOczek += (kostkaPierwsza + kostkaDruga)

        print("kostka pierwsza:", kostkaPierwsza, ", kostka druga:", kostkaDruga)
        print("suma:", self.sumaOczek)
        
        self.analizujRzut(kostkaPierwsza, kostkaDruga)

        #zapetlenie graczy
        if not self.kolejnyRzutKostka:
            self.aktualnyGracz += 1
            if self.aktualnyGracz == self.liczbaGraczy + 1:
                self.aktualnyGracz = 1


class Main:
    _SEC_TO_MS = 1000
    _background_color = pygame.color.THECOLORS["white"]
    _gra = Gra()

    def __init__(self):
        self._running = True
        self._delta_time = 0
        self._clock = pygame.time.Clock()

        pygame.init()
        os.environ['SDL_VIDEO_CENTERED'] = '1'

        self._screen_info = pygame.display.Info()
        self._screen_width = self._screen_info.current_w
        self._screen_height = self._screen_info.current_h

        self._board_png = pygame.image.load("../graphics/board.png")
        board_img = Image.open("../graphics/board.png")

        self._board_height, self._board_width = board_img.size
        self._boardOffset = (self._screen_height - self._board_height) / 2

        self._screen = pygame.display.set_mode((self._screen_width, self._screen_height), pygame.RESIZABLE)

        pygame.display.set_caption("Monopoly")

    def __del__(self):
        pygame.quit()
        del self._gra

    def _wyswietlaj(self):
        self._screen.blit(self._board_png, (self._boardOffset, self._boardOffset))
        pygame.display.update()

    def _petla_zdarzen(self, events_list):
        for event in events_list:
            if event.type == pygame.QUIT:
                self._running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self._gra.tura()


    def _aktualizuj(self, delta_time):
        # trick do IDE, aby unikna warningu o nieuzyciu zmiennej
        _delta_time = delta_time
        self._screen.fill(self._background_color)

    # zwraca roznice czasu pomiedzy tyknieciami zegara gry w sekundach(float) wychodzi ulamek
    def _aktualizuj_delta_time(self):
        self._clock.tick(60)
        self._delta_time = self._clock.get_time() / self._SEC_TO_MS

    def _petla_gry(self):
        while self._running:
            self._aktualizuj_delta_time()
            self._petla_zdarzen(pygame.event.get())
            self._aktualizuj(delta_time=self._delta_time)
            self._wyswietlaj()

    def start(self):
        self._gra.przygotuj_graczy()
        self._petla_gry()


if __name__ == "__main__":
    game_runner = Main()
    game_runner.start()

#test git commit