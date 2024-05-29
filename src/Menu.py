import pygame
from src.Przycisk import Przycisk
from src.PrzyciskiMenu import PrzyciskiMenu

class Menu:
    def __init__(self):
        self.stan = "witaj"
        self.liczba_graczy = 0
        self.gracze = []
        self.font = pygame.font.Font(None, 32)

        self.H = 800
        self.W = 1200

        self.przyciski = PrzyciskiMenu(self.H, self. W)

        self.logo = pygame.transform.scale(
            pygame.image.load("graphics/logo.png"), (0.5 * self.W, 0.5 * self.H)
        )

        self.skalar_czcionki = 22  # im wiekszy tym mniejsza czcionka
        self.font = pygame.font.Font(None, int(self.W / self.skalar_czcionki))


    def handle_event(self, event):

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

                self.stan = "nazwy_graczy"
                self.gracze.append("")

            elif self.stan == "nazwy_graczy":
                if event.key == pygame.K_RETURN:
                    if len(self.gracze) < self.liczba_graczy:
                        self.gracze.append("")
                    else:
                        self.stan = "stop"
                elif event.key == pygame.K_BACKSPACE:
                    self.gracze[-1] = self.gracze[-1][:-1]
                else:
                    self.gracze[-1] += event.unicode

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()

            
    def draw(self, screen):

        self.font = pygame.font.Font(None, int(self.W / self.skalar_czcionki))

        if self.stan == "witaj":
            self.przyciski.nowa_gra.draw(screen)
            self.przyciski.wczytaj_gre.draw(screen)
            self.przyciski.wyjscie.draw(screen)

            self.logo = pygame.transform.scale(
                self.logo, (0.5 * self.W, 0.3 * self.H)
            )
            screen.blit(self.logo, (self.W * 0.25, self.H * 0.05))

        elif self.stan == "liczba_graczy":
            text = self.font.render("Wprowadź liczbę graczy", True, (0, 0, 0))
            self.przyciski.two.draw(screen)
            self.przyciski.three.draw(screen)
            self.przyciski.four.draw(screen)
            self.przyciski.five.draw(screen)

            text = self.font.render(
                "Wybierz liczbę graczy",
                True,
                (0, 0, 0),
            )

            screen.blit(text, (self.W * 0.32, self.H * 0.35))

        elif self.stan == "nazwy_graczy":
            text = self.font.render(
                "Wprowadź nazwę gracza " + str(len(self.gracze)),
                True,
                (0, 0, 0),
            )

