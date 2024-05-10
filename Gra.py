import pygame
import os
import random
from PIL import Image
from Gracz import Gracz

KWOTA_POCZATKOWA = 10000
MIN_LICZBA_GRACZY = 2
MAX_LICZBA_GRACZY = 5

class Gra:

    def __init__(self):
        self.gracze = []        
        self.kwotaPoczatkowa = KWOTA_POCZATKOWA
        self.liczbaGraczy = 0

    def przygotujGraczy(self):

        while True:
            self.liczbaGraczy = int(input("Podaj liczbe graczy: "))
            if self.liczbaGraczy >= MIN_LICZBA_GRACZY and self.liczbaGraczy <= MAX_LICZBA_GRACZY:
                break
            else:
                print("niepoprawna ilosc graczy")

        self.aktualnyGracz = random.randint(1, self.liczbaGraczy)

        #dodawanie graczy (wymaga implementacji klasy Gracz)
        for i in range(1 , self.liczbaGraczy + 1):
            gracz = Gracz(i, self.kwotaPoczatkowa)
            self.gracze.append(gracz)
    

    def tura(self):

        #wybieranie nastepnego gracza w kolejce
        #warning! zapetli sie gdy kazdy gracz bedzie uwieziony (trzeba wymyslic co wtedy robimy i czy bedzie taka sutuacja)
        while True:
            if not self.gracze[self.aktualnyGracz - 1].uwiezienie:
                break
            else:
                print("here")
                self.gracze[self.aktualnyGracz - 1].liczbaPostojow -= 1
                self.aktualnyGracz = (self.aktualnyGracz + 1) % self.liczbaGraczy

        print("ruch gracza:", self.aktualnyGracz)

        sumaOczek = 0
        for i in range(3):
            kostkaPierwsza = random.randint(1, 6)
            kostkaDruga = random.randint(1, 6)
            sumaOczek += (kostkaPierwsza + kostkaDruga)

            print("kostka pierwsza:", kostkaPierwsza, ", kostka druga:", kostkaDruga)
            print("suma:", sumaOczek)

            if(kostkaPierwsza + kostkaDruga == 7):
                input("siodemka, rzuc jeszcze raz, (wpisz cokolwiek):")
            else:
                input("nastepny gracz, (wpisz cokolwiek):")

            print()

            if kostkaPierwsza + kostkaDruga != 7:
                break
            elif kostkaPierwsza + kostkaDruga == 7 and i == 3: #koniec tury, gracz idzie do wiezienia
                print("idziesz do wiezienia")
                self.gracze[self.aktualnyGracz - 1].uwiezienie = True
                return


        #zapetlenie ggraczy
        self.aktualnyGracz += 1
        if self.aktualnyGracz == self.liczbaGraczy + 1:
            self.aktualnyGracz = 1




#MAIN GAME MODULE
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


backgroundColor = (255, 255, 255)
gra = Gra()
gra.przygotujGraczy()

running = True
while running:
    #check if user wants to quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

    screen.fill(backgroundColor)        
    maluj()
    gra.tura()


pygame.quit()