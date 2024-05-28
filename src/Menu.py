import pygame


class Menu:
    def __init__(self):
        self.stan = "liczba_graczy"
        self.liczba_graczy = 0
        self.gracze = []
        self.font = pygame.font.Font(None, 32)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.stan == "liczba_graczy":
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
        if self.stan == "liczba_graczy":
            text = self.font.render("Wprowadź liczbę graczy", True, (0, 0, 0))
        elif self.stan == "nazwy_graczy":
            text = self.font.render(
                "Wprowadź nazwę gracza " + str(len(self.gracze)),
                True,
                (0, 0, 0),
            )
        screen.blit(text, (50, 50))
