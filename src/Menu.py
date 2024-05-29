import pygame
from src.Przycisk import Przycisk

class Menu:
    def __init__(self):
        self.stan = "witaj"
        self.liczba_graczy = 0
        self.gracze = []
        self.font = pygame.font.Font(None, 32)

        self.H = 800
        self.W = 1200

        self.nowa_gra = Przycisk(
            self.W * 0.35,
            self.H * 0.4,
            self.W * 0.3,
            self.H * 0.1,
            (70,70,70),
            (150,150,150),
            "Nowa gra",
            (200,200,200),
        )

        self.wczytaj_gre = Przycisk(
            self.W * 0.35,
            self.H * 0.52,
            self.W * 0.3,
            self.H * 0.1,
            (70,70,70),
            (150,150,150),
            "Wczytaj zapis",
            (200,200,200),
        )

        self.wyjscie = Przycisk(
            self.W * 0.35,
            self.H * 0.64,
            self.W * 0.3,
            self.H * 0.1,
            (70,70,70),
            (150,150,150),
            "Wyjscie",
            (200,200,200),
        )

        self.logo = pygame.transform.scale(
            pygame.image.load("graphics/logo.png"), (0.5 * self.W, 0.5 * self.H)
        )


    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:

            if self.stan == "witaj":
                if self.nowa_gra.is_clicked(event):
                    self.stan == "liczba_graczy"
                elif self.wyjscie.is_clicked(event):
                    pygame.quit()
                    
            elif self.stan == "liczba_graczy":
                if pygame.K_2 <= event.key <= pygame.K_5:
                    self.liczba_graczy = event.key - pygame.K_0
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

    def draw(self, screen):

        if self.stan == "witaj":
            self.nowa_gra.draw(screen)
            self.wczytaj_gre.draw(screen)
            self.wyjscie.draw(screen)

            self.logo = pygame.transform.scale(
                self.logo, (0.5 * self.W, 0.3 * self.H)
            )
            screen.blit(self.logo, (self.W * 0.25, self.H * 0.05))

        elif self.stan == "liczba_graczy":
            text = self.font.render("Wprowadź liczbę graczy", True, (0, 0, 0))
        elif self.stan == "nazwy_graczy":
            text = self.font.render(
                "Wprowadź nazwę gracza " + str(len(self.gracze)),
                True,
                (0, 0, 0),
            )

