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
        self.sumaOczek = 0
        self.kolejnyRzutKostka = False

    

    def przygotujGraczy(self):

        while True:
            self.liczbaGraczy = int(input("Podaj liczbe graczy: "))
            if self.liczbaGraczy >= MIN_LICZBA_GRACZY and self.liczbaGraczy <= MAX_LICZBA_GRACZY:
                break
            else:
                print("niepoprawna ilosc graczy")

        self.aktualnyGracz = random.randint(1, self.liczbaGraczy)

        for i in range(1 , self.liczbaGraczy + 1):
            gracz = Gracz(i, self.kwotaPoczatkowa)
            self.gracze.append(gracz)


    def wybierzKolejnegoGracza(self):
        self.sumaOczek = 0
        while True:
            if not self.gracze[self.aktualnyGracz - 1].uwiezienie:
                break
            else:
                self.gracze[self.aktualnyGracz - 1].odczekajJednaTure()
                self.aktualnyGracz = (self.aktualnyGracz + 1) % self.liczbaGraczy
                self.sumaOczek = 0


    def analizujRzut(self, kostkaPierwsza, kostkaDruga):

        if(kostkaPierwsza + kostkaDruga == 7):
            self.kolejnyRzutKostka = True
            print("siodemka, rzuc jeszcze raz")
        else:
            self.kolejnyRzutKostka = False
            print("nastepny gracz")

        print()

        #koniec tury, gracz idzie do wiezienia
        if self.sumaOczek == 21:
            print("idziesz do wiezienia")
            self.gracze[self.aktualnyGracz - 1].uwiezienie = True
            self.kolejnyRzutKostka = False
            return



    def tura(self):

        #wybieranie nastepnego gracza w kolejce 
        if not self.kolejnyRzutKostka:
            self.wybierzKolejnegoGracza()
        
        print("ruch gracza:", self.aktualnyGracz)

        kostkaPierwsza = random.randint(1, 6)
        kostkaDruga = random.randint(1, 6)
        self.sumaOczek += (kostkaPierwsza + kostkaDruga)

        print("kostka pierwsza:", kostkaPierwsza, ", kostka druga:", kostkaDruga)
        print("suma:", self.sumaOczek)
        
        self.analizujRzut(kostkaPierwsza, kostkaDruga)

        #zapetlenie graczy
        if not self.kolejnyRzutKostka:
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


def wyswietlaj():
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
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                gra.tura()


    screen.fill(backgroundColor)        
    wyswietlaj()


pygame.quit()