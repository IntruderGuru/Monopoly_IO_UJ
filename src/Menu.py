import shutil
import pygame
from src.PrzyciskiMenu import PrzyciskiMenu
from src.Wizualizator import Wizualizator


class Menu:
    def __init__(self, wizualizator, main_ref):
        self.stan = "witaj"
        self.typ_stopu = "nowa"
        self.liczba_graczy = 0
        self.gracze = []
        self.wizualizator: Wizualizator = wizualizator
        self.font = pygame.font.Font(self.wizualizator.czcionka, 32)
        self.H = 660
        self.W = 1200

        self.main = main_ref

        self.przyciski = PrzyciskiMenu(self.H, self.W, self.wizualizator)

        self.logo = pygame.transform.scale(
            pygame.image.load("graphics/logo.png"), (0.5 * self.W, 0.5 * self.H)
        )

        self.strona1 = pygame.transform.scale(
            pygame.image.load("graphics/tutorial/strona1.png"),
            (0.5 * self.W, 0.5 * self.H),
        )
        self.strona2 = pygame.transform.scale(
            pygame.image.load("graphics/tutorial/strona2.png"),
            (0.5 * self.W, 0.5 * self.H),
        )
        self.pionek1_path = "graphics/pionek/PionekColor1.png"
        self.pionek2_path = "graphics/pionek/PionekColor2.png"
        self.pionek3_path = "graphics/pionek/PionekColor3.png"
        self.pionek4_path = "graphics/pionek/PionekColor4.png"
        self.pionek5_path = "graphics/pionek/PionekColor5.png"

        self.pionek1 = pygame.transform.scale(
            pygame.image.load(self.pionek1_path),
            (0.2 * self.W, 0.2 * self.H),
        )

        self.pionek2 = pygame.transform.scale(
            pygame.image.load(self.pionek2_path),
            (0.2 * self.W, 0.2 * self.H),
        )

        self.pionek3 = pygame.transform.scale(
            pygame.image.load(self.pionek3_path),
            (0.2 * self.W, 0.2 * self.H),
        )

        self.pionek4 = pygame.transform.scale(
            pygame.image.load(self.pionek4_path),
            (0.2 * self.W, 0.2 * self.H),
        )

        self.pionek5 = pygame.transform.scale(
            pygame.image.load(self.pionek5_path),
            (0.2 * self.W, 0.2 * self.H),
        )

        self.skalar_czcionki = 22  # im wiekszy tym mniejsza czcionka
        self.font = pygame.font.Font(
            self.wizualizator.czcionka, int(self.W / self.skalar_czcionki)
        )
        self.font_gracze = pygame.font.Font(
            self.wizualizator.czcionka, int(self.W / (self.skalar_czcionki + 5))
        )
        self.font_wpisywanie = pygame.font.Font(
            self.wizualizator.czcionka, int(self.W / (self.skalar_czcionki + 5))
        )

        self.typ_karty = ""
        self.tresc_karty = ""
        self.wartosc_karty = ""

    def handle_event(self, event, W, H):

        self.W = W
        self.H = H
        self.przyciski.aktualizuj_rozmiar(self.W, self.H)

        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.stan == "witaj":
                if self.przyciski.nowa_gra.is_clicked(event):
                    self.stan = "czas_gry"
                    # self.reset_pionki()
                elif self.przyciski.wyjscie.is_clicked(event):
                    pygame.quit()
                elif self.przyciski.wczytaj_gre.is_clicked(event):
                    self.stan = "stop"
                    self.typ_stopu = "wczytana"

            elif self.stan == "czas_gry":
                if self.przyciski.trzydziesci_minut.is_clicked(event):
                    self.main.LIMIT_CZASU_GRY = 1800
                elif self.przyciski.szescdziesiat_minut.is_clicked(event):
                    self.main.LIMIT_CZASU_GRY = 3600
                elif self.przyciski.dziewiecdziesiat_minut.is_clicked(event):
                    self.main.LIMIT_CZASU_GRY = 5400
                elif self.przyciski.bez_ograniczen.is_clicked(event):
                    self.main.LIMIT_CZASU_GRY = 9999

                if self.main.LIMIT_CZASU_GRY != 0:
                    self.stan = "czas_tury"

            elif self.stan == "czas_tury":
                if self.przyciski.jedna_minuta.is_clicked(event):
                    self.main.LIMIT_CZASU_TURY = 60
                elif self.przyciski.dwie_minuty.is_clicked(event):
                    self.main.LIMIT_CZASU_TURY = 120
                elif self.przyciski.trzy_minuty.is_clicked(event):
                    self.main.LIMIT_CZASU_TURY = 180
                elif self.przyciski.bez_ograniczen.is_clicked(event):
                    self.main.LIMIT_CZASU_TURY = 999

                if self.main.LIMIT_CZASU_TURY != 0:
                    self.stan = "liczba_graczy"

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

            elif self.stan == "wybor_pionkow":
                if self.przyciski.graj.is_clicked(event):
                    self.stan = "stop"
                elif self.przyciski.personalizacja.is_clicked(event):
                    self.stan = "personalizacja"
                elif self.przyciski.nastepny.is_clicked(event):
                    self.stan = "gracz_1"

            elif self.stan == "gracz_1":
                if self.przyciski.nastepny.is_clicked(event):
                    self.stan = "gracz_2"

            elif self.stan == "gracz_2":
                if self.przyciski.poprzedni.is_clicked(event):
                    self.stan = "gracz_1"
                elif (
                    self.przyciski.nastepny.is_clicked(event) and self.liczba_graczy > 2
                ):
                    self.stan = "gracz_3"
                elif (
                    self.przyciski.nastepny.is_clicked(event)
                    and self.liczba_graczy == 2
                ):
                    self.stan = "tutorial1"

            elif self.stan == "gracz_3":
                if self.przyciski.poprzedni.is_clicked(event):
                    self.stan = "gracz_2"
                elif (
                    self.przyciski.nastepny.is_clicked(event) and self.liczba_graczy > 3
                ):
                    self.stan = "gracz_4"
                elif (
                    self.przyciski.nastepny.is_clicked(event)
                    and self.liczba_graczy == 3
                ):
                    self.stan = "tutorial1"

            elif self.stan == "gracz_4":
                if self.przyciski.poprzedni.is_clicked(event):
                    self.stan = "gracz_3"
                elif (
                    self.przyciski.nastepny.is_clicked(event) and self.liczba_graczy > 4
                ):
                    self.stan = "gracz_5"
                elif (
                    self.przyciski.nastepny.is_clicked(event)
                    and self.liczba_graczy == 4
                ):
                    self.stan = "tutorial1"

            elif self.stan == "gracz_5":
                if self.przyciski.poprzedni.is_clicked(event):
                    self.stan = "gracz_4"
                elif self.przyciski.nastepny.is_clicked(event):
                    self.stan = "tutorial1"

            elif self.stan == "tutorial1":
                if self.przyciski.poprzedni.is_clicked(event):
                    self.stan = "gracz_" + str(self.liczba_graczy)
                elif self.przyciski.graj.is_clicked(event):
                    self.stan = "stop"
                elif self.przyciski.personalizacja.is_clicked(event):
                    self.stan = "personalizacja"
                elif self.przyciski.nastepny.is_clicked(event):
                    self.stan = "tutorial2"
            elif self.stan == "tutorial2":
                if self.przyciski.graj.is_clicked(event):
                    self.stan = "stop"
                elif self.przyciski.personalizacja.is_clicked(event):
                    self.stan = "personalizacja"
                elif self.przyciski.poprzedni.is_clicked(event):
                    self.stan = "tutorial1"

            elif self.stan == "personalizacja":
                if self.przyciski.pobierz.is_clicked(event):
                    self.typ_karty = "pobierz"
                    self.stan = "wczytaj_tresc_karty"
                elif self.przyciski.pobierz_od_graczy.is_clicked(event):
                    self.typ_karty = "pobierz_od_graczy"
                    self.stan = "wczytaj_tresc_karty"
                elif self.przyciski.oplata.is_clicked(event):
                    self.typ_karty = "oplata"
                    self.stan = "wczytaj_tresc_karty"
                elif self.przyciski.oplata_za_domki.is_clicked(event):
                    self.typ_karty = "oplata_za_domki"
                    self.stan = "wczytaj_tresc_karty"
                elif self.przyciski.przejdz_na_pole.is_clicked(event):
                    self.typ_karty = "przejdz_na_pole"
                    self.stan = "wczytaj_tresc_karty"
                elif self.przyciski.cofnij_do_wiezienia.is_clicked(event):
                    self.typ_karty = "cofnij_do_wiezienia"
                    self.stan = "wczytaj_tresc_karty"
                elif self.przyciski.powrot.is_clicked(event):
                    self.typ_karty = ""
                    self.tresc_karty = ""
                    self.wartosc_karty = ""
                    self.stan = "tutorial2"

            elif self.stan == "zaakceptuj":
                if self.przyciski.zaakceptuj.is_clicked(event):
                    self.zapisz_karte_do_pliku()
                    self.stan = "tutorial2"
                if self.przyciski.powrot.is_clicked(event):
                    self.typ_karty = ""
                    self.tresc_karty = ""
                    self.wartosc_karty = ""
                    self.stan = "tutorial2"

            elif self.stan == "wczytaj_tresc_karty":
                if self.przyciski.powrot.is_clicked(event):
                    self.typ_karty = ""
                    self.tresc_karty = ""
                    self.wartosc_karty = ""
                    self.stan = "tutorial2"
            elif self.stan == "wczytaj_wartosc_karty":
                if self.przyciski.powrot.is_clicked(event):
                    self.typ_karty = ""
                    self.tresc_karty = ""
                    self.wartosc_karty = ""
                    self.stan = "tutorial2"

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                pygame.quit()

            if self.stan == "nazwy_graczy":
                if event.key == pygame.K_RETURN:
                    if len(self.gracze) < self.liczba_graczy:
                        self.gracze.append("")
                    else:
                        self.stan = "wybor_pionkow"
                elif event.key == pygame.K_BACKSPACE:
                    self.gracze[-1] = self.gracze[-1][:-1]
                else:
                    if event.key == pygame.K_SPACE:
                        if len(self.gracze[-1]) != 0 and self.gracze[-1][-1] != " ":
                            self.gracze[-1] += event.unicode
                    else:
                        self.gracze[-1] += event.unicode
            elif self.stan == "wczytaj_tresc_karty":
                if event.key == pygame.K_RETURN:
                    self.stan = "wczytaj_wartosc_karty"
                elif event.key == pygame.K_BACKSPACE:
                    self.tresc_karty = self.tresc_karty[:-1]
                else:
                    if event.key == pygame.K_SPACE:
                        if len(self.tresc_karty) != 0 and self.tresc_karty[-1] != " ":
                            self.tresc_karty += event.unicode
                    else:
                        self.tresc_karty += event.unicode
            elif self.stan == "wczytaj_wartosc_karty":
                if event.key == pygame.K_RETURN:
                    if self.wartosc_karty == "":
                        self.stan = "blad"
                    else:
                        self.stan = "zaakceptuj"
                elif event.key == pygame.K_BACKSPACE:
                    if len(self.wartosc_karty) > 0:
                        self.wartosc_karty = self.wartosc_karty[:-1]
                elif event.unicode.isdigit():
                    self.wartosc_karty += event.unicode

            elif self.stan == "blad":
                self.stan = "wczytaj_wartosc_karty"
                self.typ_karty = ""
                self.tresc_karty = ""
                self.wartosc_karty = ""

        elif event.type == pygame.DROPFILE:
            self.handle_drop_file(event.file)

    def handle_drop_file(self, file_path):
        if file_path.endswith(".png"):
            try:
                new_image = pygame.image.load(file_path)
                new_image = pygame.transform.scale(
                    new_image, (0.2 * self.W, 0.2 * self.H)
                )
                self.update_pionek(file_path, new_image)
            except pygame.error as e:
                print(f"Cannot load image: {file_path}, {e}")

    def update_pionek(self, file_path, new_image):
        if self.stan == "gracz_1":
            shutil.copy(file_path, self.pionek1_path)
            self.pionek1 = new_image
        elif self.stan == "gracz_2":
            shutil.copy(file_path, self.pionek2_path)
            self.pionek2 = new_image
        elif self.stan == "gracz_3":
            shutil.copy(file_path, self.pionek3_path)
            self.pionek3 = new_image
        elif self.stan == "gracz_4":
            shutil.copy(file_path, self.pionek4_path)
            self.pionek4 = new_image
        elif self.stan == "gracz_5":
            shutil.copy(file_path, self.pionek5_path)
            self.pionek5 = new_image

    def draw(self, screen, W, H):
        self.font = pygame.font.Font(
            self.wizualizator.czcionka, int(W / self.skalar_czcionki)
        )
        self.font_gracze = pygame.font.Font(
            self.wizualizator.czcionka, int(self.W / (self.skalar_czcionki + 5))
        )
        self.font_wpisywanie = pygame.font.Font(
            self.wizualizator.czcionka, int(self.W / (self.skalar_czcionki + 15))
        )

        if self.stan == "witaj":
            self.logo = pygame.transform.scale(self.logo, (0.5 * W, 0.45 * H))
            screen.blit(self.logo, (W * 0.25, H * 0.05))

            self.przyciski.nowa_gra.draw(screen)
            self.przyciski.wczytaj_gre.draw(screen)
            self.przyciski.wyjscie.draw(screen)

        elif self.stan == "tutorial1":
            screen.fill(self.wizualizator.kolor_tla)
            self.przyciski.graj.draw(screen)
            self.przyciski.personalizacja.draw(screen)
            self.przyciski.poprzedni_szary.draw(screen)
            self.przyciski.nastepny.draw(screen)
            self.strona1_temp = pygame.transform.scale(pygame.image.load("graphics/tutorial/strona1.png"), (0.6 * W, 0.7 * H))
            screen.blit(self.strona1_temp, (W * 0.20, H * 0.05))
        elif self.stan == "tutorial2":
            screen.fill(self.wizualizator.kolor_tla)
            self.przyciski.graj.draw(screen)
            self.przyciski.personalizacja.draw(screen)
            self.przyciski.poprzedni.draw(screen)
            self.przyciski.nastepny_szary.draw(screen)
            self.strona2_temp = pygame.transform.scale(pygame.image.load("graphics/tutorial/strona2.png"), (0.6 * W, 0.7 * H))
            screen.blit(self.strona2_temp, (W * 0.20, H * 0.05))

        elif self.stan == "zaakceptuj":
            screen.fill(self.wizualizator.kolor_tla)
            self.przyciski.zaakceptuj.draw(screen)
            self.przyciski.powrot.draw(screen)

        elif self.stan == "czas_gry":
            self.przyciski.trzydziesci_minut.draw(screen)
            self.przyciski.szescdziesiat_minut.draw(screen)
            self.przyciski.dziewiecdziesiat_minut.draw(screen)
            self.przyciski.bez_ograniczen.draw(screen)

            text = self.font.render(
                "Wybierz czas gry w minutach", True, self.wizualizator.kolor_czcionki
            )

            screen.blit(text, (W * 0.255, H * 0.3))

        elif self.stan == "czas_tury":
            self.przyciski.jedna_minuta.draw(screen)
            self.przyciski.dwie_minuty.draw(screen)
            self.przyciski.trzy_minuty.draw(screen)
            self.przyciski.bez_ograniczen.draw(screen)

            text = self.font.render(
                "Wybierz czas tury w sekundach", True, self.wizualizator.kolor_czcionki
            )

            screen.blit(text, (W * 0.255, H * 0.3))

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

            screen.blit(text, (W * 0.305, H * 0.3))

        elif self.stan == "nazwy_graczy":
            text = self.font.render(
                "Wprowadź nazwę gracza: " + str(len(self.gracze)),
                True,
                self.wizualizator.kolor_czcionki,
            )
            screen.blit(text, (W * 0.28, H * 0.25))

            odstep = 0.05
            ile_wpisanych = len(self.gracze)

            for i in range(0, len(self.gracze)):

                if i < ile_wpisanych - 1:
                    kolor_czcionki = self.wizualizator.kolor_akceptacji_nazwy_gracza
                else:
                    kolor_czcionki = self.wizualizator.kolor_czcionki

                gracz = self.font_gracze.render(
                    str(self.gracze[i]), True, kolor_czcionki
                )
                screen.blit(gracz, (W * 0.45, H * (0.45 + (i * odstep))))

        elif self.stan == "wybor_pionkow":
            self.przyciski.poprzedni_szary.draw(screen)
            self.przyciski.graj.draw(screen)
            self.przyciski.personalizacja.draw(screen)
            self.przyciski.nastepny.draw(screen)

            text = self.font.render(
                "Przegląd pionków i możliwość personalizacji",
                True,
                self.wizualizator.kolor_czcionki,
            )
            screen.blit(text, (W * 0.17, H * 0.13))

            # Wyświetlanie pionków w linii z odpowiednim odstępem
            pionki = [
                self.pionek1,
                self.pionek2,
                self.pionek3,
                self.pionek4,
                self.pionek5,
            ]
            for i, pionek in enumerate(pionki):
                pionek_wyswietlany = pygame.transform.scale(
                    pionek, (0.12 * self.W, 0.12 * self.W)
                )
                screen.blit(pionek_wyswietlany, (W * (0.2 + 0.12 * i), H * 0.4))

        elif self.stan == "gracz_1":
            self.przyciski.nastepny.draw(screen)

            text = self.font.render(
                f"Gracz: {self.gracze[0]}", True, self.wizualizator.kolor_czcionki
            )
            self.wyswietl_napis_pionek(screen, self.pionek1, text)

        elif self.stan == "gracz_2":
            self.przyciski.poprzedni.draw(screen)
            self.przyciski.nastepny.draw(screen)

            text = self.font.render(
                f"Gracz: {self.gracze[1]}", True, self.wizualizator.kolor_czcionki
            )
            self.wyswietl_napis_pionek(screen, self.pionek2, text)

        elif self.stan == "gracz_3":
            self.przyciski.poprzedni.draw(screen)
            self.przyciski.nastepny.draw(screen)

            text = self.font.render(
                "Gracz: " + str(self.gracze[2]),
                True,
                self.wizualizator.kolor_czcionki,
            )
            self.wyswietl_napis_pionek(screen, self.pionek3, text)

        elif self.stan == "gracz_4":
            self.przyciski.poprzedni.draw(screen)
            self.przyciski.nastepny.draw(screen)

            text = self.font.render(
                "Gracz: " + str(self.gracze[3]),
                True,
                self.wizualizator.kolor_czcionki,
            )
            self.wyswietl_napis_pionek(screen, self.pionek4, text)

        elif self.stan == "gracz_5":
            self.przyciski.poprzedni.draw(screen)
            self.przyciski.nastepny.draw(screen)

            text = self.font.render(
                "Gracz: " + str(self.gracze[4]),
                True,
                self.wizualizator.kolor_czcionki,
            )
            self.wyswietl_napis_pionek(screen, self.pionek5, text)

        elif self.stan == "personalizacja":
            screen.fill(self.wizualizator.kolor_tla)
            self.przyciski.pobierz.draw(screen)
            self.przyciski.pobierz_od_graczy.draw(screen)
            self.przyciski.oplata.draw(screen)
            self.przyciski.oplata_za_domki.draw(screen)
            self.przyciski.przejdz_na_pole.draw(screen)
            self.przyciski.cofnij_do_wiezienia.draw(screen)
            self.przyciski.powrot.draw(screen)

            text = self.font.render(
                "Wybierz typ Karty Szansy którą chcesz dodać",
                True,
                self.wizualizator.kolor_czcionki,
            )
            screen.blit(text, (self.W * 0.15, self.H * 0.15))

        elif self.stan == "wczytaj_tresc_karty":
            self.przyciski.powrot.draw(screen)
            text = self.font.render(
                f"Wpisz treść karty",
                True,
                self.wizualizator.kolor_czcionki,
            )
            screen.blit(text, (self.W * 0.37, self.H * 0.1))
            text = self.font_wpisywanie.render(
                str(self.tresc_karty),
                True,
                self.wizualizator.kolor_czcionki,
            )
            screen.blit(text, (self.W * 0.1, self.H * (0.5)))

        elif self.stan == "wczytaj_wartosc_karty":
            self.przyciski.powrot.draw(screen)
            text = self.font.render(
                f"Wpisz wartość karty",
                True,
                self.wizualizator.kolor_czcionki,
            )
            screen.blit(text, (self.W * 0.35, self.H * 0.1))
            text = self.font.render(
                str(self.wartosc_karty),
                True,
                self.wizualizator.kolor_czcionki,
            )
            screen.blit(text, (self.W * 0.47, self.H * (0.5)))

        elif self.stan == "blad":
            text = self.font.render(
                f"Wpisano złą wartość karty. Musisz wprowadzić liczbę naturalną",
                True,
                self.wizualizator.kolor_czcionki,
            )
            screen.blit(text, (self.W * 0.1, self.H * 0.1))

    def zapisz_karte_do_pliku(self):
        with open("data/karty.txt", "a", encoding="utf-8") as plik:
            # Zapisz dane karty
            plik.write(
                f"\n{self.typ_karty}\n{self.tresc_karty}\n{self.wartosc_karty}\n"
            )
        self.typ_karty = ""
        self.tresc_karty = ""
        self.wartosc_karty = ""

    def wyswietl_napis_pionek(self, screen, pionek, tekst):
        screen.blit(tekst, (self.W * 0.1, self.H * 0.12))
        pionek_wyswietlany = pygame.transform.scale(
            pionek, (0.12 * self.W, 0.12 * self.W)
        )
        screen.blit(pionek_wyswietlany, (self.W * 0.44, self.H * 0.35))
