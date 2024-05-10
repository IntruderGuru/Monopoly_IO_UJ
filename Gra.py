import pygame
import os
from PIL import Image

KWOTA_POCZATKOWA = 10000

class Gra:

    def __init__(self):
        self.gracze = []        
        self.kwotaPoczatkowa = KWOTA_POCZATKOWA
        self.liczbaGraczy = 0

    def przygotujGraczy(self):
        #how many players input
        self.liczbaGraczy = 4

        # for i in range(1, self.liczbaGraczy + 1):
        #     gracz = Gracz(i, self.kwotaPoczatkowa)
        #     self.gracze.append(gracz)




#main loop module
pygame.init() 

os.environ['SDL_VIDEO_CENTERED']  = '1'
info = pygame.display.Info() #pobieram info o rozmiarze ekarnu

WIDTH = info.current_w
HEIGHT = info.current_h
BOARD = pygame.image.load("board.png")
image = Image.open("board.png")
BOARD_HEIGHT, BOARD_WIDTH = image.size
offset = 10
boardOffset = (HEIGHT - BOARD_HEIGHT) / 2

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Monopoly")


def maluj():
    screen.blit(BOARD, (boardOffset, boardOffset))
    pygame.display.update()


gra = Gra()
gra.przygotujGraczy()
backgroundColor = (255, 255, 255)

running = True
while running:
    #check if user wants to quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

    screen.fill(backgroundColor)        
    maluj()


pygame.quit()