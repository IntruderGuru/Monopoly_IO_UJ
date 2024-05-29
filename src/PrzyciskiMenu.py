from src.Przycisk import Przycisk


class PrzyciskiMenu:
    
    def __init__(self, H, W):
        self.nowa_gra = Przycisk(
            W * 0.35,
            H * 0.4,
            W * 0.3,
            H * 0.1,
            (70,70,70),
            (150,150,150),
            "Nowa gra",
            (200,200,200),
        )

        self.wczytaj_gre = Przycisk(
            W * 0.35,
            H * 0.52,
            W * 0.3,
            H * 0.1,
            (70,70,70),
            (150,150,150),
            "Wczytaj zapis",
            (200,200,200),
        )

        self.wyjscie = Przycisk(
            W * 0.35,
            H * 0.64,
            W * 0.3,
            H * 0.1,
            (70,70,70),
            (150,150,150),
            "Wyjscie",
            (200,200,200),
        )

        self.two = Przycisk(
            W * 0.3,
            H * 0.5,
            H * 0.1,
            H * 0.1,
            (70,70,70),
            (150,150,150),
            "2",
            (200,200,200),
        )

        self.three = Przycisk(
            W * 0.4,
            H * 0.5,
            H * 0.1,
            H * 0.1,
            (70,70,70),
            (150,150,150),
            "3",
            (200,200,200),
        )

        self.four = Przycisk(
            W * 0.5,
            H * 0.5,
            H * 0.1,
            H * 0.1,
            (70,70,70),
            (150,150,150),
            "4",
            (200,200,200),
        )

        self.five = Przycisk(
            W * 0.6,
            H * 0.5,
            H * 0.1,
            H * 0.1,
            (70,70,70),
            (150,150,150),
            "5",
            (200,200,200),
        )

    def aktualizuj_rozmiar(self, W, H):
        self.nowa_gra.updateSize(W * 0.35,
            H * 0.4,
            W * 0.3,
            H * 0.1)
        self.wyjscie.updateSize(W * 0.35,
            H * 0.64,
            W * 0.3,
            H * 0.1)
        self.wczytaj_gre.updateSize(W * 0.35,
            H * 0.52,
            W * 0.3,
            H * 0.1)
        self.two.updateSize(W * 0.3,
            H * 0.5,
            H * 0.1,
            H * 0.1)
        self.three.updateSize(W * 0.4,
            H * 0.5,
            H * 0.1,
            H * 0.1)
        self.four.updateSize(W * 0.5,
            H * 0.5,
            H * 0.1,
            H * 0.1)
        self.five.updateSize(W * 0.6,
            H * 0.5,
            H * 0.1,
            H * 0.1)
