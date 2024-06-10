import os
import pygame
import shutil
from src.Gra import Gra
from src.KontrolerWiadomosci import KontrolerWiadomosci
from src.Wizualizator import Wizualizator
from src.Menu import Menu


class Main:
    _SEC_TO_MS = 1000
    LIMIT_CZASU_GRY = 0
    LIMIT_CZASU_TURY = 0

    def __init__(self):
        pygame.init()  # Inicjalizacja pygame
        pygame.font.init()  # Inicjalizacja modułu fontów

        os.environ["SDL_VIDEO_CENTERED"] = "1"

        self.font = pygame.font.Font(None, 20)

        pygame.display.set_caption("Monopoly")
        self._screen = pygame.display.set_mode((1200, 660), pygame.RESIZABLE)

        self._screen_info = pygame.display.Info()
        self._screen_width = self._screen_info.current_w
        self._screen_height = self._screen_info.current_h

        self._gra = None
        self._clock = pygame.time.Clock()
        self._running = True
        self.wait_flag = 0
        self._delta_time = 0
        self.input_text = ""
        self.wizualizator = Wizualizator()
        self.menu = Menu(self.wizualizator, self)
        self._kontroler_wiadomosci = KontrolerWiadomosci(self.font, self.wizualizator)

        self.uplyniety_czas_gry = 0
        self.uplyniety_czas_tury = 0
        self.turn_start_time = (
            pygame.time.get_ticks()
        )  # Inicjalizacja czasu startu tury

    def __del__(self):
        pygame.quit()
        # del self._gra

    def start(self):
        self._kontroler_wiadomosci.dodaj_wiadomosc("Witaj w UJpoly!")
        while self.menu.stan != "stop":

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                elif event.type == pygame.VIDEORESIZE:
                    self._screen_width = event.w
                    self._screen_height = event.h
                self.menu.handle_event(event, self._screen_width, self._screen_height)

            self._screen.fill(self.wizualizator.kolor_tla)
            if self.menu.stan != "stop":
                self.menu.draw(self._screen, self._screen_width, self._screen_height)
            elif self.menu.typ_stopu == "nowa":
                self._gra = Gra(
                    self._screen,
                    self._kontroler_wiadomosci,
                    self.menu.liczba_graczy,
                    self.menu.gracze,
                    self.wizualizator,
                    self._screen_width,
                    self._screen_height,
                    self,
                )
                self._petla_gry()
            else:
                self._gra = Gra(
                    self._screen,
                    self._kontroler_wiadomosci,
                    0,
                    [],
                    self.wizualizator,
                    self._screen_width,
                    self._screen_height,
                    self,
                )
                self._gra.wczytaj_gre()
                self._petla_gry()

            if self._running is True:
                pygame.display.flip()

    def _petla_gry(self):
        while self._running:
            self._aktualizuj_delta_time()
            self.uplyniety_czas_gry += self._delta_time
            self._petla_zdarzen(pygame.event.get())
            if self.wait_flag == 1:
                self._aktualizuj_czas_gry()
            # self._petla_zdarzen(pygame.event.get())
            if self._running is False:
                return

            self._aktualizuj(delta_time=self._delta_time)
            self._wyswietlaj()

    def _aktualizuj_delta_time(self):
        self._clock.tick(60)
        self._delta_time = self._clock.get_time() / Main._SEC_TO_MS

    def _aktualizuj_czas_gry(self):
        self.uplyniety_czas_tury = (
            pygame.time.get_ticks() - self.turn_start_time
        ) / Main._SEC_TO_MS

        if self.LIMIT_CZASU_GRY != 999:
            if self.uplyniety_czas_gry >= self.LIMIT_CZASU_GRY:
                self._running = False
                self._kontroler_wiadomosci.dodaj_wiadomosc(
                    "Czas gry minął! Koniec gry."
                )

        if self.LIMIT_CZASU_TURY != 999:
            if self.uplyniety_czas_tury >= self.LIMIT_CZASU_TURY:
                self._kontroler_wiadomosci.dodaj_wiadomosc(
                    "Czas tury minął! Przechodzimy do następnego gracza."
                )
                self._gra.zamknij_wszystkie_okna()
                self._wyswietlaj()
                self.wait_flag = 0
                self.turn_start_time = pygame.time.get_ticks()

    def _petla_zdarzen(self, events_list):
        for event in events_list:
            if event.type == pygame.QUIT:
                self._running = False
                break
            elif (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_SPACE
                and self.wait_flag == 0
            ):
                self._waiting_for_space = False
                self.wait_flag = 1
            elif event.type == pygame.MOUSEBUTTONDOWN and self.wait_flag == 0:
                self.wait_flag = 1
            elif event.type == pygame.MOUSEBUTTONDOWN and self.wait_flag == 1:
                self.wait_flag = 0

            elif event.type == pygame.VIDEORESIZE:
                self._screen_width = event.w
                self._screen_height = event.h
            self._gra.aktualizacja_zdarzenia(event)

    def _aktualizuj(self, delta_time):
        self._gra.aktualizuj(delta_time)

    def render_text(self, text, pos):
        text_surface = self.font.render(text, True, self.wizualizator.kolor_czcionki)
        self._screen.blit(text_surface, pos)

    def _wyswietlaj(self):
        self._screen.fill(self.wizualizator.kolor_tla)
        self._gra.wyswietl(self._screen, self._screen_width, self._screen_height)
        pygame.display.update()


def reset_pionki():
    pionek_default_dir = "graphics/pionek_default"
    pionek_dir = "graphics/pionek"

    for filename in os.listdir(pionek_dir):
        file_path = os.path.join(pionek_dir, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

    for filename in os.listdir(pionek_default_dir):
        src_path = os.path.join(pionek_default_dir, filename)
        dst_path = os.path.join(pionek_dir, filename)
        shutil.copy(src_path, dst_path)


if __name__ == "__main__":
    reset_pionki()
    game_runner = Main()
    game_runner.start()
