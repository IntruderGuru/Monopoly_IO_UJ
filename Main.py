import os
import pygame
from src.Gra import Gra
from src.KontrolerWiadomosci import KontrolerWiadomosci
from src.Wizualizator import Wizualizator
from src.Menu import Menu


class Main:
    _SEC_TO_MS = 1000
    LIMIT_CZASU_GRY = 3600
    LIMIT_CZASU_TURY = 5

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
        self._delta_time = 0
        self.input_text = ""
        self.wizualizator = Wizualizator()
        self.menu = Menu(self.wizualizator)
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
            else:
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

            pygame.display.flip()

    def _petla_gry(self):
        self.turn_start_time = (
            pygame.time.get_ticks()
        )  # Zresetowanie czasu startu tury na początku gry
        while self._running:
            self._aktualizuj_delta_time()
            self._aktualizuj_czas_gry()  # Wywołanie funkcji aktualizującej czas gry
            self._petla_zdarzen(pygame.event.get())
            self._aktualizuj(delta_time=self._delta_time)
            self._wyswietlaj()

    def _aktualizuj_delta_time(self):
        self._clock.tick(60)
        self._delta_time = self._clock.get_time() / Main._SEC_TO_MS

    def _aktualizuj_czas_gry(self):
        self.uplyniety_czas_gry += self._delta_time
        self.uplyniety_czas_tury = (
            pygame.time.get_ticks() - self.turn_start_time
        ) / Main._SEC_TO_MS

        if self.uplyniety_czas_gry >= Main.LIMIT_CZASU_GRY:
            self._running = False
            self._kontroler_wiadomosci.dodaj_wiadomosc("Czas gry minął! Koniec gry.")

        if self.uplyniety_czas_tury >= Main.LIMIT_CZASU_TURY:
            self._kontroler_wiadomosci.dodaj_wiadomosc(
                "Czas tury minął! Przechodzimy do następnego gracza."
            )
            self._gra.zamknij_wszystkie_okna()
            pygame.time.wait(2000)
            self._gra.tura()
            self.turn_start_time = pygame.time.get_ticks()

    def _petla_zdarzen(self, events_list):
        for event in events_list:
            if event.type == pygame.QUIT:
                self._running = False
                break
            elif event.type == pygame.VIDEORESIZE:
                self._screen_width = event.w
                self._screen_height = event.h

            self._gra.aktualizacja_zdarzenia(event)

    def _aktualizuj(self, delta_time):
        pass  # Aktualizacja gry, jeśli jest taka potrzeba

    def render_text(self, text, pos):
        text_surface = self.font.render(text, True, self.wizualizator.kolor_czcionki)
        self._screen.blit(text_surface, pos)

    def _wyswietlaj(self):
        self._screen.fill(self.wizualizator.kolor_tla)
        self._gra.wyswietl(self._screen, self._screen_width, self._screen_height)
        pygame.display.update()


if __name__ == "__main__":
    game_runner = Main()
    game_runner.start()
