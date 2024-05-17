import os
import pygame

from PIL import Image
from src.Gra import Gra
from src.Pionek import Pionek


class Main:
    _SEC_TO_MS = 1000
    _background_color = pygame.color.THECOLORS["white"]

    def __init__(self):
        self._gra = Gra()
        self._running = True
        self._delta_time = 0
        self._clock = pygame.time.Clock()
        self.pionek = Pionek(0, pygame.color.THECOLORS["black"], "path")

        pygame.init()
        os.environ['SDL_VIDEO_CENTERED'] = '1'

        self._screen_info = pygame.display.Info()
        self._screen_width = self._screen_info.current_w
        self._screen_height = self._screen_info.current_h

        self._board_png = pygame.image.load("graphics/board.png")
        board_img = Image.open("graphics/board.png")

        self._board_height, self._board_width = board_img.size
        self._boardOffset = (self._screen_height - self._board_height) / 2

        self._screen = pygame.display.set_mode((self._screen_width, self._screen_height), pygame.RESIZABLE)

        pygame.display.set_caption("Monopoly")

    def __del__(self):
        pygame.quit()
        del self._gra

    def _wyswietlaj(self):
        self._screen.blit(self._board_png, (self._boardOffset, self._boardOffset))
        self.pionek.wyswietlaj(self._screen)
        pygame.display.update()

    def _petla_zdarzen(self, events_list):
        for event in events_list:
            if event.type == pygame.QUIT:
                self._running = False
                break
            elif event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_SPACE:
                        self._gra.tura()

                    case pygame.K_ESCAPE:
                        self._running = False

                    # Test ruchu pionka
                    case pygame.K_LEFT:
                        self.pionek.przesun(1)

    def _aktualizuj(self, delta_time):
        # trick do IDE, aby unikna warningu o nieuzyciu zmiennej
        _delta_time = delta_time
        self._screen.fill(Main._background_color)

    # zwraca roznice czasu pomiedzy tyknieciami zegara gry w sekundach(float) wychodzi ulamek
    def _aktualizuj_delta_time(self):
        self._clock.tick(60)
        self._delta_time = self._clock.get_time() / Main._SEC_TO_MS

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
