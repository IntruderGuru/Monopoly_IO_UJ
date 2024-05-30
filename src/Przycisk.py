import pygame


class Przycisk:
    def __init__(self, x, y, width, height, color, hover_color, text, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color: pygame.Color = color
        self.hover_color: pygame.Color = hover_color
        self.text = text
        self.text_color = text_color
        self.font = pygame.font.Font(None, 36)

    def pobierz_wymiary(self) -> pygame.Rect:
        return self.rect

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        is_hover = self.rect.collidepoint(mouse_pos)
        color = self.hover_color if is_hover else self.color
        pygame.draw.rect(screen, color, self.rect)

        if self.text:
            text_surf = self.font.render(self.text, True, self.text_color)
            text_rect = text_surf.get_rect(center = self.rect.center)
            screen.blit(text_surf, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                return True
        return False

    def updateSize(self, x, y, width, height):
        if width <= 0 or height <= 0:
            return

        self.rect = pygame.Rect(x, y, width, height)