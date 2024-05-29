import os
import pygame
from src.Gra import Gra
from src.KontrolerWiadomosci import KontrolerWiadomosci
from src.Menu import Menu


class Main:
    _SEC_TO_MS = 1000
    _background_color = pygame.color.THECOLORS["white"]

    def __init__(self):
        pygame.init()  # Inicjalizacja pygame
        pygame.font.init()  # Inicjalizacja modułu fontów

        os.environ["SDL_VIDEO_CENTERED"] = "1"

        self.font = pygame.font.Font(None, 20)

        pygame.display.set_caption("Monopoly")
        self._screen = pygame.display.set_mode((1200, 800), pygame.RESIZABLE)

        self._screen_info = pygame.display.Info()
        self._screen_width = self._screen_info.current_w
        self._screen_height = self._screen_info.current_h

        self._kontroler_wiadomosci = KontrolerWiadomosci(self.font)
        self._gra = None  # Gra(self._screen, self._kontroler_wiadomosci)
        self._clock = pygame.time.Clock()
        self._running = True
        self._delta_time = 0
        self.input_text = ""
        # self.messages = []
        self.menu = Menu()

    def __del__(self):
        pygame.quit()
        # del self._gra

    def start(self):
        self._kontroler_wiadomosci.dodaj_wiadomosc("Witaj w UJpoly!")
        while self.menu.stan != "stop":
            
            self.menu.aktualizuj_rozmiar_okna(self._screen_width, self._screen_height)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                self.menu.handle_event(event)

            self._screen.fill((255, 255, 255))
            if self.menu.stan != "stop":
                self.menu.draw(self._screen)
            else:
                self._kontroler_wiadomosci.dodaj_wiadomosc(
                    "Wprowadź liczbę graczy między (2-5) :"
                )
                self._gra = Gra(
                    self._screen,
                    self._kontroler_wiadomosci,
                    self.menu.liczba_graczy,
                    self.menu.gracze,
                )
                self._petla_gry()

            pygame.display.flip()

    def _petla_gry(self):
        while self._running:
            self._aktualizuj_delta_time()
            self._petla_zdarzen(pygame.event.get())
            self._aktualizuj(delta_time=self._delta_time)
            self._wyswietlaj()

    def _aktualizuj_delta_time(self):
        self._clock.tick(60)
        self._delta_time = self._clock.get_time() / Main._SEC_TO_MS

    def _petla_zdarzen(self, events_list):
        for event in events_list:
            if event.type == pygame.QUIT:
                self._running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.process_input(self.input_text)
                    self.input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                else:
                    self.input_text += event.unicode
            elif event.type == pygame.VIDEORESIZE:
                self._screen_width = event.w
                self._screen_height = event.h
                self._gra.aktualna_szerokosc_ekranu = self._screen_width
                self._gra.aktualna_wysokosc_ekranu = self._screen_height

            self._gra.aktualizacja_zdarzenia(event)

    def _aktualizuj(self, delta_time):
        _delta_time = delta_time
        self._gra.aktualizacja()

    def render_text(self, text, pos):
        text_surface = self.font.render(text, True, (0, 0, 0))
        self._screen.blit(text_surface, pos)

    def _wyswietlaj(self):
        self._screen.fill(Main._background_color)

        # Wyświetlanie komunikatów z prawej strony
        # y_offset = 10
        # for message in self.messages[-15:]:  # Wyświetla ostatnie 15 komunikatów
        #     self.render_text(message, (self._screen_width - 400, y_offset))
        #     y_offset += 40

        self._kontroler_wiadomosci.wyswietl(self._screen, self._screen_width)

        # Wyświetlanie pola tekstowego
        self.render_text(
            self.input_text, (self._screen_width - 400, self._screen_height - 50)
        )

        self._gra.wyswietl()

        pygame.display.update()

    def process_input(self, input_text):
        self._kontroler_wiadomosci.dodaj_wiadomosc(f"Wprowadzono: {input_text}")
        if input_text.isdigit():
            liczba_graczy = int(input_text)
            if liczba_graczy >= 2 and liczba_graczy <= 5:
                self._gra._liczba_graczy = liczba_graczy
                self._kontroler_wiadomosci.dodaj_wiadomosc(
                    f"Ustaw liczbe graczy na {liczba_graczy}"
                )
                self._gra.przygotuj_graczy()
                self._kontroler_wiadomosci.dodaj_wiadomosc(
                    "Naciśnij spację, aby rzucić kostką"
                )
            else:
                self._kontroler_wiadomosci.dodaj_wiadomosc(
                    "Nieprawidłowa liczba graczy."
                )
        else:
            self._kontroler_wiadomosci.dodaj_wiadomosc(
                f"Nieznana komenda: {input_text}"
            )


if __name__ == "__main__":
    game_runner = Main()
    game_runner.start()
