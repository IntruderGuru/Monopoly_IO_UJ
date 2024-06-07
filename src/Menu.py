import pygame
from src.Przycisk import Przycisk
from src.PrzyciskiMenu import PrzyciskiMenu
from src.Wizualizator import Wizualizator


class Menu:
    def __init__(self, wizualizator):
        self.stan = "witaj"
        self.liczba_graczy = 0
        self.gracze = []
        self.wizualizator: Wizualizator = wizualizator
        self.font = pygame.font.Font(self.wizualizator.czcionka, 32)
        self.H = 660
        # self.H = 800
        self.W = 1200

        self.przyciski = PrzyciskiMenu(self.H, self.W, self.wizualizator)

        self.logo = pygame.transform.scale(
            pygame.image.load("graphics/logo.png"), (0.5 * self.W, 0.5 * self.H)
        )

        self.strona1 = pygame.transform.scale(
            pygame.image.load("graphics/tutorial/strona1.png"), (0.5 * self.W, 0.5 * self.H)
        )

        self.skalar_czcionki = 22  # im wiekszy tym mniejsza czcionka
        self.font = pygame.font.Font(self.wizualizator.czcionka, int(self.W / self.skalar_czcionki))
        self.font_gracze = pygame.font.Font(self.wizualizator.czcionka, int(self.W / (self.skalar_czcionki + 5)))

    def handle_event(self, event, W, H):

        self.W = W
        self.H = H
        self.przyciski.aktualizuj_rozmiar(self.W, self.H)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.stan == "witaj":
                if self.przyciski.nowa_gra.is_clicked(event):
                    self.stan = "liczba_graczy"
                elif self.przyciski.wyjscie.is_clicked(event):
                    pygame.quit()

            elif self.stan == "liczba_graczy":
                if self.przyciski.two.is_clicked(event):
                    self.liczba_graczy = 2
                elif self.przyciski.three.is_clicked(event):
                    self.liczba_graczy = 3
                elif self.przyciski.four.is_clicked(event):
                    self.liczba_graczy = 4
                elif self.przyciski.five.is_clicked(event):
                    self.liczba_graczy = 5

                if self.liczba_graczy > 1:
                    self.stan = "nazwy_graczy"
                    self.gracze.append("")
            elif self.stan == "tutorial1":
                if self.przyciski.graj.is_clicked(event):
                    self.stan = "stop"
                elif self.przyciski.nastepny.is_clicked(event):
                    self.stan = "tutorial2"

        elif event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_ESCAPE:
                pygame.quit()

            if self.stan == "nazwy_graczy":
                if event.key == pygame.K_RETURN:
                    if len(self.gracze) < self.liczba_graczy:
                        self.gracze.append("")
                    else:
                        self.stan = "tutorial1"
                elif event.key == pygame.K_BACKSPACE:
                    self.gracze[-1] = self.gracze[-1][:-1]
                else:
                    if event.key == pygame.K_SPACE:
                        if len(self.gracze[-1]) != 0 and self.gracze[-1][-1] != " ":
                            self.gracze[-1] += event.unicode
                    else:
                        self.gracze[-1] += event.unicode

    def draw(self, screen, W, H):

        self.font = pygame.font.Font(self.wizualizator.czcionka, int(W / self.skalar_czcionki))
        self.font_gracze = pygame.font.Font(self.wizualizator.czcionka, int(self.W / (self.skalar_czcionki + 5)))

        if self.stan == "witaj":
            self.logo = pygame.transform.scale(self.logo, (0.5 * W, 0.45 * H))
            screen.blit(self.logo, (W * 0.25, H * 0.05))

            self.przyciski.nowa_gra.draw(screen)
            self.przyciski.wczytaj_gre.draw(screen)
            self.przyciski.wyjscie.draw(screen)

        elif self.stan == "tutorial1":
            screen.fill(self.wizualizator.kolor_tla)
            self.przyciski.graj.draw(screen)
            self.przyciski.poprzedni_szary.draw(screen)
            self.przyciski.nastepny.draw(screen)
            self.strona1 = pygame.transform.scale(self.strona1, (0.5 * W, 0.45 * H))
            screen.blit(self.strona1, (W * 0.25, H * 0.05))
        
            

        elif self.stan == "liczba_graczy":
            self.przyciski.two.draw(screen)
            self.przyciski.three.draw(screen)
            self.przyciski.four.draw(screen)
            self.przyciski.five.draw(screen)

            text = self.font.render(
                "Wybierz liczbę graczy",
                True,
                self.wizualizator.kolor_czcionki,
            )

            screen.blit(text, (W * 0.32, H * 0.35))

        elif self.stan == "nazwy_graczy":
            text = self.font.render(
                "Wprowadź nazwę gracza: " + str(len(self.gracze)),
                True,
                self.wizualizator.kolor_czcionki
            )
            screen.blit(text, (W * 0.3, H * 0.35))
            
            odstep = 0.05
            ile_wpisanych = len(self.gracze)

            for i in range(0, len(self.gracze)):

                if i < ile_wpisanych - 1:
                    kolor_czcionki = self.wizualizator.kolor_akceptacji_nazwy_gracza
                else:
                    kolor_czcionki = self.wizualizator.kolor_czcionki

                gracz = self.font_gracze.render(
                    str(self.gracze[i]),
                    True,
                    kolor_czcionki
                )
                screen.blit(gracz, (W * 0.45, H * (0.45 + (i * odstep))))
            
