import pygame.color

from src.Pole import Pole
from src.Pionek import Pionek
from src.Posiadlosc import Posiadlosc
from src.KartaSzansy import *
from src.PodatekDochodowy import Zagadki
from src.PodatekDochodowy import PodatekDochodowy


class Plansza:
    @staticmethod
    def inicializacja_planszy() -> list[Pole]:
        board: list[Pole] = list()
        board.append(Pole(0, "Start"))
        board.append(Posiadlosc(1, "Automat z kawą", "brazowy", 600, 20, 300, 500))
        board.append(Pole(2, "Szansa"))
        board.append(Posiadlosc(3, 'Bistro "Świetlica"', "brazowy", 600, 40, 300, 500))
        board.append(PodatekDochodowy(4, 1000))
        board.append(Posiadlosc(5, "KNRSI", "kolo", 2000, 250, 1000))
        board.append(Posiadlosc(6, "Parking", "niebieski", 1000, 60, 500, 500))
        board.append(Pole(7, "Szansa"))
        board.append(Posiadlosc(8, "Winda", "niebieski", 1000, 60, 500, 500))
        board.append(Posiadlosc(9, "Szatnia", "niebieski", 1200, 80, 500, 500))
        board.append(Pole(10, "Wiezienie"))
        board.append(Posiadlosc(11, "Sala 1073 (sieci)", "rozowy", 1400, 100, 700, 1000))
        board.append(Posiadlosc(12, "Drążki za wydziałem", "pozaWmii", 1500, 0, 750))
        board.append(Posiadlosc(13, "Sala 0056 (laby)", "rozowy", 1400, 100, 700, 1000))
        board.append(Posiadlosc(14, "Sala 1072 (macbooki)", "rozowy", 1600, 120, 800, 1000))
        board.append(Posiadlosc(15, "KNMF", "kolo", 2000, 250, 1000))
        board.append(Posiadlosc(16, "Ślimak", "pomaranczowy", 1800, 140, 900, 1000))
        board.append(Pole(17, "Szansa"))
        board.append(Posiadlosc(18, "Serwerownia", "pomaranczowy", 1800, 140, 900, 1000))
        board.append(Posiadlosc(19, "Pokój samorządu", "pomaranczowy", 2000, 160, 1000, 1000))
        board.append(Pole(20, "Parking"))
        board.append(Posiadlosc(21, "Recepcja", "czerwony", 2200, 180, 1100, 1500))
        board.append(Pole(22, "Szansa"))
        board.append(Posiadlosc(23, "Dziekanat","czerwony", 2200, 180, 1100, 1500))
        board.append(Posiadlosc(24, "Muzeum komputerów", "czerwony", 2400, 200, 1200, 1500))
        board.append(Posiadlosc(25, "KMS", "kolo", 2000, 250, 1000))
        board.append(Posiadlosc(26, "Mural", "zolty", 2600, 220, 1300, 1500))
        board.append(Posiadlosc(27, "Pomnik Kopernika", "zolty", 2600, 220, 1300, 1500))
        board.append(Posiadlosc(28, "Przejście przez WZIKS", "pozaWmii", 1500, 0, 750))
        board.append(Posiadlosc(29, "Fontanna", "zolty", 2800, 240, 1400, 1500))
        board.append(Pole(30, "Idz do wiezienia"))
        board.append(Posiadlosc(31, "Ping-pong", "zielony", 3000, 260, 1500, 2000))
        board.append(Posiadlosc(32, "Bilard", "zielony", 3000, 260, 1500, 2000))
        board.append(Pole(33, "Szansa"))
        board.append(Posiadlosc(34, "Piłkarzyki", "zielony", 3200, 280, 1600, 2000))
        board.append(Posiadlosc(35, "KSI", "kolo", 2000, 250, 1000))
        board.append(Pole(36, "Szansa"))
        board.append(Posiadlosc(37, "sala 0004", "granatowy", 3500, 350, 1750, 2000))
        board.append(PodatekDochodowy(38, 500))
        board.append(Posiadlosc(39, "sala 0089", "granatowy", 4000, 500, 2000, 2000))

        return board

    def __init__(self):
        self.plansza: [Pole] = self.inicializacja_planszy()
        self.karty = Karty()
        self.zagadki = Zagadki()
        self.wczytaj_grafiki()

    def pobierz_pole(self, numer_pola):
        if 0 <= numer_pola <= len(self.plansza):
            return self.plansza[numer_pola]
        else:
            raise Exception("Bledny numer pola")

    # def wysrodkuj_pionki(self):
    #
    # def wysrodkuj_plansze(self):

    def aktualizacja_rozmiaru(self, szerokosc, wysokosc):
        for pole in self.plansza:
            pole.aktualizacja_rozmiaru(szerokosc, wysokosc)

    def render(self, screen):
        for pole in self.plansza:
            pole.render(screen)

    def wczytaj_grafiki(self):
        i = 0
        path = "graphics/pola/pole_"
        extension = ".png"

        for pole in self.plansza:
            pole.sciezka_do_grafiki = (path + str(i) + extension) 
            i += 1



    
